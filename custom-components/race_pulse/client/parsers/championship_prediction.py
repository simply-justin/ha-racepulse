from typing import Dict, Any
from ..interfaces import EventParser, register_parser
from ..models.championship_prediction import (
    ChampionshipPrediction,
    DriverPrediction,
    TeamPrediction,
)
from ..enums import LiveTimingEvent


@register_parser(LiveTimingEvent.CHAMPIONSHIP_PREDICTION.value)
class ChampionshipPredictionParser(EventParser):
    """Parse 'ChampionshipPrediction' into ChampionshipPrediction dataclass."""

    def parse(self, raw: Dict[str, Any]) -> ChampionshipPrediction:
        p = raw.get("Json", {})
        drivers = {
            num: DriverPrediction(
                racing_number=num,
                current_position=d.get("CurrentPosition"),
                predicted_position=d.get("PredictedPosition"),
                current_points=d.get("CurrentPoints"),
                predicted_points=d.get("PredictedPoints"),
            )
            for num, d in p.get("Drivers", {}).items()
        }
        teams = {
            name: TeamPrediction(
                team_name=name,
                current_position=t.get("CurrentPosition"),
                predicted_position=t.get("PredictedPosition"),
                current_points=t.get("CurrentPoints"),
                predicted_points=t.get("PredictedPoints"),
            )
            for name, t in p.get("Teams", {}).items()
        }
        return ChampionshipPrediction(drivers=drivers, teams=teams)
