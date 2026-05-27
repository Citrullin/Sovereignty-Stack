<script lang="ts">
	import { onMount } from 'svelte'

	import { createWeb3Modal, defaultWagmiConfig } from '@web3modal/wagmi'

	import { arbitrum, mainnet, polygon } from '@wagmi/core/chains'
	import { getAccount, signMessage, reconnect } from '@wagmi/core'
	import { SiweMessage } from 'siwe'
	import Cookies from 'js-cookie'

	// TODO: REMOVE DEFAULTS:
	// main.ts will parse the params from the server
	export let domain: string
	export let nonce: string
	export let redirect: string
	export let state: string
	export let oidc_nonce: string
	export let client_id: string
	const projectId: string = process.env.PROJECT_ID || 'ed39855b9f2f5f1c20a0a8d15229b1cc'

	$: client_metadata = {}

	const chains = [mainnet, arbitrum, polygon]

	const config = defaultWagmiConfig({
		chains,
		projectId,
		enableCoinbase: false,
		enableInjected: false,
	})

	const web3modal = createWeb3Modal({
		defaultChain: mainnet,
		wagmiConfig: config,
		projectId,
		themeMode: 'dark',
		featuredWalletIds: [],
	})

	reconnect(config)

	let oidc_nonce_param = ''
	if (oidc_nonce != null && oidc_nonce != '') {
		oidc_nonce_param = `&oidc_nonce=${oidc_nonce}`
	}
	onMount(async () => {
		try {
			const response = await fetch(
				`${window.location.origin}/client/${client_id}`
			)
			client_metadata = await response.json()
		} catch (e) {
			console.error(e)
		}
	})

	let isSigning = false;
	web3modal.subscribeState(async () => {
		const account = getAccount(config)

		if (account.isConnected && !isSigning) {
			isSigning = true;
			try {
				const expirationTime = new Date(
					new Date().getTime() + 2 * 24 * 60 * 60 * 1000 // 48h
				)

				const msgToSign = new SiweMessage({
					domain: window.location.host,
					address: account.address,
					chainId: account.chainId,
					expirationTime: expirationTime.toISOString(),
					uri: window.location.origin,
					version: '1',
					statement: `You are signing-in to ${window.location.host}.`,
					nonce,
					resources: [redirect],
				})

				const preparedMessage = msgToSign.prepareMessage()

				await new Promise(resolve => setTimeout(resolve, 1000))

				const signature = await signMessage(config, {
					account: account.address,
					message: preparedMessage,
				})

				const session = {
					message: new SiweMessage(preparedMessage),
					raw: msgToSign,
					signature,
				}
				Cookies.set('siwe', JSON.stringify(session), {
					expires: expirationTime,
				})

				window.location.replace(
					`/sign_in?redirect_uri=${encodeURI(
						redirect
					)}&state=${encodeURI(state)}&client_id=${encodeURI(
						client_id
					)}${encodeURI(oidc_nonce_param)}`
				)
				return
			} catch (e) {
				console.error(e)
				isSigning = false
			}
		}
	})
</script>

<main class="page-container">
	<div class="siwe-card">
		<!-- {#if client_metadata.logo_uri}
			<div class="flex justify-evenly items-stretch">
				<img height="72" width="72" class="page-logo" src="img/siwe.svg" alt="SIWE logo" />
				<img height="72" width="72" class="page-logo" src={client_metadata.logo_uri} alt="Client logo" />
			</div>
		{:else} -->
		<img
			height="72"
			width="72"
			class="page-logo"
			src="img/siwe.svg"
			alt="SIWE logo"
		/>
		<!-- {/if} -->
		<div class="welcome-container">
			<h4 class="welcome-title">Sign in with Ethereum</h4>
			<p class="welcome-text">
				Sign a message with your Ethereum wallet to continue to:
			</p>
			<div class="welcome-text-url-container">
				{#if client_metadata.logo_uri}
					<img
						height="36"
						width="36"
						class="client-page-logo"
						src={client_metadata.logo_uri}
						alt="Client logo"
					/>
				{/if}
				<p class="welcome-text-name">
					{client_metadata.client_name
						? client_metadata.client_name
						: domain}
				</p>
			</div>
			{#if client_metadata.client_name}
				<p class="welcome-text-domain">
					{domain}
				</p>
			{/if}
		</div>

		<button
			class="siwe-button"
			on:click={() => {
				web3modal.open()
			}}
		>
			<svg
				width="14"
				height="22"
				viewBox="0 0 14 22"
				fill="none"
				xmlns="http://www.w3.org/2000/svg"
			>
				<path
					d="M0.0518397 10.7353L6.63017 0.0331833L13.0517 10.8014L6.55569 14.6765L0.0518397 10.7353Z"
					fill="#222222"
				/>
				<path
					d="M6.5497 15.8536L0.0458522 11.9124L6.52336 21.0329L13.0457 11.9785L6.5497 15.8536Z"
					fill="#222222"
				/>
			</svg>
			<p class="siwe-button-text">Open your wallet</p>
		</button>

		<!-- {#if client_metadata.client_uri}
			<span class="request-linked-text"
				>Request linked to {client_metadata.client_uri}</span
			>
		{/if} -->
	</div>
</main>
