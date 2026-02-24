from screenplay.core.task import Task
from screenplay.interactions.click import Click
from screenplay.ui.saucedemo import SauceDemo


class ContinueCheckout(Task):
    """Task: continue from checkout information to overview."""

    def perform_as(self, actor) -> None:
        actor.attempts_to(Click(SauceDemo.CHECKOUT_CONTINUE))
