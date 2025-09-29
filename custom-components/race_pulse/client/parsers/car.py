from ..enums.live_timing_event import LiveTimingEvent
from ..interfaces import EventParser
from ..models import Car, CarTelemetry, CarTelemetrySnapshot


class CarParser(EventParser):
    def supports(self, event_type: str) -> bool:
        return event_type == LiveTimingEvent.CAR_DATA.value

    def parse(self, raw: dict) -> Car:
        payload = raw["Json"]
        cars = {}
        for driver_number, data in payload.get("Entries", {}).items():
            cars[driver_number] = CarTelemetry(
                engine_rpm=int(data.get("Rpm", 0)),
                speed_kph=float(data.get("Speed", 0.0)),
                gear=int(data.get("Gear", 0)),
                throttle_percent=int(data.get("Throttle", 0)),
                brake_percent=int(data.get("Brake", 0)),
                drs_state=int(data.get("Drs", 0)),
            )
        CarTelemetryBatch(timestamp_utc=raw["DateTime"], cars=cars)

        return Car(
            snapshots=[
                CarTelemetrySnapshot(
                    timestamp_utc=raw["DateTime"],
                    cars=cars,
                )
            ]
        )
