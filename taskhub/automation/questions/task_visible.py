from screenplay_core.core.actor import Actor
from screenplay_core.core.question import Question
from taskhub.automation.ui.targets import TaskHubTargets


class TaskVisible(Question):
    """Question: whether a task row with a given title is visible."""

    def __init__(self, title: str):
        self.title = title

    def answered_by(self, actor: Actor) -> bool:
        return TaskHubTargets.task_item_for_title(self.title).resolve_for(actor).count() > 0

    def __repr__(self) -> str:
        return f"TaskVisible(title='{self.title}')"
