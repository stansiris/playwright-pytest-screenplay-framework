from examples.work_items.automation.ui.targets import WorkItemsTargets
from screenplay_core.core.task import Task
from screenplay_core.playwright.interactions.click import Click
from screenplay_core.playwright.interactions.fill import Fill
from screenplay_core.playwright.interactions.select_by_value import SelectByValue


class EditWorkItem(Task):
    """Task: edit an existing work item in Work Items by id or title."""

    def __init__(
        self,
        new_title: str,
        current_title: str | None = None,
        work_item_id: int | None = None,
        new_description: str | None = None,
        new_priority: str | None = None,
        new_due_date: str | None = None,
    ):
        if work_item_id is None and not current_title:
            raise ValueError("EditWorkItem requires work_item_id or current_title.")

        self.current_title = current_title
        self.work_item_id = work_item_id
        self.new_title = new_title
        self.new_description = new_description
        self.new_priority = new_priority
        self.new_due_date = new_due_date

    def __repr__(self) -> str:
        if self.work_item_id is not None:
            return f"EditWorkItem(work_item_id={self.work_item_id}, new_title='{self.new_title}')"
        return (
            f"EditWorkItem(current_title='{self.current_title}', " f"new_title='{self.new_title}')"
        )

    def perform_as(self, actor) -> None:
        if self.work_item_id is not None:
            edit_button = WorkItemsTargets.edit_button_for_work_item_id(self.work_item_id)
            title_input = WorkItemsTargets.edit_title_input_for_work_item_id(self.work_item_id)
            description_input = WorkItemsTargets.edit_description_input_for_work_item_id(
                self.work_item_id
            )
            priority_input = WorkItemsTargets.edit_priority_input_for_work_item_id(
                self.work_item_id
            )
            due_date_input = WorkItemsTargets.edit_due_date_input_for_work_item_id(
                self.work_item_id
            )
            save_button = WorkItemsTargets.save_button_for_work_item_id(self.work_item_id)
        else:
            current_title = self.current_title or ""
            edit_button = WorkItemsTargets.edit_button_for_work_item_title(current_title)
            title_input = WorkItemsTargets.edit_title_input_for_work_item_title(current_title)
            description_input = WorkItemsTargets.edit_description_input_for_work_item_title(
                current_title
            )
            priority_input = WorkItemsTargets.edit_priority_input_for_work_item_title(current_title)
            due_date_input = WorkItemsTargets.edit_due_date_input_for_work_item_title(current_title)
            save_button = WorkItemsTargets.save_button_for_work_item_title(current_title)

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
    ) -> "EditWorkItem":
        return cls(
            new_title=new_title,
            current_title=current_title,
            new_description=new_description,
            new_priority=new_priority,
            new_due_date=new_due_date,
        )

    @classmethod
    def for_work_item_id(
        cls,
        work_item_id: int,
        new_title: str,
        new_description: str | None = None,
        new_priority: str | None = None,
        new_due_date: str | None = None,
    ) -> "EditWorkItem":
        return cls(
            new_title=new_title,
            work_item_id=work_item_id,
            new_description=new_description,
            new_priority=new_priority,
            new_due_date=new_due_date,
        )
