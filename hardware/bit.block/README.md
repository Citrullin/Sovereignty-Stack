# Bit.block

Bit.block are smart microbricks. They can carry electricity and data, and be stacked
together to form larger structures. Each one can also act as a pin and attach to a
breadboard for faster prototyping.

They may include sensors or actuators to interact with the physical world — making
them physical implementations of the **Heartbeat Oracle** and **Actuator Oracle**
concepts at the L4 (device) layer of the recursive architecture.

## Contents

| Directory | Description |
|---|---|
| [Prototypes](prototypes/) | Pictures and videos of bit.block prototypes (PoC, v1 etc.) |
| [Board](board/) | KiCAD PCB design files (`bit_block.kicad_pcb`, schematic, RGB LEDs, USB audio) |
| [3D prints](3D-prints/) | 3D print files for the Astronaut on the Moon set |
| [3D Web Emulation](3D-web-emulation/) | Three.js web app to view and interact with the 3D astronaut set in-browser |

## Related Software

- [`software/bit.block/arduino/safe-con-2024/`](../../software/bit.block/arduino/safe-con-2024/) —
  Arduino WoT firmware (Safe{CON} 2024 PoC). Runs on the bit.block ESP32, exposes a
  W3C Web of Things Thing Description over WiFi.
- [`software/web-of-things/arduino/`](../../software/web-of-things/arduino/) —
  The forked WebThings library the firmware depends on.

## Related Hardware

- [`hardware/tinyblock/ldraw/astronaut/`](../tinyblock/ldraw/astronaut/) —
  LDraw design files for the Astronaut on the Moon set
- [`hardware/tiny-pay/`](../tiny-pay/) — NFC disc for payment/identity at the device level

## Concept References

- [§12 — Heartbeat Oracles](../../concepts/oracles/12_heartbeat_oracles.md):
  bit.block devices as Secure Element-based Proof of Productivity nodes
- [§13 — Actuator Oracles](../../concepts/oracles/13_actuator_oracles.md):
  bit.block as a physical action oracle at the L4 device layer
- [§11 — L3/L4 Nano-Rollups](../../concepts/architecture/11_l3_l4_nano_rollups.md):
  How devices like bit.block fit into the logN/Logtree mesh