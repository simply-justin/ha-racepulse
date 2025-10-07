"""Decorator definitions for the RacePulse F1 client."""

from .event import register_event, _EVENT_REGISTRY
from .parser import register_parser, _PARSER_REGISTRY

__all__ = ["register_event", "register_parser", "_EVENT_REGISTRY", "_PARSER_REGISTRY"]
