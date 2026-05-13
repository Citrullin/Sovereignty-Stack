# Koral — Pan-European Federated Sovereign Hub

> **⚠️ Proprietary:** Koral is currently **closed-source** by partner agreement
> (Philipp Blum + Michael). The long-term intent is to open-source the stack once
> the business is established. Contributions and adaptations of the open components
> (Nextcloud, ERPNext, etc.) remain under their respective OSS licenses.

## Investment Thesis

Koral is the practical instantiation of the Sovereignty Stack's "boring reality"
principle: **sovereign tools that work today, not in maybe 20 years**.

The thesis is **Pan-European federated open source software as infrastructure for
sovereign entities** — primarily SMEs, cooperatives, and cultural collectives that
need institutional-grade tooling without cloud lock-in or vendor dependency.

**The model:**
- Buy or recycle used thin clients (recycled hardware → see [§28 Hardware Lifecycle DAO](../../concepts/banking-physicalization/28_hardware_lifecycle_dao.md))
- Install the sovereign stack
- Rent at low cost to organizations that want to own their data and identity

The hub is a **replicable template** — any continental service provider can adopt
this template. It starts with a Nordic/Baltic focus (Denmark, Estonia, Nordics)
but the architecture is jurisdiction-agnostic.

**Optional SIWE-OIDC relay:** Links a wallet identity to the federated stack
without replacing the existing UX. Users log in with Ethereum via their NFC badge
or hardware wallet — no seed phrases in the UX, no crypto exchange required.

## Service Stack

## Service Stack

All services run in a **Kubernetes cluster** fortified by two primary security layers:
1. **Network Zero-Trust:** **Istio service mesh** enforces mTLS between all services. All services authenticate via a single **Authentik** OIDC provider.
2. **Supply Chain Zero-Trust:** A **Kyverno admission controller** enforces Decentralized Verification ([§50](../../concepts/verification/50_ai_auditor_and_decentralized_verification.md)). The cluster will only pull and execute OCI images if the local AI Agent confirms the image CID has a valid DAO signature on the public transparency log.

| Service | Role | Sovereignty Notes |
|---|---|---|
| **Nextcloud** | Files, Calendar, Contacts, Talk, Office | Self-hosted data. Optional IPFS backup for decentralized resilience. |
| **ERPNext** | ERP, Accounting, HR, Inventory, CRM | On-chain payment integration via `deIBAN`/`deSWIFT` (§23) |
| **ChiefOnboarding** | Employee / member onboarding workflows | Plugin option: dispatch a hardware wallet (NFC disc / Ledger) as part of new member onboarding |
| **Coder** | Cloud development environments | Simple k8s-native dev environment deployments for distributed teams |
| **Paralus** | Kubernetes cluster audit & RBAC | Audit logs can be ZK-proved and attached on-chain for verifiable governance trails |
| **Gitea** | Git hosting, Helm chart registry | Sovereign code hosting. Future: SIWE commit signing per §17 |
| **Listmonk** | Email marketing & newsletters | Can be enriched with on-chain relationship data (wallet-verified subscribers) |
| **Apache Superset** | Dashboarding & analytics | Can consume on-chain telemetry from Heartbeat Oracles (§12) |
| **X-Road** *(optional)* | Inter-organizational data exchange | Estonian model for sovereign data sharing between hubs. Aligned with EU data sovereignty regulations |
| **Authentik** | Central OIDC / SSO provider | The single auth gateway. Everything speaks OIDC. SIWE relay optionally makes wallet = identity |
| **Istio** | Zero-trust service mesh | mTLS between all services, traffic policy enforcement, observability |

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

- [§4 — Sovereignty Manifesto](../../concepts/philosophy/04_sovereignty_manifesto.md):
  Koral is the "boring reality as a revolutionary act" — federated Web 2.5 gated by Web3 identity
- [§16 — SIWE-OIDC Bridge](../../concepts/identity-governance/16_siwe_oidc_bridge.md):
  The technical architecture of the OIDC relay that ties wallet to federated stack
- [§18 — 3-Factor Sovereign Auth](../../concepts/identity-governance/18_3factor_auth.md):
  NFC Badge + smartphone (FaceID) + password — tiered access across all hub services
- [§28 — Hardware Lifecycle DAO](../../concepts/banking-physicalization/28_hardware_lifecycle_dao.md):
  Used thin clients as the physical substrate for hub nodes
- [§46 — DAO Governance](../../concepts/tokenomics/46_dao_governance.md):
  The organizational template the hub serves

## Related

- [`hardware/tiny-pay/`](../../hardware/tiny-pay/) — NFC disc used for hub authentication
- [`software/chain/`](../chain/) — On-chain components the hub integrates with