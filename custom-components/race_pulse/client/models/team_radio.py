from dataclasses import dataclass
from datetime import datetime
from typing import List, Final
from ..enums import LiveTimingEvent
from ..interfaces import Event
from ..decorators import register_event


@dataclass(frozen=True)
class TeamRadioCapture:
    """
    Represents a single captured piece of team radio communication.

    Each entry corresponds to a recorded audio clip between a driver and their team,
    including the UTC timestamp, the driver's racing number, and the audio file path.

    Example of raw JSON payload:
        {
            "Utc": "2025-10-03T13:07:24.5595691Z",
            "RacingNumber": "30",
            "Path": "TeamRadio/LIALAW01_30_20251003_210721.mp3"
        }

    Attributes:
        datetime_utc: The UTC timestamp when the radio message was recorded.
        racing_number: The driver's racing number associated with the message.
        path: The relative API or storage path to the radio audio file.
    """

    datetime_utc: datetime
    racing_number: int
    path: str


@register_event(LiveTimingEvent.TEAM_RADIO)
@dataclass(frozen=True)
class TeamRadio(Event):
    """
    Represents a collection of all team radio captures for a Formula 1 session.

    Each capture corresponds to a single audio clip exchanged between a driver and
    their team. The F1 Live Timing feed emits this event whenever new team radio
    recordings become available during a session.

    Example of raw event payload:
        {
            "Captures": [
                {
                    "Utc": "2025-10-03T13:07:24.5595691Z",
                    "RacingNumber": "30",
                    "Path": "TeamRadio/LIALAW01_30_20251003_210721.mp3"
                }
            ],
            "_kf": true
        }

    Attributes:
        data_type: A constant identifying this event as a `TEAM_RADIO` event.
        captures: A list of `TeamRadioCapture` objects representing individual
                  radio messages captured during the session.

    Source:
        SignalR event: "TeamRadio"
    """

    data_type: Final[LiveTimingEvent] = LiveTimingEvent.TEAM_RADIO
    captures: List[TeamRadioCapture]
