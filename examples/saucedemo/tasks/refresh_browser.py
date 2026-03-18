from screenplay_core.core.actor import Actor
from screenplay_core.core.task import Task
from screenplay_core.playwright.interactions.refresh_page import RefreshPage


class RefreshBrowser(Task):
    """Task: refresh the current browser page."""

    def perform_as(self, actor: Actor) -> None:
        self.perform_interactions(actor, RefreshPage())
