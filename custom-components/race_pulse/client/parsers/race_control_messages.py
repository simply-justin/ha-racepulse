from datetime import datetime
from ..enums.live_timing_event import LiveTimingEvent
from ..interfaces import EventParser
from ..models import RaceControlMessages, RaceControlMessage

class RaceControlMessagesParser(EventParser):
    def supports(self, event_type: str) -> bool:
        return event_type == LiveTimingEvent.RACE_CONTROL_MESSAGES.value

    def parse(self, raw: dict) -> RaceControlMessages:
        messages = []
        for _, msg in raw["Json"].get("Messages", {}).items():
            messages.append(
                RaceControlMessage(
                    timestamp_utc=datetime.fromisoformat(msg["Utc"]),
                    text=msg["Message"],
                )
            )
        return RaceControlMessages(messages=messages)