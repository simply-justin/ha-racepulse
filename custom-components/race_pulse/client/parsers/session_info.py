from ..interfaces import EventParser
from ..models import (
    RawTimingEvent,
    SessionInfo,
    ArchiveStatus,
    Meeting,
    Country,
    Circuit,
)
from ..enums import LiveTimingEvent
from ..decorators import register_parser
from ...helpers import parse_int, parse_datetime, parse_timedelta


@register_parser(LiveTimingEvent.SESSION_INFO)
class SessionInfoParser(EventParser[SessionInfo]):
    """Parses 'SessionInfo' events into a `SessionInfo` dataclass."""

    def parse(self, raw: RawTimingEvent) -> SessionInfo:
        payload = raw.payload

        # Country
        country_data = payload.get("Meeting", {}).get("Country", {})
        country = Country(
            key=parse_int(country_data.get("Key")),
            code=country_data.get("Code", ""),
            name=country_data.get("Name", ""),
        )

        # Circuit
        circuit_data = payload.get("Meeting", {}).get("Circuit", {})
        circuit = Circuit(
            key=parse_int(circuit_data.get("Key")),
            short_name=circuit_data.get("ShortName", ""),
        )

        # Meeting
        meeting_data = payload.get("Meeting", {})
        meeting = Meeting(
            sessions=[],  # Not included in SessionInfo payload
            key=parse_int(meeting_data.get("Key")),
            code=meeting_data.get("Code"),
            number=meeting_data.get("Number"),
            location=meeting_data.get("Location", ""),
            official_name=meeting_data.get("OfficialName", ""),
            name=meeting_data.get("Name", ""),
            country=country,
            circuit=circuit,
        )

        # ArchiveStatus
        archive_status_data = payload.get("ArchiveStatus", {})
        archive_status = ArchiveStatus(status=archive_status_data.get("Status", ""))

        # --- Parse time fields ---
        start_date = parse_datetime(payload.get("StartDate"))
        end_date = parse_datetime(payload.get("EndDate"))
        gmt_offset = parse_timedelta(payload.get("GmtOffset"))

        # --- Create SessionInfo instance ---
        return SessionInfo(
            meeting=meeting,
            session_status=payload.get("SessionStatus", ""),
            archive_status=archive_status,
            key=parse_int(payload.get("Key")),
            type=payload.get("Type", ""),
            number=parse_int(payload.get("Number")),
            name=payload.get("Name", ""),
            start_date=start_date,
            end_date=end_date,
            gmt_offset=gmt_offset,
            path=payload.get("Path", ""),
        )
