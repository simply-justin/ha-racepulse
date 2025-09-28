from dataclasses import dataclass
from typing import Optional
from ..enums.live_timing_event import LiveTimingEvent


@dataclass(frozen=True)
class TrackStatus:
    """
    Current track status information.

    Attributes:
        data_type: Always set to `LiveTimingEvent.TrackStatus`.
        status_flag: Current track flag condition (e.g., "green", "yellow", "red").
        message: Optional descriptive message (e.g., "Yellow in sector 1").
    """

    data_type: LiveTimingEvent = LiveTimingEvent.TrackStatus
    status_flag: str = "unknown"
    message: Optional[str] = None
