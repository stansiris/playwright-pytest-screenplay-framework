from screenplay.core.task import Task
from screenplay.interactions.click import Click
from screenplay.ui.saucedemo import SauceDemo


class CompleteCheckout(Task):
    """Task: finish checkout on the overview page."""

    def __repr__(self) -> str:
        return "CompleteCheckout()"

    def perform_as(self, actor) -> None:
        actor.attempts_to(Click(SauceDemo.CHECKOUT_FINISH))
