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
    "TEE_NIXOS": 1.0,
    "LINUX_COSIGN": 0.9,
    "WSL_COSIGN": 0.8,
    "WSL_PLAIN": 0.65,
    "UNKNOWN": 0.5,
}

def score_to_band(score: float) -> str:
    if score >= 0.9: return "trusted"
    if score >= 0.6: return "acceptable"
    if score >= 0.3: return "degraded"
    return "untrusted"

def upgrade_band(band: str) -> str:
    order = ["untrusted", "degraded", "acceptable", "trusted"]
    idx = order.index(band)
    return order[min(len(order)-1, idx + 1)]

def downgrade_band(band: str) -> str:
    order = ["untrusted", "degraded", "acceptable", "trusted"]
    idx = order.index(band)
    return order[max(0, idx - 1)]

def compute_merit_velocity(score_history: List[float]) -> float:
    """
    Linear regression slope over the score history. 
    Positive = growing (Resonant Merit).
    """
    if len(score_history) < 2:
        return 0.0
    
    # Simple slope: (y_end - y_start) / len
    # //TODO: Implement proper least-squares for noisy data
    return (score_history[-1] - score_history[0]) / len(score_history)

def normalize_score(raw_score: float, env_tier: str) -> float:
    """Rescale score relative to environment capability ceiling (No Agent Left Behind)."""
    ceiling = ENVIRONMENT_TIERS.get(env_tier, 0.5)
    return min(1.0, raw_score / ceiling)

def compute_decayed_score(base_score: float, days_inactive: float, half_life: float = 90.0) -> float:
    """
    Exponential decay of merit over periods of inactivity.
    At 90 days inactive: score halved.
    """
    decay_factor = 0.5 ** (days_inactive / half_life)
    return round(base_score * decay_factor, 3)

@dataclass
class VouchAttempt:
    voucher_did: str
    subject_did: str
    timestamp: int
    subject_score_at_vouching: float
    outcome: str  # "granted" | "denied_below_threshold"

    def to_dict(self):
        return asdict(self)

def adjusted_gate_action(score: float, velocity: float, env_tier: str = "UNKNOWN", days_inactive: float = 0.0) -> dict:
    """
    Apply velocity, environment, and TEMPORAL DECAY modifiers to the DAO gate action.
    """
    # 1. Apply inactivity decay
    decayed_score = compute_decayed_score(score, days_inactive)
    
    # 2. Normalize based on environment
    norm_score = normalize_score(decayed_score, env_tier)
    band = score_to_band(norm_score)
    
    # 3. Resonant Merit: Velocity bonus/penalty
    if velocity > 0.02: # Significant growth
        band = upgrade_band(band)
    elif velocity < -0.05: # Significant decline
        band = downgrade_band(band)
        
    actions = {
        "trusted": {"action": "accept", "notify": False},
        "acceptable": {"action": "accept", "notify": "soft_log"},
        "degraded": {"action": "review", "notify": "dao_queue"},
        "untrusted": {"action": "reject", "notify": "immediate_alert"}
    }
    
    result = actions[band].copy()
    result["band"] = band
    result["raw_score"] = round(score, 3)
    result["decayed_score"] = round(decayed_score, 3)
    result["normalized_score"] = round(norm_score, 3)
    result["velocity"] = round(velocity, 4)
    result["days_inactive"] = round(days_inactive, 1)
    return result
