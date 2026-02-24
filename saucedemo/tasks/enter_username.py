from saucedemo.ui.saucedemo import SauceDemo
from screenplay_core.core.task import Task
from screenplay_core.interactions.fill import Fill


class EnterUsername(Task):
    """Task: enter text in the username field."""

    def __init__(self, username: str):
        self.username = username

    def __repr__(self) -> str:
        return f"EnterUsername(username='{self.username}')"

    def perform_as(self, actor) -> None:
        actor.attempts_to(Fill(SauceDemo.LOGIN_USERNAME, self.username))

    @classmethod
    def as_(cls, username: str) -> "EnterUsername":
        return cls(username)


