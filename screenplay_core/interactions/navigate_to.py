from screenplay_core.abilities.browse_the_web import BrowseTheWeb
from screenplay_core.core.actor import Actor
from screenplay_core.core.interaction import Interaction


class NavigateTo(Interaction):
    """Interaction: navigate the browser to a URL."""

    def __init__(self, url: str):
        self.url = url

    def __repr__(self) -> str:
        return f"NavigateTo(url='{self.url}')"

    def perform_as(self, actor: Actor) -> None:
        page = actor.ability_to(BrowseTheWeb).page
        page.goto(self.url)
