from screenplay.core.task import Task
from screenplay.interactions.fill import Fill
from screenplay.ui.saucedemo import SauceDemo


class EnterUsername(Task):
    """Task: enter text in the username field."""

    def __init__(self, username: str):
        self.username = username

    def __repr__(self) -> str:
        return f"EnterUsername(username='{self.username}')"

    def perform_as(self, actor) -> None:
        actor.attempts_to(Fill(SauceDemo.LOGIN_USERNAME, self.username))

    @staticmethod
    def as_(username: str) -> "EnterUsername":
        return EnterUsername(username)
