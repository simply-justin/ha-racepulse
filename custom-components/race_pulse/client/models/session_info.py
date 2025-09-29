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
