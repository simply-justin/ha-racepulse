from datetime import datetime
from ..enums.live_timing_event import LiveTimingEvent
from ..interfaces import EventParser
from ..models import SessionInfo, CircuitDetail, MeetingDetail


class SessionInfoParser(EventParser):
    def supports(self, event_type: str) -> bool:
        return event_type == LiveTimingEvent.SESSION_INFO.value

    def parse(self, raw: dict) -> SessionInfo:
        p = raw["Json"]

        circuit = None
        if "Circuit" in p:
            circuit = CircuitDetail(
                circuit_id=p["Circuit"].get("Key"),
                short_name=p["Circuit"].get("ShortName"),
            )

        meeting = None
        if "Meeting" in p:
            meeting = MeetingDetail(
                name=p["Meeting"].get("Name"),
                circuit=circuit,
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
