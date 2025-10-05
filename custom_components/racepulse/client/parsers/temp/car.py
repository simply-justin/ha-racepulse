from typing import Dict, Any
from ..interfaces import EventParser, register_parser
from ..models.car import CarTelemetry, CarTelemetryBatch
from ..enums import LiveTimingEvent


@register_parser(LiveTimingEvent.CAR_DATA.value)
class CarParser(EventParser):
    """Parse 'CarData' into CarTelemetryBatch with per-car telemetry."""

    def parse(self, raw: Dict[str, Any]) -> CarTelemetryBatch:
        p = raw.get("Json", {})
        cars = {}
        for num, data in p.get("Entries", {}).items():
            cars[num] = CarTelemetry(
                engine_rpm=int(data.get("Rpm", 0)),
                speed_kph=float(data.get("Speed", 0.0)),
                gear=int(data.get("Ngear", 0)),
                throttle_percent=int(data.get("Throttle", 0)),
                brake_percent=int(data.get("Brake", 0)),
                drs_state=int(data.get("Drs", 0)),
            )
        return CarTelemetryBatch(timestamp_utc=raw["DateTime"], cars=cars)
