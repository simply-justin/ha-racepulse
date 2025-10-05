from typing import Dict, List
from ..interfaces import EventParser
from ..models import (
    RawTimingEvent,
    TimingStats,
    DriverStat,
    BestSpeed,
    PersonalBestLapTime,
    Stat,
)
from ..enums import LiveTimingEvent
from ..decorators import register_parser
from ...helpers import parse_int


@register_parser(LiveTimingEvent.TIMING_STATS)
class TimingStatsParser(EventParser[TimingStats]):
    """Parses 'TimingStats' events into a `TimingStats` dataclass."""

    def parse(self, raw: RawTimingEvent) -> TimingStats:
        payload = raw.payload
        lines: Dict[str, DriverStat] = {}

        for num, data in payload.get("Lines", {}).items():
            # --- Personal best lap time ---
            personal_best_lap_time = None
            pblt_data = data.get("PersonalBestLapTime")
            if pblt_data:
                personal_best_lap_time = PersonalBestLapTime(
                    value=pblt_data.get("Value", ""),
                    lap=parse_int(pblt_data.get("Lap")),
                    position=parse_int(pblt_data.get("Position")),
                )

            # --- Best sectors ---
            best_sectors: List[Stat] = []
            for sector in data.get("BestSectors", []):
                best_sectors.append(
                    Stat(
                        value=sector.get("Value", ""),
                        position=parse_int(sector.get("Position")),
                    )
                )

            # --- Best speeds ---
            best_speeds = None
            bs_data = data.get("BestSpeeds")
            if bs_data:
                best_speeds = BestSpeed(
                    i1=self._parse_stat(bs_data.get("I1")),
                    i2=self._parse_stat(bs_data.get("I2")),
                    fl=self._parse_stat(bs_data.get("FL")),
                    st=self._parse_stat(bs_data.get("ST")),
                )

            # --- Driver stat ---
            lines[num] = DriverStat(
                line=parse_int(data.get("Line")),
                racing_number=parse_int(data.get("RacingNumber")),
                personal_best_lap_time=personal_best_lap_time,
                best_sectors=best_sectors,
                best_speeds=best_speeds,
            )

        return TimingStats(lines=lines)

    # --- Helper conversion methods ---
    @staticmethod
    def _parse_stat(data) -> Stat:
        if not data:
            return Stat(value="", position=0)
        return Stat(value=data.get("Value", ""), position=int(data.get("Position", 0)))
