from screenplay_core.core.actor import Actor
from screenplay_core.core.interaction import Interaction
from screenplay_core.playwright.target import Target


class Focus(Interaction):
    """Interaction: move focus to the provided target element."""

    def __init__(self, target: Target):
        """Store the target that should receive focus."""
        self.target = target

    def __repr__(self) -> str:
        """Return a concise representation with target description."""
        return f"Focus(target='{self.target.description}')"

    def perform_as(self, actor: Actor) -> None:
        """Resolve the target and move browser focus to it."""
        self.target.resolve_for(actor).focus()
