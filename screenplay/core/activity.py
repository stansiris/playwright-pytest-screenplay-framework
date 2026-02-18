from abc import ABC, abstractmethod

class Activity(ABC):
    @abstractmethod
    def perform_as(self, actor) -> None:
        """Execute this activity as the given actor."""