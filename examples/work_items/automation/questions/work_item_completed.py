from examples.work_items.automation.ui.targets import WorkItemsTargets
from screenplay_core.core.actor import Actor
from screenplay_core.core.question import Question


class WorkItemCompleted(Question):
    """Question: whether a work item card is visually marked completed."""

    def __init__(self, title: str | None = None, work_item_id: int | None = None):
        if work_item_id is None and not title:
            raise ValueError("WorkItemCompleted requires work_item_id or title.")

        self.title = title
        self.work_item_id = work_item_id

    def answered_by(self, actor: Actor) -> bool:
        if self.work_item_id is not None:
            row_target = WorkItemsTargets.work_item_for_id(self.work_item_id)
        else:
            row_target = WorkItemsTargets.work_item_for_title(self.title or "")

        class_attribute = row_target.resolve_for(actor).get_attribute("class") or ""
        return "completed" in class_attribute.split()

    def __repr__(self) -> str:
        if self.work_item_id is not None:
            return f"WorkItemCompleted(work_item_id={self.work_item_id})"
        return f"WorkItemCompleted(title='{self.title}')"

    @classmethod
    def for_work_item_id(cls, work_item_id: int) -> "WorkItemCompleted":
        return cls(work_item_id=work_item_id)
