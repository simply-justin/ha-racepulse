from ..interfaces import EventParser
from ..models import RawTimingEvent, TrackStatus
from ..enums import LiveTimingEvent
from ..decorators import register_parser


@register_parser(LiveTimingEvent.TRACK_STATUS)
class TrackStatusParser(EventParser):
    """Parse 'TrackStatus' event into TrackStatus dataclass."""

    def parse(self, raw: "RawTimingEvent") -> TrackStatus:
        p = raw.payload
        return TrackStatus(
            status=p.get(
                "Status", "unknown"
            ),  # TODO: Make this convert to an enum when its implemented
            message=p.get("Message"),
        )
