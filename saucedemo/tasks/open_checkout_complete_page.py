from screenplay_core.abilities.browse_the_web import BrowseTheWeb
from screenplay_core.core.actor import Actor
from screenplay_core.core.task import Task
from screenplay_core.interactions.navigate_to import NavigateTo


class OpenCheckoutCompletePage(Task):
    """Task: open checkout complete page directly by URL."""

    def perform_as(self, actor: Actor) -> None:
        base_url = actor.ability_to(BrowseTheWeb).base_url
        if not base_url:
            raise ValueError(
                "BrowseTheWeb ability must include a base_url to open checkout complete page."
            )
        self.perform_interactions(actor, NavigateTo(f"{base_url}checkout-complete.html"))
