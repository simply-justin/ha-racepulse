from typing import Dict, Any
from ..enums import LiveTimingEvent
from ..models.weather import Weather
from ..interfaces import EventParser, register_parser


@register_parser(LiveTimingEvent.WEATHER.value)
class WeatherDataParser(EventParser):
    """
    Parse 'WeatherData' raw payload into a Weather dataclass.
    Keeps dataclass pure (no JSON knowledge); conversion lives here.
    """

    def parse(self, raw: Dict[str, Any]) -> Weather:
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
