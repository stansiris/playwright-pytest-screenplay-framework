from saucedemo.ui.pages.checkout_info_page import CheckoutInfoPage
from screenplay_core.core.actor import Actor
from screenplay_core.core.task import Task
from screenplay_core.interactions.click import Click


class ContinueCheckout(Task):
    """Task: continue from checkout information to overview."""

    def perform_as(self, actor: Actor) -> None:
        self.perform_interactions(actor, Click(CheckoutInfoPage.CHECKOUT_CONTINUE))
