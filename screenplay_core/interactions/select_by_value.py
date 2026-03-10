from screenplay_core.core.actor import Actor
from screenplay_core.core.interaction import Interaction
from screenplay_core.core.target import Target


class SelectByValue(Interaction):
    """Interaction: select a dropdown option by its `value` attribute."""

    def __init__(self, target: Target, value: str):
        """Store target select element and option value to choose."""
        self.target = target
        self.value = value

    def __repr__(self) -> str:
        """Return a concise representation with target and value."""
        return f"SelectByValue(target='{self.target.description}', value='{self.value}')"

    def perform_as(self, actor: Actor) -> None:
        """Resolve target and select the configured option value."""
        self.target.resolve_for(actor).select_option(value=self.value)
