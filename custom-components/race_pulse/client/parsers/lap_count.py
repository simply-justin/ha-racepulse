from typing import Dict, Any
from ..interfaces import EventParser, register_parser
from ..models.lap_count import LapCount
from ..enums import LiveTimingEvent


@register_parser(LiveTimingEvent.LAP_COUNT.value)
class LapCountParser(EventParser):
    """Parse 'LapCount' raw payload into LapCount dataclass."""

    def parse(self, raw: Dict[str, Any]) -> LapCount:
        p = raw.get("Json", {})
        return LapCount(
            current_lap=int(p.get("CurrentLap", 0)),
            total_laps=int(p.get("TotalLaps", 0)),
        )
