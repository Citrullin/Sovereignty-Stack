# Chapter 06: Dual-Path Proof of Trust (DPoT) & Intel SGX DCAP zkVM Attestation

## 6.1 Dual-Path Admission Model (DPoT)

Traditional Proof-of-Stake (PoS) networks restrict validator enrollment to wealthy capital holders, leading to plutocratic cartel capture. The Sovereign Stack introduces **Dual-Path Proof of Trust (DPoT)**, enabling nodes to enroll as consensus validators through two complementary, cryptographically verified paths:

```text
+-----------------------------------------------------------------------------------+
|                  Dual-Path Proof of Trust (DPoT) Admission Pipeline               |
+-----------------------------------------------------------------------------------+
| PATH A: Hardware-Attested Trust                                                  |
|   Intel SGX DCAP / AMD SEV Quote ---> Local zkVM Prover ---> ZK Quote Proof      |
|                                                                    |              |
| PATH B: Vanilla Social Reputation                                  v              |
|   Identity `did:peer:4` ---> TinyMeritRank PPR Vector ---> DPoT Admission Matrix  |
|                                                                    |              |
|                                                                    v              |
|                                                   [ Validator Active Set Registry]|
+-----------------------------------------------------------------------------------+
```

---

## 6.2 Path A: Intel SGX DCAP Quote Verification inside zkVM

Nodes with access to Trusted Execution Environment (TEE) hardware (Intel SGX / AMD SEV-SNP) generate a **Data Center Attestation Primitives (DCAP)** quote proving that `sovereign-reth` is executing untampered inside secure enclave memory.

To prevent forcing on-chain smart contracts to parse heavy X.509 certificate chains and revocation lists, the DCAP quote is verified inside an **SP1 / RISC Zero zkVM**:

```text
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Header (Version, Attestation Key Type)                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Enclave Report Body:                                          |
|  - MRENCLAVE (32 bytes: Code Measurement Hash)                |
|  - MRSIGNER  (32 bytes: Enclave Signer Hash)                  |
|  - ISVPRODID / ISVSVN (Version numbers)                       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Report Data (64 bytes: Hash of Validator `did:peer:4` key)    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| ECDSA Signature + PCK Certificate Chain                       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

### 6.2.1 zkVM Circuit Attestation Algorithm
1. **Enclave Measurement Verification:** The zkVM circuit asserts that $\text{MRENCLAVE} = H(\text{sovereign-reth-v2.1})$.
2. **Identity Binding:** The circuit verifies that `ReportData` matches the SHA-256 hash of the validator's `did:peer:4` public key root.
3. **Succinct ZK Proof Generation:** The zkVM outputs a 256-byte ZK-SNARK proof $\pi_{\text{dcap}}$. The validator registry contract verifies $\pi_{\text{dcap}}$ in **<3 milliseconds**, instantly admitting the hardware node without requiring monetary stake.

---

## 6.3 Path B: Vanilla Social Reputation (TinyMeritRank)

Edge operators running low-power microcontrollers (Gachapon machines, microbricks) without TEE hardware enroll via **Path B (Vanilla Social)**:

- **Merit Rank Threshold:** The node must possess a **TinyMeritRank** score $R_i \ge R_{\text{admission}}$ calculated via static Personalized PageRank (PPR) over constructive network interactions.
- **Social Endorsements:** Requires cryptographically signed attestation vouchers from at least 3 existing active validators in good standing.

---

## 6.4 Slashing & Cartel Eviction Mechanics

To prevent Byzantine cartels or compromised TEE keys from attacking manifold consensus, DPoT implements deterministic **Slashing & Eviction**:

```text
Equivocation / Invalid State Transition Detected:
  -> Broadcast Double-Sign Proof (Block Headers A + B)
  -> Execute Slashing Circuit in `crates/consensus/src/slashing.rs`
  -> Immediate Action:
     1. Blacklist MRENCLAVE / MRSIGNER hardware measurement globally.
     2. Zero-out TinyMeritRank PPR vector ($R_i \to 0$).
     3. Distribute slashed bond to reporting relayers.
```

---

## Codebase Implementation in `sovereign-reth`

- **Validator Registry & DPoT Admission:** Implemented in [`crates/consensus/src/registry.rs`](file:///home/citrullin/git/sovereign-reth/crates/consensus/src/registry.rs).
- **Slashing Engine:** Implemented in [`crates/consensus/src/slashing.rs`](file:///home/citrullin/git/sovereign-reth/crates/consensus/src/slashing.rs).
