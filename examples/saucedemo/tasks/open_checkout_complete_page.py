from screenplay_core.core.actor import Actor
from screenplay_core.core.task import Task
from screenplay_core.interactions.navigate_to import NavigateTo


class OpenCheckoutCompletePage(Task):
    """Task: open checkout complete page directly by URL."""

    def perform_as(self, actor: Actor) -> None:
        self.perform_interactions(actor, NavigateTo("/checkout-complete.html"))
