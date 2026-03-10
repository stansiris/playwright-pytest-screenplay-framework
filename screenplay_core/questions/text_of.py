from screenplay_core.core.actor import Actor
from screenplay_core.core.question import Question
from screenplay_core.core.target import Target


class TextOf(Question):
    """Question: What text does the element present to the user?"""

    def __init__(self, target: Target):
        """Store the target from which text-like value will be read."""
        self.target = target

    def answered_by(self, actor: Actor) -> str:
        """Return visible text; fallback to value attribute when text is empty."""
        locator = self.target.resolve_for(actor)

        txt = locator.text_content()
        if txt and txt.strip():
            return txt.strip()

        val = locator.get_attribute("value")
        return (val or "").strip()

    def __repr__(self) -> str:
        """Return a concise representation with target description."""
        return f"TextOf(target='{self.target.description}')"
