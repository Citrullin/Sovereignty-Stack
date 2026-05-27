# Identity & Access: 3-Factor Sovereign Authentication (3FSA)

> *Part VI: Identity, Security & Governance* — [← Back to Architecture Index](../README.md)

## 18. 3-Factor Sovereign Authentication: Mitigating Edge Risks via NFC, BLE, and Multi-Factor Gating

In the Sovereign Manifold framework, security is treated not as a binary state but as a continuous gradient. We reject the fragile "single seed-phrase" model typical of early web3, which leads to total loss from a single mistake. Instead, we implement **3-Factor Sovereign Authentication (3FSA)**, mapping cryptographic operations directly to the physical environment and habits of daily life.

### 18.1. The Three Pillars of Identity Entropy

Access to different layers of the manifold's state space is governed by the intersection of three distinct entropy sources:

1. **Something You Have (The NFC Social Badge):** A low-cost, rugged NFC disc or physical card. It contains a hardware-bound key used for high-velocity transactions, local presence attestation, and daily interactions.
2. **Something You Are/Own (The Mobile Device):** The user's smartphone acts as a smart account co-signer (utilizing Passkeys or Secure Enclaves). It manages active sessions, coordinates Bluetooth (BLE) handshakes, and provides a rich UI.
3. **Something You Know (The Sovereign Password/PIN):** A high-entropy password or local PIN used to unlock the secure enclave or decrypt sensitive, hardware-bound cryptographic keys.

### 18.2. Tiered Access and Risk Gating

We apply Risk-Adjusted Authentication: the user’s friction should scale alongside the economic or operational risk of the requested action.

| Access Tier | Security Level | Required Factors | Core Use Cases |
| :--- | :--- | :--- | :--- |
| **Tier 1: High Velocity** | Low | NFC Badge + (Optional Terminal PIN) | POS payments (e.g., Gachapon POS), collecting rare product NFTs, quick check-ins. |
| **Tier 2: Maintenance** | Medium | NFC + Mobile Device | Merging commits on federated Gitea repositories, accessing private Nextcloud folders. |
| **Tier 3: Sovereign Board** | High | NFC + Mobile + Local BLE/Passphrase | Moving large treasury funds, modifying elastic supply, triggering [Physical Actuator](13_actuator_oracles.md) controls. |

---

### 18.3. POS & NFC Security Architecture (Edge Mitigation)

Deploying NFC tags at Point-of-Sale (POS) terminals presents unique physical attack vectors. Because a standard passive NFC chip has limited compute capacity, the merchant's POS terminal holds temporary transaction state in memory. To secure this daily transaction surface without relying on continuous cloud connectivity, we implement specific edge mitigations:

#### 18.3.1. Local Decryption and Authorization Workflows

To prevent active POS terminal skimming or malicious seed extraction, the NFC badge's seed remains fully encrypted. Decryption can occur via two pathways:
- **Terminal PIN entry:** For low-value POS transactions, the user inputs their PIN directly on the terminal, which derives the decryption key. (Note: While terminal memory poses a physical skimming threat, we mitigate this by limiting the terminal's active authorization window).
- **Local BLE Pairing (High Security):** To bypass the terminal's input interface entirely, the POS terminal initiates a local Bluetooth Low Energy (BLE) pairing request with the user's mobile device. The mobile device prompts the user locally for their passphrase/biometrics, executes the cryptographic signature within the local Secure Enclave, and relays the authorization back to the POS via BLE. This ensures complete isolation from cloud vectors.

#### 18.3.2. User-Driven Seed Rotation

Because physical tags are exposed to mechanical wear and potential skimming attempts over time, users must retain control over key lifecycles.
- **NFC-to-Phone Key Rotation:** At any time, a user can initiate a seed rotation request using their own NFC-equipped smartphone. By tapping their badge to their phone and entering their master passphrase, the phone's local client generates a new key pair, flashes it to the physical NFC tag, and updates the smart account contract's authorized keys on the manifold.

---

### 18.4. Social Recovery & The Peer-to-Peer Reset

If a user loses all authentication factors, we avoid the "forever locked" failure mode through **Sovereign Social Recovery**.

- **Active Guardian Mesh:** A user's account recovery guardians are not arbitrary entities, but trusted peers with high [TinyMeritRank](17_tinymeritrank.md) scores who have physically "beeped" (exchanged NFC contact signatures) within the last 30 days.
- **TSS Reconstruction:** To recover an account, the user must gather a threshold of their active guardians (e.g., 3-of-5). The guardians physically tap their NFC badges to the user's new device. Through a local Threshold Secret Sharing (TSS) protocol, the private keys are reconstructed, and the user's Soulbound AI Agent is safely re-linked.
