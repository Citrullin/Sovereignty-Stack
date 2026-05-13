from dataclasses import dataclass
from typing import List, Dict
import subprocess
import re
import math

@dataclass
class SignatureEvidence:
    tool: str           # "cosign" | "gpg" | "ssh" | "slsa" | "tee"
    key_type: str       # "hardware" | "software" | "ephemeral" | "keyless"
    verified: bool
    transparency_log: bool
    strength: float

def get_signature_strength(tool: str, key_type: str) -> float:
    table = {
        ("tee", "hardware"): 1.0,
        ("cosign", "hardware"): 0.95,
        ("slsa", "software"): 0.9,
        ("cosign", "keyless"): 0.85,
        ("gpg", "hardware"): 0.85,
        ("ssh", "hardware"): 0.8,
        ("cosign", "software"): 0.7,
        ("gpg", "software"): 0.65,
        ("git", "software"): 0.6,
    }
    return table.get((tool, key_type), 0.0)

def detect_signing_tool(commit_hash: str, repo_path: str = ".") -> SignatureEvidence:
    """
    Detect the signing tool used for a commit using git verify-commit or signature flags.
    """
    try:
        # Get signature status from git
        # %G?: G=Good, B=Bad, U=Unknown, X=Expired, Y=Revoked, R=Good(trusted), E=Good(untrusted), N=None
        status = subprocess.check_output(
            ["git", "log", "-1", "--format=%G?", commit_hash], 
            cwd=repo_path
        ).decode().strip()
        
        if status in ['G', 'R', 'E']:
            # Further detection (e.g. check for PGP vs SSH)
            raw_sig = subprocess.check_output(
                ["git", "log", "-1", "--format=%GG", commit_hash], 
                cwd=repo_path
            ).decode()
            
            if "BEGIN PGP SIGNATURE" in raw_sig:
                return SignatureEvidence("gpg", "software", True, False, 0.65)
            elif "BEGIN SSH SIGNATURE" in raw_sig:
                return SignatureEvidence("ssh", "software", True, False, 0.6)
            
        return SignatureEvidence("unknown", "unknown", False, False, 0.0)
    except Exception:
        return SignatureEvidence("unknown", "unknown", False, False, 0.0)

def compute_scs(commits: List[Dict]) -> float:
    """
    Compute the composite Supply Chain Soundness Score (0.0-1.0).
    Expected input: list of commit metadata dicts.
    """
    if not commits:
        return 0.0
    
    # 1. Signature Coverage
    sig_weights = [c.get("signature_strength", 0.0) for c in commits]
    sig_coverage = sum(sig_weights) / len(commits)
    
    # 2. Community Breadth
    authors = set(c.get("author_email") for c in commits)
    community_breadth = min(1.0, math.log(len(authors) + 1) / math.log(20 + 1))
    
    # 3. Build Reproducibility (Mocked/Static for now)
    # //TODO: Detect NixOS flakes or pinned Dockerfiles
    reproducibility = 0.8 
    
    # 4. Release Authority (Linus Model)
    # //TODO: Check if signed by designated release manager DID
    authority = 0.5
    
    # Composite Weighting
    weights = {
        "sig": 0.4,
        "community": 0.2,
        "repro": 0.2,
        "auth": 0.2
    }
    
    scs = (
        sig_coverage * weights["sig"] +
        community_breadth * weights["community"] +
        reproducibility * weights["repro"] +
        authority * weights["auth"]
    )
    
    return round(scs, 3)
