from examples.work_items.automation.ui.targets import WorkItemsTargets
from screenplay_core.core.task import Task
from screenplay_core.playwright.interactions.click import Click
from screenplay_core.playwright.interactions.fill import Fill
from screenplay_core.playwright.interactions.select_by_value import SelectByValue


class CreateWorkItem(Task):
    """Task: create a work item from the dashboard form."""

    def __init__(
        self,
        title: str,
        description: str = "",
        priority: str = "MEDIUM",
        due_date: str = "",
    ):
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date

    def __repr__(self) -> str:
        return f"CreateWorkItem(title='{self.title}', priority='{self.priority}')"

    def perform_as(self, actor) -> None:
        self.perform_interactions(
            actor,
            Fill(WorkItemsTargets.WORK_ITEM_TITLE_INPUT, self.title),
            Fill(WorkItemsTargets.WORK_ITEM_DESCRIPTION_INPUT, self.description),
            SelectByValue(WorkItemsTargets.WORK_ITEM_PRIORITY_INPUT, self.priority),
            Fill(WorkItemsTargets.WORK_ITEM_DUE_DATE_INPUT, self.due_date),
            Click(WorkItemsTargets.ADD_WORK_ITEM_BUTTON),
        )

    @classmethod
    def named(
        cls,
        title: str,
        description: str = "",
        priority: str = "MEDIUM",
        due_date: str = "",
    ) -> "CreateWorkItem":
        return cls(title=title, description=description, priority=priority, due_date=due_date)
