from saucedemo.ui.pages.inventory_page import InventoryPage
from screenplay_core.core.actor import Actor
from screenplay_core.core.question import Question


class InventoryCount(Question):
    def answered_by(self, actor: Actor) -> int:
        return InventoryPage.INVENTORY_ITEM_NAMES.resolve_for(actor).count()

    def __repr__(self) -> str:
        return "InventoryCount()"
