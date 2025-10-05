from ..interfaces import EventParser
from ..models import RawTimingEvent, TimingApp, DriverStints, Stint
from ..enums import LiveTimingEvent
from ..decorators import register_parser
from ...helpers import parse_int, parse_bool


@register_parser(LiveTimingEvent.TIMING_APP)
class TimingAppParser(EventParser[TimingApp]):
    """Parses 'TimingApp' events into a `TimingApp` dataclass."""

    def parse(self, raw: RawTimingEvent) -> TimingApp:
        payload = raw.payload
        lines_data = payload.get("Lines", {})

        lines = {}

        for num, data in lines_data.items():
            stints_list = data.get("Stints", [])

            stints = {}
            for i, stint_data in enumerate(stints_list):
                stints[str(i)] = Stint(
                    lap_flags=parse_int(stint_data.get("LapFlags")),
                    compound=stint_data.get("Compound", ""),
                    new=parse_bool(stint_data.get("New")),
                    tyres_not_changed=parse_int(stint_data.get("TyresNotChanged")),
                    total_laps=parse_int(stint_data.get("TotalLaps")),
                    start_laps=parse_int(stint_data.get("StartLaps")),
                    lap_time=stint_data.get("LapTime", ""),
                    lap_number=parse_int(stint_data.get("LapNumber")),
                )

            lines[num] = DriverStints(
                racing_number=parse_int(data.get("RacingNumber")),
                line=parse_int(data.get("Line")),
                stints=stints,
            )

        return TimingApp(lines=lines)
