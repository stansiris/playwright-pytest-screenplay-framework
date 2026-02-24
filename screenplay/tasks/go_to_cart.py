from screenplay.ui.saucedemo import SauceDemo
from screenplay_core.core.task import Task
from screenplay_core.interactions.click import Click


class GoToCart(Task):
    """Task: navigate to the cart page."""

    def perform_as(self, actor) -> None:
        actor.attempts_to(Click(SauceDemo.SHOPPING_CART_LINK))

