Feature: Tinyblock Culture and Philosophy
  As a decentralized manifold and high-frequency ledger
  Tinyblock preserves a globally unified state layer while delegating local Web2 frontend compliance to regional providers

  Scenario: Splinternet Architecture Filtering
    Given a user accesses the Tinyblock ledger interface
    When the request originates from a filtered jurisdiction (such as China)
    Then the Web2 frontend provider in that jurisdiction must apply local compliance filters
    And the underlying on-chain ledger state and execution layer must remain global, unfiltered, and identical across all regions
    And the routing engine must handle the transient state packets transparently
