# Sovereignty Stack: The Prerequisite for the Quantum Field Engine

The **Sovereignty Stack** is the foundational armor and engine for individual and collective "particles" within the broader framework of **Quantum Social Physics**. 

Before a macroscopic **Quantum Field Engine (QFE)** can safely operate—orchestrating complex socio-economic realities—the constituent particles *must* have absolute self-determination. Without deterministic, sovereign boundaries at the particle level, the quantum social field inevitably collapses into centralized capture or a chaotic singularity (a seismic event).

The Sovereignty Stack provides this mandatory prerequisite. It is a pragmatic, "boring reality" approach to decentralization—bringing functioning systems and societal structures on-chain and enforcing them with IoT, AI, and cryptography to ensure the particle cannot be subsumed by hostile external field forces.


## What is it?

The stack is a full-stack architecture that bridges the physical and digital worlds:
- **Physicalization of Trust:** Hardware tools like the [NFC Social Badge](hardware/tiny-pay/img/NFC_Badge.png) (acting as crypto-native cash and identity) and smart [bit.block microbricks](hardware/bit.block/) (acting as physical Oracles).
- **Federated Infrastructure:** The [Koral Hub](software/koral/), a Kubernetes-based stack of proven open-source tools (Nextcloud, ERPNext, Gitea) gated by Web3 identity (`SIWE-OIDC`).
- **Entity-Agnostic Economy:** The `$TINY` token model and Resonant Meritocracy, which funds systemic vibe and industrial output, acting as the particle's internal momentum.
- **Automated Epistemology Engine:** A machine-verifiable pipeline that binds sociological intent ([Gherkin scenarios](docs/architecture/testing/features/)) to formal mathematical specifications (TLA+) and cryptographically signed execution traces ([OCI/TPM attestations](concepts/verification/51_confidential_deployment_oci_surgery.md)). This forms the absolute truth boundary of the particle.

## The Engine: How it Works (Epistemological Pipeline)

The Sovereignty Stack does not just "hope" the code is correct; it proves it through a recursive verification loop:

1. **Sociological Intent (Gherkin):** Human-readable BDD scenarios define the "Rules of Engagement" for the collective.
2. **Formal Specification (TLA+):** The Gherkin intents are transpiled into mathematical state machines to check for systemic liveness and safety invariants.
3. **Rust Implementation (FSM):** The logic is implemented in memory-safe Rust using strict Finite State Machine patterns.
4. **Agentic Auditing (A2A):** Autonomous agents scan the repository and verify cryptographic health metrics via the [A2A Communication Protocol](docs/architecture/A2A_COMMUNICATION_PROTOCOL.md).
5. **Confidential Deployment:** The verified binaries are deployed in Trusted Execution Environments (TEEs) with remote attestation, ensuring the operator cannot mutate the state.

## The Investment Thesis

We live in a low-trust, multi-polar world. True sovereignty requires escaping the "Syndicate" (centralized cloud monopolies and captured decentralized rails) by returning to tangible, sociological trust mechanisms.

By combining federated systems with blockchain verification, we can create resilient collectives that own their data, devices, and minds. The goal is to extend existing sociological mechanisms (like [community keychains](hardware/tiny-pay/img/community_NFT_keychain.jpg) or face-to-face handshakes) with cryptographic permanence and sovereignty features.

For the deep-dive philosophical background, read the **[Concepts Manifesto](concepts/)**.

## Research Vision & Verified Architecture

The Sovereignty Stack is designed as a high-value, long-term research framework. It is not purely theoretical; it is a validated architecture running on physical devices today, backed by real-world PoCs, demos, and hardware. We approach sovereignty not just as a collection of apps, but as a formally verifiable ecosystem defined by a strict **Trust Taxonomy**:
- **L0 (Hardware):** Secure Elements and hardware entropy.
- **L1 (Kernel/OS):** Strict deterministic process isolation.
- **L2 (Network):** Metadata obfuscation and privacy routing.
- **L3 (Identity):** Cryptographically defined DIDs and Verifiable Credentials.
- **L4 (User Agency):** UI/UX designed to prevent dark patterns and enforce informed consent.

The stack solves the "Sovereignty Gap" by replacing the "Trust but Verify" paradigm with a **"Verify, then Trust"** architecture. Through Decentralized Verification, Zero-Trust Orchestration, and transparent threat modeling, the stack guarantees that users own not just their data, but the orchestration logic itself.

### Strategic Roadmap: Eliminating Operator Trust

| Component | Legacy Model | Sovereign Recommendation | Why? |
| :--- | :--- | :--- | :--- |
| **Logic** | Helm / Jinja | OCI Layer Patches (`umoci`) | Eliminates template injection/leaks. |
| **Integrity** | Ansible Scripts | `in-toto` Attestations | Cryptographic proof of physical & digital "Why/How". |
| **Isolation** | Standard Podman | Confidential Containers (CoCo) | Host cannot read container memory. |
| **Trust Root** | Admin Password | Keylime + TPM 2.0 | Hardware-level detection of physical tampering. |
| **Build Env** | Shared VM/Runner | TEE (Intel TDX / AMD SEV) | Build process is a "Black Box" even to root. |

For the formal threat model, see [`docs/architecture/THREAT_MODEL.md`](docs/architecture/THREAT_MODEL.md).

---

## Repository Map

<!-- FIXME: There are too many links and sections here. This needs to be condensed/refactored for readability, likely deferring the massive index solely to concepts/README.md or the future PDF generator script. -->

The full concept manifesto lives in [`concepts/`](concepts/). The 55-section
document is split into domain-specific subdirectories — read it as a stack, not a blog.

| Directory | What it Contains | Key Concept Sections |
|---|---|---|
| [`concepts/`](concepts/) | Full manifesto, $TINY tokenomics model | §0–54 |
| [`hardware/bit.block/`](hardware/bit.block/) | Smart microbrick PCB (KiCAD), 3D prints, Three.js web emulator | §12, §13, §11 |
| [`hardware/gachapon/`](hardware/gachapon/) | Gachapon machine — Physicalized Based Rollup Node | §3, §15, §22 |
| [`hardware/tiny-pay/`](hardware/tiny-pay/) | NFC Tiny Disc (Social Badge + Wahfare branded disc) | §22, §18, §43 |
| [`hardware/tinyblock/`](hardware/tinyblock/) | LDraw set designs (Astronaut, Lighthouse) | §44 |
| [`software/bit.block/`](software/bit.block/) | Arduino WoT firmware — W3C Thing Description PoC | §12, §16, §11 |
| [`software/tinyblock/`](software/tinyblock/) | LDraw parts submodule + AI training benchmark images | §44 |
| [`software/web-of-things/`](software/web-of-things/) | RIOT-OS WoT + Arduino WebThings submodules | §12, §13 |
| [`software/koral/`](software/koral/) | Sovereign Hub — k8s, Nextcloud, ERPNext, OIDC, Istio ⚠️ proprietary | §4, §16, §18, §46 |
| [`software/chain/`](software/chain/) | Smart contract specs: $TINY, ERC-3475 bonds, TinyMeritRank, deIBAN | §39–43, §46 |

## Quick Start

```bash
# Clone with submodules
git clone --recurse-submodules <repo-url>

# Or init submodules after cloning
git submodule update --init
```

Submodules:
- `software/tinyblock/microblock_ldraw` — LDraw parts library for microblocks
- `software/web-of-things/RIOT-OS` — W3C WoT CoAP module for RIOT-OS
- `software/web-of-things/arduino` — WebThings fork (WoT TD 1.0) for Arduino