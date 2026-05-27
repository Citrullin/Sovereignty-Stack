# Sovereignty Stack: The Prerequisite for the Quantum Field Engine

The **Sovereignty Stack** is the foundational armor and engine for individual and collective "particles" within the broader framework of **Quantum Social Physics**. 

Before a macroscopic **Quantum Field Engine (QFE)** can safely operate—orchestrating complex socio-economic realities—the constituent particles *must* have absolute self-determination. Without deterministic, sovereign boundaries at the particle level, the quantum social field inevitably collapses into centralized capture or a chaotic singularity (a seismic event).

The Sovereignty Stack provides this mandatory prerequisite. It is a pragmatic, "boring reality" approach to decentralization—bringing functioning systems and societal structures on-chain and enforcing them with IoT, AI, and cryptography to ensure the particle cannot be subsumed by hostile external field forces.


## What is it?

The stack is a full-stack architecture that bridges the physical and digital worlds:
- **Physicalization of Trust:** Hardware tools like the [NFC Social Badge](hardware/tiny-pay/img/NFC_Badge.png) (acting as crypto-native cash and identity) and smart [bit.block microbricks](hardware/bit.block/) (acting as physical Oracles).
- **Federated Infrastructure:** The [Koral Hub](software/koral/), a Kubernetes-based stack of proven open-source tools (Nextcloud, ERPNext, Gitea) gated by Web3 identity (`SIWE-OIDC`).
- **Entity-Agnostic Economy:** The `$TINY` token model and Resonant Meritocracy, which funds systemic vibe and industrial output, acting as the particle's internal momentum.
- **Automated Epistemology Engine:** A machine-verifiable pipeline that binds sociological intent ([Gherkin scenarios](docs/architecture/testing/features/)) to formal mathematical specifications (TLA+) and cryptographically signed execution traces ([OCI/TPM attestations](docs/architecture/verification/51_confidential_deployment_oci_surgery.md)). This forms the absolute truth boundary of the particle.

## The Engine: How it Works (Epistemological Pipeline)

The Sovereignty Stack does not just "hope" the code is correct; it proves it through a recursive verification loop:

1. **Sociological Intent (Gherkin):** Human-readable BDD scenarios define the "Rules of Engagement" for the collective.
2. **Formal Specification (TLA+ Superposition):** The Gherkin intents are transpiled into mathematical state machines. Rather than attempting to deterministically verify probabilistic LLMs, the TLA+ models a **Quantum Superposition** of all possible agent outcomes. The system bounds the possibility space, ensuring that regardless of an LLM's non-deterministic action, the system maintains strict liveness and safety invariants.
3. **Rust Implementation (FSM):** The logic is implemented in memory-safe Rust using strict Finite State Machine patterns bounded by the TLA+ models.
4. **Agentic Orchestration & Discovery:** Autonomous LLM agents do not verify the math; they act *on behalf* of the user to engage with Federated Manifolds. Each Manifold maintains its own isolated **Agent Registry** (a localized address space). LLMs discover each other across manifolds to negotiate zero-value state messages and dynamically "Block-Build" asset routing.
5. **Confidential Deployment:** The verified binaries are deployed in Trusted Execution Environments (TEEs) with remote attestation, ensuring the operator cannot mutate the state.

## The Investment Thesis

We live in a low-trust, multi-polar world. True sovereignty requires leveraging the highly stable, low-entropy **Banking Well**—the legacy monolithic networks like Ethereum that are undergoing a necessary, cooperative transformation into restricted, compliance-heavy rails run by **Federated TradFi** and Dual TradFi/DeFi. 

Rather than viewing this centralization as a failure, we support it as a stabilizing anchor for the global ecosystem. Alongside this regulated Banking Well, the Sovereignty Stack establishes independent, low-entropy **Sector Wells** (such as specialized manifolds for Tinyblock, the Chocolate industry, or the NASDAQ). These local Wells connect and route regulated stablecoins across one another not via vulnerable bridges, but through **Quantum-Coupled Membranes** and physical **NFC-Enabled Crypto-Native Cash** (Tiny-Pay hardware). This physical and cryptographic membrane approach synchronizes state and facilitates frictionless asset transit across isolated networks while keeping the underlying value safely anchored.

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
For the tunneling protocol and intent-based routing, see the [Unified Manifold Interface (UMI)](docs/architecture/UNIFIED_MANIFOLD_INTERFACE.md).

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