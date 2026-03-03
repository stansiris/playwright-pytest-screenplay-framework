from screenplay_core.abilities.browse_the_web import BrowseTheWeb
from screenplay_core.core.actor import Actor
from screenplay_core.core.task import Task
from screenplay_core.interactions.navigate_to import NavigateTo


class OpenSauceDemo(Task):
    """Task: open the SauceDemo application."""

    def perform_as(self, actor: Actor) -> None:
        base_url = actor.ability_to(BrowseTheWeb).base_url
        if not base_url:
            raise ValueError("BrowseTheWeb ability must include a base_url to open SauceDemo.")
        actor.attempts_to(NavigateTo(base_url))

    @classmethod
    def app(cls) -> "OpenSauceDemo":
        return cls()
