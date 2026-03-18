from screenplay_core.core.actor import Actor
from screenplay_core.core.question import Question
from screenplay_core.playwright.browse_the_web import BrowseTheWeb
from screenplay_core.playwright.target import Target


class IsFocused(Question):
    """Question: whether the provided target currently has browser focus."""

    def __init__(self, target: Target):
        """Store the target whose focus state will be checked."""
        self.target = target

    def answered_by(self, actor: Actor) -> bool:
        """Resolve target and compare against document.activeElement."""
        page = actor.ability_to(BrowseTheWeb).page
        locator = self.target.resolve_for(actor).first
        element = locator.element_handle()
        if element is None:
            return False
        return bool(page.evaluate("(element) => document.activeElement === element", element))

    def __repr__(self) -> str:
        """Return a concise representation with target description."""
        return f"IsFocused(target='{self.target.description}')"
