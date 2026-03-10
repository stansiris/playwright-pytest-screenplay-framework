from saucedemo.ui.components.back_navigation import BackNavigation
from screenplay_core.core.actor import Actor
from screenplay_core.core.task import Task
from screenplay_core.interactions.click import Click


class ReturnToProducts(Task):
    """Task: return from checkout complete page to product list."""

    def perform_as(self, actor: Actor) -> None:
        self.perform_interactions(actor, Click(BackNavigation.BACK_TO_PRODUCTS))
