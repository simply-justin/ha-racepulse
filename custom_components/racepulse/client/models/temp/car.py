from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional, List


@dataclass(frozen=True)
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


@dataclass(frozen=True)
class CarTelemetrySnapshot:
    """
    Telemetry snapshot containing data for all cars at a given timestamp.

    Attributes:
        timestamp_utc: UTC timestamp of the snapshot.
        cars: Mapping of car numbers (as strings) to their telemetry data.
    """

    timestamp_utc: datetime
    cars: Dict[str, CarTelemetry] = field(default_factory=dict)


@dataclass(frozen=True)
class Car:
    """
    A batch of telemetry snapshots collected over time.

    Attributes:
        entries: List of telemetry snapshots.
    """

    entries: List[CarTelemetrySnapshot] = field(default_factory=list)
/// <summary>
/// Car data is sent as compressed (with deflate) JSON containing Entries.
/// Each Entry is all the car data for a specific point in time, and they seem to be batched to reduce network load.
/// </summary>
public sealed class CarDataPoint : ILiveTimingDataPoint
{
    public LiveTimingDataType LiveTimingDataType => LiveTimingDataType.CarData;

    public List<Entry> Entries { get; set; } = new();

    public sealed class Entry
    {
        public DateTimeOffset Utc { get; set; }

        public Dictionary<string, Car> Cars { get; set; } = new();

        public sealed class Car
        {
            public Channel Channels { get; set; } = new();

            public sealed class Channel
            {
                [JsonPropertyName("0")]
                public int? Rpm { get; set; }

                [JsonPropertyName("2")]
                public int? Speed { get; set; }

                [JsonPropertyName("3")]
                public int? Ngear { get; set; }

                [JsonPropertyName("4")]
                public int? Throttle { get; set; }

                [JsonPropertyName("5")]
                public int? Brake { get; set; }

                /// <summary>
                /// From FastF1s understanding of this field:
                /// - DRS: 0-14 (Odd DRS is Disabled, Even DRS is Enabled?)
                ///  - 0 =  Off
                ///  - 1 =  Off
                ///  - 2 =  (?)
                ///  - 3 =  (?)
                ///  - 8 =  Detected, Eligible once in Activation Zone (Noted Sometimes)
                ///  - 10 = On (Unknown Distinction)
                ///  - 12 = On (Unknown Distinction)
                ///  - 14 = On (Unknown Distinction)
                /// </summary>
                [JsonPropertyName("45")]
                public int? Drs { get; set; }
            }
        }
    }
}