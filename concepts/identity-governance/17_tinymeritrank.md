> *Part VI: Identity, Security & Governance* — [← Back to Concepts Index](../README.md)

## 17. [Tiny](../tokenomics/TINY_token_model.md)MeritRank: Sybil-Resistant Status via Personalized PageRank and Soulbound AI Agents

In the "Syndicate" model, status is bought (Plutocracy) or farmed by bots (Sybil
attacks). In the Unified Sovereign Stack, we implement [Tiny](../tokenomics/TINY_token_model.md)MeritRank, a
mathematical social graph that treats reputation as a fluid, non-transferable
commodity. It ensures that the "Innovative Fish" hold more weight than the
"Capital Sharks".

### 17.1. The Math of Merit: Personalized PageRank (PPR)

Instead of a global "score" that can be manipulated by central authorities,
[Tiny](../tokenomics/TINY_token_model.md)MeritRank uses Personalized PageRank.

- The Seed Set: The graph starts with a "Seed Set" of verified, long-term
  sovereign contributors (e.g. the original Miner DAO or Tier 2 Maintainers).

- Trust Propagation: Influence flows through the network based on physical and
  digital interactions. When you "Beep-to-Verify" with a high-reputation peer at
  a regional hub, a portion of their "Merit" flows to you.

- Sybil Resistance: Because PageRank penalizes "circular reporting" (bots
  vouching for bots), it is mathematically expensive to fake status. To gain
  high MeritRank, you must be recognized by nodes that are themselves "deep" in
  the trust graph.

### 17.2. Soulbound AI Agents (The "Vibe" Guardians)

To bridge the gap between human intuition and on-chain data, every sovereign
identity is paired with a Soulbound AI Agent.

- The Agentic Layer: This is a local, private LLM/Agent running in your Secure
  Element. It monitors your contributions: the code you merged on Gitea, the
  "Heartbeats" of the machines you maintained, and the "Rare NFTs" you
  collected.

- Vibe-Attestation: The agent generates an "Attestation of Merit" signed by your
  hardware. This isn't just a number, it’s a cryptographically secured summary
  of your actual work.

- Non-Transferability: Because the agent is "Soulbound" to your hardware-backed
  `SIWE` identity, you cannot sell your reputation on a DEX. If you lose your
  `NFC` Social Badge, you must re-verify through your trusted peers to restore
  your agentic state.

### 17.3. Tiered Governance & Access Control

[Tiny](../tokenomics/TINY_token_model.md)MeritRank serves as the dynamic layer for your "Physical and Digital
Permissions", but to prevent instability, it is combined with structural checks
within the stack:

- Tier 3 (The Board): Requires a top 0.1% MeritRank, reinforced by a Time-Locked
  Multisig or long-term structural appointment. Only they can propose global
  Elastic Supply changes or major protocol forks.

- Tier 2 (Maintainers): Requires a top 5% MeritRank alongside a "Stable
  Determination" mechanism (e.g. a formal bonded stake, DAO ratification, or
  decentralized peer-appointment) to ensure the role isn't completely volatile
  from daily rank shifts. Grants write-access to the Federated Gitea and the
  ability to trigger "[Actuator Oracle](../oracles/13_actuator_oracles.md)s".

- Tier 1 (Sovereigns): Open to anyone with a "Beep-verified" identity. Allows
  participation in the Recycling Game and the use of Crypto-Native Cash.

### 17.4. Supply Chain & Code Sovereignty

Access control is useless if the underlying code is compromised through laziness
or supply-chain attacks.

- Individual Commit Sovereignty: Every individual commit pushed to the Federated
  `Gitea` must be cryptographically signed with the developer's `SIWE` key. This
  links every line of code definitively to an immutable on-chain profile, making
  hit-and-run code injections impossible without burning the developer's
  identity and MeritRank.

- Threshold Signature Releases: No single maintainer can push a major release or
  compile the final binaries. All critical software releases and core updates
  require a threshold signature (e.g. 5-of-9 multisig) from authorized Tier 3 /
  Tier 2 maintainers.

- The "No Blind-Upgrade" Mandate: To ensure the network is never overtaken
  simply because operators were too lazy and auto-upgraded without checking, the
  [Sahara Node](../architecture/08_l1_sahara_node.md) and Elysium clients explicitly disable "auto-upgrading"
  mechanisms. Major protocol version transitions require explicit, manual
  verification and structurally signed operator consent, neutralizing the
  primary vector for automated supply-chain capture.

### 17.5. Game Theory: The "Anti-Syndicate" Barrier

The Syndicate can buy 51% of a token supply or align them through other means,
but they cannot buy 51% of [Tiny](../tokenomics/TINY_token_model.md)MeritRank.

- The Time-Tax: Merit is earned over time through consistent physical presence
  and industrial output ($Q$).

- The Decay Function: Merit "decays" if a node becomes inactive. This prevents
  "Legacy Capture", where early participants hoard power without continuing to
  maintain the stack.

- The Payoff: High MeritRank reduces your transaction fees on Commodity Based
  Rollups and increases your share of the Security Salary, aligning your
  personal prosperity with the health of the mesh.
