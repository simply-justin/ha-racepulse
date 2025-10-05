from ..interfaces import EventParser
from ..models import RawTimingEvent, TrackStatus
from ..enums import LiveTimingEvent
from ..decorators import register_parser
from ...helpers import parse_string


@register_parser(LiveTimingEvent.TRACK_STATUS)
class TrackStatusParser(EventParser[TrackStatus]):
    """Parses 'TrackStatus' events into a `TrackStatus` dataclass."""

    def parse(self, raw: RawTimingEvent) -> TrackStatus:
        payload = raw.payload or {}

        return TrackStatus(
            status=parse_string(payload.get("Status", "unknown")),
            message=parse_string(payload.get("Message", "")),
        )
