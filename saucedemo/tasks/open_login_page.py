from saucedemo.tasks.open_saucedemo import OpenSauceDemo
from saucedemo.ui.pages.login_page import LoginPage
from screenplay_core.consequences.ensure import Ensure
from screenplay_core.core.actor import Actor
from screenplay_core.core.task import Task


class OpenLoginPage(Task):
    """Task: open the SauceDemo login page."""

    def __repr__(self) -> str:
        return "OpenLoginPage()"

    def perform_as(self, actor: Actor) -> None:
        actor.attempts_to(OpenSauceDemo.app())
        actor.attempts_to(Ensure.that(LoginPage.LOGIN_BUTTON).to_be_visible())
