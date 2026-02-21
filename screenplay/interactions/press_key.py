from screenplay.abilities.browse_the_web import BrowseTheWeb
from screenplay.core.interaction import Interaction


class PressKey(Interaction):
    """Interaction: press a keyboard key or key chord."""

    def __init__(self, key: str):
        self.key = key

    def __repr__(self) -> str:
        return f"PressKey(key='{self.key}')"

    def perform_as(self, actor) -> None:
        page = actor.ability_to(BrowseTheWeb).page
        page.keyboard.press(self.key)
