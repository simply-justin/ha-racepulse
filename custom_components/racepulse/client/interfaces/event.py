from abc import ABC, abstractmethod
from ..enums import LiveTimingEvent


class Event(ABC):
    """
    Abstract base class for all parsed Formula 1 live timing events.

    Each subclass (e.g., `WeatherData`, `DriverList`, `TimingData`)
    represents a specific SignalR event type emitted by the F1 live timing API.

    Every event must declare its corresponding `LiveTimingEvent` type
    via the `data_type` attribute and encapsulate structured, parsed data.
    """

    @property
    @abstractmethod
    def data_type(self) -> LiveTimingEvent:
        """
        The event type identifier corresponding to this model.
        Example: `LiveTimingEvent.WEATHER_DATA`.
        """
        raise NotImplementedError

    def __repr__(self) -> str:
        """Return a readable summary for logging/debugging."""
        return f"<{self.__class__.__name__}(data_type={self.data_type})>"
