from saucedemo.ui.components.app_shell import AppShell
from screenplay_core.core.task import Task
from screenplay_core.interactions.click import Click


class Logout(Task):
    """Task: Log Out of SauceDemo."""

    def perform_as(self, actor):
        self.perform_interactions(
            actor,
            Click(AppShell.MENU_BUTTON),
            Click(AppShell.LOGOUT_LINK),
        )
