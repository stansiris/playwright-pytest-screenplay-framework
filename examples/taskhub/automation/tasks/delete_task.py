from examples.taskhub.automation.ui.targets import TaskHubTargets
from screenplay_core.core.task import Task
from screenplay_core.interactions.click import Click


class DeleteTask(Task):
    """Task: delete a task row by id or title."""

    def __init__(self, title: str | None = None, task_id: int | None = None):
        if task_id is None and not title:
            raise ValueError("DeleteTask requires task_id or title.")

        self.title = title
        self.task_id = task_id

    def __repr__(self) -> str:
        if self.task_id is not None:
            return f"DeleteTask(task_id={self.task_id})"
        return f"DeleteTask(title='{self.title}')"

    def perform_as(self, actor) -> None:
        if self.task_id is not None:
            target = TaskHubTargets.delete_button_for_task_id(self.task_id)
        else:
            target = TaskHubTargets.delete_button_for_title(self.title or "")

        self.perform_interactions(actor, Click(target))

    @classmethod
    def named(cls, title: str) -> "DeleteTask":
        return cls(title=title)

    @classmethod
    def with_id(cls, task_id: int) -> "DeleteTask":
        return cls(task_id=task_id)
