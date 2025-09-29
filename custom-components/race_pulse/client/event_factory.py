from typing import Any
from .interfaces import EventParser
from .models import RawTimingEvent
from .parsers import (
    CarParser,
    ChampionshipPredictionParser,
    DriverListParser,
    ExtrapolatedClockParser,
    HeartbeatParser,
    LapCountParser,
    PitLaneTimeCollectionParser,
    PitStopSeriesParser,
    PositionParser,
    RaceControlMessagesParser,
    SessionInfoParser,
    TeamRadioParser,
    TimingAppParser,
    TimingStatsParser,
    TimingParser,
    TrackStatusParser,
    WeatherParser,
)

PARSERS: list[EventParser] = [
    CarParser(),
    ChampionshipPredictionParser(),
    DriverListParser(),
    ExtrapolatedClockParser(),
    HeartbeatParser(),
    LapCountParser(),
    PitLaneTimeCollectionParser(),
    PitStopSeriesParser(),
    PositionParser(),
    RaceControlMessagesParser(),
    SessionInfoParser(),
    TeamRadioParser(),
    TimingAppParser(),
    TimingStatsParser(),
    TimingParser(),
    TrackStatusParser(),
    WeatherParser(),
]


class EventFactory:
    """Factory to convert raw events into typed dataclasses."""

    @staticmethod
    def parse(raw: dict[str, Any]) -> object:
        event_type = raw.get("Type")
        for parser in PARSERS:
            if parser.supports(event_type):
                return parser.parse(raw)

        return RawTimingEvent(
            event_type=event_type,
            payload=raw.get("Json"),
            timestamp_utc=raw.get("DateTime"),
        )
