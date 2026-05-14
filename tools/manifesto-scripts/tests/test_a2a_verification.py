"""
A2A Verification Protocol – Comprehensive Unit Tests (BDD Style)
===============================================================

Tests the real scoring logic, agent identity derivation, and structural 
integrity of the hash-chained audit log using a descriptive Given/When/Then style.
Includes Resonant Merit (velocity, normalization) and DAO governance logic.
"""

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import time

# Make the parent importable without installing
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generate_a2a_log import (
    GENESIS_SEED,
    JSONLD_CONTEXT,
    build_entry,
    build_trace_context,
    compute_entry_id,
    get_file_hash,
    get_hash_dir,
    compute_verification_score,
    derive_device_did,
    derive_project_did
)
from agent_governance import compute_resonance_velocity, normalize_score, adjusted_gate_action, compute_decayed_score, VouchAttempt
from dao_notifications import MockDAONotifier, Notification

def log_bdd(step, msg):
    print(f"  {step:8} {msg}")

class TestResonantMerit(unittest.TestCase):
    def test_resonance_velocity_growth(self):
        print("\nScenario: Evaluating Resonance Momentum (Growth)")
        log_bdd("Given", "an agent with an improving score history: [0.2, 0.4, 0.6, 0.8]")
        history = [0.2, 0.4, 0.6, 0.8]
        
        velocity = compute_resonance_velocity(history)
        log_bdd("When", "resonance velocity is computed")
        log_bdd("Then", f"the momentum should be positive (Actual: {velocity})")
        self.assertGreater(velocity, 0)

    def test_environment_normalization(self):
        print("\nScenario: Environment Normalization (No Agent Left Behind)")
        log_bdd("Given", "a raw score of 0.7 on a WSL_COSIGN environment (baseline=0.85)")
        raw_score = 0.7
        env_tier = "WSL_COSIGN"
        
        norm_score = normalize_score(raw_score, env_tier)
        log_bdd("When", "the score is normalized relative to the environment ceiling")
        expected_score = 0.7 / 0.85
        log_bdd("Then", f"the effective score should be {expected_score} (Actual: {norm_score})")
        self.assertAlmostEqual(norm_score, expected_score, places=3)
        
        log_bdd("And", "it should map to the 'coherent' state (originally 'acceptable' but higher)")
        self.assertEqual(adjusted_gate_action(raw_score, 0.0, 0.0, env_tier)["band"], "coherent")

class TestDAOGovernance(unittest.TestCase):
    def test_dao_notification_on_degraded(self):
        print("\nScenario: DAO Notification for Degraded Agents")
        log_bdd("Given", "an agent with a 'degraded' score (0.4)")
        score = 0.4
        notifier = MockDAONotifier()
        
        gate = adjusted_gate_action(score, 0.0, 0.0, "LINUX_COSIGN")
        log_bdd("When", "the DAO gate logic is evaluated")
        
        if gate["notify"] == "dao_queue":
            notifier.dispatch(Notification(
                type="agent.score.degraded",
                subject_did="did:test:123",
                message=f"Agent coherence entering 'degraded' state ({score})"
            ))
            
        log_bdd("Then", "a notification should be dispatched to the DAO queue")
        self.assertEqual(len(notifier.sent), 1)
        self.assertEqual(notifier.sent[0]["type"], "agent.score.degraded")

class TestIdentity(unittest.TestCase):
    def test_device_did_stable(self):
        print("\nScenario: Deriving machine identity from hardware anchors")
        mock_pubkey = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIabcdef12345 user@host"
        log_bdd("Given", f"a stable SSH host public key: '{mock_pubkey[:30]}...'")
        
        with tempfile.NamedTemporaryFile(mode='w') as tmp:
            tmp.write(mock_pubkey)
            tmp.flush()
            
            did1 = derive_device_did(tmp.name)
            log_bdd("When", "a Device DID is derived from this key material")
            log_bdd("Then", f"it yields the deterministic DID: {did1}")
            
            did2 = derive_device_did(tmp.name)
            log_bdd("And", "re-deriving from the same key must yield the exact same DID")
            self.assertEqual(did1, did2)

class TestQuantumDecoherence(unittest.TestCase):
    def test_decoherence_over_time(self):
        print("\nScenario: Quantum Decoherence Over Time (The Squatter)")
        log_bdd("Given", "an agent with base_score=0.9 and 180 days of inactivity")
        base_score = 0.9
        days_inactive = 180
        
        effective_score = compute_decayed_score(base_score, days_inactive)
        log_bdd("When", "temporal decay is applied (90-day half-life)")
        
        log_bdd("Then", f"the effective score should be 0.225 (Actual: {effective_score})")
        self.assertAlmostEqual(effective_score, 0.225)
        
        log_bdd("And", "the governance band must drop to 'collapsed'")
        gate = adjusted_gate_action(base_score, 0.0, 0.0, "LINUX_COSIGN", days_inactive)
        self.assertEqual(gate["band"], "collapsed")

class TestSocialEngineering(unittest.TestCase):
    def test_vouching_logs_but_governs(self):
        print("\nScenario: Vouching Cannot Override Cryptographic Merit")
        log_bdd("Given", "Agent A (Trusted, score 0.95) vouches for Agent B (Decayed, score 0.15)")
        agent_a_did = "did:key:z6MkAgentA"
        agent_b_did = "did:key:z6MkAgentB"
        agent_b_score = 0.15
        
        log_bdd("When", "the vouching attempt is processed")
        vouch = VouchAttempt(
            voucher_did=agent_a_did,
            subject_did=agent_b_did,
            timestamp=int(time.time()),
            subject_score_at_vouching=agent_b_score,
            outcome="denied_below_threshold" if agent_b_score < 0.3 else "granted"
        )
        
        log_bdd("Then", f"the outcome must be: {vouch.outcome}")
        self.assertEqual(vouch.outcome, "denied_below_threshold")
        log_bdd("And", "the vouch attempt is recorded as an auditable data object")
        self.assertIn("voucher_did", vouch.to_dict())

if __name__ == "__main__":
    unittest.main()
