from screenplay.core.question import Question
from screenplay.core.target import Target


class TextOf(Question):
    """Question: What text does the element present to the user?"""

    def __init__(self, target: Target):
        self.target = target

    def answered_by(self, actor) -> str:
        locator = self.target.resolve_for(actor)

        txt = locator.text_content()
        if txt and txt.strip():
            return txt.strip()

        val = locator.get_attribute("value")
        return (val or "").strip()

    def __repr__(self) -> str:
        return f"TextOf(target='{self.target.description}')"
