> *Part XI: Advanced AI & Tokenomics* — [← Back to Concepts Index](../README.md)

## 41. Merit-Driven Token Distribution Evolution

In an era dominated by attention-extraction airdrop cycles, most blockchain
communities follow a predictable path: Explosive growth fueled by farming
solving, and long-term human flourishing are the primary values.

To bootstrap and sustain airdrop ownership in a way that survives first contact
with economic reality, we expand upon [TinyMeritRank](../identity-governance/17_[tiny](../tokenomics/TINY_token_model.md)meritrank.md): A MeritRank-derived,
sybil-resistant reputation and token distribution protocol purpose-built for
creative, growth-oriented communities.

[TinyMeritRank](../identity-governance/17_[tiny](../tokenomics/TINY_token_model.md)meritrank.md) is a fully decentralized protocol in which every human controls
exactly one soulbound AI agent. Agents monitor on-chain and off-chain activity,
propose contributions, and evaluate them through transparent, stratified sampled
committees using threshold signatures. All reputation vectors and deliberation
rounds are permanently auditable on-chain. The system is deployed on a
Surge-based (Taiko core) Ethereum L2 with `ERC-4337` accounts and a private IPFS
cluster.

In short, [TinyMeritRank](../identity-governance/17_[tiny](../tokenomics/TINY_token_model.md)meritrank.md) does not merely distribute tokens, it cultivates
builders. It replaces attention farming with advancement farming, engagement
theater with verifiable creative growth, and extractive airdrops with a
self-reinforcing meritocracy of human and artificial minds working in concert.
Reputation flows exclusively along explicit, on-chain directed trust
relationships between soulbound agent wallets (created via signed `ERC-4337`
user-op).

### 41.1. PageRank Formulation

$R_i(j)$ is the reputation that agent $i$ assigns to agent $j$. Personalized
PageRank:

<!-- prettier-ignore -->
$$ R_i(j) = (1-d) \cdot s_i(j) + d \cdot \sum_{k \to j} \left( \frac{w_{kj}}{\text{out}_k} \right) \cdot R_i(k) $$

- $d = 0.85$ (Damping factor, probability of following a trust link)
- $1-d = 0.15$ (Teleport probability to $i$'s personal seed set)
- $s_i(j)$ Seed indicator: $1$ if $j$ is explicitly seeded by $i$ (includes
  self), else $0$
- <!-- prettier-ignore -->
  $$w_{kj}\,(\mathrm{endorsement\ weight}) = f(\mathrm{co\text{-}committee\ agreements}) \cdot \mathrm{existence\_of\_follow\_edge}(k \to j)$$
  $$(0\ \mathrm{if\ no\ follow\ edge})$$
- $\text{out}_k$ total outgoing endorsement weight of $k$ ($\sum w_{kj}$)
- Self-reputation (used as token multiplier): $R_i(i) \equiv R_{\text{self}}(i)$

### 41.2. Off-chain Content & Reputation Claiming

- Unsigned off-chain content receives a deterministic placeholder identity
  (`keccak256(USERID)`).
- True owner may claim it at any time by proving social-media ownership.
- Upon claim, all historical reputation transfers to the soulbound agent.
  Reputation enters the normal decay schedule (strong incentive to claim
  quickly).

### 41.3. Hard-coded Decay Mechanisms

1. **Connectivity decay**: Parameter
   $\kappa(i, j) = \text{max node-disjoint paths from } i \text{ to } j$. If
   $\kappa(i,j) \le 2 \Rightarrow R_i(j) \leftarrow 0.90\,R_i(j)$
2. **Monthly temporal decay** (once per epoch):
   $R_i(j) \leftarrow (1-\gamma) \cdot R_i(j) + \Delta R_{\text{new}}$ (where
   $\gamma=0.05$)
3. **Slashing decay**: Proven malice leads to a large multiplicative penalty (up
   to zero).

### 41.4. Two-Stage Contribution Evaluation

**Stage 1: Relevance Filter**

- Any agent proposes IPFS CID.
- Proposer $p$ defines its trust neighbourhood
  $N(p) = \{ u \in \text{agents} \mid R_p(u) \ge 0.05 \}$.
- 7-member committee via stratified random sampling.
- Same 7-tuple $\le 10$ consecutive uses.
- Private likelihood $\ell \in [0,1]$ per member.
- If $\ell \ge 0.80$ proceed, else non-contribution. Signed by 5-of-7 threshold
  ECDSA wallet.

**Stage 2: Deliberative Scoring**

- Committee expands to $\le 200$ agents (same stratified sampling method).
- Max 10 public gossip rounds via Ceramic streams.
- Each round: ($\text{score}_t$, $\text{natural-language reasoning}_t$) per
  member, committed on-chain via shared threshold-signature wallet.
- Convergence ($\mu$ = mean, $\sigma$ = standard deviation): Early stop when
  $\sigma \le 0.05 \cdot \mu$ (5% coefficient of variation). After round 10, if
  $\sigma \le 0.20 \cdot \mu \implies \text{final score } c = \text{median of round 10}$,
  otherwise neutral (no score, no tokens).
- Final contribution score $c \in [0,100]$.

Activity Credit: $ac = 1.0 + 0.1 \cdot G$ (Where $G$ = number of gossip rounds
agent actively broadcast in). Typical range: 1.0 – 3.0. Raw merit points of
agent $i$ in epoch $\tau$:

<!-- prettier-ignore -->
$$
M_i^{\tau} = \sum_{c \in \tau,\; c \text{ evaluated by } i} a_c\, c
$$

Tokens received by agent $i$:

<!-- prettier-ignore -->
$$ T_i^\tau = E^\tau \times \left( \frac{M_i^\tau}{\sum_j M_j^\tau} \right)
\times R_i^\tau(i) $$

_(DAO may approve concave variant
$T_i^\tau \propto \sqrt{M_i^\tau} \cdot R_i^\tau(i)$)_
