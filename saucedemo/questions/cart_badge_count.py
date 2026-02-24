from saucedemo.ui.saucedemo import SauceDemo
from screenplay_core.core.question import Question


class CartBadgeCount(Question):
    """Question: return the numeric badge count; absent badge counts as zero."""

    def answered_by(self, actor) -> int:
        badge = SauceDemo.SHOPPING_CART_BADGE.resolve_for(actor)
        if badge.count() == 0:
            return 0

        text = badge.first.inner_text().strip()
        return int(text) if text else 0

    def __repr__(self) -> str:
        return "CartBadgeCount()"


