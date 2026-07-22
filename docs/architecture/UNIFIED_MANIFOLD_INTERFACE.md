# The Unified Manifold Interface (UMI)

*Sovereignty Stack — The Hardware Interface for Resonant Settlement*

## Objective: The Tunneling Protocol
In the context of **Quantum Social Physics (QSP)**, a sovereign particle cannot be permanently entangled with a single centralized or decentralized settlement rail (e.g., Ethereum, SEPA, ERP, Hawala). Doing so subjects the particle to external field extraction. 

The **Unified Manifold Interface (UMI)** is the hardware abstraction layer that allows particles to *tunnel* through heterogeneous settlement rails. It treats all financial and data networks as interchangeable, non-deterministic gravitational channels, preserving the "Decoherence Shield" of the particle.

## 1. Probabilistic Rail Discovery (The Gachapon Radar)
Before a transaction can tunnel, the UMI must map the local potential field. This is the **Discovery Lifecycle**:

### Stage 1: Local Field Discovery (The "Beacon" Phase)
The UMI (e.g., a Point-of-Sale terminal or mobile device) performs a Broadcast Discovery to find the path of least resistance.
*   **mDNS (Multicast DNS):** The terminal broadcasts a packet on the local mesh: *"I am looking for an `_umi-rpc._udp.local` service."*
*   **The Manifest:** Local agents respond with their supported rails (ETH-L2, SEPA-INSTANT, LOCAL-CREDIT) and current "Pressure" (server latency, gas fees).

### Stage 2: Remote Rail Discovery (The "Radar" Phase)
If no local agent is viable, the UMI queries a Decentralized RPC Registry (e.g., P2P DHT).
*   **The Ghost Probe:** The terminal sends a "fake" transaction with a zero-value signature to multiple RPCs simultaneously to measure actual Round-Trip Time (RTT) and **Permeability** (using `eth_estimateGas` simulations).
*   **Probability Weighting:** The route with the highest Settlement Finality Probability ($P_s$) and lowest Bridge Latency ($L_b$) is selected to collapse the user's entropy.

## 2. Identity & Security Model: "The Split Soul"
To maintain absolute sovereignty, the particle's core key material must never be persistently exposed. The physical interface architecture accounts for distinct threat models, ranging from low-cost passive tags to active smart cards.

### The "Triple Mode" POS Architecture
The Unified Manifold Interface operates a multi-tiered Point-of-Sale (POS) topology:
1. **Contactless EMV**: Legacy support for Mastercard/Visa routing.
2. **Crypto-Native Cash (Passive NFC)**: Support for low-cost, passive NTAG216 discs (e.g., Tiny-Pay).
3. **Active Java Cards**: Integration of active smart cards (inspired by ColossusNet) capable of true on-chip cryptographic processing for high-value sovereign roles.

### Passive NFC Constraints & Mitigations (NTAG216)
For passive tags, the silicon cannot compute signatures. The NFC tag acts as an **Encrypted Vault**. 
- **The Memory Risk**: The encrypted seed must be read into the POS terminal's active RAM to generate the signature. We accept this risk for low-value daily transactions.
- **The Hardware Gate**: To prevent brute-forcing, the tag is initialized with strict hardware gates using the native 32-bit hardware password (`PWD`) lock:
  - **AUTH0**: Set to the memory page where $E_{seed}$ begins.
  - **AUTHLIM**: Set to `3`. The silicon intrinsically enforces this limit. After three failed PWD attempts, it permanently locks read/write access.
  - **PROT**: Set to `1` (Write & Read protected).

### High-Security Decryption & Seed Rotation
For higher-value operations avoiding POS PIN entry:
- **Local BLE Pairing**: The POS terminal requests the password directly from the user's smartphone via localized, offline Bluetooth Low Energy (BLE), keeping the PIN off the POS hardware.
- **In-App Relaying**: Localized app mechanisms that prevent the password from traversing the cloud.
- **User-Initiated Seed Rotation**: Users can manually rotate the encrypted seed ($E_{seed}$) on their NFC tag using their smartphone's NFC to limit the lifespan of any potentially extracted memory data.

