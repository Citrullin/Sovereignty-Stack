# Koral — Pan-European Federated Sovereign Hub

> **🔓 Sovereign Open Source:** Koral is fully open-source, designed as a highly reproducible template for continental service providers to bootstrap decentralized, zero-trust infrastructure.

## Investment Thesis

Koral is the practical instantiation of the Sovereignty Stack's "boring reality"
principle: **sovereign tools that work today, not in maybe 20 years**.

The thesis is **Pan-European federated open source software as infrastructure for
sovereign entities** — primarily SMEs, cooperatives, and cultural collectives that
need institutional-grade tooling without cloud lock-in or vendor dependency.

**The model:**
- Buy or recycle used thin clients (recycled hardware → see [§28 Hardware Lifecycle DAO](../../docs/architecture/hardware/28_hardware_lifecycle_dao.md))
- Install the sovereign stack
- Rent at low cost to organizations that want to own their data and identity

The hub is a **replicable template** — any continental service provider can adopt
this template. It starts with a Nordic/Baltic focus (Denmark, Estonia, Nordics)
but the architecture is jurisdiction-agnostic.

**Optional SIWE-OIDC relay:** Links a wallet identity to the federated stack
without replacing the existing UX. Users log in with Ethereum via their NFC badge
or hardware wallet — no seed phrases in the UX, no crypto exchange required.

## Service Stack

All services run in a **Kubernetes cluster** fortified by two primary security layers:
1. **Network Zero-Trust:** **Istio service mesh** enforces mTLS between all services. All services authenticate via a single **Authentik** OIDC provider.
2. **Supply Chain Zero-Trust:** A **Kyverno admission controller** enforces Decentralized Verification ([§50](../../docs/architecture/verification/50_ai_auditor_and_decentralized_verification.md)). The cluster will only pull and execute **Koral Images** if they are signed and validated.

### Recursive OCI Synthesis Model (Koral Images & Patches)

We are fully migrating Koral deployment from legacy runtime Ansible playbooks to a distro-agnostic **Recursive OCI Synthesis Model**. This shifts configuration from runtime live-pod patching to immutable build-time composition:

- **Root Koral Image:** A single signed OCI image acting as an installer payload. It can recursively contain nested signed Koral images (base platforms like Nextcloud, ERPNext, Authentik) alongside regional/jurisdictional patches.
- **Recursive Synthesis Engine (`build_factory`):** Instead of Ansible scripts, the `koral_synthesis.sh` engine processes individual service recipes in `software/koral/build_factory/image_recipes/`. It stitches files and templates into layered OCI structures and compiles a deterministic linked-list synthesis manifest (`koral-manifest.json`).
- **Tail-Call Execution:** The recursive unpacking pipeline processes layers and patches until it hits the final "tail-call", producing an end-state payload ready to be flashed directly to hardware (constrained devices, USB installers) or executed as K3s/Kubernetes pods.
- **Strict Cryptographic & Enclave Enforcement:**
  - **Production Mode:** All layers, patches, and configurations are cryptographically signed down to the Git commit level. Execution and composition must run inside verified Trusted Execution Environments (TEE) (Intel TDX / AMD SEV-SNP).
  - **Development Mode:** Bypasses TEE and signing requirements to facilitate local prototyping, but **strictly emits prominent terminal warning banners** on every build alerting developers of the unsecure signing environment.
- **Zot Local Registry:** Each federated Koral Hub hosts its images locally using a fast, simple Zot registry server.
- **SUSE Fleet Recovery:** Encrypted Koral Images are pushed to upstream SUSE Fleet management clusters. If a local hub suffers physical or cryptographic failure, it can be instantly recovered and bootstrapped from the Fleet.


### Service Portfolio

To maintain absolute transparency and sovereignty, all 17 integrated service layers are categorized below. Each runs as an immutable, signed OCI payload inside the zero-trust cluster.

#### Identity & Security

| Service | Role | Sovereignty Notes |
| :--- | :--- | :--- |
| **Authentik** | Central OIDC / SSO provider | The single auth gateway. Everything speaks OIDC. SIWE relay optionally makes wallet = identity. |
| **Istio** | Zero-trust service mesh | mTLS between all services, traffic policy enforcement, observability. |
| **Step-certificates** | Internal PKI / Certificate authority | Automated, cryptographically secure certificate management (Smallstep) ensuring secure communication and cryptographic identity inside the cluster. |

#### Collaboration & Productivity

