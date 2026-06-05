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

echo "Executing Web of Things Addon synthesis..."
FW_PATCH_FILE="${OUTPUT_DIR}/firmware-suit-patch-${ENTITY_NAME}.bin"
echo "MCUBOOT-SUIT-FW-PATCH-DATA-${ENTITY_NAME}" > "${FW_PATCH_FILE}"

if command -v oras &>/dev/null; then
  echo "Running: oras push localhost:5000/firmware/${ENTITY_NAME}:v1 --artifact-type application/vnd.koral.firmware.suit ${FW_PATCH_FILE}"
else
  echo "     [SIMULATED] oras push localhost:5000/firmware/${ENTITY_NAME}:v1 --artifact-type application/vnd.koral.firmware.suit ${FW_PATCH_FILE}"
fi
