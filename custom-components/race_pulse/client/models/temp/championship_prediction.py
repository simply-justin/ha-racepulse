from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class DriverPrediction:
    """Prediction data for a single driver in championship standings."""
    racing_number: str
    current_position: int
    predicted_position: int
    current_points: float
    predicted_points: float


@dataclass(frozen=True)
class TeamPrediction:
    """Prediction data for a single team in championship standings."""
    team_name: str
    current_position: int
    predicted_position: int
    current_points: float
    predicted_points: float


@dataclass(frozen=True)
class ChampionshipPrediction:
    """
    Championship predictions for drivers and teams.
    Source: SignalR event "ChampionshipPrediction".
    """
    drivers: Dict[str, DriverPrediction]
    teams: Dict[str, TeamPrediction]
/// <summary>
/// Sample:
/// <c>
///    "Drivers": {
///      "1": {
///        "RacingNumber": "1",
///        "CurrentPosition": 1,
///        "PredictedPosition": 1,
///        "CurrentPoints": 161.0,
///        "PredictedPoints": 169.0
///      },
///      "16": {
///        "RacingNumber": "16",
///        "CurrentPosition": 2,
///        "PredictedPosition": 2,
///        "CurrentPoints": 113.0,
///        "PredictedPoints": 138.0
///      }
/// </c>
/// </summary>
public sealed class ChampionshipPredictionDataPoint : ILiveTimingDataPoint
{
    /// <inheritdoc />
    public LiveTimingDataType LiveTimingDataType => LiveTimingDataType.ChampionshipPrediction;

    public Dictionary<string, Driver> Drivers { get; set; } = new();
    public Dictionary<string, Team> Teams { get; set; } = new();

    public sealed record Driver
    {
        public string? RacingNumber { get; set; }
        public int? CurrentPosition { get; set; }
        public int? PredictedPosition { get; set; }
        public decimal? CurrentPoints { get; set; }
        public decimal? PredictedPoints { get; set; }
    }

    public sealed record Team
    {
        public string? TeamName { get; set; }
        public int? CurrentPosition { get; set; }
        public int? PredictedPosition { get; set; }
        public decimal? CurrentPoints { get; set; }
        public decimal? PredictedPoints { get; set; }
    }
}