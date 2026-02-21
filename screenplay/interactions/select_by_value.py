from screenplay.core.interaction import Interaction
from screenplay.core.target import Target


class SelectByValue(Interaction):
    """Interaction: select a dropdown option by its `value` attribute."""

    def __init__(self, target: Target, value: str):
        self.target = target
        self.value = value

    def __repr__(self) -> str:
        return f"SelectByValue(target='{self.target.description}', value='{self.value}')"

    def perform_as(self, actor) -> None:
        self.target.resolve_for(actor).select_option(value=self.value)
