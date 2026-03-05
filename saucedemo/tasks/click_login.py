from saucedemo.ui.pages.login_page import LoginPage
from screenplay_core.core.actor import Actor
from screenplay_core.core.task import Task
from screenplay_core.interactions.click import Click


class ClickLogin(Task):
    """Task: click the login button."""

    def perform_as(self, actor: Actor) -> None:
        actor.attempts_to(Click(LoginPage.LOGIN_BUTTON))
