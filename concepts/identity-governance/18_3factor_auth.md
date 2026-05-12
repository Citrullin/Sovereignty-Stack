> *Part VI: Identity, Security & Governance* — [← Back to Concepts Index](../README.md)

## 18. 3-Factor Sovereign Auth: Combining `NFC` Badges, Smartphones, and Passwords for Tiered Access

In the Unified Sovereign Stack, security is not a binary state but a gradient.
We reject the fragile "Single-Seed Phrase" model of early crypto, which leads to
total loss from a single mistake. Instead, we implement 3-Factor Sovereign Auth
(3FSA), mapping cryptographic security to the physical habits of the "Boring
Reality".

### 18.1. The Three Pillars of Identity

Access to the stack is governed by the intersection of three distinct entropy
sources:

1. Something You Have (The `NFC` Social Badge): A low-cost, rugged `NFC` [Tiny](../tokenomics/TINY_token_model.md)
   Disc or "Social Badge". This contains a hardware-bound key used for
   low-stakes interactions (Recycling Game, P2P Cash, Door Access).

2. Something You Are/Own (The Smartphone): The smartphone acts as a Smart
   Account Signer (using Passkeys/FaceID). It manages the "Active Session" and
   provides the UI for complex interactions like Forex Routing.

3. Something You Know (The Sovereign Password): A high-entropy passphrase used
   to unlock the Secure Element of your hardware wallet or to authorize "Tier 3"
   Board-level transactions.

### 18.2. Tiered Access: Security by Context

We apply Risk-Adjusted Authentication. Your level of effort to authenticate
should match the stakes of the action.

| Access Tier             | Security Level | Required Factors              | Use Case                                                                                   |
| ----------------------- | -------------- | ----------------------------- | ------------------------------------------------------------------------------------------ |
| Tier 1: High Velocity   | Low            | `NFC` Badge                   | Collecting "Rare" Bottle NFTs, paying for coffee, "Beep-to-Verify" presence.               |
| Tier 2: Maintenance     | Medium         | `NFC` + Smartphone            | Merging code to `Gitea`, accessing `NextCloud`, authorized machine repairs.                |
| Tier 3: Sovereign Board | High           | `NFC` + Smartphone + Password | Moving Large Treasury Funds, changing Elastic Supply, triggering "Actuator Kill-switches". |

### 18.3. The "Beep-to-Sign" Workflow

By leveraging NFC-to-Mobile bridging, we create a seamless UX for the industrial
floor.

- The Handshake: When a Maintainer needs to authorize a firmware update on a
  robot arm, they open the app on their phone (FaceID) and then physically "tap"
  their `NFC` Social Badge against the phone.

- The Multi-Sig Logic: The Smart Account (`ERC-4337`) sees two signatures: one
  from the phone's Secure Enclave and one from the `NFC` disc. This ensures that
  even if a phone is stolen, the attacker cannot act without the physical badge.

### 18.4. Social Recovery & The "Vibe" Reset

What happens if you lose your 3FSA devices? We solve the "Forever Locked"
problem through Sovereign Social Recovery.

- Guardian Mesh: Your "Guardians" are not just random people, but peers with
  high [TinyMeritRank](../identity-governance/17_[tiny](../tokenomics/TINY_token_model.md)meritrank.md) who have physically "Beeped" with you in the last 30 days.

- Hardware-Assisted Recovery: To reset your account, you must gather 3 of your 5
  Guardians. They physically tap their badges to your new phone, reconstruct
  your identity through a Threshold Secret Sharing (TSS) scheme, and re-link
  your Soulbound AI Agent.
