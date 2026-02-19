from collections.abc import Callable

from playwright.sync_api import Locator, Page

from screenplay.abilities.browse_the_web import BrowseTheWeb


class Target:
    """
    Represents a UI element.

    Encapsulates how to locate an element for an Actor.
    """

    def __init__(self, description: str, locator_function: Callable[[Page], Locator]):
        self.description = description
        self.locator_function = locator_function

    def resolve_for(self, actor) -> Locator:
        page = actor.ability_to(BrowseTheWeb).page
        return self.locator_function(page)

    def __repr__(self) -> str:
        return f"Target(description='{self.description}')"
