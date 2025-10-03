from dataclasses import dataclass
from datetime import timedelta
from typing import List, Optional


# https://livetiming.formula1.com/static/2025/Index.json
@dataclass(frozen=True)
class Session:
    """
    Information about a Formula 1 Session.

    Raw example:
        {
            "Key": 9889,
            "Type": "Practice",
            "Number": 1,
            "Name": "Practice 1",
            "StartDate": "2025-10-03T17:30:00",
            "EndDate": "2025-10-03T18:30:00",
            "GmtOffset": "08:00:00",
            "Path": "2025/2025-10-05_Singapore_Grand_Prix/2025-10-03_Practice_1/",
        }
    """

    key: int
    type: str
    number: int
    name: str
    start_date: timedelta
    end_date: timedelta
    gmt_offset: timedelta
    path: str


@dataclass(frozen=True)
class Country:
    """
    Information about a Formula 1 Country.

    Raw example:
        {
            "Key": 157,
            "Code": "SGP",
            "Name": "Singapore"
        }
    """

    key: int
    code: str
    name: str


@dataclass(frozen=True)
class Circuit:
    """
    Information about a Formula 1 Circuit.

    Raw example:
        {
            "Key": 61,
            "ShortName": "Singapore"
        }
    """

    key: int
    short_name: str


@dataclass(frozen=True)
class Meeting:
    """
    Information about a Formula 1 meeting (Grand Prix).

    Raw example:
        {
            "Sessions": [
                ...
            ],
            "Key": 1270,
            "Code": "F1202518",
            "Number": 18,
            "Location": "Marina Bay",
            "OfficialName": "FORMULA 1 SINGAPORE AIRLINES SINGAPORE GRAND PRIX 2025",
            "Name": "Singapore Grand Prix",
            "Country": {
                ...
            },
            "Circuit": {
                ...
            }
        }
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
