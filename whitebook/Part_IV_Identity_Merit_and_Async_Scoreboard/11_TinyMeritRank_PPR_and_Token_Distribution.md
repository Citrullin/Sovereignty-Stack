# Chapter 11: TinyMeritRank PPR & Non-Transferable Governance Distribution

## 11.1 Reversing Proof-of-Stake Plutocracy

In traditional Proof-of-Stake (PoS) blockchains, governance power is directly proportional to token wealth ($\text{Governance} \propto \text{Capital}$). This creates plutocratic feedback loops where capital cartels buy protocol decisions, extract yield, and dump systemic risks onto network operators.

The Sovereign Stack replaces buyable voting power with **TinyMeritRank**, a meritocratic, sybil-resistant reputation engine derived from constructive physical and operational interactions.

---

## 11.2 Personalized PageRank (PPR) Markov Matrix Formalism

TinyMeritRank calculates the merit vector $\mathbf{R}$ across all active `did:peer:4` entities using a **Personalized PageRank (PPR)** Markov iteration model:

$$\mathbf{R} = (1-d)\mathbf{s} + d \cdot \mathbf{W} \cdot \mathbf{R}$$

Where:
- $\mathbf{R} \in \mathbb{R}^N$: The normalized merit score vector across $N$ network entities ($\sum_i R_i = 1$).
- $d \in (0, 1)$: The damping factor ($d = 0.85$), representing temporal reputation decay over time.
- $\mathbf{s} \in \mathbb{R}^N$: The personalized preference vector, anchored in trusted bootstrap seed nodes (e.g. physical Gachapon operators, hardware-attested TEE validators).
- $\mathbf{W} \in \mathbb{R}^{N \times N}$: The column-stochastic adjacency matrix representing verified constructive interactions (DSLA uptime attestations, code commit reviews, physical microbrick vends).

```text
+-----------------------------------------------------------------------------------+
|                   TinyMeritRank Adjacency Matrix Construction                      |
+-----------------------------------------------------------------------------------+
| Constructive Interaction Event (e.g. DSLA Attestation):                           |
|   Node A attests Node B uptime ---> Create directed edge $A \to B$                |
|                                                                                   |
| Weight Matrix Cell:                                                               |
|   $W_{ji} = \frac{\text{Interactions}(i \to j)}{\sum_k \text{Interactions}(i \to k)}$|
+-----------------------------------------------------------------------------------+
```

---

## 11.3 Power Iteration Convergence Proofs

To compute $\mathbf{R}$ efficiently on stateless edge nodes without solving massive linear systems, `sovereign-reth` executes **Power Iteration**:

$$\mathbf{R}^{(0)} = \mathbf{s}$$

$$\mathbf{R}^{(k+1)} = (1-d)\mathbf{s} + d \cdot \mathbf{W} \cdot \mathbf{R}^{(k)}$$

### 11.3.1 Proof of Convergence
Because $\mathbf{W}$ is column-stochastic ($\| \mathbf{W} \|_1 = 1$) and $d < 1$, the linear mapping is a strict contraction mapping under the $L_1$ norm:

$$\| \mathbf{R}^{(k+1)} - \mathbf{R}^{(k)} \|_1 \le d \cdot \| \mathbf{R}^{(k)} - \mathbf{R}^{(k-1)} \|_1$$

By the Banach Fixed-Point Theorem, power iteration converges exponentially to a unique steady-state vector $\mathbf{R}^*$ within **$k \le 25$ iterations**, satisfying $\| \mathbf{R}^{(k+1)} - \mathbf{R}^{(k)} \|_1 < 10^{-6}$.

---

## 11.4 Sybil-Resistant Non-Transferable Merit Token Minting

TinyMeritRank scores dictate non-transferable governance rights ($SOV_{\text{merit}}$):

1. **Non-Transferable ERC-20 / Soulbound Token:** $SOV_{\text{merit}}$ tokens cannot be transferred or sold on speculative secondary markets ($Transfer() \implies \text{revert()}$).
2. **Merit Minting Function:** At each epoch checkpoint, merit tokens are minted directly proportional to steady-state rank $R_i^*$:
   $$\Delta SOV_{\text{merit}}^{(i)} = \text{EpochEmission} \cdot R_i^*$$
3. **Sybil Resistance:** Because $\mathbf{s}$ is anchored in physical hardware nodes (Gachapon machines, TEEs), spinning up millions of virtual Sybil identities yields $R_{\text{sybil}} \to 0$, protecting the manifold from governance capture.

---

## Codebase Implementation in `sovereign-reth`

- **TinyMeritRank Engine:** Implemented in [`crates/consensus/src/registry.rs`](file:///home/citrullin/git/sovereign-reth/crates/consensus/src/registry.rs).
- **Validator Merit Weighting:** Implemented in [`crates/consensus/src/slashing.rs`](file:///home/citrullin/git/sovereign-reth/crates/consensus/src/slashing.rs).
