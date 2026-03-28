from screenplay_core.core.actor import Actor
from screenplay_core.core.task import Task
from screenplay_core.playwright.interactions.navigate_to import NavigateTo


class OpenWorkItems(Task):
    """Task: open the Work Items root URL from BrowseTheWeb base_url."""

    def perform_as(self, actor: Actor) -> None:
        self.perform_interactions(actor, NavigateTo("/login"))

    @classmethod
    def app(cls) -> "OpenWorkItems":
        return cls()
