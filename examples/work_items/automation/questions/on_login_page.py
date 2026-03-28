from urllib.parse import urlparse

from examples.work_items.automation.ui.targets import WorkItemsTargets
from screenplay_core.core.actor import Actor
from screenplay_core.core.question import Question
from screenplay_core.playwright.browse_the_web import BrowseTheWeb


class OnWorkItemsLoginPage(Question):
    """Question: whether the browser is on the Work Items login page."""

    def answered_by(self, actor: Actor) -> bool:
        browse = actor.ability_to(BrowseTheWeb)
        path = urlparse(browse.page.url).path.rstrip("/")
        return (
            path.endswith("/login")
            and WorkItemsTargets.LOGIN_SUBMIT_BUTTON.resolve_for(actor).is_visible()
        )

    def __repr__(self) -> str:
        return "OnWorkItemsLoginPage()"
