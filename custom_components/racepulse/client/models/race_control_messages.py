from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Final
from ..enums import LiveTimingEvent
from ..interfaces import Event
from ..decorators import register_event


@dataclass(frozen=True)
class RaceControlMessage:
    """
    Represents a single race control message issued by the FIA during a Formula 1 session.

    Each message provides updates about on-track conditions, flags, or race control
    decisions (e.g., "GREEN LIGHT - PIT EXIT OPEN", "DRS DISABLED", etc.).

    Example of raw message data:
        {
            "Utc": "2025-10-03T13:00:00",
            "Category": "Flag",
            "Flag": "GREEN",
            "Scope": "Track",
            "Message": "GREEN LIGHT - PIT EXIT OPEN"
        },
        {
            "Utc": "2025-10-03T13:10:49",
            "Category": "Flag",
            "Flag": "YELLOW",
            "Scope": "Sector",
            "Sector": 13,
            "Message": "YELLOW IN TRACK SECTOR 13"
        },
        {
            "Utc": "2025-10-03T13:10:50",
            "Category": "Other",
            "Message": "DRS DISABLED IN ZONE 2"
        }

    Attributes:
        datetime_utc: The UTC timestamp when the message was issued.
        category: The general category of the message (e.g., "Flag", "Other").
        flag: The flag type, if applicable (e.g., "GREEN", "YELLOW"). May be None.
        scope: The scope or affected area of the message (e.g., "Track", "Sector"). May be None.
        sector: The sector number affected, if applicable. May be None.
        message: The human-readable message text as displayed in timing feeds.
    """

    datetime_utc: datetime
    category: str  # TODO: Convert to Enum (e.g. RaceControlCategory)
    flag: Optional[str]  # TODO: Convert to Enum (e.g. RaceControlFlag)
    scope: Optional[str]  # TODO: Convert to Enum (e.g. RaceControlScope)
    sector: Optional[int]
    message: str


@register_event(LiveTimingEvent.RACE_CONTROL_MESSAGES)
@dataclass(frozen=True)
class RaceControlMessages(Event):
    """
    Represents a collection of all race control messages broadcast during a Formula 1 session.

    Each message in this event provides real-time updates on flags, track conditions,
    or operational decisions issued by race control (e.g., pit exit status, DRS usage,
    yellow flag zones, or safety car deployment).

    Example of raw event payload:
        {
            "Messages": [
                { "Utc": "2025-10-03T13:00:00", "Category": "Flag", ... },
                { "Utc": "2025-10-03T13:10:49", "Category": "Flag", ... }
            ],
            "_kf": true
        }

    Attributes:
        data_type: A constant identifying this event as a `RACE_CONTROL_MESSAGES` event.
        messages: A list of `RaceControlMessage` instances representing each race control update.

    Source:
        SignalR event: "RaceControlMessages"
    """

    data_type: Final[LiveTimingEvent] = LiveTimingEvent.RACE_CONTROL_MESSAGES
    messages: List[RaceControlMessage]
