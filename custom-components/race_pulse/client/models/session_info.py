from dataclasses import dataclass
from datetime import timedelta
from . import Meeting
from ..enums import LiveTimingEvent
from ..interfaces import Event
from ..decorators import register_event


@dataclass(frozen=True)
class ArchiveStatus:
    """
    Archive status of a session.

    Raw example:
        {
            "Status": "Complete"
        }
    """

    status: str  # TODO: Make enum


@register_event(LiveTimingEvent.SESSION_INFO)
@dataclass(frozen=True)
class SessionInfo(Event):
    """
    Metadata about a Formula 1 session.

    Source: SignalR event "SessionInfo"
    Raw example:
        {
            "Meeting": {
                ...
            },
            "SessionStatus": "Finalised",
            "ArchiveStatus": {
                ...
            },
            "Key": 9890,
            "Type": "Practice",
            "Number": 2,
            "Name": "Practice 2",
            "StartDate": "2025-10-03T21:00:00",
            "EndDate": "2025-10-03T22:00:00",
            "GmtOffset": "08:00:00",
            "Path": "2025/2025-10-05_Singapore_Grand_Prix/2025-10-03_Practice_2/",
            "_kf": true
        }
    """

    data_type: LiveTimingEvent = LiveTimingEvent.SESSION_INFO
    meeting: Meeting
    session_status: str  # TODO: Make enum -> Scheduled / InProgress / Finalised
    archive_status: ArchiveStatus
    key: int
    type: str
    number: int
    name: str
    start_date: timedelta
    end_date: timedelta
    gmt_offset: timedelta
    path: str
