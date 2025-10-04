from dataclasses import dataclass
from ..enums import LiveTimingEvent
from ..interfaces import Event
from ..decorators import register_event


@register_event(LiveTimingEvent.TRACK_STATUS)
@dataclass(frozen=True)
class TrackStatus(Event):
    """
    Current track status information.

    Source: SignalR event "TrackStatus"
    Raw example:
        {
            "Status": "1",
            "Message": "AllClear",
            "_kf": true
        }
    """

    data_type: LiveTimingEvent = LiveTimingEvent.TRACK_STATUS
    status: str  # TODO: Make this into an Enum?
    message: str
