from ..enums.live_timing_event import LiveTimingEvent
from ..interfaces import EventMapper
from ..models import Weather

class WeatherParser(EventMapper):
    def supports(self, event_type: str) -> bool:
        return event_type == LiveTimingEvent.WEATHER.value

    def map(self, raw: dict) -> Weather:
        p = raw["Json"]
        return Weather(
            air_temperature=float(p.get("AirTemp", 0.0)),
            humidity_percent=float(p.get("Humidity", 0.0)),
            air_pressure_hpa=float(p.get("Pressure", 0.0)),
            rainfall_mm=float(p.get("Rainfall", 0.0)),
            track_temperature=float(p.get("TrackTemp", 0.0)),
            wind_direction_deg=float(p.get("WindDirection", 0.0)),
            wind_speed_kph=float(p.get("WindSpeed", 0.0)),
        )