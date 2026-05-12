# Sovereignty Stack

The **Sovereignty Stack** is a technological framework and template for sovereign entities in the 21st century. It is a pragmatic, "boring reality" approach to decentralization—bringing functioning systems and societal structures on-chain and enforcing them with IoT, AI, and cryptography.

Instead of waiting for a utopian Web3 future or relying on [decaying legacy institutions](concepts/philosophy/00_w3c_critique.md), the Sovereignty Stack provides tools that work *today*, using widely accessible hardware to build high-trust, resilient collectives.

## What is it?

The stack is a full-stack architecture that bridges the physical and digital worlds:
- **Physicalization of Trust:** Hardware tools like the [NFC Social Badge](hardware/tiny-pay/img/NFC_Badge.png) (acting as crypto-native cash and identity) and smart [bit.block microbricks](hardware/bit.block/) (acting as physical Oracles).
- **Federated Infrastructure:** The [Koral Hub](software/koral/), a Kubernetes-based stack of proven open-source tools (Nextcloud, ERPNext, Gitea) gated by Web3 identity (`SIWE-OIDC`).
- **Entity-Agnostic Economy:** The `$TINY` token model and Resonant Meritocracy, which funds systemic vibe and industrial output rather than speculative farming.

## The Investment Thesis

We live in a low-trust, multi-polar world. True sovereignty requires escaping the "Syndicate" (centralized cloud monopolies and captured decentralized rails) by returning to tangible, sociological trust mechanisms.

By combining federated systems with blockchain verification, we can create resilient collectives that own their data, devices, and minds. The goal is to extend existing sociological mechanisms (like [community keychains](hardware/tiny-pay/img/community_NFT_keychain.jpg) or face-to-face handshakes) with cryptographic permanence and sovereignty features.

For the deep-dive philosophical background, read the **[Concepts Manifesto](concepts/)**.

---

## Repository Map

The full concept manifesto lives in [`concepts/`](concepts/). The 47-section
document is split into domain-specific subdirectories — read it as a stack, not a blog.

| Directory | What it Contains | Key Concept Sections |
|---|---|---|
| [`concepts/`](concepts/) | Full manifesto, $TINY tokenomics model | §0–46 |
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