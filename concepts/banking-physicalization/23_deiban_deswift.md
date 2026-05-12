> *Part VII: Banking & Physicalization* — [← Back to Concepts Index](../README.md)

## 23. deIBAN & deSWIFT: The On-Chain Banking Stack

We disrupt the "Syndicate's" monopoly on routing by separating Identifiers
(vIBAN/vSWIFT) from the Settlement Infrastructure (deIBAN/deSWIFT).

### 23.1. vIBAN & vSWIFT: The ENS Routing Protocol

We extend ENS to host verifiable, human-readable financial endpoints.

- **vIBAN (Virtual IBAN)**: A text record (e.g. `viban=EE47...`) attached to an
  ENS domain (e.g. `innovator.eth`).
- **Hierarchical Resolution**: A decentralized tree of Country and Bank
  Resolvers (DAOs) maps these strings to blockchain addresses.
- **vSWIFT**: A messaging protocol on the Elysium Backbone that transmits
  "Industrial Payment Instructions". Unlike legacy SWIFT, the message contains
  the ZK-Proof of Solvency, making the message and the value movement atomic.

### 23.2. deIBAN & deSWIFT: The Infrastructure

While vIBAN is the address, deIBAN is the bank. It is the full decentralized
stack:

- **On-Chain SEPA**: Automated minting of $EURe$ upon receipt of fiat, and
  burning $EURe$ to trigger off-chain SEPA credit via regulated proxies.
- **deSWIFT Settlement**: Utilizing the [Elysium Quantum Backbone](../architecture/09_l2_elysium_backbone.md) to handle
  international $\text{Yuan} \leftrightarrow \text{EURe}$ swaps instantly.
- **Fallback Logic**: If a recipient IBAN is unresolvable on-chain, the system
  routes to a Burn Address (Redemption Contract), triggering a legacy SEPA
  transfer via an off-chain gateway.

This architecture ensures that a factory in the Middle East can settle an
invoice with a European partner using only an ENS handle, bypassing the
Syndicate's 3% fee and 3-day delay.

### 23.4. The "Tax-Free" Corridor

By using deIBAN/deSWIFT infrastructure, an industrial manufacturer can bypass
the 3-5 intermediary banks usually required for international trade.

- Fee Compression: Costs drop from $30-$100 per wire to <$0.01 via Based
  Nano-Rollups.
- Instant Finality: The "Message" (vSWIFT) and the "Value" (The Token) are
  bundled together. Receipt of the message is the settlement.
- Sovereign Routing: Using the [Sahara Node](../architecture/08_l1_sahara_node.md) (L1) as the ultimate truth, no
  central authority can "unplug" a deIBAN endpoint, ensuring permanent access to
  global liquidity.
