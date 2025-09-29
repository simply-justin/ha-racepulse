from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class Heartbeat:
    """
    A live timing heartbeat event.

    Attributes:
        timestamp_utc: UTC time when the heartbeat was emitted.
    """
    timestamp_utc: datetime = datetime.utcnow()
