> *Part VIII: Market Dynamics & Protocol Neutrality* — [← Back to Concepts Index](../README.md)

## 32. TEE-Based Builders: Enforcing Neutrality in Block Construction

In the boring reality users are blind to Toxic MEV (front-running) by
"Syndicate" sequencers. We mandate the use of Trusted Execution Environments
(TEEs) for block construction, effectively creating a "black box" where even the
builder cannot discriminate.

### 32.1. The "Black Box" Builder

Drawing on the SUAVE (Flashbots) model, our builders run their construction
engine inside a TEE.

- **Remote Attestation**: The TEE generates a cryptographic proof (Attestation
  Report) proving to the Anarchy DAO that the code is running the "Neutral
  Inclusion" version without tampering.

### 32.2. Inviolable Inclusion Rules

The TEE enforces a non-discriminatory environment:

- **Strict Order Flow**: Transactions are processed via the Cross-Domain Intent
  Mempool rules, not "side-bribes".
- **Zero-Peeking**: The Builder cannot view transaction contents before
  commitment, eliminating "Secret Front-running" by VC-backed entities.
- **Latency Equalization**: An L3 Nano-Rollup from a local "Grid Hero" receives
  the same computational weight as a high-frequency Syndicate bot. This ensures
  the "Innovative Fish" are never crowded out by the "Whales".

### 32.3. The "Anti-Slop" Kill-Switch

If a Builder attempts to modify their hardware or "jailbreak" the TEE to favor a
specific partner, the attestation fails instantly.

- The Heartbeat Check: Much like the machines in our mesh, the Builder’s TEE
  must provide a "Neutrality Heartbeat".

- The Automatic Squelch: If the heartbeat stops or the attestation is
  invalidated, the [Sahara Node](../architecture/08_l1_sahara_node.md) (L1) automatically ignores the Builder's block
  bids. Their Security Salary is slashed and redirected to the Diversity Fund,
  making "dishonesty" the most expensive strategy a Builder can pursue.

### 32.4. Game Theory: The "Race to the Light"

This system flips the "Race to the Bottom" (who can be the most predatory
builder) into a "Race to the Light":

- The Premium for Truth: Sovereign users and Commodity Rollups will naturally
  route their intents to "TEE-Verified" Builders.

- Syndicate Isolation: Any Builder who refuses to use a Transparency TEE is
  flagged as "Opaque" on the L2 Diversity Scorecard. They are left with the
  "Syndicate Slop", while the high-velocity, high-quality industrial traffic
  stays within the TEE-verified ecosystem.

# Part IX: Inter-DAO Coordination & Transparency
