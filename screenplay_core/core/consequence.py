from abc import ABC, abstractmethod


class Consequence(ABC):
    @abstractmethod
    def check_as(self, actor) -> None:
        """Assert an expected outcome as the given actor."""
