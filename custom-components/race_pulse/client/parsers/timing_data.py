from ..interfaces import EventParser
from ..models import (
    RawTimingEvent,
    TimingData,
    DriverTiming,
    LastLapTime,
    BestLapTime,
    Speed,
    SpeedData,
    Sector,
    Segment,
)
from ..enums import LiveTimingEvent
from ..decorators import register_parser
from ...helpers import parse_int, parse_bool


@register_parser(LiveTimingEvent.TIMING_DATA)
class TimingDataParser(EventParser):
    """Parses 'TimingData' events into a fully structured `TimingData` dataclass."""

    def parse(self, raw: RawTimingEvent) -> TimingData:
        payload = raw.payload
        lines_data = payload.get("Lines", {})
        lines = {}

        for num, data in lines_data.items():
            # --- Parse nested segments ---
            sectors = []
            for s in data.get("Sectors", []):
                segments = [
                    Segment(status=parse_int(seg.get("Status")))
                    for seg in s.get("Segments", [])
                ]
                sectors.append(
                    Sector(
                        stopped=parse_bool(s.get("Stopped")),
                        value=s.get("Value", ""),
                        status=parse_int(s.get("Status")),
                        overall_fastest=parse_bool(s.get("OverallFastest")),
                        personal_fastest=parse_bool(s.get("PersonalFastest")),
                        segments=segments,
                        previous_value=s.get("PreviousValue"),
                    )
                )

            # --- Parse speeds ---
            speeds = None
            if "Speeds" in data:
                sp = data["Speeds"]
                speeds = Speed(
                    i1=self._parse_speed_data(sp.get("I1")),
                    i2=self._parse_speed_data(sp.get("I2")),
                    fl=self._parse_speed_data(sp.get("FL")),
                    st=self._parse_speed_data(sp.get("ST")),
                )

            # --- Parse best and last lap times ---
            best_lap = None
            if "BestLapTime" in data:
                b = data["BestLapTime"]
                best_lap = BestLapTime(
                    value=b.get("Value", ""), lap=parse_int(b.get("Lap"))
                )

            last_lap = None
            if "LastLapTime" in data:
                l = data["LastLapTime"]
                last_lap = LastLapTime(
                    value=l.get("Value", ""),
                    status=parse_int(l.get("Status")),
                    overall_fastest=parse_bool(l.get("OverallFastest")),
                    personal_fastest=parse_bool(l.get("PersonalFastest")),
                )

            # --- Build driver timing entry ---
            lines[num] = DriverTiming(
                time_diff_to_fastest=data.get("TimeDiffToFastest", ""),
                time_diff_to_position_ahead=data.get("TimeDiffToPositionAhead", ""),
                line=parse_int(data.get("Line")),
                position=data.get("Position", ""),
                show_position=parse_bool(data.get("ShowPosition")),
                racing_number=parse_int(data.get("RacingNumber")),
                retired=parse_bool(data.get("Retired")),
                in_pit=parse_bool(data.get("InPit")),
                pit_out=parse_bool(data.get("PitOut")),
                stopped=parse_bool(data.get("Stopped")),
                status=parse_int(data.get("Status")),
                sectors=sectors,
                speeds=speeds,
                best_lap_time=best_lap,
                last_lap_time=last_lap,
                number_of_laps=parse_int(data.get("NumberOfLaps")),
                number_of_pit_stops=parse_int(data.get("NumberOfPitStops")),
            )

        return TimingData(
            lines=lines, withheld=parse_bool(payload.get("Withheld", False))
        )

    # --- Helper methods ---
    @staticmethod
    def _parse_speed_data(data) -> SpeedData:
        if not data:
            return SpeedData(
                value=0, status=0, overall_fastest=False, personal_fastest=False
            )
        return SpeedData(
            value=int(data.get("Value", 0)) if data.get("Value", "").isdigit() else 0,
            status=int(data.get("Status", 0)),
            overall_fastest=str(data.get("OverallFastest", "")).lower() == "true",
            personal_fastest=str(data.get("PersonalFastest", "")).lower() == "true",
        )
