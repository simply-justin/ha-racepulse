from ..enums.live_timing_event import LiveTimingEvent
from ..models.raw_timing_event import RawTimingEvent
from ..models.weather_data import WeatherData
from ..interfaces.event_parser import EventParser
from ..decorators.parser import register_parser
from ...helpers import parse_float


@register_parser(LiveTimingEvent.WEATHER)
class WeatherDataParser(EventParser[WeatherData]):
    """
    Parses a 'WeatherData' event payload into a `WeatherData` dataclass.

    This parser converts the raw numeric strings from the F1 Live Timing feed
    into properly typed float fields for temperature, humidity, and wind data.

    Example of raw payload:
        {
            "AirTemp": "28.5",
            "Humidity": "73.0",
            "Pressure": "1012.6",
            "Rainfall": "0",
            "TrackTemp": "32.5",
            "WindDirection": "115",
            "WindSpeed": "0.5"
        }
    """

    def parse(self, raw: RawTimingEvent) -> WeatherData:
        payload = raw.payload or {}

        return WeatherData(
            air_temperature=parse_float(payload.get("AirTemp")),
            humidity=parse_float(payload.get("Humidity")),
            air_pressure=parse_float(payload.get("Pressure")),
            rainfall=parse_float(payload.get("Rainfall")),
            track_temperature=parse_float(payload.get("TrackTemp")),
            wind_direction=parse_float(payload.get("WindDirection")),
            wind_speed=parse_float(payload.get("WindSpeed")),
        )
