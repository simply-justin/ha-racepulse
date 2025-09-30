from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Tuple


@dataclass(frozen=True)
class CircuitDetail:
    """
    Information about the race circuit.

    Attributes:
        circuit_id: Unique circuit identifier.
        short_name: Short circuit name.
    """

    circuit_id: Optional[int] = None
    short_name: Optional[str] = None


@dataclass(frozen=True)
class MeetingDetail:
    """
    Information about the race meeting.

    Attributes:
        name: Meeting name (e.g., "Australian Grand Prix").
        circuit: Circuit details for this meeting.
    """

    name: Optional[str] = None
    circuit: Optional[CircuitDetail] = None


@dataclass(frozen=True)
class SessionInfo:
    """
    Metadata about a Formula 1 session.

    Attributes:
        session_id: Unique session identifier.
        session_type: Type of session (e.g., Practice, Qualifying, Race).
        name: Human-readable session name.
        start_time: UTC start time of the session.
        end_time: UTC end time of the session.
        gmt_offset: Offset from GMT as string (e.g., "+02:00").
        path: Internal path identifier.
        meeting: Associated meeting details.
        circuit_points: Circuit outline as a list of (x, y) points.
        circuit_corners: Circuit corners with car number and coordinates.
        circuit_rotation: Rotation angle to align with F1 visualization.
    """

    session_id: Optional[int] = None
    session_type: Optional[str] = None
    name: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    gmt_offset: Optional[str] = None
    path: Optional[str] = None

    meeting: Optional[MeetingDetail] = None

    circuit_points: List[Tuple[int, int]] = field(default_factory=list)
    circuit_corners: List[Tuple[int, float, float]] = field(default_factory=list)
    circuit_rotation: int = 0
/// <summary>
/// Sample: {"Messages": {"2": {"Utc": "2021-03-27T12:00:00", "Category": "Flag", "Flag": "GREEN", "Scope": "Track", "Message": "GREEN LIGHT - PIT EXIT OPEN"}}}
/// </summary>
public sealed record SessionInfoDataPoint : ILiveTimingDataPoint
{
    /// <inheritdoc />
    public LiveTimingDataType LiveTimingDataType => LiveTimingDataType.SessionInfo;

    public int? Key { get; init; }
    public string? Type { get; init; }
    public string? Name { get; init; }
    public DateTime? StartDate { get; init; }
    public DateTime? EndDate { get; init; }
    public string? GmtOffset { get; init; }
    public string? Path { get; init; }

    public MeetingDetail? Meeting { get; init; }

    /// <summary>
    /// Populated manually by UndercutF1.Data when the data is first processed, from an external API provider.
    /// Not provided by F1.
    /// </summary>
    public List<(int x, int y)> CircuitPoints { get; set; } = [];
    public List<(int number, float x, float y)> CircuitCorners { get; set; } = [];

    /// <summary>
    /// Populated manually by UndercutF1.Data when the data is first processed, from an external API provider.
    /// The rotation that should be applied to the circuit image to make it match the F1 visualisation.
    /// </summary>
    public int CircuitRotation { get; set; } = 0;

    public sealed record MeetingDetail
    {
        public string? Name { get; init; }

        public CircuitDetail? Circuit { get; init; }

        public sealed record CircuitDetail
        {
            public int? Key { get; init; }
            public string? ShortName { get; init; }
        }
    }
}