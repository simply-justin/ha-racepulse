from typing import Any, Dict
from datetime import datetime
from .interfaces import _PARSER_REGISTRY
from .models import RawTimingEvent


class EventFactory:
    """
    Resolve raw SignalR events to typed dataclasses via the parser registry.
    Add a new parser by creating a class with @register_parser("Type").
    """

    @staticmethod
    def parse(raw: Dict[str, Any]) -> object:
        event_type = raw.get("Type")
        parser_cls = _PARSER_REGISTRY.get(event_type)
        if parser_cls:
            try:
                return parser_cls().parse(raw)
            except Exception:
                pass

        ts = raw.get("DateTime")
        ts_dt = None
        if isinstance(ts, str):
            ts_dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return RawTimingEvent(
            event_type=event_type, payload=raw.get("Json"), timestamp_utc=ts_dt
        )
