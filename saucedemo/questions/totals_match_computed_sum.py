import re
from decimal import Decimal

from saucedemo.ui.pages.checkout_overview_page import CheckoutOverviewPage
from screenplay_core.core.actor import Actor
from screenplay_core.core.question import Question
from screenplay_core.questions.text_of import TextOf
from screenplay_core.questions.texts_of import TextsOf

MONEY_PATTERN = re.compile(r"\$([0-9]+(?:\.[0-9]{2})?)")
TWO_DECIMAL_PLACES = Decimal("0.01")


def _parse_money(text: str) -> Decimal:
    match = MONEY_PATTERN.search(text)
    if not match:
        raise ValueError(f"Could not parse money value from '{text}'.")
    return Decimal(match.group(1))


class TotalsMatchComputedSum(Question):
    """Question: whether overview totals are internally consistent."""

    def answered_by(self, actor: Actor) -> bool:
        item_prices = [
            _parse_money(text)
            for text in actor.asks_for(TextsOf(CheckoutOverviewPage.CHECKOUT_OVERVIEW_ITEM_PRICES))
        ]
        subtotal = _parse_money(actor.asks_for(TextOf(CheckoutOverviewPage.CHECKOUT_SUBTOTAL)))
        tax = _parse_money(actor.asks_for(TextOf(CheckoutOverviewPage.CHECKOUT_TAX)))
        total = _parse_money(actor.asks_for(TextOf(CheckoutOverviewPage.CHECKOUT_TOTAL)))

        computed_subtotal = sum(item_prices, start=Decimal("0"))
        computed_total = computed_subtotal + tax

        return computed_subtotal.quantize(TWO_DECIMAL_PLACES) == subtotal.quantize(
            TWO_DECIMAL_PLACES
        ) and computed_total.quantize(TWO_DECIMAL_PLACES) == total.quantize(TWO_DECIMAL_PLACES)

    def __repr__(self) -> str:
        return "TotalsMatchComputedSum()"
