Feature: DAO Sociology and Mechanism Design
  As a decentralized architect and sociologist
  I want to formally model the aggregate behavior of agents under various mechanism designs
  So that I can mathematically verify resilience against extractive equilibria, bridge exploits, and social engineering.

  # --- Scenarios Provided by Architect ---

  Scenario: Bootstrapping a market under Knightian uncertainty
    Given fragmented agents with heterogeneous beliefs, risk tolerances, and private information
    And high coordination costs + trust deficits in legacy financial sociology
    When a constant-product AMM (or successor) is deployed with public code, immutable rules, and permissionless entry/exit
    Then agents deposit capital according to their private utility (no KYC gate)
    And the on-chain state transitions deterministically: reserves -> spot price -> new invariant
    And emergent liquidity emerges as aggregate revealed preference
    But MEV, impermanent loss, and sybil attacks become the new attack surface on the social graph

  Scenario: Incentive alignment vs. extractive equilibria
    Given token emissions as a coordination subsidy
    When farming yield > fundamental cash flow yield for long enough
    Then rational agents optimize for token velocity and governance capture rather than protocol longevity
    And the system transitions toward "vampire" or "ponzi-adjacent" attractors unless mechanism design counters it
    And sociological outcome: new status hierarchies, bagholder narratives, exit scams, and "community" as memetic warfare

  Scenario: TEE-augmented verifiable off-chain computation
    Given a hybrid system (on-chain settlement + TEE for private order flow / risk models)
    When remote attestation + public input/output commitments match the published Gherkin + formal spec
    Then agents can trust the transition function without trusting the operator
    And sociological upgrade: reduced reliance on "trust the team" or "trust the brand" — closer to math than priesthood

  # --- New Scenarios: Threat Vectors & Exploits ---

  Scenario: Cross-Chain Bridge Exploitation (The "Infinite Mint" Threat)
    Given a two-way pegged cross-chain bridge holding locked TVL on Layer 1
    And a wrapped asset contract on Layer 2 relying on an external Oracle or multi-sig
    When a malicious agent exploits a state desynchronization (e.g., forged Merkle proof or compromised Validator keys)
    Then the agent mints unbacked wrapped assets on Layer 2
    And drains the equivalent real TVL from Layer 1
    And the invariant "Layer 1 Locked TVL == Layer 2 Minted Supply" is mathematically violated
    But the Sovereignty Stack TEE verification halts the transaction before execution, proving the state divergence.

  Scenario: Governance Capture via Flash Loans (The DAO Coup)
    Given a DAO relying on token-weighted voting (1 token = 1 vote)
    And a highly liquid lending market (e.g., Aave) where governance tokens can be borrowed
    When an attacker uses a Flash Loan to borrow 51% of the voting supply in a single block
    And the attacker passes a malicious proposal to drain the DAO treasury
    Then the sociological assumption of "community consensus" is bypassed by pure capital velocity
    And the system must either employ Time-Weighted Voting (veTokens) or physical Oracles to invalidate single-block coups.
