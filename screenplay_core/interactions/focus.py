from screenplay_core.core.actor import Actor
from screenplay_core.core.interaction import Interaction
from screenplay_core.core.target import Target


class Focus(Interaction):
    """Interaction: move focus to the provided target element."""

    def __init__(self, target: Target):
        self.target = target

    def __repr__(self) -> str:
        return f"Focus(target='{self.target.description}')"

    def perform_as(self, actor: Actor) -> None:
        self.target.resolve_for(actor).focus()
