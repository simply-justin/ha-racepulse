from dataclasses import dataclass
from datetime import datetime
from ..enums import LiveTimingEvent
from ..interfaces import Event
from ..decorators import register_event


@register_event(LiveTimingEvent.HEARTBEAT)
@dataclass(frozen=True)
class Heartbeat(Event):
    """
    A live timing heartbeat event.

    Source: SignalR event "Heartbeat"
    Raw example:
        {
            "Utc": "2025-10-03T14:26:58.0863771Z",
            "_kf": true
        }
    """

    data_type: LiveTimingEvent = LiveTimingEvent.HEARTBEAT
    datetime_utc: datetime
