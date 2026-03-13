from examples.taskhub.automation.ui.targets import TaskHubTargets
from screenplay_core.core.task import Task
from screenplay_core.interactions.click import Click


class LogoutFromTaskHub(Task):
    """Task: log out from TaskHub dashboard."""

    def perform_as(self, actor) -> None:
        self.perform_interactions(actor, Click(TaskHubTargets.LOGOUT_BUTTON))
