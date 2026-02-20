from screenplay.core.task import Task
from screenplay.interactions.click import Click
from screenplay.ui.saucedemo import SauceDemo


class BeginCheckout(Task):
    """Task: open the cart and start checkout."""

    def __repr__(self) -> str:
        return "BeginCheckout()"

    def perform_as(self, actor) -> None:
        actor.attempts_to(
            Click(SauceDemo.SHOPPING_CART_LINK),
            Click(SauceDemo.CHECKOUT_BUTTON),
        )
