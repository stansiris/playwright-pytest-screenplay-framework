from screenplay.core.interaction import Interaction
from screenplay.core.target import Target


class Fill(Interaction):
    """Interaction: fill an input using a CSS selector."""

    def __init__(self, target: Target, text: str):
        self.target = target
        self.text = text

    def perform_as(self, actor):
        self.target.resolve_for(actor).fill(self.text)
