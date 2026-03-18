from screenplay_core.core.actor import Actor
from screenplay_core.core.task import Task
from screenplay_core.playwright.interactions.navigate_to import NavigateTo


class OpenTaskHub(Task):
    """Task: open TaskHub root URL from BrowseTheWeb base_url."""

    def perform_as(self, actor: Actor) -> None:
        self.perform_interactions(actor, NavigateTo("/login"))

    @classmethod
    def app(cls) -> "OpenTaskHub":
        return cls()
