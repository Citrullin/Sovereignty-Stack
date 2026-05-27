# Economics & Incentives: deIBAN & deSWIFT Spec

> *Part VII: Banking & Physicalization* — [← Back to Architecture Index](../README.md)

## 23. deIBAN & deSWIFT: On-Chain Banking & Sovereign Payment Routing

Sovereign Manifolds dismantle the monopoly on international transaction clearing and value routing controlled by the **Regulated Banking Well**. We achieve this by decoupling payment identifiers (such as vIBAN and vSWIFT) from the underlying centralized settlement infrastructure, replacing them with a decentralized, open-source stack composed of **deIBAN** and **deSWIFT**.

---

### 23.1. vIBAN & vSWIFT: The ENS Payment Routing Protocol

To bridge the gap between traditional banking infrastructure and sovereign web3 execution, we extend the Ethereum Name Service (ENS) to serve as a decentralized directory for verifiable, human-readable financial routing endpoints:

#### 1. vIBAN (Virtual IBAN)
A vIBAN is a standard-compliant, ENS-routable virtual IBAN directly attached to a domain’s text record:
- **ENS Record Gating:** A `viban` text record (e.g., `viban=EE47...`) is registered onto an ENS domain (e.g., `innovator.eth`).
- **Hierarchical Resolution:** A decentralized tree of Country and Bank Resolvers (operated by regional cooperatives and guilds) maps these human-readable strings to active manifold smart contract addresses.
- **Double Verification:** 
  1. The sender's wallet queries the resolver for the recipient's ENS domain.
  2. The resolver validates the ENS record and verifies a signed cryptographic message proving ownership of the corresponding `viban` string. If resolved successfully, the system executes locally, converting the transaction into a near-instant native smart contract transfer.

#### 2. vSWIFT Messaging
An atomic payment messaging protocol executing on the high-speed backbone (such as [Elysium](../network/09_l2_elysium_backbone.md)). Unlike legacy SWIFT, which merely transmits data instructions that are settled manually days later, a vSWIFT message bundles the payment instruction with a Zero-Knowledge Proof (ZKP) of Solvency. The payment instruction and the value movement are fully atomic: the receipt of the message *is* the settlement.

---

### 23.2. deIBAN & deSWIFT Settlement Infrastructure

While vIBAN acts as the address space, deIBAN functions as the settlement engine, managing the physical and digital bridging layers:

- **On-Chain Fiat Bridging:** Dynamic minting of compliant stablecoins (such as $EURe$) upon receipt of traditional fiat bank transfers, alongside burning stablecoins to trigger off-chain bank credits via regulated, automated proxies.
- **deSWIFT Instant Settlement:** Utilizing high-capacity backbones to handle instant, cross-border token swaps (e.g., $USD \leftrightarrow EUR$) without routing through intermediate correspondent banks.
- **Off-Chain SEPA Fallback:** If an IBAN query fails to resolve an equivalent `vIBAN` on-chain (returning a `NOROUTE` signal), the deIBAN gateway automatically triggers fallback routing. The transaction is routed to a designated Burn Address (a Redemption Contract) along with the destination IBAN parameters, executing a traditional bank wire via an automated fiat gateway.

---

### 23.3. CountryResolver Solidity Contract Specification

The following Solidity contract represents the base layer Country and Bank Resolver routing specification:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IBankResolver {
    function resolve(string calldata bban) external view returns (address wallet, string memory ens);
}

contract CountryResolver {
    address public constant BURN_ADDRESS = 0x000000000000000000000000000000000000dEaD;
    mapping(bytes2 => address) public bankResolvers;

    event ResolverUpdated(bytes2 indexed countryCode, address indexed resolver);

    function resolve(string calldata iban) external view returns (address wallet, string memory ens) {
        (bytes2 country, string memory bban) = parseIBAN(iban);
        address resolver = bankResolvers[country];
        if (resolver != address(0)) {
            return IBankResolver(resolver).resolve(bban);
        }
        return (BURN_ADDRESS, "NOROUTE");
    }

    function parseIBAN(string calldata iban) internal pure returns (bytes2 country, string memory bban) {
        // Extracts the 2-letter country code and the remaining Basic Bank Account Number (BBAN)
        bytes calldata ibanBytes = bytes(iban);
        require(ibanBytes.length >= 4, "Invalid IBAN length");
        country = bytes2(ibanBytes[0:2]);
        bban = string(ibanBytes[4:]);
    }
}
```

---

### 23.4. Strategic Resiliency against Financial Intermediary Tax

By deploying deIBAN/deSWIFT routing rails, regional manufacturers and commerce cooperatives bypass the multi-layered correspondent banking network dominated by the legacy financial cartels:

- **Fee Elimination:** Operational costs drop from conventional $30–$100 bank wire fees to less than a fraction of a cent per batch via [Based Nano-Manifolds](../network/11_based_nano_rollups.md).
- **Zero Settlement Delay:** Transactions are settled with cryptographic finality in minutes rather than being delayed for days by compliance processing and geographical clearinghouses.
- **Sovereign Access:** Anchored to decentralized consensus nodes, no centralized state or corporate banking entity can freeze or disconnect a deIBAN/deSWIFT routing endpoint, guaranteeing permanent, uninterrupted access to global liquidity pools.
