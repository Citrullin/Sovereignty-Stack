# Microblocks — Software

This directory has two distinct scopes:

## 1. `microblock_ldraw/` — Parts Library (Submodule)

A git submodule (`github.com:bind-systems/ldraw_microblock.git`) containing the
LDraw parts library for microblocks: bricks, plates, primitives in `.dat` format.

This is the **parts palette** used by MLCAD and other LDraw-compatible tools when
designing sets. Required by the AI parsing pipeline as the target vocabulary.

> `git submodule update --init software/tinyblock/microblock_ldraw`

## 2. `instructions/` — AI Training Benchmark Images

A curated set of physical microblock instruction booklets (photographed/scanned)
used as input benchmarks for the AI instruction parser pipeline.

| Model | Format | Notes |
|---|---|---|
| Clownfish | .webp | Simple two-page instruction |
| Black Cat | .jpeg | Multi-picture instruction |
| Snake | .jpeg | Two-page with rotations |
| Soldier | .jpeg | Includes stickers and uncommon parts |
| Kitty Airplane | .png | Two-page vertical scan |

These images represent the "2D input" side of the pipeline. The target output is
LDraw (`.ldr`) using parts from `microblock_ldraw/`.

## Tooling

**MLCAD** is bundled as `MLCad_V3.40.zip`. It is Windows-only but the most
stable tool for microblock-compatible LDraw editing.
In the web viewer, different layout sizes don't cause issues.

## Concept References

- [§44 — AI Instruction Parser](../../concepts/tokenomics/44_ai_instruction_parser.md):
  The full pipeline: MobileViT → Layer 0 ground truth → Offset Solver → LDraw
- [§40 — Prediction Markets](../../concepts/tokenomics/40_prediction_markets.md):
  Set designs and instruction data feed the microblock industry forecasting market
- [§41 — TinyMeritRank](../../concepts/tokenomics/41_merit_token_distribution.md):
  The DAO community creates and validates instruction datasets — a merit-earning activity

## Related

- [`hardware/tinyblock/ldraw/`](../../hardware/tinyblock/ldraw/) —
  Finished set design files (the output of the design process)
- [`software/web-of-things/`](../web-of-things/) — The WoT layer that connects
  physical sets to on-chain state