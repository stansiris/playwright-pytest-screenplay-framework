from urllib.parse import urlparse

from examples.work_items.automation.ui.targets import WorkItemsTargets
from screenplay_core.core.actor import Actor
from screenplay_core.core.question import Question
from screenplay_core.playwright.browse_the_web import BrowseTheWeb


class OnWorkItemsPage(Question):
    """Question: whether the browser is on the Work Items dashboard page."""

    def answered_by(self, actor: Actor) -> bool:
        browse = actor.ability_to(BrowseTheWeb)
        path = urlparse(browse.page.url).path.rstrip("/")
        is_path_match = path.endswith("/work-items")
        return (
            is_path_match
            and WorkItemsTargets.WORK_ITEM_LIST_CONTAINER.resolve_for(actor).is_visible()
        )

    def __repr__(self) -> str:
        return "OnWorkItemsPage()"
