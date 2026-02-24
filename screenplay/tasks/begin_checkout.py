from screenplay.core.task import Task
from screenplay.tasks.go_to_cart import GoToCart
from screenplay.tasks.proceed_to_checkout import ProceedToCheckout


class BeginCheckout(Task):
    """Task: open the cart and start checkout."""

    def perform_as(self, actor) -> None:
        actor.attempts_to(
            GoToCart(),
            ProceedToCheckout(),
        )
