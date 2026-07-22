# Chapter 13: Crypto-Native Cash, 3-Factor Sovereign Auth, & UMI Specification

## 13.1 3-Factor Sovereign Auth Architecture (3FSA)

Centralized identity providers (Google, Web2 OAuth) and vulnerable single-key seed phrases fail to provide resilient security for physical edge operators. The Sovereign Stack enforces **3-Factor Sovereign Auth (3FSA)**, requiring three distinct cryptographic authentication factors before granting root control:

1. **Something You Have (Passive NFC Tag):** A low-cost NTAG216 hardware token containing the encrypted master seed.
2. **Something You Are (Biometrics/Smartphone):** Local smartphone authentication (Passkey/FaceID) to authorize active sessions and sign transactions.
3. **Something You Know (PIN/Password):** A high-entropy user PIN used as a deterministic index for post-quantum signature schemes.

---

## 13.2 The Triple Mode POS Architecture & UMI Peering

For physical retail and localized coordination, the Unified Manifold Interface (UMI) operates a multi-tiered Point-of-Sale (POS) topology:

1. **Contactless EMV:** Legacy support for merchant routing and backwards-compatibility.
2. **Crypto-Native Cash (Passive NFC):** Support for low-cost, passive NTAG216 discs, functioning as secure local storage.
3. **Active Java Cards:** Integration of active smart cards capable of true on-chip cryptographic processing (e.g. signing transactions directly on the card).

### 13.2.1 Passive NFC Hardware Gates
For passive NTAG216 discs, the silicon cannot compute signatures. The tag acts as an **Encrypted Vault**. To prevent brute-forcing in the event of physical theft, the tag is initialized with strict hardware gates using the native 32-bit hardware password (`PWD`) lock:
- **AUTH0:** Configured to the exact memory page where the encrypted seed ($E_{\text{seed}}$) begins.
- **AUTHLIM:** Set to `3`. The silicon intrinsically enforces this limit. After three failed PWD attempts, it permanently locks read/write access to the storage.
- **PROT:** Set to `1` (Write & Read protected).

---

## 13.3 Post-Quantum Signatures: W-OTS+ and Merkle Indexing

To ensure long-term cryptographic integrity against future algorithmic breakthroughs, the UMI utilizes **W-OTS+** (Winternitz One-Time Signature+) organized in a Merkle Tree.

### 13.3.1 The PIN as a Leaf Index Pointer
The user's PIN is not merely a password; it acts as a deterministic index pointer ($Leaf_i$) in the Merkle tree. Entering the PIN resolves the specific leaf index.

- **Verification:** The border nodes and validator agents receive the signature and verify it against the Master Merkle Root stored on the card. The hardware gate on the NTAG216 is enforced natively by the `PWD` register on the silicon *before* the signature is even generated, preventing a malicious POS from brute-forcing the key.

### 13.3.2 Temporal Confinement via TOTP Salting
To prevent replay attacks and ensure transaction decay, the UMI implements **Temporal Confinement** via TOTP-derived salting:
- **Chained Settlement:** The POS terminal and the user agree on a micro-timestamp ($T_u$). The validator verifies the W-OTS+ signature against $T_u$, allowing a tight temporal window for execution.
- If the transaction is not settled within the temporal window ($\Delta t$), the signature decays and becomes invalid, eliminating long-term transaction suspension risks.

---

## Codebase Implementation in `sovereign-reth` & Hardware

- **W-OTS+ Verification & Merkle Parsing:** Implemented in [`crates/identity/src/w_ots.rs`](file:///home/citrullin/git/sovereign-reth/crates/identity/src/w_ots.rs).
- **UMI Hardware Drivers & POS Integration:** Implemented in [`hardware/tiny-pay/`](file:///home/citrullin/git/sovereign_stack_vision/hardware/tiny-pay/).
