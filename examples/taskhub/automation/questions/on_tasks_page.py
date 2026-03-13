from urllib.parse import urlparse

from examples.taskhub.automation.ui.targets import TaskHubTargets
from screenplay_core.abilities.browse_the_web import BrowseTheWeb
from screenplay_core.core.actor import Actor
from screenplay_core.core.question import Question


class OnTaskHubTasksPage(Question):
    """Question: whether the browser is on the TaskHub dashboard page."""

    def answered_by(self, actor: Actor) -> bool:
        browse = actor.ability_to(BrowseTheWeb)
        path = urlparse(browse.page.url).path.rstrip("/")
        is_path_match = path.endswith("/tasks")
        return is_path_match and TaskHubTargets.TASK_LIST_CONTAINER.resolve_for(actor).is_visible()

    def __repr__(self) -> str:
        return "OnTaskHubTasksPage()"
