from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass(frozen=True)
class Interval:
    """
    Gap or interval to another driver.

    Attributes:
        value: String representation of the gap (e.g. "+1.123" or "5L" for 5 laps down).
        catching: Whether the driver is closing the gap.
    """

    value: Optional[str] = None
    catching: Optional[bool] = None


@dataclass(frozen=True)
class Segment:
    """
    Represents a sector segment status.
    Typical values: yellow, green, purple, pit lane, chequered flag.
    """

    status: str


@dataclass(frozen=True)
class SectorTime:
    """
    Timing information for a sector.

    Attributes:
        value: Sector lap time as string.
        is_overall_fastest: True if fastest sector overall.
        is_personal_fastest: True if fastest sector for the driver.
        segments: Mini-sector breakdown with statuses.
    """

    value: Optional[str] = None
    is_overall_fastest: bool = False
    is_personal_fastest: bool = False
    segments: Dict[str, Segment] = field(default_factory=dict)


@dataclass(frozen=True)
class DriverTiming:
    """
    Live timing state for a single driver.

    Attributes:
        gap_to_leader: Gap string (e.g. "LAP 54", "+1.123", "5L").
        interval_to_ahead: Interval to the car ahead.
        racing_line: Driver’s racing line number.
        position: Current position in classification.
        in_pit: Whether the driver is in the pit lane.
        pit_exit: Whether the driver has exited the pits.
        pit_stops: Number of pit stops made.
        is_pit_lap: Whether the current lap is a pit lap.
        completed_laps: Number of laps completed.
        last_lap: Last lap sector times.
        sectors: Per-sector timing for the current lap.
        best_lap_time: Driver’s best lap time.
        knocked_out: Whether eliminated in qualifying.
        retired: Whether retired from session.
        stopped: Whether car is stopped on track.
        status: Current status flag (yellow, pit, chequered, etc.).
    """

    gap_to_leader: Optional[str] = None
    interval_to_ahead: Optional[Interval] = None
    racing_line: Optional[int] = None
    position: Optional[str] = None
    in_pit: bool = False
    pit_exit: bool = False
    pit_stops: int = 0
    is_pit_lap: bool = False
    completed_laps: int = 0
    last_lap: Optional[SectorTime] = None
    sectors: Dict[str, SectorTime] = field(default_factory=dict)
    best_lap_time: Optional[str] = None
    knocked_out: bool = False
    retired: bool = False
    stopped: bool = False
    status: Optional[str] = None


@dataclass(frozen=True)
class Timing:
    """
    Full live timing dataset.

    Attributes:
        drivers: Mapping of driver IDs to their live timing data.
    """

    drivers: Dict[str, DriverTiming] = field(default_factory=dict)
public sealed record TimingDataPoint : ILiveTimingDataPoint
{
    /// <inheritdoc />
    public LiveTimingDataType LiveTimingDataType => LiveTimingDataType.TimingData;

    public Dictionary<string, Driver> Lines { get; set; } = new();

    public sealed record Driver
    {
        /// <summary>
        /// For the leader, this is the lap number e.g. <c>LAP 54</c>,
        /// but everyone else is a time in the format <c>+1.123</c>,
        /// or if more than a lap down then <c>5L</c> (i.e. 5 laps behind).
        /// </summary>
        public string? GapToLeader { get; set; }
        public Interval? IntervalToPositionAhead { get; set; }

        public int? Line { get; set; }
        public string? Position { get; set; }

        public bool? InPit { get; set; }
        public bool? PitOut { get; set; }
        public int? NumberOfPitStops { get; set; }

        /// <summary>
        /// A custom property where we track if the current lap had <see cref="InPit"/> or <see cref="PitOut"/>
        /// set at any time.
        ///
        /// The intention of the property is to allow for easy filtering of non-flying laps from lap-by-lap data.
        /// </summary>
        public bool IsPitLap { get; set; }

        public int? NumberOfLaps { get; set; }
        public LapSectorTime? LastLapTime { get; set; }

        public Dictionary<string, LapSectorTime> Sectors { get; set; } = new();

        public BestLap BestLapTime { get; set; } = new();

        /// <summary>
        /// In qualifying, indicates if the driver is knocked out of qualifying
        /// </summary>
        public bool? KnockedOut { get; set; }

        /// <summary>
        /// In race sessions, indicates if the driver has retired
        /// </summary>
        public bool? Retired { get; set; }

        /// <summary>
        /// Whether the car has stopped or not. Usually means retried.
        /// </summary>
        public bool? Stopped { get; set; }

        /// <summary>
        /// This is actually a flags enum
        /// </summary>
        public StatusFlags? Status { get; set; }

        public sealed record Interval
        {
            /// <summary>
            /// Can be in the format <c>+1.123</c>,
            /// or if more than a lap then <c>5L</c> (i.e. 5 laps behind)
            /// </summary>
            public string? Value { get; set; }
            public bool? Catching { get; set; }
        }

        /// <summary>
        /// Represents both Laps and Sectors (same model in different places)
        /// </summary>
        public sealed record LapSectorTime
        {
            public string? Value { get; set; }
            public bool? OverallFastest { get; set; }
            public bool? PersonalFastest { get; set; }
            public Dictionary<int, Segment>? Segments { get; set; }

            public sealed record Segment
            {
                public StatusFlags? Status { get; set; }
            }
        }

        public sealed record BestLap
        {
            public string? Value { get; set; }
            public int? Lap { get; set; }
        }

        [Flags]
        public enum StatusFlags
        {
            PersonalBest = 1,
            OverallBest = 2,

            /// <summary>
            /// Went through this mini sector in the pit lane
            /// </summary>
            PitLane = 16,

            /// <summary>
            /// Set when the driver passes the chequered flag in quali or race sessions
            /// </summary>
            ChequeredFlag = 1024,

            /// <summary>
            /// Segment completed. If this is the only flag set, means a yellow segment.
            /// </summary>
            SegmentComplete = 2048,
        }
    }
}