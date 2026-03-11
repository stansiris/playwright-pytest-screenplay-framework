from screenplay_core.core.task import Task
from screenplay_core.interactions.click import Click
from screenplay_core.interactions.fill import Fill
from screenplay_core.interactions.select_by_value import SelectByValue
from taskhub.automation.ui.targets import TaskHubTargets


class EditTask(Task):
    """Task: edit an existing task row in TaskHub."""

    def __init__(
        self,
        current_title: str,
        new_title: str,
        new_description: str | None = None,
        new_priority: str | None = None,
        new_due_date: str | None = None,
    ):
        self.current_title = current_title
        self.new_title = new_title
        self.new_description = new_description
        self.new_priority = new_priority
        self.new_due_date = new_due_date

    def __repr__(self) -> str:
        return f"EditTask(current_title='{self.current_title}', new_title='{self.new_title}')"

    def perform_as(self, actor) -> None:
        interactions = [
            Click(TaskHubTargets.edit_button_for_title(self.current_title)),
            Fill(TaskHubTargets.edit_title_input_for_title(self.current_title), self.new_title),
        ]

        if self.new_description is not None:
            interactions.append(
                Fill(
                    TaskHubTargets.edit_description_input_for_title(self.current_title),
                    self.new_description,
                )
            )

        if self.new_priority is not None:
            interactions.append(
                SelectByValue(
                    TaskHubTargets.edit_priority_input_for_title(self.current_title),
                    self.new_priority,
                )
            )

        if self.new_due_date is not None:
            interactions.append(
                Fill(
                    TaskHubTargets.edit_due_date_input_for_title(self.current_title),
                    self.new_due_date,
                )
            )

        interactions.append(Click(TaskHubTargets.save_button_for_title(self.current_title)))
        self.perform_interactions(actor, *interactions)

    @classmethod
    def from_title(
        cls,
        current_title: str,
        new_title: str,
        new_description: str | None = None,
        new_priority: str | None = None,
        new_due_date: str | None = None,
    ) -> "EditTask":
        return cls(
            current_title=current_title,
            new_title=new_title,
            new_description=new_description,
            new_priority=new_priority,
            new_due_date=new_due_date,
        )
