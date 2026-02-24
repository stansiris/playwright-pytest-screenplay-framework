from saucedemo.ui.saucedemo import SauceDemo
from screenplay_core.core.task import Task
from screenplay_core.interactions.click import Click


class Logout(Task):
    """Task: Log Out of SauceDemo."""

    def perform_as(self, actor):
        actor.attempts_to(
            Click(SauceDemo.MENU_BUTTON),
            Click(SauceDemo.LOGOUT_LINK),
        )
