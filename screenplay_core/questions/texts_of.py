from screenplay_core.core.actor import Actor
from screenplay_core.core.question import Question
from screenplay_core.core.target import Target


class TextsOf(Question):
    """Question: return normalized text values for all elements in a target collection."""

    def __init__(self, target: Target):
        """Store target collection whose text values will be read."""
        self.target = target

    def answered_by(self, actor: Actor) -> list[str]:
        """Return stripped non-empty text values from all matched elements."""
        texts = self.target.resolve_for(actor).all_inner_texts()
        return [text.strip() for text in texts if text and text.strip()]

    def __repr__(self) -> str:
        """Return a concise representation with target description."""
        return f"TextsOf(target='{self.target.description}')"
