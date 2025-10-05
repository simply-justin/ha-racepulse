from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Final
from ..enums import LiveTimingEvent
from ..interfaces import Event
from ..decorators import register_event


@register_event(LiveTimingEvent.EXTRAPOLATED_CLOCK)
@dataclass(frozen=True)
class ExtrapolatedClock(Event):
    """
    Represents the extrapolated session clock used in Formula 1 live timing data.

    This event provides the session's current UTC timestamp, the remaining session
    time, and a flag indicating whether the timing system is extrapolating data
    (e.g., during red flags, pauses, or system downtime).

    Example of raw event payload:
        {
            "Utc": "2025-10-03T15:37:14.4783763Z",
            "Remaining": "00:00:00",
            "Extrapolating": false,
            "_kf": true
        }

    Attributes:
        data_type: A constant identifying this event as an `EXTRAPOLATED_CLOCK` event.
        datetime_utc: The current UTC time according to the timing system.
        remaining_time: The remaining duration in the session as a `timedelta`.
        extrapolating: True if the system is extrapolating time data, otherwise False.

    Source:
        SignalR event: "ExtrapolatedClock"
    """

    data_type: Final[LiveTimingEvent] = LiveTimingEvent.EXTRAPOLATED_CLOCK
    datetime_utc: datetime
    remaining_time: timedelta
    extrapolating: bool
