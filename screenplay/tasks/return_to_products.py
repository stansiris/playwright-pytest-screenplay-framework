from screenplay.ui.saucedemo import SauceDemo
from screenplay_core.core.task import Task
from screenplay_core.interactions.click import Click


class ReturnToProducts(Task):
    """Task: return from checkout complete page to product list."""

    def perform_as(self, actor) -> None:
        actor.attempts_to(Click(SauceDemo.BACK_TO_PRODUCTS))

