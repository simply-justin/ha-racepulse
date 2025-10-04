from dataclasses import dataclass
from datetime import timedelta
from ..enums import LiveTimingEvent
from ..interfaces import Event
from ..decorators import register_event


@register_event(LiveTimingEvent.EXTRAPOLATED_CLOCK)
@dataclass(frozen=True)
class ExtrapolatedClock(Event):
    """
    Extrapolated session clock.

    Source: SignalR event "ExtrapolatedClock"
    Raw example:
        {
            "Utc": "2025-10-03T15:37:14.4783763Z",
            "Remaining": "00:00:00",
            "Extrapolating": false,
            "_kf": true
        }
    """

    data_type: LiveTimingEvent = LiveTimingEvent.EXTRAPOLATED_CLOCK
    datetime_utc: timedelta
    remaining_time: timedelta
    extrapolating: bool
