from screenplay.abilities.browse_the_web import BrowseTheWeb


class IsVisible:
    """Question: is a selector visible?"""

    def __init__(self, selector: str):
        self.selector = selector

    def answered_by(self, actor):
        page = actor.ability_to(BrowseTheWeb).page
        return page.locator(self.selector).is_visible()
