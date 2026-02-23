from screenplay.core.task import Task
from screenplay.interactions.navigate_to import NavigateTo
from screenplay.ui.saucedemo import SauceDemo


class OpenSauceDemo(Task):
    """Task: open the SauceDemo application."""

    def __repr__(self) -> str:
        return "OpenSauceDemo()"

    def perform_as(self, actor) -> None:
        actor.attempts_to(NavigateTo(SauceDemo.URL))

    @staticmethod
    def app() -> "OpenSauceDemo":
        return OpenSauceDemo()
