from screenplay.core.interaction import Interaction
from screenplay.abilities.browse_the_web import BrowseTheWeb


class NavigateTo(Interaction):
    """Interaction: navigate the browser to a URL."""

    def __init__(self, url: str):
        self.url = url

    def perform_as(self, actor):
        page = actor.ability_to(BrowseTheWeb).page
        page.goto(self.url)
