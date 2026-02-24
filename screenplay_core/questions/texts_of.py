from screenplay_core.core.question import Question
from screenplay_core.core.target import Target


class TextsOf(Question):
    """Question: return normalized text values for all elements in a target collection."""

    def __init__(self, target: Target):
        self.target = target

    def answered_by(self, actor) -> list[str]:
        texts = self.target.resolve_for(actor).all_inner_texts()
        return [text.strip() for text in texts if text and text.strip()]

    def __repr__(self) -> str:
        return f"TextsOf(target='{self.target.description}')"
