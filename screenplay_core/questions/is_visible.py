from screenplay_core.core.actor import Actor
from screenplay_core.core.question import Question
from screenplay_core.core.target import Target


class IsVisible(Question):
    """Question: is an element visible?"""

    def __init__(self, target: Target):
        """Store the target whose visibility will be checked."""
        self.target = target

    def answered_by(self, actor: Actor) -> bool:
        """Resolve target and return Playwright visibility state."""
        return self.target.resolve_for(actor).is_visible()

    def __repr__(self) -> str:
        """Return a concise representation with target description."""
        return f"IsVisible(target='{self.target.description}')"
