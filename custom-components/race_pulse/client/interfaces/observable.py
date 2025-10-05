from __future__ import annotations
from typing import TYPE_CHECKING, Protocol, TypeVar, Generic

if TYPE_CHECKING:
    from .notifiable import Notifiable

T = TypeVar("T")


class Observable(Protocol, Generic[T]):
    """
    Observer interface for receiving updates from subjects.

    This defines the "Observer" side of the Observer pattern.
    Classes implementing this interface can be attached to
    a `Notifiable` subject and will receive updates when
    the subject's state changes.

    Example:
        class Dashboard(Observable[str]):
            def update(self, subject: Notifiable[str], message: str) -> None:
                print(f"Dashboard received: {message}")
    """

    def update(self, subject: Notifiable[T], message: T) -> None:
        """
        Called by the subject when notifying observers.

        Args:
            subject: The subject sending the update.
            message: The event or telemetry payload being sent.
        """
        pass
