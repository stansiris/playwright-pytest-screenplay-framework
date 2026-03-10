from screenplay_core.core.actor import Actor
from screenplay_core.core.interaction import Interaction
from screenplay_core.core.target import Target


class Fill(Interaction):
    """Interaction: fill an input field identified by a Target."""

    def __init__(self, target: Target, text: str):
        """Store target and text payload for later execution."""
        self.target = target
        self.text = text

    def __repr__(self) -> str:
        """Return a representation with masked text when appropriate."""
        safe_text = self._masked_text()
        return f"Fill(target='{self.target.description}', text='{safe_text}')"

    def _masked_text(self) -> str:
        """Mask values for likely password inputs in logs."""
        # Mask if likely password field
        if "password" in self.target.description.lower():
            return "*" * len(self.text)
        return self.text

    def perform_as(self, actor: Actor) -> None:
        """Resolve the target and fill it with provided text."""
        self.target.resolve_for(actor).fill(self.text)
