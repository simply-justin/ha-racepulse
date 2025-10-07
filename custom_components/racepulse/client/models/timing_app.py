from dataclasses import dataclass
from typing import Dict, Final
from ..enums import LiveTimingEvent
from ..interfaces import Event
from ..decorators import register_event


@dataclass(frozen=True)
class Stint:
    """
    Represents a single tyre stint completed by a driver.

    A stint describes the number of laps a driver has run on a specific tyre compound,
    including whether the tyres were new or reused and the associated lap information.

    Example of raw JSON payload:
        {
            "LapFlags": 0,
            "Compound": "MEDIUM",
            "New": "true",
            "TyresNotChanged": "0",
            "TotalLaps": 8,
            "StartLaps": 0,
            "LapTime": "1:32.345",
            "LapNumber": 6
        }

    Attributes:
        lap_flags: Numeric flags describing the stint's state (purpose TBD).
        compound: The tyre compound used (e.g., "SOFT", "MEDIUM", "HARD").
                  TODO: Convert to enum (e.g., TyreCompoundType).
        new: Whether the tyres were new (`true`) or previously used.
        tyres_not_changed: Indicates if tyres were reused (`1`) or changed (`0`).
        total_laps: Total laps completed on this set of tyres.
        start_laps: Lap number where the stint began.
        lap_time: Best lap time within the stint, formatted as "M:SS.mmm".
        lap_number: The last lap number of the stint.
    """

    lap_flags: int
    compound: str
    new: bool
    tyres_not_changed: int
    total_laps: int
    start_laps: int
    lap_time: str
    lap_number: int


@dataclass(frozen=True)
class DriverStints:
    """
    Represents tyre stint and strategy information for a single driver.

    Example of raw JSON payload:
        "1": {
            "RacingNumber": "1",
            "Line": 3,
            "Stints": [
                { "LapFlags": 0, "Compound": "MEDIUM", "TotalLaps": 8, ... }
            ]
        }

    Attributes:
        racing_number: The driver's racing number.
        line: The line index used for display in timing data.
        stints: A mapping of stint indices (or identifiers) to `Stint` objects.
    """

    racing_number: int
    line: int
    stints: Dict[str, Stint]


@register_event(LiveTimingEvent.TIMING_APP)
@dataclass(frozen=True)
class TimingApp(Event):
    """
    Represents strategy and tyre data for all drivers in a Formula 1 session.

    This event contains detailed tyre stint information for each driver, including
    compound choices, stint lengths, and tyre usage patterns throughout the session.

    Example of raw event payload:
        {
            "Lines": {
                "1": {
                    "RacingNumber": "1",
                    "Line": 3,
                    "Stints": [ ... ]
                },
                "16": {
                    "RacingNumber": "16",
                    "Line": 7,
                    "Stints": [ ... ]
                }
            },
            "_kf": true
        }

    Attributes:
        data_type: A constant identifying this event as a `TIMING_APP` event.
        lines: A mapping of driver identifiers to their corresponding `DriverStints` objects.

    Source:
        SignalR event: "TimingApp"
    """

    data_type: Final[LiveTimingEvent] = LiveTimingEvent.TIMING_APP
    lines: Dict[str, DriverStints]
