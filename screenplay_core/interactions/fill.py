from screenplay_core.core.interaction import Interaction
from screenplay_core.core.target import Target
from screenplay_core.core.actor import Actor


class Fill(Interaction):
    """Interaction: fill an input field identified by a Target."""

    def __init__(self, target: Target, text: str):
        self.target = target
        self.text = text

    def __repr__(self) -> str:
        safe_text = self._masked_text()
        return f"Fill(target='{self.target.description}', text='{safe_text}')"

    def _masked_text(self) -> str:
        # Mask if likely password field
        if "password" in self.target.description.lower():
            return "*" * len(self.text)
        return self.text

    def perform_as(self, actor: Actor):
        self.target.resolve_for(actor).fill(self.text)
