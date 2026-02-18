from screenplay.core.task import Task
from screenplay.interactions.click import Click
from screenplay.ui.saucedemo import SauceDemo


class Logout(Task):
    """Task: Log Out of SauceDemo."""

    def perform_as(self, actor):
        actor.attempts_to(
            Click(SauceDemo.MENU_BUTTON),
            Click(SauceDemo.LOGOUT_LINK),
        )
