from dataclasses import dataclass
from typing import Dict
from ..enums import LiveTimingEvent
from ..interfaces import Event
from ..decorators import register_event


@dataclass(frozen=True)
class Stint:
    """
    Represents a stint.

    Raw example:
        {
            "LapFlags": 0,
            "Compound": "MEDIUM",
            "New": "true",
            "TyresNotChanged": "0",
            "TotalLaps": 8,
            "StartLaps": 0,
            "LapTime": "1:32.345",
            "LapNumber": 6
        },
    """

    lap_flags: int
    compound: int
    new: bool
    tyres_not_changed: int
    total_laps: int
    start_laps: int
    lap_time: str
    lap_number: int


@dataclass(frozen=True)
class DriverStints:
    """
    Tyre stint and strategy data for a driver.

    Raw example:
        "1": {
            "RacingNumber": "1",
            "Line": 3,
            "Stints": [
                ...
            ]
        }
    """

    racing_number: int
    line: int
    stints: Dict[str, Stint]


@register_event(LiveTimingEvent.TIMING_APP)
@dataclass(frozen=True)
class TimingApp(Event):
    """
    Strategy and tyre data for all drivers.

    Source: SignalR event "TimingApp"
    Raw example:
        {
            "Lines": {
                ...
            },
            "_kf": true
        }
    """

    data_type: LiveTimingEvent = LiveTimingEvent.TIMING_APP
    lines: Dict[str, DriverStints]
