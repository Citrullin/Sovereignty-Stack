#!/usr/bin/env bash
set -euo pipefail

ENTITY_DIR=""
OUTPUT_DIR=""
PROJECT_CONFIG=""

while [[ $# -gt 0 ]]; do
  case $1 in
    --entity-dir) ENTITY_DIR="$2"; shift 2 ;;
    --output-dir) OUTPUT_DIR="$2"; shift 2 ;;
    --config) PROJECT_CONFIG="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

ENTITY_NAME=$(basename "${ENTITY_DIR}")

echo "Executing Tinyblock Addon synthesis..."
GENESIS_BUNDLE="${OUTPUT_DIR}/tinyblock-genesis-${ENTITY_NAME}.tar.gz"
tar -czf "${GENESIS_BUNDLE}" -C "${ENTITY_DIR}" addons/tinyblock/ || true
echo "     [SIMULATED] oras push localhost:5000/blockchain/${ENTITY_NAME}:genesis --artifact-type application/vnd.koral.genesis ${GENESIS_BUNDLE}"
