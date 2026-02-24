from screenplay_core.core.question import Question
from screenplay_core.core.target import Target


class AttributeOf(Question):
    """Question: read an attribute value from a target element."""

    def __init__(self, target: Target, attribute_name: str):
        self.target = target
        self.attribute_name = attribute_name

    def answered_by(self, actor) -> str | None:
        return self.target.resolve_for(actor).get_attribute(self.attribute_name)

    def __repr__(self) -> str:
        return (
            "AttributeOf("
            f"target='{self.target.description}', "
            f"attribute_name='{self.attribute_name}')"
        )