### The Key Derivation Flow
The private key is a Virtual Particle, reconstructed only during the tap event:
1.  **Hardware Salt:** 7-byte Chip UID.
2.  **Encrypted Entropy ($E_{seed}$):** PWD-wrapped seed stored securely on-chip.
3.  **Synthesis:** $Key = KDF(PIN + Decrypt(E_{seed}, PIN) + UID)$.

## 3. Signature Mechanism: Winternitz & Temporal Confinement
To ensure the Quantum Shield is impervious to future algorithmic breakthroughs, we utilize **W-OTS+** (Post-Quantum Hash-Based Signatures) organized in a Merkle Tree.

### The Indexer (PIN)
The user’s PIN is not merely a password; it acts as a deterministic index pointer ($Leaf_i$) in the Merkle tree. Entering the PIN resolves the specific leaf index.

**Validation:** The agent receives the signature and retrieves the Merkle Tree. The hardware gate for passive tags is enforced natively by the `PWD` register on the silicon *before* the signature is even generated, removing the vulnerability of a malicious POS terminal failing to write a "strike" back to the card.

### Temporal Confinement (Chained Settlement & Future Scaling)
We implement Temporal Authentication Constraints via TOTP-derived Salting to ensure the transaction intent decays.
*   **Chained Settlement (5-Minute Window):** The POS terminal and the user agree on a micro-timestamp ($T_u$). The smart contract verifies the W-OTS+ signature against $T_u$, but allows a 5-minute settlement window for the ERC-4337 bundler to resolve latency and land the transaction on-chain.
*   **The Hardware Horizon (FPGAs/ASICs):** While we currently use a 5-minute window for blockchain latency, the future architecture envisions true sub-second TOTP pulse validation via dedicated FPGAs or ASICs on the verifier side. In this future state, if the transaction does not tunnel within the micro-window ($\Delta t$), the virtual particle decays instantly.

## 4. The Data Schema: NFC Payload
The following 888-byte binary structure is written to the NTAG216 during initialization:
```json
{
  "v": 1,
  "root": "0x4e...a2", // The Master Merkle Root
  "meta": {
    "rail_pref": ["eth_rpc", "sepa_instant"],
    "created_at": 1715764000
  },
  "payload": "0x_ENCRYPTED_BLOB_CONTAINING_SEED_AND_METRONOME_KEY"
}
```

## 5. Packetized Intent Emission (Resonant Settlement)
The UMI does not settle transactions; it emits **Packetized Intent** (often referred to as **"Scraps"** or probability tokens). These scraps do not actually "exist" until the moment you try to spend them. The actual transaction is executed by an Agentic Observer.

### The Ethereum RPC Tunnel (The Collapse)
The UMI treats the Ethereum RPC as a Measurement Device.
1. **Ping & Estimate:** The UMI pings the endpoint. If resistance (Gas) > Vibe_Threshold, it attempts to Tunnel through an L2 or an ERC-4337 Paymaster Bundler.
2. **Broadcast:** The signed packet (the Scrap) is emitted.
3. **Observation:** Once a Transaction Hash is confirmed, the probability settles somewhere and the Waveform Collapses.

### The Medium is Irrelevant
Because we use Quantum Physics mechanisms to calculate the scraps and the probability of settlement, the transport medium is irrelevant. 
*   **The Intent:** The W-OTS+ fragment authorizes the movement of value.
*   **The Agent:** An ERP system observes the signature, validates it against the Merkle Root, and marks the invoice as Paid immediately. The value moves because the ERP accepted the Resonance, even if the actual bank ledger settles hours later.

All payment rails are equal in a sovereign system. This completely abstracts the whole USD/Fiat system away. A SEPA instant transfer could have a higher probability of settlement than Ethereum. It is an Asynchronous, Delay-Tolerant Network that harvests trajectory energy to pull other wells into its momentum without paying standard fees.
