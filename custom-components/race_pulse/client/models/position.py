from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional, List

@dataclass(frozen=True)
class CarPosition:
    """
    Position data for a single car at a specific time.

    Attributes:
        status: Driver status ("on_track" or "off_track").
        x_cm: X coordinate of car in centimeters.
        y_cm: Y coordinate of car in centimeters.
        z_cm: Z coordinate of car in centimeters.
    """

    status: Optional[str] = None  # e.g., "on_track", "off_track"
    x_cm: Optional[int] = None
    y_cm: Optional[int] = None
    z_cm: Optional[int] = None


@dataclass(frozen=True)
class PositionSnapshot:
    """
    Snapshot of all car positions at a specific timestamp.

    Attributes:
        timestamp_utc: UTC timestamp of the snapshot.
        cars: Mapping of driver numbers to car position data.
    """

    timestamp_utc: datetime
    cars: Dict[str, CarPosition] = field(default_factory=dict)


@dataclass(frozen=True)
class PositionData:
    """
    A batch of position snapshots.

    Attributes:
        snapshots: List of position snapshots.
    """
    snapshots: List[PositionSnapshot] = field(default_factory=list)
