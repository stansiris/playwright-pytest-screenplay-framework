from examples.work_items.automation.ui.targets import WorkItemsTargets
from screenplay_core.core.task import Task
from screenplay_core.playwright.interactions.click import Click


class DeleteWorkItem(Task):
    """Task: delete a work item by id or title."""

    def __init__(self, title: str | None = None, work_item_id: int | None = None):
        if work_item_id is None and not title:
            raise ValueError("DeleteWorkItem requires work_item_id or title.")

        self.title = title
        self.work_item_id = work_item_id

    def __repr__(self) -> str:
        if self.work_item_id is not None:
            return f"DeleteWorkItem(work_item_id={self.work_item_id})"
        return f"DeleteWorkItem(title='{self.title}')"

    def perform_as(self, actor) -> None:
        if self.work_item_id is not None:
            target = WorkItemsTargets.delete_button_for_work_item_id(self.work_item_id)
        else:
            target = WorkItemsTargets.delete_button_for_work_item_title(self.title or "")

        self.perform_interactions(actor, Click(target))

    @classmethod
    def named(cls, title: str) -> "DeleteWorkItem":
        return cls(title=title)

    @classmethod
    def with_id(cls, work_item_id: int) -> "DeleteWorkItem":
        return cls(work_item_id=work_item_id)
