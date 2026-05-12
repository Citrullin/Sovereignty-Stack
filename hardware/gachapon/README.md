# Gachapon — Physicalized Based Rollup Node

The Gachapon machine is not just a toy vending unit. In the Sovereignty Stack, it
is a **Physicalized Based Rollup Node**: a point-of-sale interface for the
on-chain economy that any person can interact with using only an NFC disc or badge.

It represents the "Soft-Gambling Hook" — the familiar "surprise and delight"
mechanics of capsule toys used as a frictionless on-ramp into the on-chain
ecosystem. No crypto exchange required.

## Concept References

- [§3 — Fukuyama High-Trust / Beep-to-Verify](../../concepts/identity-governance/16_siwe_oidc_bridge.md):
  The Gachapon with LCD panel demonstrates how an NFC badge "beep" can trigger
  smart contract interactions physically.
- [§15 — Recycling NFTs](../../concepts/recycling-game/15_recycling_nfts.md):
  Gachapon machines can dispense physical assets tied to NFTs (e.g. Rare Bottle
  NFTs redeemed for capsule toys).
- [§22 — Crypto-Native Cash](../../concepts/banking-physicalization/22_crypto_native_cash.md):
  Revenue from each capsule sale routes on-chain automatically: designer
  royalties, operator fees, DAO treasury — no middleware.

## Physical Setup

The machine accepts coin input (see [Coin Acceptor Manual](Coin-Acceptor_Manual.pdf))
and can be extended with NFC/RFID readers for wallet-based payment via Wahfare
discs or NFC Social Badges.

## Media

| File | Description |
|---|---|
| [crypto-native-cash-gachapon.mp4](crypto-native-cash-gachapon.mp4) | Full demo: crypto-native cash payment at a Gachapon |
| [welcome-to-the-gachapon-world.mp4](welcome-to-the-gachapon-world.mp4) | Introduction video |
| [coin-take-out-the-gachapon.mp4](coin-take-out-the-gachapon.mp4) | Coin acceptor mechanism |
| [gachapon_at_cypherpunk_rave.png](gachapon_at_cypherpunk_rave.png) | Gachapon deployed at a cypherpunk event |
| [assembled_set_capsules.jpg](assembled_set_capsules.jpg) | Assembled microblock sets in capsules |
| [gachapon_capsules.jpg](gachapon_capsules.jpg) | Capsule contents overview |

## Related Hardware

- [`hardware/tiny-pay/`](../tiny-pay/) — The NFC disc (Wahfare / Social Badge) used
  for payment at the Gachapon
- [`hardware/tinyblock/`](../tinyblock/) — The microblock sets dispensed inside capsules

## Related Software

- [`software/bit.block/`](../../software/bit.block/) — The WoT firmware that can
  expose machine state as a W3C Thing Description on the local network
