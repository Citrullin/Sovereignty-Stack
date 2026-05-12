# Safe{CON} 2024 — bit.block WoT PoC Firmware

This is a **W3C Web of Things (WoT) Proof of Concept** running on an ESP32-based
bit.block device. It was demonstrated at Safe{CON} 2024 with the Astronaut on the
Moon set.

It is the lowest-level implementation of the **Heartbeat Oracle** concept: a
physical device that exposes its state and accepts commands via a W3C Thing
Description over WiFi — no cloud, no proprietary protocol.

> **Note:** This is Arduino IDE code — a PoC/learning tool, not production firmware.
> For the upstream RIOT-OS WoT implementation (W3C plugfest-tested), see
> [`software/web-of-things/RIOT-OS/`](../../web-of-things/RIOT-OS/).

## Dependencies

- **WoT Library**: [`software/web-of-things/arduino/`](../../web-of-things/arduino/) —
  the forked `web-of-thing-arduino` WebThings library that provides `Thing.h`,
  `WebThingAdapter.h` etc. This submodule must be initialised before compiling.
- **Hardware**: [`hardware/bit.block/`](../../../hardware/bit.block/) — the bit.block
  ESP32 board (KiCAD files, 3D prints)
- SD card with MP3 files flashed, and a trained speech recognition model for
  voice commands.

## Setup

1. `git submodule update --init` to pull the WoT arduino library
2. Open `sketch_may21a.ino` in Arduino IDE
3. Set WiFi credentials (`ssid`/`password`) in the sketch
4. Flash to the bit.block ESP32

## API — Thing Description Endpoints

The device exposes a W3C WoT Thing Description at `/.well-known/wot-thing-description`.

| Endpoint | Method | Example Payload |
| :--- | :--- | :--- |
| `<IP>/.well-known/wot-thing-description` | GET | *None* |
| `<IP>/things/bit_block/actions/sound` | POST | `{"repeat": 0, "data": [[57, 200], [0, 0]]}` |
| `<IP>/things/bit_block/actions/stop_sound` | POST | `{}` |
| `<IP>/things/bit_block/actions/moon_light` | POST | `{"repeat": 1, "data": [[1000, 255, 0, 0], [1000, 0, 255, 0], [1000, 50, 0, 200], [1000, 50, 150, 155], [1000, 100, 0, 50], [0, 0, 0, 0]]}` |
| `<IP>/things/bit_block/actions/base_light` | POST | `{"repeat": 1, "data": [[keep, index, time, r, g, b], ...]}` |
| `<IP>/things/bit_block/actions/head_light` | POST | `{"repeat": 1, "data": [[1000, 255, 0, 0], [1000, 0, 255, 0], [1000, 0, 0, 255], [0, 0, 0, 0]]}` |

## Concept References

- [§12 — Heartbeat Oracles](../../../concepts/oracles/12_heartbeat_oracles.md):
  This firmware is a minimal implementation of a device-layer Heartbeat Oracle
- [§16 — SIWE-OIDC Bridge](../../../concepts/identity-governance/16_siwe_oidc_bridge.md):
  Future iteration: gate WoT actions behind SIWE-verified identity
- [§11 — L3/L4 Nano-Rollups](../../../concepts/architecture/11_l3_l4_nano_rollups.md):
  bit.block as an L4 device node in the sovereign mesh