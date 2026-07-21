# Chapter 07: Zero-Config Mesh, 6LoWPAN, BLE, & WireGuard Peering

## 7.1 Transport-Agnostic Local Discovery & Mesh Peering

In local-first manifold deployments, edge validator cells and IoT nodes must maintain full operational capability when completely disconnected from central cloud infrastructure or global internet backbones. Relying on public DNS or centralized discovery introduces single points of failure.

The Sovereign Stack implements an autonomous, transport-agnostic local discovery and messaging pipeline utilizing **multicast DNS (mDNS)**, **DNS Service Discovery (DNS-SD)**, and **DIDComm Messaging v2**.

---

## 7.2 Zero-Config Discovery Protocol (`mDNS` / `DNS-SD`)

When a containerized node initializes inside a local network, it bypasses public DNS registration:
1. **Multicast Advertising:** The mDNS daemon advertises presence over link-local IPv6 space (`fe80::/10`) via UDP port 5353 (`ff02::fb`).
2. **Service Discovery:** Uses standardized RFC 6763 service strings:
   ```text
   _didcommv2._udp.local
   ```
3. **Record Resolution:** Resolves PTR, SRV, and TXT records. Crucially, the TXT record contains the node's Base58BTC **Short-Form `did:peer:4` hash**, allowing adjacent peers to verify node identity without ledger queries.

---

## 7.3 Network Compression for IoT: 6LoWPAN, BLE, and CBOR over CoAP/UDP

Running edge validator nodes and Heartbeat Oracles on low-power microcontrollers (e.g. RISC-V / ARM Cortex-M) over lossy wireless networks poses severe packet size constraints. Standard IEEE 802.15.4 frame capacity is 127 bytes.

```text
6LoWPAN + Compressed UDP / CoAP Datagram Byte Layout (Max 127 Bytes):
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| 802.15.4 MAC  | 6LoWPAN IPHC Header (RFC 6282) | UDP Comp Header|
|  (9-23 bytes) |         (2-7 bytes)            |   (1-4 bytes)  |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| CoAP Header (RFC 7252) (4 bytes) | Payload Marker |           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                 Transcoded CBOR State Payload                 |
|                   (Compact JSON-RPC Frame)                    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

### 7.3.1 MTU Frame Sizing Breakdown
- **IEEE 802.15.4 MAC Header:** 9 to 23 bytes.
- **6LoWPAN Header Compression (LOWPAN_IPHC):** Compresses 40-byte IPv6 header down to **2 to 7 bytes**.
- **Compressed UDP / CoAP Header:** Compresses 8-byte UDP header down to **1 to 4 bytes**, followed by 4-byte CoAP header.
- **Available Data Payload:** **~85-95 bytes** available for transcoded CBOR payloads.

### 7.3.2 JSON-RPC to CBOR Transcoding
To query state diffs or submit intents over 6LoWPAN, edge gateways transcode standard verbose JSON-RPC payloads into **Concise Binary Object Representation (CBOR - RFC 8949)**:
- Verbose strings (`"method": "eth_call"`) map to single-byte integer keys (`0x01: 0x0A`).
- Hex cryptographic strings (`0x9bb...78f`) compress to raw byte arrays (`b"\x9b\xb..."`), shrinking payload footprint by **up to 70%**.

### 7.3.3 Freestanding Embedded Network Engine (`smoltcp`)
Bare-metal microcontrollers run **`smoltcp`**, a event-driven Rust networking stack with zero heap allocation. `smoltcp` handles 6LoWPAN frame reassembly, CoAP datagram dispatch, and link-local IPv6 address autoconfiguration without requiring POSIX OS abstractions.

---

## 7.4 DIDComm v2 & Automated WireGuard (`wg0`) Tunnel Orchestration

Once mDNS resolves link-local parameters:
1. **Deriving WireGuard Keys from Master Seed:** The node derives X25519 transport keys directly from the BIP-32 Ed25519 key path ($m/44'/60'/0'/0/0$) via Curve25519 conversion:
   $$K_{\text{x25519}} = \text{ed25519\_pk\_to\_curve25519}(K_{\text{ed25519}})$$
2. **Automated Tunnel Setup:** The node invokes the `sovereign-reth` network daemon to dynamically instantiate a WireGuard tunnel interface (`wg0`):
   ```bash
   # Programmatic wireguard configuration via crate/network/src/wireguard.rs
   wg set wg0 peer <Peer_X25519_PubKey> allowed-ips fe80::/64 endpoint [fe80::1%eth0]:51820
   ```
3. **Zero-Trust Encrypted P2P Backbone:** High-bandwidth data (stateless block witnesses, CDC database streams) flows through encrypted WireGuard tunnels tied directly to `did:peer:4` cryptographic identities.

---

## Codebase Implementation in `sovereign-reth`

- **WireGuard Interface Management:** Implemented in [`crates/network/src/wireguard.rs`](file:///home/citrullin/git/sovereign-reth/crates/network/src/wireguard.rs).
- **Single-Key Handshake Derivation:** Implemented in [`crates/network/src/handshake.rs`](file:///home/citrullin/git/sovereign-reth/crates/network/src/handshake.rs).
