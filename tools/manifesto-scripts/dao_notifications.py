from dataclasses import dataclass, asdict
import datetime

@dataclass
class Notification:
    type: str  # e.g. "agent.stale.rotation_required"
    subject_did: str
    message: str
    severity: str = "warning"
    timestamp: str = datetime.datetime.now().isoformat() + "Z"

class MockDAONotifier:
    def __init__(self):
        self.sent = []

    def dispatch(self, notification: Notification) -> bool:
        """
        //TODO: Replace with real DIDComm v2 message to DAO agent controller.
        Current: Appends to local audit log.
        """
        self.sent.append(asdict(notification))
        print(f"  [DAO NOTIFY] {notification.type.upper()}: {notification.message}")
        return True
