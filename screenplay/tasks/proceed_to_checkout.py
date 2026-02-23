from screenplay.core.task import Task
from screenplay.interactions.click import Click
from screenplay.ui.saucedemo import SauceDemo


class ProceedToCheckout(Task):
    """Task: continue from cart page to checkout information."""

    def __repr__(self) -> str:
        return "ProceedToCheckout()"

    def perform_as(self, actor) -> None:
        actor.attempts_to(Click(SauceDemo.CHECKOUT_BUTTON))
