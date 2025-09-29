from dataclasses import dataclass, field
from typing import Dict, Optional

@dataclass(frozen=True)
class DriverPrediction:
    """
    Championship prediction for a single driver.

    Attributes:
        racing_number: Driver’s racing number.
        current_position: Current championship position.
        predicted_position: Predicted final position.
        current_points: Current championship points.
        predicted_points: Predicted championship points.
    """
    racing_number: Optional[str] = None
    current_position: Optional[int] = None
    predicted_position: Optional[int] = None
    current_points: Optional[float] = None
    predicted_points: Optional[float] = None


@dataclass(frozen=True)
class TeamPrediction:
    """
    Championship prediction for a team.

    Attributes:
        team_name: Team name.
        current_position: Current championship position.
        predicted_position: Predicted final position.
        current_points: Current championship points.
        predicted_points: Predicted championship points.
    """
    team_name: Optional[str] = None
    current_position: Optional[int] = None
    predicted_position: Optional[int] = None
    current_points: Optional[float] = None
    predicted_points: Optional[float] = None


@dataclass(frozen=True)
class ChampionshipPrediction:
    """
    Championship predictions for drivers and teams.

    Attributes:
        drivers: Mapping of driver IDs to driver predictions.
        teams: Mapping of team names to team predictions.
    """
    drivers: Dict[str, DriverPrediction] = field(default_factory=dict)
    teams: Dict[str, TeamPrediction] = field(default_factory=dict)
