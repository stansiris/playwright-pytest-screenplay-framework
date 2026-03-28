from examples.work_items.automation.ui.targets import WorkItemsTargets
from screenplay_core.core.task import Task
from screenplay_core.playwright.interactions.click import Click


class LogoutFromWorkItems(Task):
    """Task: log out from the Work Items dashboard."""

    def perform_as(self, actor) -> None:
        self.perform_interactions(actor, Click(WorkItemsTargets.LOGOUT_BUTTON))
