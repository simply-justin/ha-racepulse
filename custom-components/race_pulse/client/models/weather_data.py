from dataclasses import dataclass
from ..enums import LiveTimingEvent


@dataclass(frozen=True)
class WeatherData:
    """
    Current weather and track conditions.

    Source: SignalR event "WeatherData"
    Raw example:
        {
            "AirTemp": "28.5",
            "Humidity": "73.0",
            "Pressure": "1012.6",
            "Rainfall": "0",
            "TrackTemp": "32.5",
            "WindDirection": "115",
            "WindSpeed": "0.5",
            "_kf": true
        }
    """

    data_type: LiveTimingEvent = LiveTimingEvent.WEATHER
    air_temperature: float
    humidity: float
    air_pressure: float
    rainfall: float
    track_temperature: float
    wind_direction: float
    wind_speed: float
