from screenplay_core.abilities.browse_the_web import BrowseTheWeb
from screenplay_core.core.actor import Actor
from screenplay_core.core.interaction import Interaction


class RefreshPage(Interaction):
    """Interaction: reload the current browser page."""

    def __repr__(self) -> str:
        """Return a compact representation for logs."""
        return "RefreshPage()"

    def perform_as(self, actor: Actor) -> None:
        """Reload the active page via BrowseTheWeb ability."""
        actor.ability_to(BrowseTheWeb).page.reload()
