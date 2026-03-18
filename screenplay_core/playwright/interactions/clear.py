from screenplay_core.core.actor import Actor
from screenplay_core.core.interaction import Interaction
from screenplay_core.playwright.target import Target


class Clear(Interaction):
    """Interaction: clear the text value from an input field."""

    def __init__(self, target: Target):
        """Store the target input element to clear."""
        self.target = target

    def __repr__(self) -> str:
        """Return a concise representation with target description."""
        return f"Clear(target='{self.target.description}')"

    def perform_as(self, actor: Actor) -> None:
        """Resolve the target and clear its value."""
        # `fill("")` is stable across Playwright versions and input types.
        self.target.resolve_for(actor).fill("")
