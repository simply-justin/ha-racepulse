from datetime import datetime
from ..interfaces import EventParser
from ..models import RawTimingEvent, TeamRadio, TeamRadioCapture
from ..enums import LiveTimingEvent
from ..decorators import register_parser


@register_parser(LiveTimingEvent.TEAM_RADIO)
class TeamRadioParser(EventParser):
    """Parse 'TeamRadio' into TeamRadio with a list of captures."""

    def parse(self, raw: "RawTimingEvent") -> TeamRadio:
        p = raw.get("Json", {})
        captures = [
            TeamRadioCapture(
                datetime_utc=datetime.fromisoformat(c["Utc"]),
                racing_number=c.get("RacingNumber"),
                path=c.get("Path")
            )
            for c in p.get("Captures", [])
        ]
        return TeamRadio(captures=captures)
