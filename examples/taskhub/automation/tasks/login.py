from examples.taskhub.automation.ui.targets import TaskHubTargets
from screenplay_core.core.task import Task
from screenplay_core.playwright.interactions.click import Click
from screenplay_core.playwright.interactions.fill import Fill


class LoginToTaskHub(Task):
    """Task: authenticate with TaskHub credentials."""

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def __repr__(self) -> str:
        return f"LoginToTaskHub(username='{self.username}')"

    def perform_as(self, actor) -> None:
        self.perform_interactions(
            actor,
            Fill(TaskHubTargets.LOGIN_USERNAME_INPUT, self.username),
            Fill(TaskHubTargets.LOGIN_PASSWORD_INPUT, self.password),
            Click(TaskHubTargets.LOGIN_SUBMIT_BUTTON),
        )

    @classmethod
    def with_credentials(cls, username: str, password: str) -> "LoginToTaskHub":
        return cls(username=username, password=password)
