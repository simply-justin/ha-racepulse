from abc import ABC, abstractmethod
from typing import Any, Dict


class Event(ABC):
    """Strategy interface: raw dict → typed dataclass."""
