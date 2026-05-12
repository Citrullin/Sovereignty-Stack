# $TINY Token Model

> *Part XI: Advanced AI & Tokenomics* — [← Back to Concepts Index](../README.md)

The $TINY token is the core economic unit of the Sovereignty Stack microblock
ecosystem. It is **entity-agnostic by design** — no single corporate entity
controls issuance. It is governed by [TinyMeritRank](../identity-governance/17_tinymeritrank.md) ([§41](../tokenomics/41_merit_token_distribution.md)) and the DAO ([§46](../tokenomics/46_dao_governance.md)).

Used for: governance voting, service access, merit reward, bond collateral ([§39](../tokenomics/39_web3_collateralized_bonds.md)).

---

## Initial Supply: 1,000,000,000 (Fixed Cap)

| Allocation | % | Notes |
|---|---|---|
| Community Epochs | 25% | [TinyMeritRank](../identity-governance/17_tinymeritrank.md) merit distribution — organic, earned |
| Protocol Treasury | 25% | Strategic growth, ecosystem support — DAO-voted |
| Core Contributors | 20% | 8-year backloaded vesting (see [§46.2](../tokenomics/46_dao_governance.md) vesting table) |
| Ecosystem Bootstrap | 20% | Hub operators, ambassador programs, onboarding |
| Protocol Reserve | 10% | Locked — requires DAO supermajority to unlock |

**Design intent:** No DEX liquidity buckets, no VC tranches. Growth is organic
and merit-first. The 10% reserve is an emergency lever — not a slush fund.

---

## Monetary Policy (Sociostasis)

### Phase 1 — Fixed Supply
Distribution exclusively via merit epochs. No inflation.

### Phase 2 — Elastic Issuance (Circuit-Breaker Gated)
Max **2% annual inflation**, triggered ONLY when:
1. Community reserve is exhausted, AND
2. Productive Velocity `Vt × Vc` demonstrates sustained real output `Q`

**Issuance halts** if Efficiency Ratio `η = Q/V` drops below `η_min`
(detects speculative churn — not productive velocity).

**Burn mechanism:** Social Slag Tax on high-V, low-Q accounts ([§5.7](../monetary-policy/05_beyond_sound_money.md) Circuit Breaker).

The inflation function is not a constant — it is a derivative of industrial output:

```
I = f(Q, V)
```

See [§5.2](../monetary-policy/05_beyond_sound_money.md) for the full Sovereign Output Function: `Q(V) = k·V^α·e^(−δV)`

---

## Merit Engine ([TinyMeritRank](../identity-governance/17_tinymeritrank.md) — [§41](../tokenomics/41_merit_token_distribution.md))

Reward formula per epoch τ:

```
T_i = E_τ × (M_i / ΣM_j) × R_i(i)
```

Where:
- `E_τ` = total epoch token allocation
- `M_i` = raw merit points (2-stage evaluation: relevance filter + deliberative scoring)
- `R_i(i)` = self-reputation via Personalized PageRank (PPR, damping d=0.85)
- Decay: 5% monthly (γ=0.05), hard slashing for proven malice

DAO may approve a concave variant: `T_i ∝ √(M_i) · R_i(i)` (reduces winner-take-all dynamics).

---

## Systemic Valuation (W — [§45](../tokenomics/45_resonant_meritocracy.md))

The "vibe" is literally funded and measured — not just felt:

```
W = [∫(Σ Mi·Fi·Hi dt) · (Vt + Vc)] / (1 + D)
```

Where:
- `Mi · Fi · Hi` = Instantaneous Resonance (Work × Vitality × Harmony)
- `Vt` = Utility Velocity (tokens used for service exchanges)
- `Vc` = Capital Velocity (speed of invested funds deployment)
- `D` = Systemic Discordance (authority fallacies, unresolved burnout)

---

## Debt: Time-Shifted Resonance ([Vibe-Collateralized Bonds](../banking-physicalization/24_vibe_collateralized_bonds.md) — [§24](../banking-physicalization/24_vibe_collateralized_bonds.md), [§39](../tokenomics/39_web3_collateralized_bonds.md))

| Property | Value |
|---|---|
| Collateral type | Future merit — not hard assets |
| Lender validates | Trajectory (high-entropy → low-entropy), not balance sheet |
| Margin call trigger | [TinyMeritRank](../identity-governance/17_tinymeritrank.md) drop below threshold (Vibe-Oracle) |
| Bond structure | ERC-3475 tranches A–D ([§39](../tokenomics/39_web3_collateralized_bonds.md) tranche math: `b_i = W·r·e^((r-d)t)`) |

Senior tranche (A) backed by physical inventory (Smart Containers).
Junior tranche (D) backed by "Innovative Potential" — 12.5% yield, 3% modeled default.

---

## Governance ([§46](../tokenomics/46_dao_governance.md))

- **DAO Assembly**: Ratifies major decisions via on-chain votes (Snapshot)
- **Elected Board**: 7–9 members, 2-year terms. 80% elected (45% merit-weighted, 35% stake-weighted), 20% public candidates
- **CEO/Executive Lead**: 4-year term, multi-sig + automated dashboards

**8-year backloaded vesting (core contributors):**

| Year | Release % | Cumulative % |
|---|---|---|
| 1 | 0% (cliff) | 0% |
| 2 | 12.5% | 12.5% |
| 3 | 12.5% | 25% |
| 4 | 25% | 50% |
| 5 | 7.5% | 57.5% |
| 6 | 10% | 67.5% |
| 7 | 15% | 82.5% |
| 8 | 17.5% | 100% |

Clawbacks apply for underperformance or malice. Slashing extends to governance violations per [TinyMeritRank](../identity-governance/17_tinymeritrank.md).

---

## Related Sections

- [§39 — Web3 Collateralized Bonds](39_web3_collateralized_bonds.md) — ERC-3475 tranche math
- [§41 — Merit-Driven Token Distribution](41_merit_token_distribution.md) — Full PPR + evaluation protocol
- [§45 — Resonant Meritocracy](45_resonant_meritocracy.md) — Systemic Valuation W integral
- [§46 — DAO Governance](46_dao_governance.md) — Full governance structure + vesting table
- [§5 — Beyond Sound Money](../monetary-policy/05_beyond_sound_money.md) — Circuit breaker, DSSR, EASC
