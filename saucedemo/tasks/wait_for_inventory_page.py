from saucedemo.ui.pages.inventory_page import InventoryPage
from screenplay_core.core.actor import Actor
from screenplay_core.core.task import Task
from screenplay_core.interactions.wait_until_visible import WaitUntilVisible


class WaitForInventoryPage(Task):
    """Task: wait for the inventory page container to be visible."""

    def perform_as(self, actor: Actor) -> None:
        self.perform_interactions(actor, WaitUntilVisible.for_(InventoryPage.INVENTORY_CONTAINER))
