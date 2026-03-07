from saucedemo.ui.pages.checkout_complete_page import CheckoutCompletePage
from screenplay_core.core.actor import Actor
from screenplay_core.core.task import Task
from screenplay_core.interactions.wait_until_visible import WaitUntilVisible


class WaitForCheckoutCompletePage(Task):
    """Task: wait for checkout complete confirmation page to be visible."""

    def perform_as(self, actor: Actor) -> None:
        self.perform_interactions(
            actor, WaitUntilVisible.for_(CheckoutCompletePage.CHECKOUT_COMPLETE_TITLE)
        )
