import re

from saucedemo.ui.saucedemo import SauceDemo
from screenplay_core.core.question import Question
from screenplay_core.questions.text_of import TextOf
from screenplay_core.questions.texts_of import TextsOf

MONEY_PATTERN = re.compile(r"\$([0-9]+(?:\.[0-9]{2})?)")


def _parse_money(text: str) -> float:
    match = MONEY_PATTERN.search(text)
    if not match:
        raise ValueError(f"Could not parse money value from '{text}'.")
    return float(match.group(1))


class TotalsMatchComputedSum(Question):
    """Question: whether overview totals are internally consistent."""

    def answered_by(self, actor) -> bool:
        item_prices = [
            _parse_money(text) for text in actor.asks_for(TextsOf(SauceDemo.INVENTORY_ITEM_PRICES))
        ]
        subtotal = _parse_money(actor.asks_for(TextOf(SauceDemo.CHECKOUT_SUBTOTAL)))
        tax = _parse_money(actor.asks_for(TextOf(SauceDemo.CHECKOUT_TAX)))
        total = _parse_money(actor.asks_for(TextOf(SauceDemo.CHECKOUT_TOTAL)))

        computed_subtotal = round(sum(item_prices), 2)
        computed_total = round(subtotal + tax, 2)
        return computed_subtotal == round(subtotal, 2) and computed_total == round(total, 2)

    def __repr__(self) -> str:
        return "TotalsMatchComputedSum()"
