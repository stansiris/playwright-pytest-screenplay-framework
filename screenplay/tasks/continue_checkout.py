from screenplay.ui.saucedemo import SauceDemo
from screenplay_core.core.task import Task
from screenplay_core.interactions.click import Click


class ContinueCheckout(Task):
    """Task: continue from checkout information to overview."""

    def perform_as(self, actor) -> None:
        actor.attempts_to(Click(SauceDemo.CHECKOUT_CONTINUE))

