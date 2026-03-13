from examples.saucedemo.ui.pages.checkout_overview_page import CheckoutOverviewPage
from screenplay_core.core.actor import Actor
from screenplay_core.core.task import Task
from screenplay_core.interactions.click import Click


class CompleteCheckout(Task):
    """Task: finish checkout on the overview page."""

    def perform_as(self, actor: Actor) -> None:
        self.perform_interactions(actor, Click(CheckoutOverviewPage.CHECKOUT_FINISH))
