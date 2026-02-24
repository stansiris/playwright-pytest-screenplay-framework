from saucedemo.tasks.go_to_cart import GoToCart
from saucedemo.tasks.proceed_to_checkout import ProceedToCheckout
from screenplay_core.core.task import Task


class BeginCheckout(Task):
    """Task: open the cart and start checkout."""

    def perform_as(self, actor) -> None:
        actor.attempts_to(
            GoToCart(),
            ProceedToCheckout(),
        )


