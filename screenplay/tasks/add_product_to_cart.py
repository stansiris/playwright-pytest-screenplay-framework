from screenplay.core.task import Task
from screenplay.interactions.click import Click
from screenplay.ui.saucedemo import SauceDemo


class AddProductToCart(Task):
    """Task: add a product to the cart by product name."""

    def __init__(self, product_name: str):
        self.product_name = product_name

    def __repr__(self) -> str:
        return f"AddProductToCart(product_name='{self.product_name}')"

    def perform_as(self, actor) -> None:
        actor.attempts_to(Click(SauceDemo.add_to_cart_button_for(self.product_name)))

    @staticmethod
    def named(product_name: str) -> "AddProductToCart":
        return AddProductToCart(product_name)
