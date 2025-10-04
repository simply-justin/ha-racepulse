from datetime import datetime
from ..interfaces import EventParser
from ..models import RawTimingEvent, SessionInfo, ArchiveStatus, Meeting, Country, Circuit
from ..enums import LiveTimingEvent
from ..decorators import register_parser


@register_parser(LiveTimingEvent.SESSION_INFO)
class SessionInfoParser(EventParser):
    """Parse 'SessionInfo' into SessionInfo dataclass."""

    def parse(self, raw: "RawTimingEvent") -> SessionInfo:
        p = raw.payload
        circuit = (
            CircuitDetail(
                circuit_id=p.get("Circuit", {}).get("Key"),
                short_name=p.get("Circuit", {}).get("ShortName"),
            )
            if "Circuit" in p
            else None
        )
        meeting = (
            MeetingDetail(
                name=p.get("Meeting", {}).get("Name"),
                circuit=circuit,
            )
            if "Meeting" in p
            else None
        )
        return SessionInfo(
            session_id=p.get("Key"),
            session_type=p.get("Type"),
            name=p.get("Name"),
            start_time=(
                datetime.fromisoformat(p["StartDate"]) if p.get("StartDate") else None
            ),
            end_time=datetime.fromisoformat(p["EndDate"]) if p.get("EndDate") else None,
            gmt_offset=p.get("GmtOffset"),
            path=p.get("Path"),
            meeting=meeting,
            circuit_points=p.get("CircuitPoints", []),
            circuit_corners=p.get("CircuitCorners", []),
            circuit_rotation=p.get("CircuitRotation", 0),
        )
