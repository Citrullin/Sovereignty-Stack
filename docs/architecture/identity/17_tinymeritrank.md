# Identity & Access: TinyMeritRank System

> *Part VI: Identity, Security & Governance* — [← Back to Architecture Index](../README.md)

## 17. TinyMeritRank: Sybil-Resistant Reputation Graph via Personalized PageRank and Soulbound Agents

In conventional governance and blockchain networks dominated by the **Regulated Banking Well**, status is plutocratic (purchased with capital) or easily farmed by automated bot networks (Sybil attacks). 

Within the Sovereign Manifold framework, we implement **TinyMeritRank**—a mathematical social graph that treats reputation as a fluid, non-transferable commodity. It guarantees that localized, active economic contributors (the "Innovative Fish") hold disproportionately higher structural weight than passive capital consolidators (the "Sharks").

### 17.1. The Math of Merit: Personalized PageRank (PPR)

Instead of relying on a global credit score or centralized state-issued reputation score—which invites regulatory capture and systemic fragility—TinyMeritRank utilizes **Personalized PageRank (PPR)** algorithms.

- **The Seed Set:** The graph’s trust foundation is rooted in a "Seed Set" composed of verified, long-term sovereign contributors (such as neutral core maintainers, registered hardware operators, and certified regional participants).
- **Sovereign Trust Propagation:** Influence propagates through the network based on verified physical and cryptographic interactions. When users execute "Beep-to-Verify" (NFC peer-attestations) at regional POS terminals or local meetings with high-reputation peers, a fractional portion of the peer’s "Merit" propagates to them.
- **Sybil Resistance:** Because PageRank naturally penalizes circular trust structures (automated accounts mutually endorsing one another), fabricating reputation is highly expensive. To acquire meaningful merit, a node must be cryptographically endorsed by nodes already situated deep within the trusted sub-graph.

### 17.2. Soulbound AI Agents (The "Vibe" Guardians)

To bridge the gap between human, qualitative evaluation and on-chain, quantitative data, every sovereign identity is paired with a private, edge-running **Soulbound AI Agent**.

- **Edge Execution:** The agent is a lightweight LLM running inside the secure element of a user's mobile device or home server. It monitors local contributions: code commits on federated repositories, hardware telemetry from machines they maintain, and raw recycling/production events.
- **Cryptographic Attestations:** The agent generates an "Attestation of Merit" signed by the user's secure hardware. This attestation represents a mathematically verifiable summary of actual, physical-economic contributions rather than a arbitrary speculative token balance.
- **Strict Non-Transferability:** Because the agent is "Soulbound" to the hardware-backed [SIWE Identity](16_siwe_oidc_bridge.md), reputation cannot be bought, sold, or lent on open exchanges. If an operator loses their NFC badge, they must re-verify via multi-party peer endorsement to recover their active agentic state.

### 17.3. Tiered Governance & Access Control

TinyMeritRank serves as the dynamic layer for coordinating physical and digital permissions, structured in three distinct tiers:

- **Tier 3 (Core Architecture):** Requires a top 0.1% MeritRank alongside structural checks (e.g., long-term time-locked multisigs). Only Tier 3 actors can propose structural changes to the manifold's elastic supply or core state transitions.
- **Tier 2 (Maintainers):** Requires a top 5% MeritRank combined with stable determination mechanisms (such as bonded escrow stakes). Tier 2 access grants code commit rights to the federated codebases and authorization to trigger [Physical Actuators](../hardware/13_actuator_oracles.md).
- **Tier 1 (Sovereigns):** Open to anyone possessing a verified SIWE/NFC identity. Allows basic transacting, participation in the circular economy (Recycling Game), and peer-to-peer settlement.

### 17.4. Supply Chain & Code Sovereignty

Access control is meaningless if the underlying software can be compromised via supply-chain attacks.

- **Individual Commit Signing:** Every commit pushed to the federated repositories must be signed by the contributor's SIWE private key. This links code directly to their reputation profile, preventing anonymous or rogue code injections.
- **Threshold Signature Releases:** No individual maintainer possesses the authority to compile or sign a final release. Major client upgrades require threshold multi-signatures (e.g., 5-of-9) from authorized Tier 3 and Tier 2 entities.
- **No Automatic Upgrades:** To prevent systemic exploits through compromised automated updates, core manifold clients explicitly disable auto-update features. Upgrades require manual operator consent, ensuring structural sovereignty.

### 17.5. Strategic Resilience against Banking Well Capture

By tying governance power to thermodynamic physical output and mathematical reputation graphs rather than capital ownership:

- **Capital Immunity:** The Regulated Banking Well cannot hostilely take over a Sovereign Manifold by simply acquiring 51% of its liquid tokens.
- **Active Contribution Incentives:** Reputation decays over time if a node becomes inactive, ensuring that early-stage contributors cannot permanently hoard governance weight.
- **Economic Alignment:** High MeritRank actors benefit from reduced transaction fees on regional manifolds and a share of the network's security salary, aligning self-interest with network stability.
