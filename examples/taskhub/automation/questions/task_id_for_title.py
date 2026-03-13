import re

from examples.taskhub.automation.ui.targets import TaskHubTargets
from screenplay_core.core.actor import Actor
from screenplay_core.core.question import Question


class TaskIdForTitle(Question):
    """Question: resolve a TaskHub row ID from an exact task title."""

    def __init__(self, title: str):
        self.title = title

    def answered_by(self, actor: Actor) -> int | None:
        task_row = TaskHubTargets.task_item_for_title(self.title).resolve_for(actor)
        if task_row.count() == 0:
            return None

        title_locator = task_row.locator('[data-testid="task-title-text"]')
        if title_locator.count() == 0:
            return None

        row_title = (title_locator.first.inner_text() or "").strip()
        if not re.fullmatch(re.escape(self.title), row_title):
            return None

        task_id_raw = task_row.get_attribute("data-task-id")
        if task_id_raw is None:
            return None

        try:
            return int(task_id_raw)
        except ValueError:
            return None

    def __repr__(self) -> str:
        return f"TaskIdForTitle(title='{self.title}')"
