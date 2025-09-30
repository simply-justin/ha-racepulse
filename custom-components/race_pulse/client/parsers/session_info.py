from datetime import datetime
from typing import Dict, Any
from ..interfaces import EventParser, register_parser
from ..models.session_info import SessionInfo, MeetingDetail, CircuitDetail
from ..enums import LiveTimingEvent


@register_parser(LiveTimingEvent.SESSION_INFO.value)
class SessionInfoParser(EventParser):
    """Parse 'SessionInfo' into SessionInfo dataclass."""

    def parse(self, raw: Dict[str, Any]) -> SessionInfo:
        p = raw.get("Json", {})
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
