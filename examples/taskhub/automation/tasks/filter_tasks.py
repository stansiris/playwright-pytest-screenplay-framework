from examples.taskhub.automation.ui.targets import TaskHubTargets
from screenplay_core.core.task import Task
from screenplay_core.interactions.click import Click


class FilterTasks(Task):
    """Task: apply a task filter in the dashboard."""

    def __init__(self, filter_name: str):
        self.filter_name = filter_name

    def __repr__(self) -> str:
        return f"FilterTasks(filter_name='{self.filter_name}')"

    def perform_as(self, actor) -> None:
        self.perform_interactions(actor, Click(TaskHubTargets.filter_button(self.filter_name)))

    @classmethod
    def by(cls, filter_name: str) -> "FilterTasks":
        return cls(filter_name=filter_name)
