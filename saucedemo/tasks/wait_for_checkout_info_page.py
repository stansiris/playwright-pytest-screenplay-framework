from saucedemo.ui.pages.checkout_info_page import CheckoutInfoPage
from screenplay_core.core.actor import Actor
from screenplay_core.core.task import Task
from screenplay_core.interactions.wait_until_visible import WaitUntilVisible


class WaitForCheckoutInfoPage(Task):
    """Task: wait for checkout information page form to be visible."""

    def perform_as(self, actor: Actor) -> None:
        actor.attempts_to(WaitUntilVisible.for_(CheckoutInfoPage.CHECKOUT_FIRST_NAME))
