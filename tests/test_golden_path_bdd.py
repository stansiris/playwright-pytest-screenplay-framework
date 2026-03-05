from collections import Counter
from collections.abc import Sequence

from pytest_bdd import given, parsers, scenario, then, when

from saucedemo.questions.cart_badge_count import CartBadgeCount
from saucedemo.questions.on_inventory_page import OnInventoryPage
from saucedemo.questions.totals_match_computed_sum import TotalsMatchComputedSum
from saucedemo.tasks.add_product_to_cart import AddProductToCart
from saucedemo.tasks.complete_checkout import CompleteCheckout
from saucedemo.tasks.continue_checkout import ContinueCheckout
from saucedemo.tasks.enter_checkout_information import EnterCheckoutInformation
from saucedemo.tasks.go_to_cart import GoToCart
from saucedemo.tasks.login import Login
from saucedemo.tasks.open_login_page import OpenLoginPage
from saucedemo.tasks.proceed_to_checkout import ProceedToCheckout
from saucedemo.tasks.return_to_products import ReturnToProducts
from saucedemo.ui.saucedemo import SauceDemo
from screenplay_core.core.actor import Actor
from screenplay_core.interactions.wait_until_visible import WaitUntilVisible
from screenplay_core.questions.text_of import TextOf
from screenplay_core.questions.texts_of import TextsOf


@scenario(
    "features/golden_path.feature",
    "Successful purchase of multiple items and cart resets after checkout",
)
def test_successful_purchase_of_multiple_items_and_cart_resets_after_checkout() -> None:
    """Run the golden-path BDD scenario for multi-item purchase through completion."""
    pass


def as_row_dicts(datatable: Sequence[Sequence[object]]) -> list[dict[str, str]]:
    if not datatable:
        return []

    headers = [str(cell).strip() for cell in datatable[0]]
    if not headers:
        raise ValueError("Datatable must include at least one header column.")
    if any(not header for header in headers):
        raise ValueError(f"Datatable headers cannot be empty: {headers}")

    duplicate_headers = [header for header, count in Counter(headers).items() if count > 1]
    if duplicate_headers:
        raise ValueError(f"Datatable headers must be unique: {duplicate_headers}")

    row_dicts: list[dict[str, str]] = []

    for row_number, row in enumerate(datatable[1:], start=2):
        values = [str(cell).strip() for cell in row]
        if len(values) != len(headers):
            raise ValueError(
                "Malformed datatable row "
                f"{row_number}: expected {len(headers)} column(s) {headers}, "
                f"got {len(values)} value(s) {values}."
            )

        row_dicts.append(dict(zip(headers, values, strict=True)))

    return row_dicts


def _expected_items(datatable) -> list[str]:
    return [row["item_name"] for row in as_row_dicts(datatable)]


@given("I open the SauceDemo application")
def open_saucedemo(customer: Actor) -> None:
    customer.attempts_to(
        OpenLoginPage(),
    )


@when(parsers.parse('I log in with username "{username}" and password "{password}"'))
def login_with_credentials(customer: Actor, username: str, password: str) -> None:
    customer.attempts_to(Login.with_credentials(username, password))


@then("I should be on the inventory page")
def should_be_on_inventory_page(customer: Actor) -> None:
    customer.attempts_to(WaitUntilVisible.for_(SauceDemo.INVENTORY_CONTAINER))
    assert customer.asks_for(OnInventoryPage())


@when("I add the following items to the cart:")
def add_items_to_cart(customer: Actor, datatable) -> None:
    for item_name in _expected_items(datatable):
        customer.attempts_to(AddProductToCart.named(item_name))


@then(parsers.parse("the cart badge count should be {count:d}"))
def cart_badge_count_should_be(customer: Actor, count: int) -> None:
    assert customer.asks_for(CartBadgeCount()) == count


@when("I go to the cart")
def go_to_cart(customer: Actor) -> None:
    customer.attempts_to(GoToCart())


@then("the cart should contain the following items:")
def cart_should_contain_items(customer: Actor, datatable) -> None:
    expected_items = _expected_items(datatable)
    actual_items = customer.asks_for(TextsOf(SauceDemo.CART_ITEM_NAMES))
    assert Counter(actual_items) == Counter(expected_items)


@then(parsers.parse("the cart item count should be {count:d}"))
def cart_item_count_should_be(customer: Actor, count: int) -> None:
    assert len(customer.asks_for(TextsOf(SauceDemo.CART_ITEM_NAMES))) == count


@when("I proceed to checkout")
def proceed_to_checkout(customer: Actor) -> None:
    customer.attempts_to(ProceedToCheckout())


@when("I enter checkout information:")
def enter_checkout_information(customer: Actor, datatable) -> None:
    rows = as_row_dicts(datatable)
    if len(rows) != 1:
        raise ValueError("Checkout information table must contain exactly one data row.")

    checkout = rows[0]
    customer.attempts_to(
        EnterCheckoutInformation.as_customer(
            checkout["first_name"],
            checkout["last_name"],
            checkout["postal_code"],
        )
    )


@when("I continue checkout")
def continue_checkout(customer: Actor) -> None:
    customer.attempts_to(ContinueCheckout())


@then("the overview should contain the following items:")
def overview_should_contain_items(customer: Actor, datatable) -> None:
    expected_items = _expected_items(datatable)
    actual_items = customer.asks_for(TextsOf(SauceDemo.CHECKOUT_OVERVIEW_ITEM_NAMES))
    assert Counter(actual_items) == Counter(expected_items)


@then(parsers.parse('the payment information should be "{text}"'))
def payment_information_should_be(customer: Actor, text: str) -> None:
    assert customer.asks_for(TextOf(SauceDemo.CHECKOUT_PAYMENT_INFO)) == text


@then(parsers.parse('the shipping information should be "{text}"'))
def shipping_information_should_be(customer: Actor, text: str) -> None:
    assert customer.asks_for(TextOf(SauceDemo.CHECKOUT_SHIPPING_INFO)) == text


@then("totals should match the computed sum")
def totals_should_match(customer: Actor) -> None:
    assert customer.asks_for(TotalsMatchComputedSum())


@when("I finish checkout")
def finish_checkout(customer: Actor) -> None:
    customer.attempts_to(CompleteCheckout())


@then("I should see a checkout complete confirmation")
def should_see_checkout_complete_confirmation(customer: Actor) -> None:
    customer.attempts_to(WaitUntilVisible.for_(SauceDemo.CHECKOUT_COMPLETE_TITLE))
    assert customer.asks_for(TextOf(SauceDemo.CHECKOUT_COMPLETE_TITLE)) == "Checkout: Complete!"


@when("I return home to the inventory")
def return_home_to_inventory(customer: Actor) -> None:
    customer.attempts_to(
        ReturnToProducts(),
        WaitUntilVisible.for_(SauceDemo.INVENTORY_CONTAINER),
    )
