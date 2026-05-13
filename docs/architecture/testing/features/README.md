# Gherkin Feature Specifications

[← Back to Testing Hub](../README.md)

This directory contains the machine-readable BDD (Behavior-Driven Development) specifications that define the sociological and technical invariants of the Sovereignty Stack.

## Core Features

| Feature File | Focus Area |
| :--- | :--- |
| [`philosophical_thermodynamics.feature`](philosophical_thermodynamics.feature) | Thermodynamics of trust, entropy reduction, Dunbar limits. |
| [`identity_governance_banking.feature`](identity_governance_banking.feature) | SIWE-OIDC, MeritRank, and deIBAN interactions. |
| [`tokenomics_and_resilience.feature`](tokenomics_and_resilience.feature) | $TINY supply shocks, margin calls, and harmonic stabilization. |
| [`dao_sociology_mechanics.feature`](dao_sociology_mechanics.feature) | AMM mechanics, governance coups, and TEE-augmented voting. |
| [`compliance_automation.feature`](compliance_automation.feature) | **ISO 9001, 27001, 42001, and ES³ (European Sovereign Stack) auditing.** |
| [`agentic_auditor.feature`](agentic_auditor.feature) | Formal verification of the Auditor Agent and OCI surgery. |
| [`catastrophic_recovery.feature`](catastrophic_recovery.feature) | Systemic reboot protocols and state restoration in hostile environments. |

## Execution

These features are consumed by the `identity-worker` test suite:
- **Rust:** `software/identity-worker/tests/cucumber_test.rs`
- **Python:** `software/identity-worker/tests/integration/test_dao_mechanics.py`

---
*Sovereignty Stack — Automated Epistemology Engine*
