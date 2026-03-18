from screenplay_core.core.actor import Actor
from screenplay_core.core.interaction import Interaction
from screenplay_core.playwright.browse_the_web import BrowseTheWeb


class PressKey(Interaction):
    """Interaction: press a keyboard key or key chord."""

    def __init__(self, key: str):
        """Store key expression for keyboard press."""
        self.key = key

    def __repr__(self) -> str:
        """Return a concise representation with key expression."""
        return f"PressKey(key='{self.key}')"

    def perform_as(self, actor: Actor) -> None:
        """Use BrowseTheWeb ability keyboard to press the configured key."""
        page = actor.ability_to(BrowseTheWeb).page
        page.keyboard.press(self.key)
