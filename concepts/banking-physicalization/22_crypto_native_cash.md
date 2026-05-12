> *Part VII: Banking & Physicalization* — [← Back to Concepts Index](../README.md)

## 22. Crypto-Native Cash: The Consortium Model

We solve the "final mile" of economic friction through physicalized
cryptographic claims. This system treats "Cash" not as a separate ledger, but as
a physical state of a Smart Account.

### 22.1. Banknote vs. Badge: The Logic of Possession

We utilize ERC-4337 to partition liquidity into two modes.

**Banknote Mode (Object-Bound / Movable):**

- The value is "jailed" within a physical NFC object.
- **Bearer Instrument**: Possession of the physical disc/paper equals ownership.
- **The Destroy-to-Settle Rule**: To move these funds to an online wallet, the
  physical object must be "destroyed" (redeemed on-chain). This bridges the
  "Slop" of offline P2P trade without double-spend risk.

**Badge Mode (Identity-Bound / Fixed):**

- The NFC chip acts as Key A in a 3-Key Consortium.
- Requires Key B (Smartphone/Biometric) to sign.
- Used for the Security Salary and high-value vaulting.
