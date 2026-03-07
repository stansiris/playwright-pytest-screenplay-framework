from saucedemo.ui.pages.inventory_page import InventoryPage
from screenplay_core.core.actor import Actor
from screenplay_core.core.task import Task
from screenplay_core.interactions.click import Click


class OpenProductDetails(Task):
    """Task: open product details page from inventory by product name."""

    def __init__(self, product_name: str):
        self.product_name = product_name

    def __repr__(self) -> str:
        return f"OpenProductDetails(product_name='{self.product_name}')"

    def perform_as(self, actor: Actor) -> None:
        self.perform_interactions(
            actor, Click(InventoryPage.inventory_item_name_for(self.product_name))
        )

    @classmethod
    def named(cls, product_name: str) -> "OpenProductDetails":
        return cls(product_name)
