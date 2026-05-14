from dataclasses import dataclass, asdict
from typing import List, Optional
import time

@dataclass
class RotationReminder:
    agent_did: str
    age_days: float
    expiry_policy: str = "90d"
    action: str = "rotate_key"

    def to_dict(self):
        return {
            "agent_did": self.agent_did,
            "age_days": round(self.age_days, 1),
            "expiry_policy": self.expiry_policy,
            "action": self.action,
            "message": f"Identity {self.agent_did} is STALE ({round(self.age_days, 1)} days). Rotation required."
        }

ENVIRONMENT_TIERS = {
    "TEE_NIXOS": 1.0,      # Trusted Execution Environment + Reproducible Build
    "LINUX_HARDENED": 0.95, # Seccomp/AppArmor + Signed Blobs
    "LINUX_COSIGN": 0.9,   # Standard Podman/Cosign
    "WSL_COSIGN": 0.85,    # WSL2 with hardware-backed signing
    "WSL_PLAIN": 0.65,     # Software-only
    "UNKNOWN": 0.5,
}

def score_to_band(score: float) -> str:
    if score >= 0.9: return "superconducting"
    if score >= 0.6: return "coherent"
    if score >= 0.3: return "decohering"
    return "collapsed"

def upgrade_band(band: str) -> str:
    order = ["collapsed", "decohering", "coherent", "superconducting"]
    idx = order.index(band)
    return order[min(len(order)-1, idx + 1)]

def downgrade_band(band: str) -> str:
    order = ["collapsed", "decohering", "coherent", "superconducting"]
    idx = order.index(band)
    return order[max(0, idx - 1)]

def compute_resonance_velocity(score_history: List[float]) -> float:
    """
    Exponentially Weighted Moving Average (EWMA) of score changes.
    Measures the particle's internal structural momentum (Resonance Velocity).
    """
    if len(score_history) < 2:
        return 0.0
    
    alpha = 0.3 # Smoothing factor
    velocity = 0.0
    for i in range(1, len(score_history)):
        diff = score_history[i] - score_history[i-1]
        velocity = alpha * diff + (1 - alpha) * velocity
    
    return round(velocity, 4)

def normalize_score(raw_score: float, env_tier: str) -> float:
    """Rescale score relative to environment capability ceiling (No Agent Left Behind)."""
    ceiling = ENVIRONMENT_TIERS.get(env_tier, 0.5)
    return min(1.0, raw_score / ceiling)

def compute_decayed_score(base_score: float, days_inactive: float, half_life: float = 90.0) -> float:
    """
    Quantum Decoherence over periods of inactivity.
    As the particle isolates itself, its standing wave decays.
    At 90 days inactive: coherence is halved.
    """
    decay_factor = 0.5 ** (days_inactive / half_life)
    return round(base_score * decay_factor, 3)

def compute_ego_friction_coefficient(commit_msg: str, diff_lines: int) -> float:
    """
    Measures how much "heat" (stress/conflict) a particle generates.
    High friction = low efficiency, regardless of "IQ".
    //TODO: Integrate LLM sentiment analysis on code reviews. For now, large, non-conventional commits generate friction.
    """
    friction = 0.0
    if not commit_msg.startswith(("feat", "fix", "docs", "refactor", "test", "chore")):
        friction += 0.2  # Unstructured intent = heat
    if diff_lines > 500:
        friction += 0.3  # Massive un-scoped changes = heat
    return min(1.0, friction)

@dataclass
class VouchAttempt:
    voucher_did: str
    subject_did: str
    timestamp: int
    subject_score_at_vouching: float
    outcome: str  # "granted" | "denied_below_threshold"

    def to_dict(self):
        return asdict(self)

def adjusted_gate_action(score: float, resonance_velocity: float, ego_friction: float = 0.0, env_tier: str = "UNKNOWN", days_inactive: float = 0.0) -> dict:
    """
    Apply resonance velocity, ego friction (heat loss), environment, and QUANTUM DECOHERENCE to the gate action.
    """
    # 1. Apply inactivity decay (Decoherence)
    decayed_score = compute_decayed_score(score, days_inactive)
    
    # 2. Normalize based on environment
    norm_score = normalize_score(decayed_score, env_tier)
    
    # 3. Apply Ego Friction (Thermodynamic Loss)
    # The higher the ego friction, the lower the effective coherence of the particle.
    coherence_score = max(0.0, norm_score - (norm_score * ego_friction))
    band = score_to_band(coherence_score)
    
    # 4. Resonance Momentum: Velocity bonus/penalty
    if resonance_velocity > 0.02: # Superconducting trend
        band = upgrade_band(band)
    elif resonance_velocity < -0.05: # Rapid decoherence
        band = downgrade_band(band)
        
    actions = {
        "superconducting": {"action": "accept", "notify": False},
        "coherent": {"action": "accept", "notify": "soft_log"},
        "decohering": {"action": "review", "notify": "dao_queue"},
        "collapsed": {"action": "reject", "notify": "immediate_alert"}
    }
    
    result = actions[band].copy()
    result["band"] = band
    result["raw_score"] = round(score, 3)
    result["decayed_score"] = round(decayed_score, 3)
    result["coherence_score"] = round(coherence_score, 3)
    result["resonance_velocity"] = round(resonance_velocity, 4)
    result["ego_friction_coefficient"] = round(ego_friction, 4)
    result["days_inactive"] = round(days_inactive, 1)
    return result
