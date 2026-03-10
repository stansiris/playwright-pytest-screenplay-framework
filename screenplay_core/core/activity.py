from abc import ABC, abstractmethod


class Activity(ABC):
    """Executable unit in Screenplay, performed by an actor."""

    @abstractmethod
    def perform_as(self, actor) -> None:
        """Execute this activity as the given actor."""
