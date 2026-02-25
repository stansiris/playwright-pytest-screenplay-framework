from saucedemo.ui.saucedemo import SauceDemo
from screenplay_core.core.actor import Actor
from screenplay_core.core.task import Task
from screenplay_core.interactions.navigate_to import NavigateTo


class OpenSauceDemo(Task):
    """Task: open the SauceDemo application."""

    def perform_as(self, actor: Actor) -> None:
        actor.attempts_to(NavigateTo(SauceDemo.URL))

    @classmethod
    def app(cls) -> "OpenSauceDemo":
        return cls()
