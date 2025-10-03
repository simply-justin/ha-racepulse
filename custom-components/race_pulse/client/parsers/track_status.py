from typing import Dict, Any
from ..interfaces import EventParser, register_parser
from ..models.track_status import TrackStatus
from ..enums import LiveTimingEvent


@register_parser(LiveTimingEvent.TRACK_STATUS.value)
class TrackStatusParser(EventParser):
    """Parse 'TrackStatus' event into TrackStatus dataclass."""

    def parse(self, raw: Dict[str, Any]) -> TrackStatus:
        p = raw.get("Json", {})
        return TrackStatus(
            status_flag=p.get("Status", "unknown"),
            message=p.get("Message"),
        )

        # "TrackStatus": {
        #     "Status": "1",
        #     "Message": "AllClear",
        #     "_kf": true
        # },