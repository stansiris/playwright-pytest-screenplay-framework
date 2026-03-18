from screenplay_core.core.actor import Actor
from screenplay_core.core.interaction import Interaction
from screenplay_core.playwright.target import Target


class Click(Interaction):
    """Interaction: click a target element."""

    def __init__(self, target: Target):
        """Store the target to click at execution time."""
        self.target = target

    def __repr__(self) -> str:
        """Return a concise representation with target description."""
        return f"Click(target='{self.target.description}')"

    def perform_as(self, actor: Actor) -> None:
        """Resolve the target and perform a click action."""
        self.target.resolve_for(actor).click()
