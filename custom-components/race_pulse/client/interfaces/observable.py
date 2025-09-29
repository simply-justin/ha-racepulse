from abc import abstractmethod
from typing import Protocol, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .notifiable import Notifiable

class Observable(Protocol):
    """
    Observer interface for receiving updates from subjects.
    """

    @abstractmethod
    def update(self, subject: "Notifiable", message: Any) -> None:
        """
        Receive an update from the subject.

        Args:
            subject: The subject sending the update.
            message: The event or telemetry payload.
        """
        pass