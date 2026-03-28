from examples.work_items.automation.ui.targets import WorkItemsTargets
from screenplay_core.core.task import Task
from screenplay_core.playwright.interactions.click import Click
from screenplay_core.playwright.interactions.fill import Fill


class LoginToWorkItems(Task):
    """Task: authenticate with Work Items credentials."""

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def __repr__(self) -> str:
        return f"LoginToWorkItems(username='{self.username}')"

    def perform_as(self, actor) -> None:
        self.perform_interactions(
            actor,
            Fill(WorkItemsTargets.LOGIN_USERNAME_INPUT, self.username),
            Fill(WorkItemsTargets.LOGIN_PASSWORD_INPUT, self.password),
            Click(WorkItemsTargets.LOGIN_SUBMIT_BUTTON),
        )

    @classmethod
    def with_credentials(cls, username: str, password: str) -> "LoginToWorkItems":
        return cls(username=username, password=password)
