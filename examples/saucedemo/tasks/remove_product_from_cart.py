from examples.saucedemo.ui.pages.inventory_page import InventoryPage
from screenplay_core.core.actor import Actor
from screenplay_core.core.task import Task
from screenplay_core.playwright.interactions.click import Click


class RemoveProductFromCart(Task):
    """Task: remove a product from cart by product name on inventory page."""

    def __init__(self, product_name: str):
        self.product_name = product_name

    def __repr__(self) -> str:
        return f"RemoveProductFromCart(product_name='{self.product_name}')"

    def perform_as(self, actor: Actor) -> None:
        self.perform_interactions(
            actor, Click(InventoryPage.inventory_item_action_button_for(self.product_name))
        )

    @classmethod
    def named(cls, product_name: str) -> "RemoveProductFromCart":
        return cls(product_name)
