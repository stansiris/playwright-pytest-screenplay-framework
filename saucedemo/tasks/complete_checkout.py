from saucedemo.ui.saucedemo import SauceDemo
from screenplay_core.core.actor import Actor
from screenplay_core.core.task import Task
from screenplay_core.interactions.click import Click


class CompleteCheckout(Task):
    """Task: finish checkout on the overview page."""

    def perform_as(self, actor: Actor) -> None:
        actor.attempts_to(Click(SauceDemo.CHECKOUT_FINISH))
