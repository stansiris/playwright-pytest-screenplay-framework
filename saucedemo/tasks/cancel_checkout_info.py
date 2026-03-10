from saucedemo.ui.pages.checkout_info_page import CheckoutInfoPage
from screenplay_core.core.actor import Actor
from screenplay_core.core.task import Task
from screenplay_core.interactions.click import Click


class CancelCheckoutInfo(Task):
    """Task: cancel from checkout information page back to cart."""

    def perform_as(self, actor: Actor) -> None:
        self.perform_interactions(actor, Click(CheckoutInfoPage.CHECKOUT_INFO_CANCEL_BUTTON))
