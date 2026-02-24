from screenplay_core.abilities.browse_the_web import BrowseTheWeb
from screenplay_core.core.interaction import Interaction


class RefreshPage(Interaction):
    """Interaction: reload the current browser page."""

    def __repr__(self) -> str:
        return "RefreshPage()"

    def perform_as(self, actor) -> None:
        actor.ability_to(BrowseTheWeb).page.reload()
