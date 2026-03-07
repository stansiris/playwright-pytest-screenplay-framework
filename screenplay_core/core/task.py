from typing import TYPE_CHECKING

from screenplay_core.core.activity import Activity
from screenplay_core.core.interaction import Interaction

if TYPE_CHECKING:
    from screenplay_core.core.actor import Actor


class Task(Activity):
    """Base class for higher-level actions composed of interactions."""

    def perform_interactions(self, actor: "Actor", *interactions: Interaction) -> None:
        actor._attempts_to_interactions(*interactions)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"
