from ..enums import LiveTimingEvent
from ..models import RawTimingEvent, WeatherData
from ..interfaces import EventParser
from ..decorators import register_parser


@register_parser(LiveTimingEvent.WEATHER_DATA)
class WeatherDataParser(EventParser):
    """
    Parse 'WeatherData' raw payload into a Weather dataclass.
    Keeps dataclass pure (no JSON knowledge); conversion lives here.
    """

    def parse(self, raw: "RawTimingEvent") -> WeatherData:
        p = raw.payload
        return WeatherData(
            air_temperature=float(p.get("AirTemp", 0.0)),
            humidity=float(p.get("Humidity", 0.0)),
            air_pressure=float(p.get("Pressure", 0.0)),
            rainfall=float(p.get("Rainfall", 0.0)),
            track_temperature=float(p.get("TrackTemp", 0.0)),
            wind_direction=float(p.get("WindDirection", 0.0)),
            wind_speed=float(p.get("WindSpeed", 0.0)),
        )
