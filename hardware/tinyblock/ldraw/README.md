# Tinyblock LDraw Set Designs

This directory contains **set design artifacts** — LDraw model files for specific
physical sets (Astronaut on the Moon, Lighthouse). These are finished or in-progress
designs for physical sets, not the parts library.

> **⚠️ Note:** This is NOT the microblock parts library (bricks, plates, etc.).
> The LDraw parts/primitives library lives in the git submodule at
> [`software/tinyblock/microblock_ldraw/`](../../../software/tinyblock/microblock_ldraw/)
> (sourced from `github.com:bind-systems/ldraw_microblock.git`).

## Sets

| File / Directory | Description |
|---|---|
| [astronaut/](astronaut/) | Astronaut on the Moon — the first bit.block set |
| [lighthouse.ldr](lighthouse.ldr) | Lighthouse set (no bit.block integration yet) |

## Tooling

Recommended: **MLCAD** (Windows only, but stable and microblock-compatible). See
[`software/tinyblock/`](../../../software/tinyblock/) for the bundled MLCAD zip.

## Concept References

- [§44 — AI Instruction Parser](../../../concepts/tokenomics/44_ai_instruction_parser.md):
  These LDraw files are the target output format for the AI pipeline that converts
  2D microblock instructions into 3D models (MobileViT → Layer 0 → LDraw)
- [§40 — Prediction Markets](../../../concepts/tokenomics/40_prediction_markets.md):
  Set designs feed the microblock industry prediction market (demand forecasting)

## Related

- [`software/tinyblock/instructions/`](../../../software/tinyblock/instructions/) —
  AI training benchmark images (the 2D instructions the parser reads)
- [`hardware/bit.block/`](../../bit.block/) — The electronic hardware paired with these sets
