<?php

declare(strict_types=1);
/**
 * SPDX-FileCopyrightText: 2020 Nextcloud GmbH and Nextcloud contributors
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

namespace OCA\UserOIDC\AppInfo;

use Exception;
use OC_App;
use OCA\Files\Event\LoadAdditionalScriptsEvent;
use OCA\UserOIDC\Db\ProviderMapper;
use OCA\UserOIDC\Event\ExchangedTokenRequestedEvent;
use OCA\UserOIDC\Event\ExternalTokenRequestedEvent;
use OCA\UserOIDC\Event\InternalTokenRequestedEvent;
use OCA\UserOIDC\Listener\ExchangedTokenRequestedListener;
use OCA\UserOIDC\Listener\ExternalTokenRequestedListener;
use OCA\UserOIDC\Listener\InternalTokenRequestedListener;
use OCA\UserOIDC\Listener\TimezoneHandlingListener;
use OCA\UserOIDC\Listener\TokenInvalidatedListener;
use OCA\UserOIDC\Service\SettingsService;
use OCA\UserOIDC\Service\TokenService;
use OCA\UserOIDC\User\Backend;
use OCP\AppFramework\App;
use OCP\AppFramework\Bootstrap\IBootContext;
use OCP\AppFramework\Bootstrap\IBootstrap;
use OCP\AppFramework\Bootstrap\IRegistrationContext;
use OCP\IConfig;
use OCP\IL10N;
use OCP\IRequest;
use OCP\IURLGenerator;
use OCP\Authentication\IAlternativeLogin;
use OCP\IUserManager;
use OCP\IUserSession;
use Throwable;

class AuthentikLogin implements IAlternativeLogin {
	private IURLGenerator $urlGenerator;
	
	public function __construct(IURLGenerator $urlGenerator) {
		$this->urlGenerator = $urlGenerator;
	}

	public function getLabel(): string {
		return 'Login with Authentik';
	}

	public function getLink(): string {
		return $this->urlGenerator->linkToRoute(Application::APP_ID . '.login.login', ['providerId' => 1, 'redirectUrl' => '']);
	}

	public function getClass(): string {
		return 'authentik';
	}

	public function load(): void {
	}
}

class Application extends App implements IBootstrap {
	public const APP_ID = 'user_oidc';
	public const OIDC_API_REQ_HEADER = 'Authorization';

	private $backend;
	private $cachedProviders;

	public function __construct(array $urlParams = []) {
		parent::__construct(self::APP_ID, $urlParams);
	}

	public function register(IRegistrationContext $context): void {
		error_log("USER_OIDC: register() called");
		/** @var IUserManager $userManager */
		$userManager = $this->getContainer()->get(IUserManager::class);

		/* Register our own user backend */
		$this->backend = $this->getContainer()->get(Backend::class);

		$userManager->registerBackend($this->backend);

		$context->registerEventListener(LoadAdditionalScriptsEvent::class, TimezoneHandlingListener::class);
		$context->registerEventListener(ExchangedTokenRequestedEvent::class, ExchangedTokenRequestedListener::class);
		$context->registerEventListener(ExternalTokenRequestedEvent::class, ExternalTokenRequestedListener::class);
		$context->registerEventListener(InternalTokenRequestedEvent::class, InternalTokenRequestedListener::class);

		if (class_exists(\OCP\Authentication\Events\TokenInvalidatedEvent::class)) {
			$context->registerEventListener(\OCP\Authentication\Events\TokenInvalidatedEvent::class, TokenInvalidatedListener::class);
		}

		$context->registerService(AuthentikLogin::class, function($c) {
			return new AuthentikLogin($c->get(IURLGenerator::class));
		});
		if (method_exists($context, 'registerAlternativeLogin')) {
			$context->registerAlternativeLogin(AuthentikLogin::class);
		}
	}

	public function boot(IBootContext $context): void {
		$context->injectFn(function(Backend $backend, \OCP\ISession $session) {
			$backend->injectSession($session);
		});
		$context->injectFn(function(TokenService $tokenService) {
			$tokenService->checkLoginToken();
		});
		
		/** @var IUserSession $userSession */
		$userSession = $this->getContainer()->get(IUserSession::class);
		if ($userSession->isLoggedIn()) {
			return;
		}

		try {
			$context->injectFn(function(IRequest $request, IURLGenerator $urlGenerator, SettingsService $settings, ProviderMapper $providerMapper) {
				$this->registerRedirect($request, $urlGenerator, $settings, $providerMapper);
			});
			$context->injectFn(function(IRequest $request, IL10N $l10n, IURLGenerator $urlGenerator, IConfig $config, ProviderMapper $providerMapper) {
				$this->registerLogin($request, $l10n, $urlGenerator, $config, $providerMapper);
			});
		} catch (Throwable $e) {
			error_log("USER_OIDC BOOT ERROR: " . $e->getMessage() . " in " . $e->getFile() . " on line " . $e->getLine());
		}
	}

	private function checkLoginToken(TokenService $tokenService): void {
		$tokenService->checkLoginToken();
	}

	private function registerRedirect(IRequest $request, IURLGenerator $urlGenerator, SettingsService $settings, ProviderMapper $providerMapper): void {
		$redirectUrl = $request->getParam('redirect_url');
		$absoluteRedirectUrl = !empty($redirectUrl) ? $urlGenerator->getAbsoluteURL($redirectUrl) : $redirectUrl;

		$isDefaultLogin = false;
		try {
			$isDefaultLogin = $request->getPathInfo() === '/login' && $request->getParam('direct') !== '1';
		} catch (Exception $e) {
		}
		if ($isDefaultLogin && !$settings->getAllowMultipleUserBackEnds()) {
			$targetUrl = $urlGenerator->linkToRoute(self::APP_ID . '.login.login', [
				'providerId' => 1,
				'redirectUrl' => $absoluteRedirectUrl
			]);
			header('Location: ' . $targetUrl);
			exit();
		}
	}

	private function registerLogin(
		IRequest $request, IL10N $l10n, IURLGenerator $urlGenerator, IConfig $config, ProviderMapper $providerMapper,
	): void {
		// Suppressed in favor of IAlternativeLogin via register() method
	}

	private function getCachedProviders(ProviderMapper $providerMapper): array {
		if (!isset($this->cachedProviders)) {
			try {
				$this->cachedProviders = $providerMapper->getProviders();
			} catch (\Throwable $e) {
				$this->cachedProviders = [];
			}
		}

		return $this->cachedProviders;
	}
}
