from examples.taskhub.automation.ui.targets import TaskHubTargets
from screenplay_core.core.task import Task
from screenplay_core.interactions.click import Click
from screenplay_core.interactions.fill import Fill
from screenplay_core.interactions.select_by_value import SelectByValue


class EditTask(Task):
    """Task: edit an existing task row in TaskHub by id or title."""

    def __init__(
        self,
        new_title: str,
        current_title: str | None = None,
        task_id: int | None = None,
        new_description: str | None = None,
        new_priority: str | None = None,
        new_due_date: str | None = None,
    ):
        if task_id is None and not current_title:
            raise ValueError("EditTask requires task_id or current_title.")

        self.current_title = current_title
        self.task_id = task_id
        self.new_title = new_title
        self.new_description = new_description
        self.new_priority = new_priority
        self.new_due_date = new_due_date

    def __repr__(self) -> str:
        if self.task_id is not None:
            return f"EditTask(task_id={self.task_id}, new_title='{self.new_title}')"
        return f"EditTask(current_title='{self.current_title}', new_title='{self.new_title}')"

    def perform_as(self, actor) -> None:
        if self.task_id is not None:
            edit_button = TaskHubTargets.edit_button_for_task_id(self.task_id)
            title_input = TaskHubTargets.edit_title_input_for_task_id(self.task_id)
            description_input = TaskHubTargets.edit_description_input_for_task_id(self.task_id)
            priority_input = TaskHubTargets.edit_priority_input_for_task_id(self.task_id)
            due_date_input = TaskHubTargets.edit_due_date_input_for_task_id(self.task_id)
            save_button = TaskHubTargets.save_button_for_task_id(self.task_id)
        else:
            current_title = self.current_title or ""
            edit_button = TaskHubTargets.edit_button_for_title(current_title)
            title_input = TaskHubTargets.edit_title_input_for_title(current_title)
            description_input = TaskHubTargets.edit_description_input_for_title(current_title)
            priority_input = TaskHubTargets.edit_priority_input_for_title(current_title)
            due_date_input = TaskHubTargets.edit_due_date_input_for_title(current_title)
            save_button = TaskHubTargets.save_button_for_title(current_title)

        interactions = [
            Click(edit_button),
            Fill(title_input, self.new_title),
        ]

        if self.new_description is not None:
            interactions.append(Fill(description_input, self.new_description))

        if self.new_priority is not None:
            interactions.append(SelectByValue(priority_input, self.new_priority))

        if self.new_due_date is not None:
            interactions.append(Fill(due_date_input, self.new_due_date))

        interactions.append(Click(save_button))
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
            new_title=new_title,
            current_title=current_title,
            new_description=new_description,
            new_priority=new_priority,
            new_due_date=new_due_date,
        )

    @classmethod
    def for_task_id(
        cls,
        task_id: int,
        new_title: str,
        new_description: str | None = None,
        new_priority: str | None = None,
        new_due_date: str | None = None,
    ) -> "EditTask":
        return cls(
            new_title=new_title,
            task_id=task_id,
            new_description=new_description,
            new_priority=new_priority,
            new_due_date=new_due_date,
        )
