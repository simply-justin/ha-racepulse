from dataclasses import dataclass
from ..enums.live_timing_event import LiveTimingEvent

@dataclass(frozen=True)
class Weather:
    """
    Current weather and track conditions.

    Attributes:
        data_type: Always set to `LiveTimingEvent.WeatherData`.
        air_temperature: Ambient air temperature in °C.
        humidity_percent: Relative humidity (%).
        air_pressure_hpa: Atmospheric pressure in hPa.
        rainfall_mm: Rainfall intensity in millimeters.
        track_temperature: Track surface temperature in °C.
        wind_direction_deg: Wind direction in degrees (0–360).
        wind_speed_kph: Wind speed in kilometers per hour.
    """

    data_type: LiveTimingEvent = LiveTimingEvent.WeatherData

    air_temperature: float
    humidity_percent: float
    air_pressure_hpa: float
    rainfall_mm: float
    track_temperature: float
    wind_direction_deg: float
    wind_speed_kph: float

    def is_raining(self) -> bool:
        """Return True if rainfall is greater than zero."""
        return self.rainfall_mm > 0