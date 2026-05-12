# chain/ — On-Chain Smart Contracts

> **Status:** Planned / in-progress. Implementation depends on the L2/chain
> selection decision (Taiko/Surge vs. sovereign L1 — see §46 governance).

This directory will contain the smart contract layer of the Sovereignty Stack:
the on-chain primitives that make the physical and financial systems trustless.

## Planned Contracts

### ERC-3475 — Web3 Collateralized Bonds (§39)
Risk-adjusted bond tranches A–D for industrial inventory financing.

```
b_i(t, r, d, W) = W·r·e^((r-d)t)
```

- Tranche A: Senior (W=0.50, r=5%, d=0.15%) — OECD-grade collateral
- Tranche B: Mezzanine (W=0.25, r=7.5%, d=0.5%)
- Tranche C: Sub-mezzanine (W=0.15, r=10%, d=1.5%)
- Tranche D: Junior (W=0.10, r=12.5%, d=3%) — emerging market micro-credit

### ERC-4337 — Smart Account / Crypto-Native Cash (§43)
Account abstraction for the 3-Key Consortium model:
- Key A: NFC chip (physical possession, `Thing.h` interface)
- Key B: Authority (smartphone/biometric, governance veto)
- Key C: Ownership (ultimate economic control, on-chain wallet)

Spending rules, threshold signatures (FROST), loss/recovery protections.

### TinyMeritRank Registry (§41)
Personalized PageRank reputation system:
- Soulbound AI agent wallets (ERC-4337 + ERC-5192)
- On-chain deliberation via Ceramic streams
- 2-stage contribution evaluation with threshold ECDSA committee (5-of-7)
- Decay: 5% monthly (γ=0.05), slashing for malice

### CountryResolver — vIBAN / deIBAN (§42)
ENS extension for on-chain IBAN routing:

```solidity
contract CountryResolver {
    mapping(bytes2 => address) public bankResolvers;
    function resolve(string calldata iban) external view
      returns (address wallet, string memory ens) { ... }
}
```

### DSLA — Decentralized SLA (§20)
Protocol-level performance enforcement:
- Performance bonds for service providers
- Automated slashing on Heartbeat Oracle failure
- Payout redistribution to affected users

### $TINY Token (§41, §46)
ERC-20 with merit-distribution hooks:
- Max supply: 1,000,000,000
- Epoch-based distribution: `T_i = E_τ × (M_i / ΣM_j) × R_i(i)`
- 8-year backloaded vesting for core contributors (see §46.2 vesting table)
- Inflation circuit breaker tied to Efficiency Ratio η = Q/V

## Concept References

- [§39 — Web3 Collateralized Bonds](../../concepts/tokenomics/39_web3_collateralized_bonds.md)
- [§41 — Merit-Driven Token Distribution](../../concepts/tokenomics/41_merit_token_distribution.md)
- [§42 — ENS-IBAN Extension](../../concepts/tokenomics/42_ens_iban_extension.md)
- [§43 — Crypto-Native Cash Spec](../../concepts/tokenomics/43_crypto_native_cash_spec.md)
- [§20 — DSLA](../../concepts/identity-governance/20_dsla.md)
- [§46 — DAO Governance & Tokenomics](../../concepts/tokenomics/46_dao_governance.md)
- [TINY_token_model.md](../../concepts/tokenomics/TINY_token_model.md) — The full $TINY spec

## Related

- [`software/koral/`](../koral/) — Hub that integrates on-chain identity via SIWE-OIDC
- [`hardware/tiny-pay/`](../../hardware/tiny-pay/) — Physical Key A (NFC disc) for ERC-4337 accounts
