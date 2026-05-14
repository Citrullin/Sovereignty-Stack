#!/usr/bin/env python3
import sys
import os
import subprocess

# Add tools/manifesto-scripts to path to reuse governance logic
# Correct relative path: from software/koral/governance/ to tools/manifesto-scripts/ is ../../../tools/manifesto-scripts
manifesto_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../tools/manifesto-scripts"))
sys.path.append(manifesto_path)

try:
    from agent_governance import score_to_band
except ImportError as e:
    print(f"[KORAL-GOV] Error: Could not import manifesto scripts governance logic from {manifesto_path}")
    print(f"[KORAL-GOV] ImportError details: {e}")
    sys.exit(1)

def get_agent_merit(agent_did):
    """
    Mock merit retrieval.
    //TODO: Integrate with verification_history.jsonl or an on-chain registry.
    """
    # High merit for the project agent, low for unknown
    if "Project" in agent_did:
        return 0.95
    return 0.2

def verify_patch_merit(patch_path, agent_did):
    """
    Verifies that a patch is signed by an agent with sufficient merit.
    Enforces the Sovereignty Stack merit-based access control.
    """
    print(f"[KORAL-GOV] Verifying patch: {patch_path}")
    print(f"[KORAL-GOV] Agent DID: {agent_did}")
    
    # 1. Verify Signature (Mocked for now)
    print(f"[KORAL-GOV] //TODO: Cryptographic signature verification for {patch_path}")
    
    # 2. Check Merit
    merit = get_agent_merit(agent_did)
    band = score_to_band(merit)
    
    print(f"[KORAL-GOV] Agent Merit Score: {merit:.3f} ({band})")
    
    if band in ["superconducting", "coherent"]:
        print(f"[KORAL-GOV] ✅ Patch Merit Approved. Proceeding to synthesis.")
        return True
    else:
        print(f"[KORAL-GOV] ❌ Patch Merit Rejected. Agent band '{band}' is insufficient.")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        # Default test case (Project Agent)
        patch = "software/koral/demo/example.patch"
        agent = "did:key:z6MkProjectf22c6de6316cdcab7e615090ebe7c7f2"
    else:
        patch = sys.argv[1]
        agent = sys.argv[2]
        
    verify_patch_merit(patch, agent)
