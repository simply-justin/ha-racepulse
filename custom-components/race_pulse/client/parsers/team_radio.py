from ..interfaces import EventParser
from ..models import RawTimingEvent, TeamRadio, TeamRadioCapture
from ..enums import LiveTimingEvent
from ..decorators import register_parser
from ...helpers import parse_int, parse_datetime


@register_parser(LiveTimingEvent.TEAM_RADIO)
class TeamRadioParser(EventParser):
    """Parses 'TeamRadio' events into a `TeamRadio` dataclass."""

    def parse(self, raw: RawTimingEvent) -> TeamRadio:
        payload = raw.payload
        captures_data = payload.get("Captures", [])

        captures = []
        for c in captures_data:
            captures.append(
                TeamRadioCapture(
                    datetime_utc=parse_datetime((c.get("Utc").replace("Z", "+00:00"))),
                    racing_number=parse_int(c.get("RacingNumber")),
                    path=c.get("Path", ""),
                )
            )

        return TeamRadio(captures=captures)
