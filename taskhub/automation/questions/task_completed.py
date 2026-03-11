from screenplay_core.core.actor import Actor
from screenplay_core.core.question import Question
from taskhub.automation.ui.targets import TaskHubTargets


class TaskCompleted(Question):
    """Question: whether a task row is visually marked completed."""

    def __init__(self, title: str | None = None, task_id: int | None = None):
        if task_id is None and not title:
            raise ValueError("TaskCompleted requires task_id or title.")

        self.title = title
        self.task_id = task_id

    def answered_by(self, actor: Actor) -> bool:
        if self.task_id is not None:
            row_target = TaskHubTargets.task_item_for_id(self.task_id)
        else:
            row_target = TaskHubTargets.task_item_for_title(self.title or "")

        class_attribute = row_target.resolve_for(actor).get_attribute("class") or ""
        return "completed" in class_attribute.split()

    def __repr__(self) -> str:
        if self.task_id is not None:
            return f"TaskCompleted(task_id={self.task_id})"
        return f"TaskCompleted(title='{self.title}')"

    @classmethod
    def for_task_id(cls, task_id: int) -> "TaskCompleted":
        return cls(task_id=task_id)
