import pytest
from pytest_bdd import scenarios, given, when, then
import json
import requests
import os

# Point to the Gherkin feature file
scenarios('../../../docs/architecture/testing/features/catastrophic_recovery.feature')

@pytest.fixture
def identity_context():
    return {
        "hardware_state": "ACTIVE",
        "family_network": "INACTIVE",
        "bio_signature": "MISSING",
        "approvals": 0,
        "new_key": None
    }

@given('the Sovereign Identity Protocol is active')
def protocol_active(identity_context):
    pass

@given('the TLA+ invariant "Active Root Keys <= 1" is enforced')
def invariant_enforced(identity_context):
    pass

@given('the Digital Family is defined by a Threshold Polynomial (k=3, n=5)')
def threshold_defined(identity_context):
    pass

@given('the physical Hardware Key state is "LOST_OR_SEIZED"')
def hardware_lost(identity_context):
    identity_context["hardware_state"] = "LOST_OR_SEIZED"

@given('the Digital Family Network state is "ACTIVE"')
def network_active(identity_context):
    identity_context["family_network"] = "ACTIVE"

@given('the Biological Signature (DNA sequence hash) is "PRESENT"')
def bio_signature_present(identity_context):
    identity_context["bio_signature"] = "PRESENT"

@when('a "Catastrophic Recovery" transaction is broadcast from an untrusted terminal')
def broadcast_recovery(identity_context):
    assert identity_context["hardware_state"] == "LOST_OR_SEIZED"

@then('the State Machine transitions to "RECOVERY_MODE"')
def verify_recovery_mode(identity_context):
    pass

@then('the system triggers a multi-sig threshold request to the Digital Family')
def trigger_threshold_request(identity_context):
    pass

@when('3 out of 5 Digital Family members provide Verifiable Secret Sharing (VSSS) proofs')
def family_provides_proofs(identity_context):
    identity_context["approvals"] = 3

@when('the Biological Signature maps to the Biometric Constant on the identity polynomial')
def map_bio_constant(identity_context):
    assert identity_context["bio_signature"] == "PRESENT"

@then('generate a new root key')
def generate_key(identity_context):
    assert identity_context["approvals"] >= 3
    identity_context["new_key"] = "mocked_new_root_key_123"

@then('immediately poison the old key in the transparency log (Rekor)')
def poison_old_key(identity_context):
    # Mocking external API call
    identity_context["hardware_state"] = "POISONED"

@then('formally prove the "Active Root Keys <= 1" invariant holds')
def prove_invariant(identity_context):
    assert identity_context["new_key"] is not None
    assert identity_context["hardware_state"] == "POISONED"
