from saucedemo.ui.saucedemo import SauceDemo
from screenplay_core.core.task import Task
from screenplay_core.interactions.fill import Fill


class EnterPassword(Task):
    """Task: enter text in the password field."""

    def __init__(self, password: str):
        self.password = password

    def __repr__(self) -> str:
        return "EnterPassword(password='***')"

    def perform_as(self, actor) -> None:
        actor.attempts_to(Fill(SauceDemo.LOGIN_PASSWORD, self.password))

    @classmethod
    def as_(cls, password: str) -> "EnterPassword":
        return cls(password)
