from abc import abstractmethod
from . import Observer

class Notifiable:
    """
    Observer interface for receiving telemetry updates.

    Classes that implement this interface can register, remove,
    and notify observers about state changes or telemetry updates.
    """

    @abstractmethod
    def attach(self, observer: Observer)-> None:
        """
        Register an observer to receive updates.

        Args:
            observer (Observer): The observer instance to attach.
        """
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        """
        Unregister an observer so it no longer receives updates.

        Args:
            observer (Observer): The observer instance to detach.
        """
        pass

    @abstractmethod
    def notify(self) -> None:
        """
        Notify all registered observers about a state change or telemetry update.
        """
        pass