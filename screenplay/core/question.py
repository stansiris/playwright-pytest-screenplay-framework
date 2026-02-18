from abc import ABC, abstractmethod

class Question(ABC):
    """Base class for queries about the system under test."""

    @abstractmethod
    def answered_by(self, actor):
        """Return an answer computed by the given actor."""
