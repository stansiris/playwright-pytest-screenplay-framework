from screenplay.core.interaction import Interaction
from screenplay.core.target import Target


class ScrollIntoView(Interaction):
    """Interaction: ensure a target element is scrolled into the viewport."""

    def __init__(self, target: Target):
        self.target = target

    def __repr__(self) -> str:
        return f"ScrollIntoView(target='{self.target.description}')"

    def perform_as(self, actor) -> None:
        self.target.resolve_for(actor).scroll_into_view_if_needed()
