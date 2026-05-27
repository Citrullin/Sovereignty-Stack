> *Part VII: Banking & Physicalization* — [← Back to Concepts Index](../README.md)

## 22. Crypto-Native Cash: The Consortium Model

We solve the "final mile" of economic friction through physicalized cryptographic claims. This system treats "Cash" not as a separate ledger, but as a physical state of a Smart Account.

### 22.1. Banknote vs. Badge: The Logic of Possession

We utilize ERC-4337 to partition liquidity into two modes.

**Banknote Mode (Object-Bound / Movable):**

- The value is "jailed" within a physical NFC object.
- **Bearer Instrument**: Possession of the physical disc/paper equals ownership.
- **The Destroy-to-Settle Rule**: To move these funds to an online wallet, the physical object must be "destroyed" (redeemed on-chain). This bridges the "Slop" of offline P2P trade without double-spend risk.

**Badge Mode (Identity-Bound / Fixed):**

- The NFC chip acts as Key A in a multi-key or threshold consortium.
- Requires Key B (Smartphone/Biometric) to sign.
- Used for the Security Salary and high-value vaulting.

---

### 22.2. The Triple Mode Point-of-Sale (POS) & Hardware Co-Existence
To integrate these physicalized assets into daily trade, the verifier terminal operates in a unified **Triple Mode**:
1. **Contactless EMV Mode**: Legacy payment rails (Visa/Mastercard) for fallback.
2. **Crypto-Native Cash Mode**: Utilizing cheap passive NFC NTAG216 tags (Tiny-Pay) for high-velocity, low-value retail taps.
3. **Active Java Card Mode**: Using programmable smart cards (inspired by ColossusNet) for secure on-chip cryptographic processing in high-value, active roles.

---

### 22.3. Physical Threat Models & Cryptographic Mitigations

#### Passive Tag Security (The Gachapon Threat)
Passive NFC tags (NTAG216) cannot compute signatures on-board. Under **Badge Mode** at a POS terminal:
- **POS Memory Exposure**: The encrypted seed must be read into the POS terminal’s active memory to generate the W-OTS+ signature. We accept this risk for daily retail velocity.
- **Hardware-Level Enforced Gate**: To block unauthorized extraction, the silicon's native 32-bit `PWD` register and `AUTHLIM` are locked. If three incorrect passwords are sent, the silicon permanently brick-locks itself. This hardware gate fires natively on the tag, nullifying POS software-level bypasses.
- **User-Initiated Seed Rotation**: Users can utilize their own smartphone's NFC to rotate the encrypted seed on their tag, limiting the lifespan and value of any potentially intercepted memory state.

#### Offline Decryption & High-Value Channels
For high-value transactions, the physical tap triggers local **BLE (Bluetooth Low Energy) Pairing** or **In-App Relaying**. The POS queries the user's phone for the password directly over an offline local channel, ensuring the PIN/password never sits in POS terminal memory or traverses the cloud.

---

### 22.4. Chained Settlement Dynamics
Instead of unviable sub-second block times, transactions utilize a **Chained Settlement** pipeline. 
- A micro-timestamp ($T_u$) is agreed upon locally between the card and the terminal.
- The W-OTS+ signature is submitted with a **5-minute Settlement Window** allowed for the ERC-4337 bundler to resolve network latency.
- Future scalability maps to dedicated **FPGAs or ASICs** on the validation hardware to perform sub-second dynamic checkouts.

