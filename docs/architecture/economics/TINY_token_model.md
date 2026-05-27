# Economics & Incentives: TINY Token Model & Merit Engine

> *Part XI: Advanced AI & Tokenomics* — [← Back to Architecture Index](../README.md)

The **$TINY** token is the core economic utility and incentive-alignment unit of the Sovereign Manifold ecosystem. It is **entity-agnostic by design**—no single corporate or centralized entity controls its issuance, monetary policy, or ledger. It is governed programmatically by the [TinyMeritRank](../identity/17_tinymeritrank.md) reputation protocol, structured guild consensus, and decentralized market dynamics.

---

### 2.1. Initial Token Allocation (Fixed Supply Cap)

The initial aggregate supply of $TINY is capped at **1,000,000,000 tokens**.

| Allocation | Percentage | Primary Purpose | Governance Mechanism |
| :--- | :--- | :--- | :--- |
| **Community Epochs** | $25\%$ | Organic merit-based distribution. | Distributed via TinyMeritRank PPR engine. |
| **Protocol Treasury** | $25\%$ | Strategic ecosystem growth and tooling. | DAO Assembly vote. |
| **Core Contributors** | $20\%$ | Developer and architect compensation. | Locked in an 8-year backloaded vesting schedule. |
| **Ecosystem Bootstrap** | $20\%$ | Regional node onboarding and hardware setup. | Monitored by Tinyblock & regional guilds. |
| **Protocol Reserve** | $10\%$ | Emergency systemic security buffer. | Requires DAO Assembly supermajority (80%) to unlock. |

There are no VC allocations, private token pre-sales, or dedicated DEX liquidity buckets. Token acquisition is organic, merit-first, and aligned with physical economic production.

---

### 2.2. Monetary Policy & Sociostasis

To maintain economic balance between capital velocity and physical resource output:

#### Phase 1: Fixed Cap Issuance
During bootstrap phases, the supply remains strictly capped at 1,000,000,000 tokens. Distribution is driven exclusively by merit allocations across epochs.

#### Phase 2: Dynamic Elastic Issuance
An elastic inflation rate of up to **2.0% annually** can be programmatically activated if and only if:
1. The initial Community Epoch pool is completely exhausted, AND
2. The real productive output ($Q$) of the network’s physical-economic base satisfies the **Sovereign Output Function**:

$$Q(V) = k \cdot V^{\alpha} \cdot e^{-\delta V}$$

Where $V$ represents aggregate transaction velocity, composed of utility velocity ($V_t$) and capital velocity ($V_c$).
- **Speculative Dampening:** Elastic inflation halts automatically if the system’s Efficiency Ratio $\eta = Q/V$ drops below a specified threshold ($\eta_{\text{min}}$). This dampens speculative token churn while sustaining physical value creation.
- **Dynamic Burn (Social Slag Tax):** High-velocity, low-productivity accounts are subject to transaction fee burns, removing speculative froth from the token supply.

---

### 2.3. The Merit Engine (TinyMeritRank PPR)

The distribution of epoch tokens ($E^{\tau}$) to participants is governed by a personalized PageRank reputation graph:

#### 1. PageRank Formulation
The reputation score $R_i(j)$ that agent $i$ assigns to agent $j$ is calculated as:

$$R_i(j) = (1-d) \cdot s_i(j) + d \cdot \sum_{k \to j} \left( \frac{w_{kj}}{\text{out}_k} \right) \cdot R_i(k)$$

Where:
- $d = 0.85$: The damping factor representing the probability of traversing a trust relationship.
- $1-d = 0.15$: The teleport probability returning to agent $i$'s personal seed set.
- $s_i(j)$: Seed indicator—1 if $j$ is explicitly designated within $i$'s trust seed (including self), else 0.
- $w_{kj}$: Endorsement weight—derived from co-committee voting consensus and the existence of a signed trust connection.
- $\text{out}_k$: The sum of all outgoing trust links from agent $k$ ($\sum w_{kj}$).
- $R_{\text{self}}(i) \equiv R_i(i)$: Self-reputation, utilized as the direct token distribution multiplier.

#### 2. Reputation Decay & Slashing
To prevent early-stage capital dominance and permanent power capture:
- **Connectivity Decay:** If the maximum node-disjoint paths between agent $i$ and agent $j$ drops to $\kappa(i, j) \le 2$, the reputation degrades: $R_i(j) \leftarrow 0.90 \cdot R_i(j)$.
- **Temporal Decay:** Once per epoch, reputation values decay: $R_i(j) \leftarrow (1-\gamma) \cdot R_i(j)$ (where $\gamma = 0.05$).
- **Slashing:** Proven malicious behavior or DSLA violations execute a multiplicative slashing penalty, reducing reputation scores to zero.

#### 3. Two-Stage Contribution Evaluation
- **Stage 1: Relevance Filtering:** A proposed contribution (published to IPFS) is audited by a 7-member committee selected via stratified random sampling from the proposer's trust neighborhood. If five of seven committee members verify relevancy, the proposal is signed and moves to Stage 2.
- **Stage 2: Deliberative Scoring:** The committee expands to up to 200 agents. Over up to 10 gossip rounds, members commit scores ($c \in [0, 100]$) and natural-language reasoning. Early stop is triggered when the standard deviation of scores drops below 5% coefficient of variation. The final score $c$ is established by the median value of the final round.

Raw merit points ($M_i^{\tau}$) accumulated by agent $i$ in epoch $\tau$ are calculated as:

$$M_i^{\tau} = \sum_{c \in \tau} a_c \cdot c$$

Where $a_c$ represents an activity coefficient (1.0 to 3.0) based on active participation in deliberation. The corresponding token distribution ($T_i^{\tau}$) received by agent $i$ is calculated as:

$$T_i^{\tau} = E^{\tau} \times \left( \frac{M_i^{\tau}}{\sum_j M_j^{\tau}} \right) \times R_i(i)$$

*(Ecosystem agreements can authorize a concave distribution variant $T_i^{\tau} \propto \sqrt{M_i^{\tau}} \cdot R_i(i)$ to reduce winner-take-all dynamics.)*

---

### 2.4. Systemic Valuation & Instantaneous Resonance ($W$)

Systemic economic value ($W$) is modeled not merely as trade volume, but as an integral of qualitative human-machine alignment, transaction velocity, and friction:

$$W = \frac{\left( \int_{t_0}^{t_{\text{epoch}}} \sum_{i=1}^{n} \left( M_i(t) \cdot F_i(t) \cdot H_i(t) \right) dt \right) \cdot (V_t + V_c)}{1 + D}$$

Where:
- $M_i(t) \cdot F_i(t) \cdot H_i(t)$: Instantaneous Resonance of node $i$ (Work output $\times$ Vitality frequency $\times$ Harmony).
- $V_t$: Utility Velocity (rate of token exchange for services and coordination missions).
- $V_c$: Capital Velocity (speed of capital deployment for infrastructure funding).
- $D$: Systemic Discordance (mathematical friction representing unresolved grid/social burnout and coordination fallacies).
