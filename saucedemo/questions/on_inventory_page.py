from urllib.parse import urlparse

from saucedemo.ui.pages.inventory_page import InventoryPage
from screenplay_core.abilities.browse_the_web import BrowseTheWeb
from screenplay_core.core.actor import Actor
from screenplay_core.core.question import Question


class OnInventoryPage(Question):
    """Question: whether the browser is currently on the inventory page."""

    def answered_by(self, actor: Actor) -> bool:
        page = actor.ability_to(BrowseTheWeb).page
        path = urlparse(page.url).path.rstrip("/")
        on_inventory_path = path.endswith("/inventory.html")
        inventory_visible = InventoryPage.INVENTORY_CONTAINER.resolve_for(actor).is_visible()
        return on_inventory_path and inventory_visible

    def __repr__(self) -> str:
        return "OnInventoryPage()"
