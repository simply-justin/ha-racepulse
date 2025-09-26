from abc import abstractmethod
from . import Notifiable

class Observable:
    """
    The Observer interface declares the update method, which is called by
    subjects (Notifiable) to notify observers of changes.
    """

    @abstractmethod
    def update(self, subject: Notifiable) -> None:
        """
        Receive an update from the subject.

        Args:
            subject (Notifiable): The subject instance sending the update.
        """
        pass