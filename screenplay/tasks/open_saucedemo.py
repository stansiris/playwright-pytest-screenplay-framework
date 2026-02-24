from screenplay.core.task import Task
from screenplay.interactions.navigate_to import NavigateTo
from screenplay.ui.saucedemo import SauceDemo


class OpenSauceDemo(Task):
    """Task: open the SauceDemo application."""

    def perform_as(self, actor) -> None:
        actor.attempts_to(NavigateTo(SauceDemo.URL))

    @classmethod
    def app(cls) -> "OpenSauceDemo":
        return cls()
