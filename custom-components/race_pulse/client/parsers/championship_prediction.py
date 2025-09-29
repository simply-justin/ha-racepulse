from ..enums.live_timing_event import LiveTimingEvent
from ..interfaces import EventParser
from ..models import ChampionshipPrediction, DriverPrediction, TeamPrediction


class ChampionshipPredictionParser(EventParser):
    def supports(self, event_type: str) -> bool:
        return event_type == LiveTimingEvent.CHAMPIONSHIP_PREDICTION.value

    def parse(self, raw: dict) -> ChampionshipPrediction:
        drivers = {}
        for num, d in raw["Json"].get("Drivers", {}).items():
            drivers[num] = DriverPrediction(
                racing_number=num,
                current_position=d.get("CurrentPosition"),
                predicted_position=d.get("PredictedPosition"),
                current_points=d.get("CurrentPoints"),
                predicted_points=d.get("PredictedPoints"),
            )

        teams = {}
        for name, t in raw["Json"].get("Teams", {}).items():
            teams[name] = TeamPrediction(
                team_name=name,
                current_position=t.get("CurrentPosition"),
                predicted_position=t.get("PredictedPosition"),
                current_points=t.get("CurrentPoints"),
                predicted_points=t.get("PredictedPoints"),
            )

        return ChampionshipPrediction(drivers=drivers, teams=teams)
