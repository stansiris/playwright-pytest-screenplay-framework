from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from screenplay_core.core.actor import Actor

class Question(ABC):
    """Base class for queries about the system under test."""

    @abstractmethod
    def answered_by(self, actor: "Actor"):
        """Return an answer computed by the given actor."""
