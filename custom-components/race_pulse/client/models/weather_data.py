from dataclasses import dataclass
from typing import Final
from ..enums import LiveTimingEvent
from ..interfaces import Event
from ..decorators import register_event


@register_event(LiveTimingEvent.WEATHER_DATA)
@dataclass(frozen=True)
class WeatherData(Event):
    """
    Represents current weather and track conditions during a Formula 1 session.

    This event provides continuous updates on atmospheric and circuit parameters,
    such as air and track temperatures, humidity, pressure, and wind conditions.

    Example of raw event payload:
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

    Attributes:
        data_type: A constant identifying this event as a `WEATHER_DATA` event.
        air_temperature: The current air temperature in degrees Celsius.
        humidity: The relative humidity as a percentage (0–100).
        air_pressure: The atmospheric pressure in hPa.
        rainfall: The rainfall intensity in mm/h.
        track_temperature: The current track surface temperature in degrees Celsius.
        wind_direction: The wind direction in degrees (0–360, where 0 = North).
        wind_speed: The wind speed in m/s.

    Source:
        SignalR event: "WeatherData"
    """

    data_type: Final[LiveTimingEvent] = LiveTimingEvent.WEATHER_DATA
    air_temperature: float
    humidity: float
    air_pressure: float
    rainfall: float
    track_temperature: float
    wind_direction: float
    wind_speed: float
