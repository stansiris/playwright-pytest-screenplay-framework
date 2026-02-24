from screenplay.ui.saucedemo import SauceDemo
from screenplay_core.core.task import Task
from screenplay_core.interactions.navigate_to import NavigateTo


class OpenSauceDemo(Task):
    """Task: open the SauceDemo application."""

    def perform_as(self, actor) -> None:
        actor.attempts_to(NavigateTo(SauceDemo.URL))

    @classmethod
    def app(cls) -> "OpenSauceDemo":
        return cls()

