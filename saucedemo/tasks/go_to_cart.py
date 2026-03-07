from saucedemo.ui.components.app_shell import AppShell
from screenplay_core.core.actor import Actor
from screenplay_core.core.task import Task
from screenplay_core.interactions.click import Click


class GoToCart(Task):
    """Task: navigate to the cart page."""

    def perform_as(self, actor: Actor) -> None:
        self.perform_interactions(actor, Click(AppShell.SHOPPING_CART_LINK))
