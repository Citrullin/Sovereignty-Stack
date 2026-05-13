#!/bin/bash
set -e

echo "==============================================="
echo "Initializing The Sovereign Sandbox..."
echo "==============================================="

# 1. Generate Cosign Keys if they don't exist
if [ ! -f "cosign.key" ]; then
    echo ">> Generating ephemeral Cosign keys (mocking TEE Hardware Root)..."
    # Set empty password for automation
    env COSIGN_PASSWORD="" cosign generate-key-pair
fi

echo ">> Starting Decentralized Infrastructure (Anvil RPC & IPFS)..."
# Start the mocked infrastructure in the background
podman-compose up -d blockchain-rpc ipfs-node

echo ">> Waiting for IPFS and Anvil to spin up..."
sleep 5

echo ">> Building the Identity Worker Image..."
podman-compose build identity-worker

echo ">> Cryptographically Signing the Identity Worker Image..."
# We use the local image ID to sign it, mocking the TEE Attestation phase
IMAGE_ID=$(podman images -q sovereign-identity-worker:v0.1)
# Note: In a real environment, you'd push to a registry first before signing,
# but for local Sandbox purposes, we just demonstrate the attestation command:
echo "   Mock Cosign Signature Command:"
echo "   cosign sign --key cosign.key -a \"attestation=mocked_tee_quote_xyz\" sovereign-identity-worker:v0.1"

echo ">> Executing the BDD Formal Verification within the TEE Container..."
# Run the test container (this executes `cargo test --test cucumber_test`)
podman-compose run --rm identity-worker

echo "==============================================="
echo "Sovereign Sandbox Verification Complete."
echo "==============================================="
# Clean up
podman-compose down
