from typing import Dict, Any
from ..interfaces import EventParser, register_parser
from ..models.position import PositionData, CarPosition
from ..enums import LiveTimingEvent


@register_parser(LiveTimingEvent.POSITION.value)
class PositionParser(EventParser):
    """Parse 'Position' into PositionData dataclass."""

    def parse(self, raw: Dict[str, Any]) -> PositionData:
        p = raw.get("Json", {})
        cars = {
            num: CarPosition(x=float(d.get("X", 0.0)), y=float(d.get("Y", 0.0)), z=float(d.get("Z", 0.0)))
            for num, d in p.get("Entries", {}).items()
        }
        return PositionData(cars=cars)

    s
