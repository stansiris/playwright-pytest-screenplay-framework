from screenplay.core.task import Task
from screenplay.interactions.click import Click
from screenplay.ui.saucedemo import SauceDemo


class ReturnToProducts(Task):
    """Task: return from checkout complete page to product list."""

    def __repr__(self) -> str:
        return "ReturnToProducts()"

    def perform_as(self, actor) -> None:
        actor.attempts_to(Click(SauceDemo.BACK_TO_PRODUCTS))
