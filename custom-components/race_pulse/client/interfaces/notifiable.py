from abc import abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .observable import Observable


class Notifiable:
    """
    Notifiable subject interface for managing observers.
    """

    @abstractmethod
    def attach(self, observer: "Observable") -> None:
        """Register an observer to receive updates."""
        pass

    @abstractmethod
    def detach(self, observer: "Observable") -> None:
        """Unregister an observer so it no longer receives updates."""
        pass

    @abstractmethod
    def notify(self, message: Any) -> None:
        """Notify all registered observers with a message."""
        pass
