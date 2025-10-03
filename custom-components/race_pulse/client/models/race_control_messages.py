from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from ..enums import LiveTimingEvent


@dataclass(frozen=True)
class RaceControlMessage:
    """
    A single race control message issued by the FIA.

    Raw example:
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
        },
    """

    datetime_utc: datetime
    category: str  # TODO: Make enum -> Flag / Other
    flag: Optional[str]  # TODO: Make enum
    scope: Optional[str]  # TODO: Make enum
    sector: Optional[int]
    message: str


@dataclass(frozen=True)
class RaceControlMessages:
    """
    Collection of race control messages during a session.

    Source: SignalR event "RaceControlMessages"
    Raw example:
        {
            "Messages": [
            ],
            "_kf": true
        }
    """

    data_type: LiveTimingEvent = LiveTimingEvent.RACE_CONTROL_MESSAGES
    messages: List[RaceControlMessage]
