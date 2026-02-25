from screenplay_core.core.actor import Actor
from screenplay_core.core.question import Question
from screenplay_core.core.target import Target


class IsVisible(Question):
    """Question: is an element visible?"""

    def __init__(self, target: Target):
        self.target = target

    def answered_by(self, actor: Actor):
        return self.target.resolve_for(actor).is_visible()

    def __repr__(self) -> str:
        return f"IsVisible(target='{self.target.description}')"
