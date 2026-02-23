from screenplay.core.task import Task
from screenplay.interactions.fill import Fill
from screenplay.ui.saucedemo import SauceDemo


class EnterPassword(Task):
    """Task: enter text in the password field."""

    def __init__(self, password: str):
        self.password = password

    def __repr__(self) -> str:
        return "EnterPassword(password='***')"

    def perform_as(self, actor) -> None:
        actor.attempts_to(Fill(SauceDemo.LOGIN_PASSWORD, self.password))

    @staticmethod
    def as_(password: str) -> "EnterPassword":
        return EnterPassword(password)
