# Web of Things — Sovereign IoT Contributions

This directory contains two W3C Web of Things implementations as git submodules,
enabling sovereign IoT devices that expose standardized Thing Descriptions (TD)
over open protocols — no proprietary cloud required.

> [!NOTE]
> We leverage W3C Web of Things (WoT) standards as a pragmatic technical substrate, 
> not as an endorsement of the [captured W3C institution](../../concepts/philosophy/00_w3c_critique.md) (§0). 
> The Sovereignty Stack uses these tools to reclaim the physical web from 
> centralized corporate boards.

## Submodules

### `RIOT-OS/` — W3C WoT CoAP Module
→ `git@github.com:namib-project/RIOT.git`

Adds comprehensive W3C WoT functionality to RIOT-OS:
- Thing Description (TD) code generation
- TD exposure via CoAP (`wot-gcoap2`)
- Tested in W3C WoT plugfests ([report](https://w3c.github.io/wot-architecture/testing/report11.html#impl-riot-wot))
- Tutorial from W3C testing event: [2020.09.Online RIOT-OS prototype](https://github.com/w3c/wot-testing/blob/a7df7b8ab250441c1a0d9667ea18e91883e35287/events/2020.09.Online/prototypes/RIOT-OS/README.md)
- Best code examples: [wot_coap_generation tests](https://github.com/namib-project/RIOT/tree/wot-gcoap2/tests/wot_coap_generation)
- Upstreaming to mainline RIOT would benefit the sovereignty stack significantly

> `git submodule update --init software/web-of-things/RIOT-OS`

### `arduino/` — WebThings Fork (WoT TD 1.0)
→ `git@github.com:Citrullin/web-of-thing-arduino.git`

A fork of the Mozilla WebThings Arduino library, upgraded to support the W3C Web
of Things Thing Description 1.0 specification.

**Primary consumer:** [`software/bit.block/arduino/safe-con-2024/`](../bit.block/arduino/safe-con-2024/) —
the Safe{CON} 2024 bit.block firmware depends on this library for `Thing.h` and
`WebThingAdapter.h`.

> `git submodule update --init software/web-of-things/arduino`

## What These Enable

Together these tools allow building **sovereign IoT devices** — devices that:
- Expose machine-readable APIs (Thing Descriptions) without cloud lock-in
- Can be discovered and controlled by any WoT-compatible client
- Serve as the device-layer building blocks for Heartbeat and Actuator Oracles

Neither has been battle-tested in full production deployments yet, though RIOT-OS
has been validated in W3C plugfest scenarios.

## Concept References

- [§12 — Heartbeat Oracles](../../concepts/oracles/12_heartbeat_oracles.md):
  These WoT tools implement the device-side of the Heartbeat Oracle pattern
- [§13 — Actuator Oracles](../../concepts/oracles/13_actuator_oracles.md):
  WoT Thing Actions are the interface layer for Physical Action Oracles
- [§11 — L3/L4 Nano-Rollups](../../concepts/architecture/11_l3_l4_nano_rollups.md):
  WoT devices feed data into L4 Based Nano-Rollups in the sovereign mesh

## Related

- [`software/bit.block/`](../bit.block/) — Primary firmware using the Arduino WoT submodule
- [`hardware/bit.block/`](../../hardware/bit.block/) — The physical board these run on