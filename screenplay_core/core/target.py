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
        """Create a named locator recipe resolved later in actor context."""
        self.description = description
        self.locator_function = locator_function

    def resolve_for(self, actor: "Actor") -> Locator:
        """Resolve the target to a Playwright Locator using actor ability context."""
        page = actor.ability_to(BrowseTheWeb).page
        return self.locator_function(page)

    def __repr__(self) -> str:
        """Return a human-readable representation for logs and debugging."""
        return f"Target(description='{self.description}')"
