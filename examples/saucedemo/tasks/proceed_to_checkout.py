from examples.saucedemo.ui.pages.cart_page import CartPage
from screenplay_core.core.actor import Actor
from screenplay_core.core.task import Task
from screenplay_core.playwright.interactions.click import Click


class ProceedToCheckout(Task):
    """Task: continue from cart page to checkout information."""

    def perform_as(self, actor: Actor) -> None:
        self.perform_interactions(actor, Click(CartPage.CHECKOUT_BUTTON))
