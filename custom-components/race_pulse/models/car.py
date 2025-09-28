from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional, List
from ..enums.live_timing_event import LiveTimingEvent

@dataclass
class CarTelemetry:
    """
    Telemetry data for a single car at a specific time.

    Attributes:
        engine_rpm: Engine revolutions per minute.
        speed_kph: Vehicle speed in kilometers per hour.
        gear: Current gear number.
        throttle_percent: Throttle pedal position (0–100).
        brake_percent: Brake pedal pressure (0–100).
        drs_state: Drag Reduction System state.
    """

    engine_rpm: Optional[int] = None
    speed_kph: Optional[int] = None
    gear: Optional[int] = None
    throttle_percent: Optional[int] = None
    brake_percent: Optional[int] = None
    drs_state: Optional[int] = None

@dataclass
class CarTelemetrySnapshot:
    """
    Telemetry snapshot containing data for all cars at a given timestamp.

    Attributes:
        timestamp_utc: UTC timestamp of the snapshot.
        cars: Mapping of car numbers (as strings) to their telemetry data.
    """

    timestamp_utc: datetime
    cars: Dict[str, CarTelemetry] = field(default_factory=dict)

@dataclass
class Car:
    """
    A batch of telemetry snapshots collected over time.

    Attributes:
        snapshots: List of telemetry snapshots.
    """

    data_type: LiveTimingEvent = LiveTimingEvent.Car
    snapshots: List[CarTelemetrySnapshot] = field(default_factory=list)