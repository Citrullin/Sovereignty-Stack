#!/usr/bin/env python3
import sys
import os
import subprocess
import shutil

# Add governance to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../governance")))
from verify_patch import verify_patch_merit

def apply_verifiable_patch(patch_path, target_dir, agent_did):
    """
    Koral Patch Application:
    1. Verify merit and signature.
    2. //TODO: TEE_MEASUREMENT: Measure state before patch.
    3. Apply patch to target directory.
    4. //TODO: Sign the resulting state.
    """
    if not verify_patch_merit(patch_path, agent_did):
        print(f"[KORAL-APPLY] ❌ Patch verification failed. Aborting.")
        return False

    print(f"[KORAL-APPLY] Applying verifiable patch to {target_dir}")
    
    # Use 'patch' utility to apply the signed delta
    try:
        subprocess.run(
            ["patch", "-p0", "-d", target_dir, "-i", os.path.abspath(patch_path)],
            check=True, capture_output=True, text=True
        )
        print(f"[KORAL-APPLY] ✅ Patch successfully applied.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[KORAL-APPLY] ❌ Patch application failed: {e.stderr}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        # Test default
        patch = "software/koral/patches/koral-oidc-naming.patch"
        target = "software/koral/k3s-hub"
        agent = "did:key:z6MkProjectf22c6de6316cdcab7e615090ebe7c7f2"
    else:
        patch = sys.argv[1]
        target = sys.argv[2]
        agent = sys.argv[3]

    apply_verifiable_patch(patch, target, agent)
