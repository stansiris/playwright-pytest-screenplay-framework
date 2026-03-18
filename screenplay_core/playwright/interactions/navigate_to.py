from screenplay_core.playwright.browse_the_web import BrowseTheWeb
from screenplay_core.core.actor import Actor
from screenplay_core.core.interaction import Interaction


class NavigateTo(Interaction):
    """Interaction: navigate the browser to a URL."""

    def __init__(self, url: str):
        """Store destination URL."""
        self.url = url

    def __repr__(self) -> str:
        """Return a concise representation with destination URL."""
        return f"NavigateTo(url='{self.url}')"

    def perform_as(self, actor: Actor) -> None:
        """Use BrowseTheWeb ability page to navigate to the configured URL."""
        page = actor.ability_to(BrowseTheWeb).page
        page.goto(self.url)
