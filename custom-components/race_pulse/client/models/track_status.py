from dataclasses import dataclass
from typing import Final
from ..enums import LiveTimingEvent
from ..interfaces import Event
from ..decorators import register_event


@register_event(LiveTimingEvent.TRACK_STATUS)
@dataclass(frozen=True)
class TrackStatus(Event):
    """
    Represents the current track status during a Formula 1 session.

    This event provides real-time updates on the condition of the circuit,
    such as whether it is clear, under yellow flag, or red-flagged.

    Example of raw event payload:
        {
            "Status": "1",
            "Message": "AllClear",
            "_kf": true
        }

    Attributes:
        data_type: A constant identifying this event as a `TRACK_STATUS` event.
        status: The numeric or string code representing the current track state.
                TODO: Convert to enum (e.g., `TrackStatusType`).
        message: A textual description of the track status (e.g., "AllClear", "YellowFlag", "RedFlag").

    Source:
        SignalR event: "TrackStatus"
    """

    data_type: Final[LiveTimingEvent] = LiveTimingEvent.TRACK_STATUS
    status: str  # TODO: Make this into an Enum (TrackStatusType)
    message: str
