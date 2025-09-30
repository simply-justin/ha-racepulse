from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass(frozen=True)
class Stat:
    """Best speed/time statistic entry."""
    value: float
    position: int


@dataclass(frozen=True)
class DriverStats:
    """Per-driver statistics (best speeds, sectors)."""
    best_speeds: Dict[str, Stat]


@dataclass(frozen=True)
class TimingStats:
    """
    Timing statistics for all drivers.
    Source: SignalR event "TimingStats".
    """
    drivers: Dict[str, DriverStats]
public sealed record TimingStatsDataPoint : ILiveTimingDataPoint
{
    /// <inheritdoc />
    public LiveTimingDataType LiveTimingDataType => LiveTimingDataType.TimingStats;

    public Dictionary<string, Driver> Lines { get; set; } = new();

    public sealed record Driver
    {
        public Dictionary<string, Stat> BestSpeeds { get; set; } = [];

        public record Stat
        {
            public string? Value { get; set; }
            public int? Position { get; set; }
        }
    }
}