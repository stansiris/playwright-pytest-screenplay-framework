from screenplay.abilities.browse_the_web import BrowseTheWeb


class Fill:
    """Interaction: fill an input using a CSS selector."""

    def __init__(self, selector: str, text: str):
        self.selector = selector
        self.text = text

    def perform_as(self, actor):
        page = actor.ability_to(BrowseTheWeb).page
        page.locator(self.selector).fill(self.text)
