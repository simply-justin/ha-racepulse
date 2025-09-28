from dataclasses import dataclass
from datetime import datetime
from ..enums.live_timing_event import LiveTimingEvent

@dataclass
class Heartbeat:
    """
    A live timing heartbeat event.

    Attributes:
        data_type: Always set to `LiveTimingEvent.Heartbeat`.
        timestamp_utc: UTC time when the heartbeat was emitted.
    """

    data_type: LiveTimingEvent = LiveTimingEvent.Heartbeat
    timestamp_utc: datetime = datetime.utcnow()
