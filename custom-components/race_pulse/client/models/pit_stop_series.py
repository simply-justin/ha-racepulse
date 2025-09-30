from dataclasses import dataclass
from datetime import datetime
from typing import Dict


@dataclass(frozen=True)
class PitStopEntry:
    """
    Details of a single pit stop.

    Attributes:
        racing_number: Driver's racing number.
        pit_stop_time: Duration of the pit stop (string, e.g., "2.5s").
        pit_lane_time: Total time spent in the pit lane (string).
        lap: Lap number when the pit stop occurred.
    """

    racing_number: str
    pit_stop_time: str
    pit_lane_time: str
    lap: str


@dataclass(frozen=True)
class PitStopTime:
    """
    Timestamped record of a pit stop.

    Attributes:
        timestamp_utc: UTC time when the pit stop occurred.
        pit_stop: Pit stop entry details.
    """

    timestamp_utc: datetime
    pit_stop: PitStopEntry


@dataclass(frozen=True)
class PitStopSeries:
    """
    Series of pit stops for all drivers.

    Attributes:
        pit_times: Nested mapping of driver -> lap -> pit stop time.
    """

    pit_times: Dict[str, Dict[str, PitStopTime]]
public sealed record PitStopSeriesDataPoint : ILiveTimingDataPoint
{
    /// <inheritdoc />
    public LiveTimingDataType LiveTimingDataType => LiveTimingDataType.PitStopSeries;

    public Dictionary<string, Dictionary<string, PitTime>> PitTimes { get; set; } = [];

    public sealed record PitTime
    {
        public DateTime? Timestamp { get; set; }
        public PitStopEntry? PitStop { get; set; }

        public sealed record PitStopEntry
        {
            public string? RacingNumber { get; set; }
            public string? PitStopTime { get; set; }
            public string? PitLaneTime { get; set; }
            public string? Lap { get; set; }
        }
    }
}