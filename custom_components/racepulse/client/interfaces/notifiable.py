from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .observable import Observable
    from .event import Event


class Notifiable(ABC):
    """
    Abstract base class representing a subject that can notify observers.

    Implements the "Subject" side of the Observer pattern.

    Classes inheriting from this interface should maintain a collection of
    observers and call `notify()` when the internal state changes.

    Observers must implement the `Observable` interface, which defines
    how they respond to updates.

    Example:
        class WeatherStation(Notifiable):
            def __init__(self):
                self._observers = set()

            def attach(self, observer: Observable) -> None:
                self._observers.add(observer)

            def detach(self, observer: Observable) -> None:
                self._observers.discard(observer)

            def notify(self, message: Event) -> None:
                for obs in self._observers:
                    obs.update(message)
    """

    @abstractmethod
    def attach(self, observer: Observable) -> None:
        """Register an observer to receive updates."""
        raise NotImplementedError

    @abstractmethod
    def detach(self, observer: Observable) -> None:
        """Unregister an observer so it no longer receives updates."""
        raise NotImplementedError

    @abstractmethod
    def notify(self, message: Event) -> None:
        """Notify all registered observers with a message."""
        raise NotImplementedError
