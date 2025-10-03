from dataclasses import dataclass
from datetime import datetime
from typing import List
from ..enums import LiveTimingEvent


@dataclass(frozen=True)
class TeamRadioCapture:
    """
    A single captured piece of team radio.

    Raw example:
        {
            "Utc": "2025-10-03T13:07:24.5595691Z",
            "RacingNumber": "30",
            "Path": "TeamRadio/LIALAW01_30_20251003_210721.mp3"
        }
    """

    datetime_utc: datetime
    racing_number: int
    path: str


@dataclass(frozen=True)
class TeamRadio:
    """
    Collection of all captured team radio messages for a session.

    Source: SignalR event "TrackStatus"
    Raw example:
        {
            "Captures": [
                ...
            ],
            "_kf": true
        }
    """

    data_type: LiveTimingEvent = LiveTimingEvent.TEAM_RADIO
    captures: List[TeamRadioCapture]
