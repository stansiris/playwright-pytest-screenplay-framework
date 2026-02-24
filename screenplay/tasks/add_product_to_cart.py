from screenplay.ui.saucedemo import SauceDemo
from screenplay_core.core.task import Task
from screenplay_core.interactions.click import Click


class AddProductToCart(Task):
    """Task: add a product to the cart by product name."""

    def __init__(self, product_name: str):
        self.product_name = product_name

    def __repr__(self) -> str:
        return f"AddProductToCart(product_name='{self.product_name}')"

    def perform_as(self, actor) -> None:
        actor.attempts_to(Click(SauceDemo.add_to_cart_button_for(self.product_name)))

    @classmethod
    def named(cls, product_name: str) -> "AddProductToCart":
        return cls(product_name)

