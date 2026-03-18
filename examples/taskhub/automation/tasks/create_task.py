from examples.taskhub.automation.ui.targets import TaskHubTargets
from screenplay_core.core.task import Task
from screenplay_core.playwright.interactions.click import Click
from screenplay_core.playwright.interactions.fill import Fill
from screenplay_core.playwright.interactions.select_by_value import SelectByValue


class CreateTask(Task):
    """Task: create a TaskHub task from the dashboard form."""

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
        return f"CreateTask(title='{self.title}', priority='{self.priority}')"

    def perform_as(self, actor) -> None:
        self.perform_interactions(
            actor,
            Fill(TaskHubTargets.TASK_TITLE_INPUT, self.title),
            Fill(TaskHubTargets.TASK_DESCRIPTION_INPUT, self.description),
            SelectByValue(TaskHubTargets.TASK_PRIORITY_INPUT, self.priority),
            Fill(TaskHubTargets.TASK_DUE_DATE_INPUT, self.due_date),
            Click(TaskHubTargets.ADD_TASK_BUTTON),
        )

    @classmethod
    def named(
        cls,
        title: str,
        description: str = "",
        priority: str = "MEDIUM",
        due_date: str = "",
    ) -> "CreateTask":
        return cls(title=title, description=description, priority=priority, due_date=due_date)
