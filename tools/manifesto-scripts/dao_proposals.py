from dataclasses import dataclass, asdict
import datetime

@dataclass
class Proposal:
    proposal_type: str   # "agent_revocation"
    subject_did: str
    evidence_cid: str    # CID of the stale trace file
    vote_deadline: int   # unix_ts
    quorum_pct: float = 0.51
    status: str = "open" # "open" | "passed" | "rejected"

class GovernanceScheduler:
    def __init__(self):
        self.proposals = []

    def create_proposal(self, reminder_data: dict) -> Proposal:
        """
        Escalate a stale reminder to a formal revocation vote.
        """
        deadline = int(datetime.datetime.now().timestamp()) + (7 * 86400) # 1 week
        p = Proposal(
            proposal_type="agent_revocation",
            subject_did=reminder_data["agent_did"],
            evidence_cid="unknown", # //TODO: link to actual trace CID
            vote_deadline=deadline
        )
        self.proposals.append(p)
        print(f"  [DAO PROPOSAL] Created REVOCATION VOTE for {p.subject_did}. Deadline: {deadline}")
        return p
