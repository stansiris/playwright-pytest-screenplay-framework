from screenplay.core.interaction import Interaction
from screenplay.abilities.browse_the_web import BrowseTheWeb


class Click(Interaction):
    """Interaction: click an element using a CSS selector."""

    def __init__(self, selector: str):
        self.selector = selector

    def perform_as(self, actor):
        page = actor.ability_to(BrowseTheWeb).page
        page.locator(self.selector).click()
