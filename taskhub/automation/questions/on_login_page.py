from urllib.parse import urlparse

from screenplay_core.abilities.browse_the_web import BrowseTheWeb
from screenplay_core.core.actor import Actor
from screenplay_core.core.question import Question
from taskhub.automation.ui.targets import TaskHubTargets


class OnTaskHubLoginPage(Question):
    """Question: whether the browser is on the TaskHub login page."""

    def answered_by(self, actor: Actor) -> bool:
        browse = actor.ability_to(BrowseTheWeb)
        path = urlparse(browse.page.url).path.rstrip("/")
        return (
            path.endswith("/login")
            and TaskHubTargets.LOGIN_SUBMIT_BUTTON.resolve_for(actor).is_visible()
        )

    def __repr__(self) -> str:
        return "OnTaskHubLoginPage()"
