from collections.abc import Callable
from typing import TYPE_CHECKING

from playwright.sync_api import Locator, Page

from screenplay_core.abilities.browse_the_web import BrowseTheWeb

if TYPE_CHECKING:
    from screenplay_core.core.actor import Actor


class Target:
    """
    Represents a UI element.

    Encapsulates how to locate an element for an Actor.
    """

    def __init__(self, description: str, locator_function: Callable[[Page], Locator]):
        self.description = description
        self.locator_function = locator_function

    def resolve_for(self, actor: "Actor") -> Locator:
        page = actor.ability_to(BrowseTheWeb).page
        return self.locator_function(page)

    def __repr__(self) -> str:
        return f"Target(description='{self.description}')"
