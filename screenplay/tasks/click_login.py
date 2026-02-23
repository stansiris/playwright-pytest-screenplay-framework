from screenplay.core.task import Task
from screenplay.interactions.click import Click
from screenplay.ui.saucedemo import SauceDemo


class ClickLogin(Task):
    """Task: click the login button."""

    def __repr__(self) -> str:
        return "ClickLogin()"

    def perform_as(self, actor) -> None:
        actor.attempts_to(Click(SauceDemo.LOGIN_BUTTON))
