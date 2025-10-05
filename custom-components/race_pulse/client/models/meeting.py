from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional, Final


# https://livetiming.formula1.com/static/2025/Index.json
@dataclass(frozen=True)
class Session:
    """
    Represents a single Formula 1 session (e.g., Practice, Qualifying, or Race)
    as defined in the Live Timing Index data.

    Example of raw JSON payload:
        {
            "Key": 9889,
            "Type": "Practice",
            "Number": 1,
            "Name": "Practice 1",
            "StartDate": "2025-10-03T17:30:00",
            "EndDate": "2025-10-03T18:30:00",
            "GmtOffset": "08:00:00",
            "Path": "2025/2025-10-05_Singapore_Grand_Prix/2025-10-03_Practice_1/"
        }

    Attributes:
        key: Unique numeric identifier for the session.
        type: The session type (e.g., "Practice", "Qualifying", "Race").
        number: The session number (e.g., 1 for Practice 1).
        name: Human-readable session name.
        start_date: Scheduled UTC start time of the session.
        end_date: Scheduled UTC end time of the session.
        gmt_offset: The session’s timezone offset from UTC as a `timedelta`.
        path: Relative path to the session data within the Live Timing API.
    """

    key: int
    type: str
    number: int
    name: str
    start_date: datetime
    end_date: datetime
    gmt_offset: timedelta
    path: str


@dataclass(frozen=True)
class Country:
    """
    Represents a country in which a Formula 1 event takes place.

    Example of raw JSON payload:
        {
            "Key": 157,
            "Code": "SGP",
            "Name": "Singapore"
        }

    Attributes:
        key: Unique numeric identifier for the country.
        code: The ISO 3166-1 alpha-3 country code (e.g., "SGP", "GBR").
        name: Full display name of the country.
    """

    key: int
    code: str
    name: str


@dataclass(frozen=True)
class Circuit:
    """
    Represents a Formula 1 racing circuit.

    Example of raw JSON payload:
        {
            "Key": 61,
            "ShortName": "Singapore"
        }

    Attributes:
        key: Unique numeric identifier for the circuit.
        short_name: The circuit’s short name or display label.
    """

    key: int
    short_name: str


@dataclass(frozen=True)
class Meeting:
    """
    Represents a Formula 1 meeting (Grand Prix event) containing multiple sessions.

    Example of raw JSON payload:
        {
            "Sessions": [
                { ... }
            ],
            "Key": 1270,
            "Code": "F1202518",
            "Number": 18,
            "Location": "Marina Bay",
            "OfficialName": "FORMULA 1 SINGAPORE AIRLINES SINGAPORE GRAND PRIX 2025",
            "Name": "Singapore Grand Prix",
            "Country": { ... },
            "Circuit": { ... }
        }

    Attributes:
        sessions: A list of `Session` objects associated with this meeting.
        key: Unique numeric identifier for the meeting.
        code: Internal event code (e.g., "F1202518"), optional.
        number: The championship round number for this meeting, optional.
        location: The geographic location or city where the event is held.
        official_name: The official FIA-registered event name.
        name: The display name of the event (e.g., "Singapore Grand Prix").
        country: The `Country` object representing the host nation.
        circuit: The `Circuit` object representing the race circuit.
    """

    sessions: List[Session]
    key: int
    code: Optional[str]
    number: Optional[int]
    location: str
    official_name: str
    name: str
    country: Country
    circuit: Circuit
