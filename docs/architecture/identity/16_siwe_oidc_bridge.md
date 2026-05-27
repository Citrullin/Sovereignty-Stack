# Identity & Access: SIWE-OIDC Relay Bridge

> *Part VI: Identity, Security & Governance* — [← Back to Architecture Index](../README.md)

## 16. The SIWE-OIDC Relay Bridge: Gating Federated Web 2.5 via Tinyblock and Neutral Org Orchestration

In the Sovereign Manifold paradigm, we reject the false dichotomy between the corporate cloud (monopolized by the **Regulated Banking Well**) and unusable, raw on-chain state storage. Instead, we architect a Federated Web 2.5 infrastructure. We wrap enterprise-grade open-source tools (like Nextcloud, Gitea, and Matrix) inside a sovereign cryptographic envelope using the **SIWE-OIDC Relay Bridge**. 

To maximize accessibility and prevent platform lock-in, the SIWE-OIDC Relay is orchestrated by **Tinyblock and neutral organizations**, serving as the primary authentication relay for users interacting with multiple independent Manifolds.

### 16.1. Reclaiming Single Sign-On (SSO)

The legacy corporate state is gated by central identity providers (such as Google, Okta, and Microsoft). If these providers decide to de-platform or censor an entity, that entity loses access to its codebase, private communications, and operational documents.

- **The Bridge Architecture:** We utilize Sign-In with Ethereum (SIWE) as the primary public-key cryptographic authentication mechanism.
- **OIDC Integration:** The bridge translates a cryptographic signature into a standard OpenID Connect (OIDC) token. To legacy software applications, the user appears to be logging in via a standard corporate Single Sign-On (SSO) provider. To the user, authentication is executed locally via their sovereign hardware wallet or NFC-equipped device.
- **Neutral Orchestration (Tinyblock Relay):** To ensure decentralization, the OIDC identity provider is operated as a neutral relay by Tinyblock and allied community organizations. This neutral registry maintains no private user data but serves as an open, high-availability cryptographic gatekeeper that validates signatures and translates them into federated session credentials.

### 16.2. The NFC Badge and Hardware Wallet as the "Office Key"

Access to restricted workspace repositories and coordination environments is gated physically rather than by traditional usernames and passwords stored in vulnerable databases.

- **Physical Gating:** User access to operational workspaces is bound directly to their physical NFC Social Badge or hardware security module.
- **The Cryptographic Handshake:** When attempting to log in, the user interacts with the terminal or client application, which triggers an authentication request via the Tinyblock OIDC Relay. The user taps their NFC badge (or signs via a Bluetooth/BLE-connected wallet).
- **Reputation Integration:** The relay validates the signature and cross-references the user's cryptographic identity with the [TinyMeritRank](17_tinymeritrank.md) registry updated across the parent Manifold. If the user possesses the necessary merit score or active role, the bridge automatically mints a short-lived OIDC session token.

### 16.3. Federated, High-Resiliency Architecture

Physical data does not reside in monopolized cloud data centers. It is distributed across federated hardware nodes and sovereign servers owned by the community and ecosystem participants.

1. **Nextcloud Workspaces:** Stores high-resolution assets, operational documentation, and designs for [Physical Oracles](../hardware/12_heartbeat_oracles.md).
2. **Gitea Repositories:** Hosts source code for sovereign protocols, local manifold clients, and hardware verification tools.
3. **Dynamic Rule Enforcement:** Permissions are dynamically derived from the manifold's state. If an operator violates a decentralized service-level agreement ([DSLA](../economics/20_dsla.md)) or is slashed, the Tinyblock SIWE-OIDC Relay dynamically revokes their access tokens, immediately disabling credentials across all federated apps.

### 16.4. Strategic Resiliency against Platform Risk

By establishing this Web 2.5 bridge, organizations achieve high engineering productivity alongside absolute operational sovereignty:

- **Zero Migration Cost:** Developers and administrators continue utilizing robust, high-performance open-source tools with which they are already familiar, without the friction of unoptimized "fully on-chain" web applications.
- **Provider Portability:** Because the identity anchor is public-key cryptography and the OIDC relay is run by a neutral organization (Tinyblock), a cooperative or DAO can migrate their entire host infrastructure to domestic servers or alternative clouds in minutes. There are no user credentials to migrate, reset, or secure—identities are owned by the users' private keys and validated by protocol math.
