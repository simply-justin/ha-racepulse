from typing import Dict
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


@register_parser(LiveTimingEvent.TIMING_STATS)
class TimingStatsParser(EventParser):
    """Parse 'TimingStats' into TimingStats dataclass."""

    def parse(self, raw: "RawTimingEvent") -> TimingStats:
        p = raw.payload
        lines: Dict[str, DriverStat] = {}
        for num, line in p.get("Lines", {}).items():
            personal_best_lap_time: PersonalBestLapTime | None = None
            best_sectors: list[Stat] = []
            best_speeds: BestSpeed | None = None

            if "PersonalBestLapTime" in line:
                PersonalBestLapTime(
                    value=line["PersonalBestLapTime"].get("Value", ""),
                    lap=int(line["PersonalBestLapTime"].get("Lap", 0)),
                    position=int(line["PersonalBestLapTime"].get("Position", 0)),
                )

            if "BestSectors" in line:
                for sector in line["BestSectors"]:
                    best_sectors.append(
                        Stat(
                            value=sector.get("Value", ""),
                            position=int(sector.get("Position", 0)),
                        )
                    )

            if "BestSpeeds" in line:
                best_speeds = {
                    k: Stat(
                        value=stat.get("Value", ""),
                        position=int(stat.get("Position", 0)),
                    )
                    for k, stat in line.get("BestSpeeds", {}).items()
                }

            lines[num] = DriverStat(
                line=int(line.get("Line", 0)),
                racing_number=int(line.get("RacingNumber", 0)),
                personal_best_lap_time=personal_best_lap_time,
                best_sectors=best_sectors,
                best_speeds=best_speeds,
            )

        return TimingStats(lines=lines)
