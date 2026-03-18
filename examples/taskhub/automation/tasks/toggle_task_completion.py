from examples.taskhub.automation.ui.targets import TaskHubTargets
from screenplay_core.core.task import Task
from screenplay_core.playwright.interactions.click import Click


class ToggleTaskCompletion(Task):
    """Task: toggle completion state for a task row by id or title."""

    def __init__(self, title: str | None = None, task_id: int | None = None):
        if task_id is None and not title:
            raise ValueError("ToggleTaskCompletion requires task_id or title.")

        self.title = title
        self.task_id = task_id

    def __repr__(self) -> str:
        if self.task_id is not None:
            return f"ToggleTaskCompletion(task_id={self.task_id})"
        return f"ToggleTaskCompletion(title='{self.title}')"

    def perform_as(self, actor) -> None:
        if self.task_id is not None:
            target = TaskHubTargets.complete_toggle_for_task_id(self.task_id)
        else:
            target = TaskHubTargets.complete_toggle_for_title(self.title or "")

        self.perform_interactions(
            actor,
            Click(target),
        )

    @classmethod
    def for_title(cls, title: str) -> "ToggleTaskCompletion":
        return cls(title=title)

    @classmethod
    def for_task_id(cls, task_id: int) -> "ToggleTaskCompletion":
        return cls(task_id=task_id)
