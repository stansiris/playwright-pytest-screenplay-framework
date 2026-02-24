from screenplay.ui.saucedemo import SauceDemo
from screenplay_core.core.task import Task
from screenplay_core.interactions.click import Click


class ClickLogin(Task):
    """Task: click the login button."""

    def perform_as(self, actor) -> None:
        actor.attempts_to(Click(SauceDemo.LOGIN_BUTTON))

