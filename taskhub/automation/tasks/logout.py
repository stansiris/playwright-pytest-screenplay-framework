from screenplay_core.core.target import Target
from screenplay_core.core.task import Task
from screenplay_core.interactions.click import Click


class LogoutFromTaskHub(Task):
    """Task: log out from TaskHub dashboard."""

    LOGOUT_BUTTON = Target(
        "TaskHub logout button",
        lambda page: page.get_by_role("button", name="Logout"),
    )

    def perform_as(self, actor) -> None:
        self.perform_interactions(actor, Click(self.LOGOUT_BUTTON))
