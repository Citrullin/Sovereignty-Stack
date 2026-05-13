# Sovereign Identity Worker (Prototype)

This directory contains the compilable pipeline that transpiles human-readable intent (Gherkin "Social Contracts") into cryptographic reality (Signed OCI Images).

## The Refinery Pipeline
We do not use shell scripts to manage state. We use a **Refinery Pipeline** moving through layers of increasing "Hardness":
1. **Intent (Gherkin/BPMN):** The Sociologist defines the "What" (`docs/architecture/testing/features/`).
2. **Validation (Rust/TLA+):** The Math proves the "What" is safe. This worker uses Rust's Enum type system to make illegal state transitions mathematically unrepresentable in memory.
3. **Synthesis (Buildah/TEE):** The Machine builds the "How" (the OCI image) inside a hardware enclave.
4. **Attestation (Cosign/Rekor):** The Hardware proves the "How" actually happened.

## Architecture

- `src/lib.rs`: The Finite State Machine (FSM). It defines `IdentityState` using Rust Enums. Because of Rust's ownership model, when the old key is poisoned, the state mutates irreversibly.
- `tests/cucumber_test.rs`: The BDD test suite utilizing `cucumber-rs`. It reads the sociologist's plain-text `.feature` files and binds them to the underlying cryptographic state machine.

### Integration with OCI & BPMN

In production, this worker acts as a gRPC endpoint for a BPMN Orchestrator like **Zeebe** (Camunda 8).
Once the state machine successfully completes the `generate_new_root_key` step, the worker synthesizes the proof:

```bash
# Push the recovery proof to the registry
oras push registry.sovereignty.io/recovery/dev-01:v2 \
  --artifact-type application/vnd.sovereignty.recovery+json \
  recovery_proof.json

# Sign the artifact with the TEE hardware key
cosign sign --key tpm://handle_1234 registry.sovereignty.io/recovery/dev-01:v2 \
  -a "attestation=$(cat tee_quote.json)" \
  -a "scenario=catastrophic_recovery"
```

## Running the Verification

To run the formal Gherkin validation against the FSM:
```bash
cargo test --test cucumber_test
```
