from screenplay.core.target import Target
from screenplay.core.task import Task
from screenplay.interactions.click import Click
from screenplay.ui.saucedemo import SauceDemo


class AddProductToCart(Task):
    """Task: add a product to the cart."""

    def __init__(self, add_to_cart_button: Target):
        self.add_to_cart_button = add_to_cart_button

    def __repr__(self) -> str:
        return f"AddProductToCart(product='{self.add_to_cart_button.description}')"

    def perform_as(self, actor) -> None:
        actor.attempts_to(Click(self.add_to_cart_button))

    @staticmethod
    def red_t_shirt() -> "AddProductToCart":
        return AddProductToCart(SauceDemo.ADD_TO_CART_RED_TSHIRT)
