from dataclasses import dataclass
from . import Session, Meeting
from ..enums import LiveTimingEvent


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


@dataclass(frozen=True)
class SessionInfo(Session):
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
