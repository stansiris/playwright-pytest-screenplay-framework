from saucedemo.ui.saucedemo import SauceDemo
from screenplay_core.core.task import Task
from screenplay_core.interactions.click import Click


class ProceedToCheckout(Task):
    """Task: continue from cart page to checkout information."""

    def perform_as(self, actor) -> None:
        actor.attempts_to(Click(SauceDemo.CHECKOUT_BUTTON))


