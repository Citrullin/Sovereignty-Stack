# Economics & Incentives: Crypto-Native Cash Spec

> *Part VII: Banking & Physicalization* — [← Back to Architecture Index](../README.md)

## 22. Crypto-Native Cash: Physicalized Cryptographic Value & POS Consortium Model

Sovereign Manifolds solve the "final mile" of retail economic friction through **Crypto-Native Cash**—a hybrid of digital blockchain security and physical, offline usability. This system treats "cash" not as a separate legacy ledger, but as a physicalized, tokenized state of a Smart Account. By combining account abstraction, NFC hardware, localized spending limits, and possessory bearer logic, we establish a payment medium that matches the fluid usability of physical banknotes while preserving the absolute self-sovereignty of a decentralized ledger.

---

### 22.1. Banknote vs. Badge: The Logic of Physical Possession

Using account abstraction (ERC-4337), we partition localized liquidity into two primary operating modes:

#### 1. Banknote Mode (Object-Bound / Movable Bearer Value)
In this mode, economic value is cryptographically locked within a physical NFC object (such as a low-cost card, paper token, or collectible coin):
- **Bearer Instrument:** Possession of the physical object equals absolute ownership of the localized state space.
- **Destroy-to-Settle Rule:** To transfer these funds back to an online hot wallet, the physical card must be cryptographically redeemed on-chain, which invalidates the card's local keys. This allows risk-free, zero-latency offline peer-to-peer physical trading without the risk of online double-spending.

#### 2. Badge Mode (Identity-Bound / Fixed Sovereign Access)
In this mode, the physical NFC tag functions as an access credential:
- **Multi-Key Gating:** The tag serves as **Key A** (Physical Possession) in a multi-signature or threshold consortium.
- **Factor Verification:** Initiating transactions requires co-signing by **Key B** (the user's mobile device or biometric passkey) or a local terminal PIN.
- **Applications:** Used for receiving maintenance salaries, high-value vault access, and professional credentials.

---

### 22.2. The Triple-Mode Point-of-Sale (POS) Terminal

To integrate physicalized cryptographic assets seamlessly into daily commerce, regional Point-of-Sale (POS) terminals operate in a unified **Triple-Mode** hardware configuration:

1. **Contactless EMV Mode:** Fallback support for legacy credit and debit payment cards (Visa/Mastercard) to maintain backward compatibility during the transitional economy.
2. **Crypto-Native Cash Mode:** Low-value, high-velocity checkout utilizing low-cost (approx. €0.30) passive NFC tags (such as NTAG216/Tiny-Pay) for rapid tap-and-pay transactions.
3. **Active Java Card Mode:** Advanced, programmable smart cards (equipped with Secure Enclaves) executing full on-chip cryptographic processing (e.g., FROST or ECDSA threshold signatures) for high-value operations.

---

### 22.3. Physical Threat Models & Edge Mitigations

Because physical tags are exposed to mechanical wear, theft, and malicious scanning in retail environments, the protocol implements strict hardware and software safeguards:

#### Passive Tag Security (Mitigating the POS Skimming Vector)
Passive NFC tags cannot compute asymmetric cryptographic signatures on-board. Under retail conditions, the tag’s encrypted seed is read into the POS terminal's memory to generate the required one-time signature (W-OTS+):
- **The POS Skimming Threat:** If a merchant’s POS terminal is compromised, the transaction seed could theoretically be extracted from active terminal memory. While we accept this risk for high-velocity, low-value retail transactions, we mitigate it through hardware and rotating keys.
- **Hardware-Level Access Lock:** To block unauthorized raw seed extraction, the silicon's native 32-bit `PWD` register and `AUTHLIM` are locked during provisioning. If three consecutive incorrect password commands are sent to the chip, the silicon permanently brick-locks itself, neutralizing software-level extraction bypasses.
- **User-Driven Seed Rotation:** Users can utilize their own NFC-equipped smartphones at any time to tap their cards, decrypt the tag state locally, and rotate the encrypted seed. This limits the temporal window and economic utility of any potentially intercepted memory state.

#### Local BLE Isolation for High-Value Operations
For transactions exceeding retail limits, the POS terminal does not read keys into active memory. Instead, the physical tap triggers local **Bluetooth Low Energy (BLE) Pairing** or **In-App Relaying**:
- **Offline Local Gating:** The POS terminal queries the user's phone directly over an isolated BLE connection.
- **Local Decryption:** The user enters their passphrase on their personal phone, executing the signature within their local secure enclave. The POS terminal only receives the completed cryptographic signature, ensuring high-value keys never enter terminal memory.

---

### 22.4. Chained Settlement Dynamics

To maintain high throughput without demanding impossible sub-second block times from the underlying manifold:

- **Local Micro-Timestamping:** A micro-timestamp ($T_u$) is negotiated locally between the payment card and the POS terminal during the NFC handshake.
- **Chained Queue:** The transaction proof is added to a local execution queue, allowing the ERC-4337 bundler a **5-minute Settlement Window** to submit and settle the transaction batch on-chain, smoothing out network latency.
- **Hardware Acceleration:** Future retail terminals utilize dedicated **FPGAs or ASICs** on the validation hardware to perform sub-second dynamic checkouts, keeping retail lanes moving smoothly.

---

### 22.5. The Cryptographic Consortium Structure

To ensure complete economic security, the system divides wallet access among three distinct cryptographic roles:

- **Physical Possession (Key A - NFC Tag):** Proves physical presence at the terminal but cannot unilaterally bypass systemic safety rules. The tag’s memory is written once, locked, and protected by hardware registers.
- **Administrative Authority (Key B - Coordinating Entity):** Serves as a neutral, revocable coordinator (orchestrated by Tinyblock or a cooperative guild). Key B possesses the capability to veto high-value transfers, freeze lost cards, or authorize reissuance based on reputation metrics.
- **Economic Ownership (Key C - Smart Account / Master Key):** Holds the ultimate economic right to the underlying assets. 

Key C maintains absolute control; the physical NFC tag itself does not "own" the assets. Transferring the wallet’s stablecoins to a new smart account requires explicit signature by Key C and the absence of a veto by Key B. Consequently, physical loss of the card does not equal economic loss—the user's on-chain revocation is the absolute kill switch.
