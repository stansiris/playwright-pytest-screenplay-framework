from screenplay_core.core.task import Task
from screenplay_core.interactions.click import Click
from taskhub.automation.ui.targets import TaskHubTargets


class ToggleTaskCompletion(Task):
    """Task: toggle completion state for a task row."""

    def __init__(self, title: str):
        self.title = title

    def __repr__(self) -> str:
        return f"ToggleTaskCompletion(title='{self.title}')"

    def perform_as(self, actor) -> None:
        self.perform_interactions(
            actor, Click(TaskHubTargets.complete_toggle_for_title(self.title))
        )

    @classmethod
    def for_title(cls, title: str) -> "ToggleTaskCompletion":
        return cls(title=title)
