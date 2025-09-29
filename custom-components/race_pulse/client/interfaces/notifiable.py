from abc import abstractmethod
from typing import Any
from .observable import Observer

class Notifiable:
    """
    Notifiable subject interface for managing observers.
    """

    @abstractmethod
    def attach(self, observer: Observer) -> None:
        """Register an observer to receive updates."""
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        """Unregister an observer so it no longer receives updates."""
        pass

    @abstractmethod
    def notify(self, message: Any) -> None:
        """Notify all registered observers with a message."""
        pass