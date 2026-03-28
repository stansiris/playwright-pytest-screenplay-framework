from examples.work_items.automation.ui.targets import WorkItemsTargets
from screenplay_core.core.actor import Actor
from screenplay_core.core.question import Question


class WorkItemVisible(Question):
    """Question: whether a work item card with a given id/title is visible."""

    def __init__(self, title: str | None = None, work_item_id: int | None = None):
        if work_item_id is None and not title:
            raise ValueError("WorkItemVisible requires work_item_id or title.")

        self.title = title
        self.work_item_id = work_item_id

    def answered_by(self, actor: Actor) -> bool:
        if self.work_item_id is not None:
            target = WorkItemsTargets.work_item_for_id(self.work_item_id)
        else:
            target = WorkItemsTargets.work_item_for_title(self.title or "")
        return target.resolve_for(actor).count() > 0

    def __repr__(self) -> str:
        if self.work_item_id is not None:
            return f"WorkItemVisible(work_item_id={self.work_item_id})"
        return f"WorkItemVisible(title='{self.title}')"

    @classmethod
    def for_work_item_id(cls, work_item_id: int) -> "WorkItemVisible":
        return cls(work_item_id=work_item_id)
