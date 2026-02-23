from screenplay.core.task import Task
from screenplay.interactions.click import Click
from screenplay.ui.saucedemo import SauceDemo


class GoToCart(Task):
    """Task: navigate to the cart page."""

    def __repr__(self) -> str:
        return "GoToCart()"

    def perform_as(self, actor) -> None:
        actor.attempts_to(Click(SauceDemo.SHOPPING_CART_LINK))
