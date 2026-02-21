from screenplay.core.interaction import Interaction
from screenplay.core.target import Target


class Clear(Interaction):
    """Interaction: clear the text value from an input field."""

    def __init__(self, target: Target):
        self.target = target

    def __repr__(self) -> str:
        return f"Clear(target='{self.target.description}')"

    def perform_as(self, actor) -> None:
        # `fill("")` is stable across Playwright versions and input types.
        self.target.resolve_for(actor).fill("")
