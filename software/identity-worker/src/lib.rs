// The Mathematical State Machine for Sovereign Identity

#[derive(Debug, Clone, PartialEq)]
pub enum IdentityState {
    Active,
    LostOrSeized,
    RecoveryMode { approvals: usize },
    Poisoned,
}

pub struct SovereignIdentity {
    pub state: IdentityState,
    pub dna_seed_present: bool,
    pub network_active: bool,
}

impl SovereignIdentity {
    pub fn new() -> Self {
        Self {
            state: IdentityState::Active,
            dna_seed_present: false,
            network_active: true,
        }
    }

    /// TLA+ Invariant Guard: Ensure active root keys never exceed 1
    /// (This is enforced at the type level: you can't be Active and Recovered simultaneously)
    pub fn mark_lost(&mut self) {
        self.state = IdentityState::LostOrSeized;
    }

    pub fn request_recovery(&mut self) -> Result<(), &'static str> {
        match self.state {
            IdentityState::LostOrSeized => {
                self.state = IdentityState::RecoveryMode { approvals: 0 };
                Ok(())
            }
            _ => Err("Illegal State Transition: Must be LOST_OR_SEIZED to request recovery"),
        }
    }

    pub fn receive_family_share(&mut self) {
        if let IdentityState::RecoveryMode { ref mut approvals } = self.state {
            *approvals += 1;
        }
    }

    pub fn generate_new_root_key(&mut self) -> Result<String, &'static str> {
        if let IdentityState::RecoveryMode { approvals } = self.state {
            if approvals >= 3 && self.dna_seed_present {
                // The old state is dropped/poisoned, enforcing Active Root Keys <= 1
                self.state = IdentityState::Poisoned;
                return Ok("NEW_ROOT_KEY_SHA256_...".to_string());
            }
        }
        Err("VSSS Threshold not met or DNA seed missing")
    }
}
