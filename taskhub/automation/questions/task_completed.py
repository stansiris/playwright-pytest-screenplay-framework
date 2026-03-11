from screenplay_core.core.actor import Actor
from screenplay_core.core.question import Question
from taskhub.automation.ui.targets import TaskHubTargets


class TaskCompleted(Question):
    """Question: whether a task row is visually marked completed."""

    def __init__(self, title: str):
        self.title = title

    def answered_by(self, actor: Actor) -> bool:
        class_attribute = (
            TaskHubTargets.task_item_for_title(self.title).resolve_for(actor).get_attribute("class")
            or ""
        )
        return "completed" in class_attribute.split()

    def __repr__(self) -> str:
        return f"TaskCompleted(title='{self.title}')"