| Service | Role | Sovereignty Notes |
| :--- | :--- | :--- |
| **Nextcloud** | Files, Calendar, Contacts, Talk, Office | Self-hosted data. Optional IPFS backup for decentralized resilience. |
| **Collabora** | Office document editing | Fully integrated with Nextcloud, enabling collaborative real-time editing without leaking data to proprietary document clouds. |
| **Bookstack** | Sovereign wiki and internal documentation | Structured markdown-based knowledge management. Can be backed up to IPFS or Git repositories to prevent documentation loss. |
| **Taiga** | Agile project management and tracking | Sovereign project and issue tracking. Supports cryptographic export/import of project structures for portability. |
| **Whiteboard** | Digital collaboration & whiteboarding | Ephemeral or persistent collaborative drawing board run entirely locally with zero external tracking. |

#### Business Operations

| Service | Role | Sovereignty Notes |
| :--- | :--- | :--- |
| **ERPNext** | ERP, Accounting, HR, Inventory, CRM | On-chain payment integration via `deIBAN`/`deSWIFT` (§23). Complete operational sovereignty. |
| **ChiefOnboarding** | Employee / member onboarding workflows | Plugin option: dispatch a hardware wallet (NFC disc / Ledger) as part of new member onboarding. |
| **Listmonk** | Email marketing & newsletters | Can be enriched with on-chain relationship data (wallet-verified subscribers) and self-hosted SMTP relays. |

#### Data & Integration

| Service | Role | Sovereignty Notes |
| :--- | :--- | :--- |
| **Apache Superset** | Dashboarding & analytics | Can consume on-chain telemetry from Heartbeat Oracles (§12) and read directly from local sovereign databases. |
| **X-Road** *(optional)* | Inter-organizational data exchange | Estonian model for sovereign data sharing between hubs. Aligned with EU data sovereignty regulations. |

#### DevOps & Infrastructure

| Service | Role | Sovereignty Notes |
| :--- | :--- | :--- |
| **Coder** | Cloud development environments | Simple k8s-native dev environment deployments for distributed teams, keeping source code strictly in sovereign clusters. |
| **Paralus** | Kubernetes cluster audit & RBAC | Audit logs can be ZK-proved and attached on-chain for verifiable governance trails. |
| **Gitea** | Git hosting, Helm chart registry | Sovereign code hosting. Future: SIWE commit signing per §17. |
| **Velero** | Cluster backup and disaster recovery | Automated back-up of cluster state and persistent volumes directly to sovereign Object Storage (S3/MinIO/IPFS). |

## Key Integration Points

**ChiefOnboarding → Hardware Wallet dispatch**
New member onboarding can trigger shipment of a pre-loaded NFC Wahfare disc or
Ledger as part of the welcome package. Physical + digital sovereignty from day one.

**Listmonk → On-chain relationship enrichment**
Subscriber lists can be enriched with wallet-verified relationship data for
community campaigns. Know your community without KYC.

**Paralus → ZK audit trail on-chain**
Kubernetes audit logs exported from Paralus → ZK-proof of cluster state →
attached on-chain. Verifiable governance without exposing internal infrastructure.

**X-Road → Inter-hub data sovereignty**
Two Koral hubs in different organizations can exchange data via X-Road without
a central intermediary. The Estonian model applied at the SME level.

**SIWE-OIDC Relay → Wallet as identity**
The `OIDC_SIWE_demo.mp4` demonstrates this working. One OIDC request is relayed
and fulfilled by an Ethereum wallet signature. All federated tools gain wallet-based
SSO without modification — they only see a standard OIDC token.

## Demos

| Demo | Description |
|---|---|
| [hub_demo.mp4](demo/hub_demo.mp4) | General hub workflow: Nextcloud, ERPNext etc. |
| [OIDC_SIWE_demo.mp4](demo/OIDC_SIWE_demo.mp4) | Sign in with Ethereum (SIWE) OIDC relay demo |

## Concept References

- [§4 — Sovereignty Manifesto](../../concepts/01_entropy_of_capture/04_metric_separation_manifesto.md):
  Koral is the "boring reality as a revolutionary act" — federated Web 2.5 gated by Web3 identity
- [§16 — SIWE-OIDC Bridge](../../docs/architecture/identity/16_siwe_oidc_bridge.md):
  The technical architecture of the OIDC relay that ties wallet to federated stack
- [§18 — 3-Factor Sovereign Auth](../../docs/architecture/identity/18_3factor_auth.md):
  NFC Badge + smartphone (FaceID) + password — tiered access across all hub services
- [§28 — Hardware Lifecycle DAO](../../docs/architecture/hardware/28_hardware_lifecycle_dao.md):
  Used thin clients as the physical substrate for hub nodes
- [§46 — DAO Governance](../../docs/architecture/economics/40_governance_market_dynamics.md):
  The organizational template the hub serves

## Related

- [`hardware/tiny-pay/`](../../hardware/tiny-pay/) — NFC disc used for hub authentication
- [`software/chain/`](../chain/) — On-chain components the hub integrates with