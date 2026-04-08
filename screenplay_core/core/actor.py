from typing import TypeVar

from screenplay_core.core.activity import Activity
from screenplay_core.core.consequence import Consequence
from screenplay_core.core.interaction import Interaction
from screenplay_core.core.question import Question
from screenplay_core.core.task import Task
from screenplay_core.lifecycle.decorators import log_screenplay_step

T = TypeVar("T")


class AmbiguousAbilityError(Exception):
    """Raised when a base-contract lookup matches multiple registered abilities."""


class Actor:
    """Screenplay actor that executes activities and asks questions."""

    def __init__(self, name: str):
        """Create an actor with a display name and empty ability registry."""
        self.name = name
        self._abilities = {}

    def can(self, ability) -> "Actor":
        """Register an ability instance and return self for fluent setup."""
        self._abilities[ability.__class__] = ability
        return self

    def ability_to(self, ability_class: type[T]) -> T:
        """Resolve a previously registered ability by class or base class."""
        # Fast path: exact ability class lookup.
        if ability_class in self._abilities:
            return self._abilities[ability_class]

        # Fallback: resolve by base class/interface contract.
        matches = [
            ability for ability in self._abilities.values() if isinstance(ability, ability_class)
        ]
        if len(matches) == 1:
            return matches[0]

        if len(matches) > 1:
            # Explicit disambiguation keeps lookup deterministic.
            # Without this check, result depends on registration order.
            matched_types = ", ".join(sorted({ability.__class__.__name__ for ability in matches}))
            raise AmbiguousAbilityError(
                f"{self.name} has multiple abilities compatible with {ability_class.__name__}: "
                f"{matched_types}. Request a more specific ability class."
            )

        raise Exception(f"{self.name} does not have ability {ability_class.__name__}.")

    # @log_screenplay_step
    def attempts_to(self, *activities: Task | Consequence) -> None:
        """Execute Task/Consequence activities in order."""
        for activity in activities:
            if isinstance(activity, Interaction):
                raise TypeError(
                    f"{self.name}.attempts_to() accepts Task/Consequence only; "
                    f"got Interaction '{activity.__class__.__name__}'. "
                    "Wrap low-level interactions inside a Task."
                )
            if not isinstance(activity, (Task, Consequence)):
                raise TypeError(
                    f"{self.name}.attempts_to() accepts Task/Consequence only; "
                    f"got {activity.__class__.__name__}."
                )
            self._perform_activity(activity)

    def _attempts_to_interactions(self, *interactions: Interaction) -> None:
        """Internal helper for Task composition of low-level interactions."""
        for interaction in interactions:
            if not isinstance(interaction, Interaction):
                raise TypeError(
                    f"{self.name}._attempts_to_interactions() accepts Interaction only; "
                    f"got {interaction.__class__.__name__}."
                )
            self._perform_activity(interaction)

    @log_screenplay_step
    def asks_for(self, question: Question):
        """Execute a question and return its answer."""
        return question.answered_by(self)

    @log_screenplay_step
    def _perform_activity(self, activity: Activity) -> None:
        """Run a single activity."""
        activity.perform_as(self)
