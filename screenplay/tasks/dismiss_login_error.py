from screenplay.core.task import Task
from screenplay.interactions.click import Click
from screenplay.ui.saucedemo import SauceDemo


class DismissLoginError(Task):
    """Task: dismiss the login error banner."""

    def __repr__(self) -> str:
        return "DismissLoginError()"

    def perform_as(self, actor) -> None:
        actor.attempts_to(Click(SauceDemo.LOGIN_ERROR_CLOSE_BUTTON))
