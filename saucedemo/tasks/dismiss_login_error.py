from saucedemo.ui.saucedemo import SauceDemo
from screenplay_core.core.actor import Actor
from screenplay_core.core.task import Task
from screenplay_core.interactions.click import Click


class DismissLoginError(Task):
    """Task: dismiss the login error banner."""

    def perform_as(self, actor: Actor) -> None:
        actor.attempts_to(Click(SauceDemo.LOGIN_ERROR_CLOSE_BUTTON))
