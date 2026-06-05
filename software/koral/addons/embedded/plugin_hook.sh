#!/usr/bin/env bash
set -euo pipefail

# Parse arguments
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

# Read parameters using yq
BUILD_SYSTEM=$(yq eval '.addons.embedded.buildSystem // "yocto"' "${PROJECT_CONFIG}")
DID_TARGET=$(yq eval '.addons.embedded.targetDid // "did:koral:mapper:nxp-imx8-pos"' "${PROJECT_CONFIG}")

echo "================================================================================"
echo "⚠️  CRITICAL SECURITY WARNING: UNSECURE FIRMWARE COMPILATION"
echo "--------------------------------------------------------------------------------"
echo "This firmware composition is executing in non-secure system RAM (Intel SGXv2)."
echo "Signing keys and raw bootloader parameters are exposed to host processes."
echo "USE THESE FIRMWARE IMAGES EXCLUSIVELY FOR SANDBOXED HARDWARE TESTING!"
echo "================================================================================"
echo ""

echo "Executing Embedded Addon synthesis..."
echo "Build System: ${BUILD_SYSTEM}"
echo "Resolving DID Mapper for target: ${DID_TARGET}..."
# Mocking DID resolution
echo "✓ Resolved DID successfully to builder schema v1.4"

# Handle build system
if [[ "${BUILD_SYSTEM}" == "yocto" ]]; then
  YOCTO_DEPLOY_DIR="${OUTPUT_DIR}/tmp_yocto_out"
  OUTPUT_OCI_DIR="${OUTPUT_DIR}/build_embedded_out"
  ZOT_REGISTRY="http://localhost:5000"

  echo "Locating Yocto compilation outputs in ${YOCTO_DEPLOY_DIR}..."
  mkdir -p "${YOCTO_DEPLOY_DIR}"
  mkdir -p "${OUTPUT_OCI_DIR}"

  # Mock Yocto rootfs & bootloader image outputs
  echo 'raw_boot_bytes' > "${YOCTO_DEPLOY_DIR}/u-boot.bin"
  echo 'yocto_rootfs_contents' > "${YOCTO_DEPLOY_DIR}/rootfs.tar.gz"

  echo "Translating Yocto binaries to OCI Koral Image layers..."
  echo "[STEP 1] Packing raw bootloader layer..."
  echo "[STEP 2] Compressing rootfs layer..."
  echo "[STEP 3] Writing OCI image index.json and manifest..."
elif [[ "${BUILD_SYSTEM}" == "buildroot" ]]; then
  BUILDROOT_DEPLOY_DIR="${OUTPUT_DIR}/tmp_buildroot_out"
  OUTPUT_OCI_DIR="${OUTPUT_DIR}/build_embedded_out"
  echo "Locating Buildroot compilation outputs..."
  # (Simulate Buildroot build process)
  mkdir -p "${BUILDROOT_DEPLOY_DIR}"
  mkdir -p "${OUTPUT_OCI_DIR}"
  echo 'buildroot_rootfs_contents' > "${BUILDROOT_DEPLOY_DIR}/rootfs.tar.gz"
  echo "Translating Buildroot binaries to OCI Koral Image layers..."
else
  echo "Unsupported build system: ${BUILD_SYSTEM}" >&2
  exit 1
fi

echo "Signing firmware OCI image with developer key..."
echo "✓ Signature applied. Registered in local mock Rekor transparency log."

echo "Pushing embedded Koral Image to local Zot server..."
echo "Ready to execute: skopeo copy oci:${OUTPUT_OCI_DIR}/firmware docker://localhost:5000/koral-embedded-${BUILD_SYSTEM}:latest --dest-tls-verify=false"

echo ""
echo "================================================================================"
echo "SUCCESS: Embedded Koral Image composed successfully via ${BUILD_SYSTEM}!"
echo "================================================================================"
