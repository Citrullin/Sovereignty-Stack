# tiny-pay — NFC Crypto-Native Cash Hardware

This directory contains hardware prototypes and media for the **physical layer of
the Sovereignty Stack's payment system**: NFC-enabled instruments that carry
cryptographic value in the real world.

Two distinct products live here:

## 1. NFC Social Badge / Tiny Disc

A low-cost, rugged NFC chip embedded in a card, disc, or paper form factor. Acts
as the **Key A physical possession layer** in the 3-Key Consortium model (§43).

Operates in two modes:

| Mode | Description | Use Case |
|---|---|---|
| **Banknote Mode** (Movable) | Value is "jailed" on the physical object. Bearer instrument — possession = ownership. Destroy-to-settle rule prevents double-spend. | P2P payments, Gachapon, Recycling Game |
| **Badge Mode** (Identity-bound) | NFC chip acts as Key A in 3-Key Consortium. Requires Key B (smartphone/biometric) to co-sign. | SIWE login, Maintenance handshake, High-value auth |

Demo videos:
- [NFC Tiny Disc wallet demo](NFC-crypto-native-cash-wallet-tiny-disc.m4v)
- [E-Ink NFC wallet tag demo](tiny-eink-NFC-crypto-native-cash-wallet-tag.m4v)

Images:
- [NFC Badge](img/NFC_Badge.png) — The Social Badge form factor
- [NFT Keychain](img/NFT_keychain.png) — NFT-linked keychain variant
- [Community NFT Keychain](img/community_NFT_keychain.jpg) — Sociological extension
  of existing community NFT keychains (referenced in root README)

## 2. Wahfare

**Wahfare** is the branded Crypto Native Cash disc product — see [`wahfare-hits/`](wahfare-hits/).

It is the physical "banknote" equivalent of the stack: a fun, collectible NFC/RFID
disc designed for everyday P2P value transfer.

## Concept References

- [§22 — Crypto-Native Cash](../../concepts/banking-physicalization/22_crypto_native_cash.md):
  The full consortium model (Key A/B/C), banknote vs badge mode, ERC-4337 integration
- [§18 — 3-Factor Sovereign Auth](../../concepts/identity-governance/18_3factor_auth.md):
  How NFC Badge + smartphone + password create tiered access (table)
- [§43 — Crypto-Native Cash Spec](../../concepts/tokenomics/43_crypto_native_cash_spec.md):
  Physical, digital and technical specification

## Related Hardware

- [`hardware/gachapon/`](../gachapon/) — Gachapon machine that accepts NFC disc payment
- [`hardware/bit.block/`](../bit.block/) — Smart bricks with embedded NFC capability
