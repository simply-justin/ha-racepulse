from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass(frozen=True)
class PitLaneTime:
    """
    A single pit lane time entry.

    Attributes:
        duration: Duration spent in the pit lane (string, e.g., "25.4s").
        lap: Lap number when the pit lane entry occurred.
    """

    duration: Optional[str] = None
    lap: Optional[str] = None


@dataclass(frozen=True)
class PitLaneTimeCollection:
    """
    Collection of pit lane times for all drivers.

    Attributes:
        data_type: Always set to `LiveTimingEvent.PitLaneTimeCollection`.
        pit_times: Mapping of driver numbers to their most recent pit lane time.
        pit_times_list: Mapping of driver numbers to a list of pit lane time entries.
    """

    pit_times: Dict[str, PitLaneTime] = field(default_factory=dict)
    pit_times_list: Dict[str, List[PitLaneTime]] = field(default_factory=dict)
// {"Type":"PitLaneTimeCollection","Json":{"PitTimes":{"1":{"RacingNumber":"1","Duration":"","Lap":"5"}}},"DateTime":"2025-09-05T15:16:10.363+00:00"}
public sealed record PitLaneTimeCollectionDataPoint : ILiveTimingDataPoint
{
    /// <inheritdoc />
    public LiveTimingDataType LiveTimingDataType => LiveTimingDataType.PitLaneTimeCollection;

    public Dictionary<string, PitTime> PitTimes { get; set; } = new();
    public Dictionary<string, List<PitTime>> PitTimesList { get; set; } = new();

    public sealed record PitTime
    {
        public string? Duration { get; set; }
        public string? Lap { get; set; }
    }
}