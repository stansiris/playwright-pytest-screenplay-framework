import re

from examples.work_items.automation.ui.targets import WorkItemsTargets
from screenplay_core.core.actor import Actor
from screenplay_core.core.question import Question


class WorkItemIdForTitle(Question):
    """Question: resolve a work item id from an exact work item title."""

    def __init__(self, title: str):
        self.title = title

    def answered_by(self, actor: Actor) -> int | None:
        work_item_card = WorkItemsTargets.work_item_for_title(self.title).resolve_for(actor)
        if work_item_card.count() == 0:
            return None

        title_locator = work_item_card.locator('[data-testid="work-item-title-text"]')
        if title_locator.count() == 0:
            return None

        resolved_title = (title_locator.first.inner_text() or "").strip()
        if not re.fullmatch(re.escape(self.title), resolved_title):
            return None

        work_item_id_raw = work_item_card.get_attribute("data-work-item-id")
        if work_item_id_raw is None:
            return None

        try:
            return int(work_item_id_raw)
        except ValueError:
            return None

    def __repr__(self) -> str:
        return f"WorkItemIdForTitle(title='{self.title}')"
