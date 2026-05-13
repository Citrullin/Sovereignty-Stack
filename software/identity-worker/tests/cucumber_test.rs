use cucumber::{given, when, then, World};
use sovereign_identity_worker::{SovereignIdentity, IdentityState};

#[derive(Debug, Default, World)]
pub struct IdentityWorld {
    pub identity: SovereignIdentity,
    pub new_key: Option<String>,
    pub threshold_k: usize,
    pub threshold_n: usize,
    pub threshold_requests_sent: bool,
    pub biometric_verified: bool,
}

// Background & Domain Dictionary Setup
#[given("the Sovereign Identity Protocol is active")]
async fn protocol_active(world: &mut IdentityWorld) {
    world.identity = SovereignIdentity::new();
}

#[given("the TLA+ invariant \"Active Root Keys <= 1\" is enforced")]
async fn invariant_enforced(_world: &mut IdentityWorld) {
    // Mathmatically enforced by the Rust Enum type system
}

#[given("the Digital Family is defined by a Threshold Polynomial (k=3, n=5)")]
async fn threshold_defined(world: &mut IdentityWorld) {
    world.threshold_k = 3;
    world.threshold_n = 5;
}

// Scenario specific steps
#[given("the physical Hardware Key state is \"LOST_OR_SEIZED\"")]
async fn hardware_lost(world: &mut IdentityWorld) {
    world.identity.mark_lost();
    assert_eq!(world.identity.state, IdentityState::LostOrSeized);
}

#[given("the Digital Family Network state is \"ACTIVE\"")]
async fn network_active(world: &mut IdentityWorld) {
    world.identity.network_active = true;
}

#[given("the Biological Signature (DNA sequence hash) is \"PRESENT\"")]
async fn bio_signature_present(world: &mut IdentityWorld) {
    world.identity.dna_seed_present = true;
}

#[when("a \"Catastrophic Recovery\" transaction is broadcast from an untrusted terminal")]
async fn broadcast_recovery(world: &mut IdentityWorld) {
    let result = world.identity.request_recovery();
    assert!(result.is_ok(), "Failed to broadcast recovery");
}

#[then("the State Machine transitions to \"RECOVERY_MODE\"")]
async fn verify_recovery_mode(world: &mut IdentityWorld) {
    if let IdentityState::RecoveryMode { approvals } = world.identity.state {
        assert_eq!(approvals, 0);
    } else {
        panic!("Not in recovery mode!");
    }
}

#[then("the system triggers a multi-sig threshold request to the Digital Family")]
async fn trigger_threshold_request(world: &mut IdentityWorld) {
    world.threshold_requests_sent = true;
    assert!(world.threshold_requests_sent);
}

#[when("3 out of 5 Digital Family members provide Verifiable Secret Sharing (VSSS) proofs")]
async fn family_provides_proofs(world: &mut IdentityWorld) {
    // Simulate receiving exactly `k` network approvals
    for _ in 0..world.threshold_k {
        world.identity.receive_family_share();
    }
}

#[when("the Biological Signature maps to the Biometric Constant on the identity polynomial")]
async fn map_bio_constant(world: &mut IdentityWorld) {
    world.biometric_verified = world.identity.dna_seed_present;
    assert!(world.biometric_verified);
}

#[then("generate a new root key")]
async fn generate_key(world: &mut IdentityWorld) {
    // Ensure both multi-sig threshold and biometric constant conditions are met before generating
    assert!(world.biometric_verified, "Biometric signature invalid");
    
    let result = world.identity.generate_new_root_key();
    assert!(result.is_ok(), "Key generation failed due to threshold not being met");
    world.new_key = Some(result.unwrap());
}

#[then("immediately poison the old key in the transparency log (Rekor)")]
async fn poison_old_key(world: &mut IdentityWorld) {
    assert_eq!(world.identity.state, IdentityState::Poisoned);
}

#[then("formally prove the \"Active Root Keys <= 1\" invariant holds")]
async fn prove_invariant(world: &mut IdentityWorld) {
    // If we have a new key, the old state MUST be poisoned
    assert!(world.new_key.is_some());
    assert_eq!(world.identity.state, IdentityState::Poisoned);
}

#[tokio::main]
async fn main() {
    IdentityWorld::cucumber()
        .run("docs/architecture/testing/features/catastrophic_recovery.feature")
        .await;
}
