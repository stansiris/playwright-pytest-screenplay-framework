from saucedemo.ui.pages.checkout_info_page import CheckoutInfoPage
from screenplay_core.core.actor import Actor
from screenplay_core.core.task import Task
from screenplay_core.interactions.click import Click


class DismissCheckoutInfoError(Task):
    """Task: dismiss the checkout information error banner."""

    def perform_as(self, actor: Actor) -> None:
        actor.attempts_to(Click(CheckoutInfoPage.CHECKOUT_INFO_ERROR_CLOSE_BUTTON))
