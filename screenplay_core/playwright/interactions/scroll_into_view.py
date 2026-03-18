from screenplay_core.core.actor import Actor
from screenplay_core.core.interaction import Interaction
from screenplay_core.playwright.target import Target


class ScrollIntoView(Interaction):
    """Interaction: ensure a target element is scrolled into the viewport."""

    def __init__(self, target: Target):
        """Store target to scroll into viewport."""
        self.target = target

    def __repr__(self) -> str:
        """Return a concise representation with target description."""
        return f"ScrollIntoView(target='{self.target.description}')"

    def perform_as(self, actor: Actor) -> None:
        """Resolve target and scroll it into view if needed."""
        self.target.resolve_for(actor).scroll_into_view_if_needed()
