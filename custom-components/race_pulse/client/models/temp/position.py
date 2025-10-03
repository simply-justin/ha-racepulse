from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List


@dataclass(frozen=True)
class CarPosition:
    """
    Position data for a single car at a specific time.

    Attributes:
        status: Driver status ("on_track" or "off_track").
        x: X coordinate of car in centimeters.
        y: Y coordinate of car in centimeters.
        z: Z coordinate of car in centimeters.
    """

    status: str  # e.g., "on_track", "off_track"
    x: int
    y: int
    z: int


@dataclass(frozen=True)
class PositionSnapshot:
    """
    Snapshot of all car positions at a specific timestamp.

    Attributes:
        timestamp_utc: UTC timestamp of the snapshot.
        cars: Mapping of driver numbers to car position data.
    """

    timestamp_utc: datetime
    cars: Dict[str, CarPosition]


@dataclass(frozen=True)
class Position:
    """
    A batch of position snapshots.

    Attributes:
        snapshots: List of position snapshots.
    """

    snapshots: List[PositionSnapshot]
/// <summary>
/// Position data is sent as compressed (with deflate) JSON containing Entries.
/// Each Position Entry is the cars position at a specific point of time, and they seem to be batched to reduce network load.
/// </summary>
public sealed class PositionDataPoint : ILiveTimingDataPoint
{
    public LiveTimingDataType LiveTimingDataType => LiveTimingDataType.Position;

    public List<PositionData> Position { get; set; } = [new()];

    public sealed class PositionData
    {
        public DateTimeOffset Timestamp { get; set; }

        /// <summary>
        /// Dictionary of DriverNumber to Entry with position data.
        /// </summary>
        public Dictionary<string, Entry> Entries { get; set; } = [];

        public sealed class Entry
        {
            public DriverStatus? Status { get; set; }

            /// <summary>
            /// X position of the car in 1/10ths of a meter (cm).
            /// </summary>
            public int? X { get; set; }

            /// <summary>
            /// Y position of the car in 1/10ths of a meter (cm).
            /// </summary>
            public int? Y { get; set; }

            /// <summary>
            /// Z position of the car in 1/10ths of a meter (cm).
            /// </summary>
            public int? Z { get; set; }

            public enum DriverStatus
            {
                OnTrack,
                OffTrack,
            }
        }
    }
}