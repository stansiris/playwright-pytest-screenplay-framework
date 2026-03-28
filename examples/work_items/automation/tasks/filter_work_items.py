from examples.work_items.automation.ui.targets import WorkItemsTargets
from screenplay_core.core.task import Task
from screenplay_core.playwright.interactions.click import Click


class FilterWorkItems(Task):
    """Task: apply a work item filter in the dashboard."""

    def __init__(self, filter_name: str):
        self.filter_name = filter_name

    def __repr__(self) -> str:
        return f"FilterWorkItems(filter_name='{self.filter_name}')"

    def perform_as(self, actor) -> None:
        self.perform_interactions(actor, Click(WorkItemsTargets.filter_button(self.filter_name)))

    @classmethod
    def by(cls, filter_name: str) -> "FilterWorkItems":
        return cls(filter_name=filter_name)
