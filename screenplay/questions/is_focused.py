from screenplay.abilities.browse_the_web import BrowseTheWeb
from screenplay.core.question import Question
from screenplay.core.target import Target


class IsFocused(Question):
    """Question: whether the provided target currently has browser focus."""

    def __init__(self, target: Target):
        self.target = target

    def answered_by(self, actor) -> bool:
        page = actor.ability_to(BrowseTheWeb).page
        locator = self.target.resolve_for(actor).first
        element = locator.element_handle()
        if element is None:
            return False
        return bool(page.evaluate("(element) => document.activeElement === element", element))

    def __repr__(self) -> str:
        return f"IsFocused(target='{self.target.description}')"
