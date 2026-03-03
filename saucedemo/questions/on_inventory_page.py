from screenplay_core.abilities.browse_the_web import BrowseTheWeb
from screenplay_core.core.actor import Actor
from screenplay_core.core.question import Question


class OnInventoryPage(Question):
    """Question: whether the browser is currently on the inventory page."""

    def answered_by(self, actor: Actor) -> bool:
        return "inventory.html" in actor.ability_to(BrowseTheWeb).page.url

    def __repr__(self) -> str:
        return "OnInventoryPage()"
