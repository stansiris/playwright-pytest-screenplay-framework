from examples.taskhub.automation.ui.targets import TaskHubTargets
from screenplay_core.core.actor import Actor
from screenplay_core.core.question import Question


class TaskVisible(Question):
    """Question: whether a task row with a given id/title is visible."""

    def __init__(self, title: str | None = None, task_id: int | None = None):
        if task_id is None and not title:
            raise ValueError("TaskVisible requires task_id or title.")

        self.title = title
        self.task_id = task_id

    def answered_by(self, actor: Actor) -> bool:
        if self.task_id is not None:
            target = TaskHubTargets.task_item_for_id(self.task_id)
        else:
            target = TaskHubTargets.task_item_for_title(self.title or "")
        return target.resolve_for(actor).count() > 0

    def __repr__(self) -> str:
        if self.task_id is not None:
            return f"TaskVisible(task_id={self.task_id})"
        return f"TaskVisible(title='{self.title}')"

    @classmethod
    def for_task_id(cls, task_id: int) -> "TaskVisible":
        return cls(task_id=task_id)
