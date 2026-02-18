from screenplay.core.question import Question
from screenplay.core.target import Target


class IsVisible(Question):
    """Question: is an element visible?"""

    def __init__(self, target: Target):
        self.target = target

    def answered_by(self, actor):
        return self.target.resolve_for(actor).is_visible()
