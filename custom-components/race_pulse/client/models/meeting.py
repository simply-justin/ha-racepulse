from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional


@dataclass
class SessionInfo:
    """
    Information about a single session within a race meeting.

    Attributes:
        session_id: Unique identifier for the session.
        name: Human-readable session name (e.g., "Qualifying").
        session_type: Session type (e.g., "Practice", "Race").
        start_time: UTC start datetime.
        end_time: UTC end datetime.
        gmt_offset: Time offset from GMT as timedelta.
        path: Optional internal path identifier.
    """

    session_id: int
    name: str
    session_type: str
    start_time: datetime
    end_time: datetime
    gmt_offset: timedelta
    path: Optional[str] = None


@dataclass
class Meeting:
    """
    Information about a Formula 1 meeting (Grand Prix).

    Attributes:
        meeting_id: Unique identifier for the meeting.
        name: Name of the meeting (e.g., "Australian Grand Prix").
        location: Meeting location (e.g., "Melbourne").
        sessions: List of sessions associated with the meeting.
    """

    meeting_id: int
    name: str
    location: str
    sessions: List[SessionInfo] = field(default_factory=list)


@dataclass
class MeetingIndex:
    """
    List of meetings for a given year.

    Attributes:
        year: Championship year.
        meetings: All Formula 1 meetings for the year.
    """

    year: int
    meetings: List[Meeting] = field(default_factory=list)
/// <summary>
/// The response model for the F1 Live Timing meetings and sessions index.
/// </summary>
public record ListMeetingsApiResponse
{
    public required int Year { get; set; }
    public required List<Meeting> Meetings { get; set; }

    public record Meeting
    {
        public required int Key { get; set; }
        public required string Name { get; set; }
        public required string Location { get; set; }
        public required List<Session> Sessions { get; set; }

        public record Session
        {
            public required int Key { get; set; }
            public required string Name { get; set; }
            public required string Type { get; set; }
            public required DateTime StartDate { get; set; }
            public required DateTime EndDate { get; set; }
            public required TimeSpan GmtOffset { get; set; }
            public string? Path { get; set; }
        }
    }
}