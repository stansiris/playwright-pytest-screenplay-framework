from examples.work_items.automation.ui.targets import WorkItemsTargets
from screenplay_core.core.actor import Actor
from screenplay_core.core.question import Question


class FlashMessages(Question):
    """Question: return non-empty flash message strings currently shown."""

    def answered_by(self, actor: Actor) -> list[str]:
        messages = WorkItemsTargets.FLASH_MESSAGE_CONTAINER.resolve_for(actor).locator(".flash")
        texts = messages.all_inner_texts()
        return [text.strip() for text in texts if text and text.strip()]

    def __repr__(self) -> str:
        return "FlashMessages()"
