from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Final
from . import Meeting
from ..enums import LiveTimingEvent
from ..interfaces import Event
from ..decorators import register_event


@dataclass(frozen=True)
class ArchiveStatus:
    """
    Represents the archive status of a Formula 1 session.

    Example of raw JSON payload:
        {
            "Status": "Complete"
        }

    Attributes:
        status: The archive state of the session (e.g., "Live", "Complete").
                TODO: Convert to enum (e.g., ArchiveStatusType).
    """

    status: str  # TODO: Make enum


@register_event(LiveTimingEvent.SESSION_INFO)
@dataclass(frozen=True)
class SessionInfo(Event):
    """
    Represents metadata about a Formula 1 session, including its schedule,
    current status, and related meeting information.

    This event provides high-level session context such as timing, status,
    and linked meeting (Grand Prix) details.

    Example of raw event payload:
        {
            "Meeting": { ... },
            "SessionStatus": "Finalised",
            "ArchiveStatus": { "Status": "Complete" },
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

    Attributes:
        data_type: A constant identifying this event as a `SESSION_INFO` event.
        meeting: A `Meeting` object representing the associated Grand Prix.
        session_status: The current session status (e.g., "Scheduled", "InProgress", "Finalised").
                        TODO: Convert to enum (e.g., SessionStatusType).
        archive_status: The current archive status of the session.
        key: Unique numeric identifier for the session.
        type: The session type (e.g., "Practice", "Qualifying", "Race").
        number: The session number (e.g., 1 for Practice 1, 2 for Practice 2).
        name: The official name of the session.
        start_date: The UTC start datetime of the session.
        end_date: The UTC end datetime of the session.
        gmt_offset: The timezone offset from UTC as a `timedelta`.
        path: The relative API path for accessing session data.

    Source:
        SignalR event: "SessionInfo"
    """

    data_type: Final[LiveTimingEvent] = LiveTimingEvent.SESSION_INFO
    meeting: Meeting
    session_status: str  # TODO: Make enum -> Scheduled / InProgress / Finalised
    archive_status: ArchiveStatus
    key: int
    type: str
    number: int
    name: str
    start_date: datetime
    end_date: datetime
    gmt_offset: timedelta
    path: str
