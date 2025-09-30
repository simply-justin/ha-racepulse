from dataclasses import dataclass
from ..enums import LiveTimingEvent


@dataclass(frozen=True)
class Weather:
    """
    Current weather and track conditions.

    Source: SignalR event "WeatherData"
    Raw example:
        {
          "AirTemp": "25.6", "Humidity": "62.0", "Pressure": "1013.1",
          "Rainfall": "0", "TrackTemp": "31.2", "WindDirection": "7", "WindSpeed": "1.2"
        }

    Attributes:
        air_temperature: Ambient air temperature (°C).
        humidity_percent: Relative humidity (%).
        air_pressure_hpa: Air pressure (hPa).
        rainfall_mm: Rainfall in millimeters (mm/h if rate; F1 docs vary).
        track_temperature: Track surface temperature (°C).
        wind_direction_deg: Wind direction (0–360 degrees).
        wind_speed_kph: Wind speed (km/h).
    """

    air_temperature: float
    humidity_percent: float
    air_pressure_hpa: float
    rainfall_mm: float
    track_temperature: float
    wind_direction_deg: float
    wind_speed_kph: float

    data_type: LiveTimingEvent = LiveTimingEvent.WEATHER
/// <summary>
/// Sample: { "AirTemp": "25.6", "Humidity": "62.0", "Pressure": "1013.1", "Rainfall": "0", "TrackTemp": "31.2", "WindDirection": "7", "WindSpeed": "1.2" }
/// </summary>
public sealed record WeatherDataPoint : ILiveTimingDataPoint
{
    /// <inheritdoc />
    public LiveTimingDataType LiveTimingDataType => LiveTimingDataType.WeatherData;

    public string? AirTemp { get; set; }
    public string? Humidity { get; set; }
    public string? Pressure { get; set; }
    public string? Rainfall { get; set; }
    public string? TrackTemp { get; set; }
    public string? WindDirection { get; set; }
    public string? WindSpeed { get; set; }
}