from screenplay_core.core.task import Task
from screenplay_core.interactions.click import Click
from taskhub.automation.ui.targets import TaskHubTargets


class DeleteTask(Task):
    """Task: delete a task row by title."""

    def __init__(self, title: str):
        self.title = title

    def __repr__(self) -> str:
        return f"DeleteTask(title='{self.title}')"

    def perform_as(self, actor) -> None:
        self.perform_interactions(actor, Click(TaskHubTargets.delete_button_for_title(self.title)))

    @classmethod
    def named(cls, title: str) -> "DeleteTask":
        return cls(title=title)
