from screenplay_core.abilities.browse_the_web import BrowseTheWeb
from screenplay_core.core.question import Question


class CurrentUrl(Question):
    """Question: return the current page URL."""

    def answered_by(self, actor) -> str:
        return actor.ability_to(BrowseTheWeb).page.url

    def __repr__(self) -> str:
        return "CurrentUrl()"
