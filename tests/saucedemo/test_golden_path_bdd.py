from collections import Counter
from collections.abc import Sequence

from pytest_bdd import given, parsers, scenario, then, when

from examples.saucedemo.questions.on_inventory_page import OnInventoryPage
from examples.saucedemo.questions.totals_match_computed_sum import TotalsMatchComputedSum
from examples.saucedemo.tasks.add_product_to_cart import AddProductToCart
from examples.saucedemo.tasks.complete_checkout import CompleteCheckout
from examples.saucedemo.tasks.continue_checkout import ContinueCheckout
from examples.saucedemo.tasks.enter_checkout_information import EnterCheckoutInformation
from examples.saucedemo.tasks.go_to_cart import GoToCart
from examples.saucedemo.tasks.login import Login
from examples.saucedemo.tasks.open_saucedemo import OpenSauceDemo
from examples.saucedemo.tasks.proceed_to_checkout import ProceedToCheckout
from examples.saucedemo.tasks.return_to_products import ReturnToProducts
from examples.saucedemo.ui.components.app_shell import AppShell
from examples.saucedemo.ui.pages.cart_page import CartPage
from examples.saucedemo.ui.pages.checkout_complete_page import CheckoutCompletePage
from examples.saucedemo.ui.pages.checkout_overview_page import CheckoutOverviewPage
from examples.saucedemo.ui.pages.inventory_page import InventoryPage
from examples.saucedemo.ui.pages.login_page import LoginPage
from screenplay_core.consequences.ensure import Ensure
from screenplay_core.core.actor import Actor
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
        OpenSauceDemo.app(),
        Ensure.that(LoginPage.LOGIN_BUTTON).to_be_visible(),
    )


@when(parsers.parse('I log in with username "{username}" and password "{password}"'))
def login_with_credentials(customer: Actor, username: str, password: str) -> None:
    customer.attempts_to(Login.with_credentials(username, password))


@then("I should be on the inventory page")
def should_be_on_inventory_page(customer: Actor) -> None:
    customer.attempts_to(Ensure.that(InventoryPage.INVENTORY_CONTAINER).to_be_visible())
    assert customer.asks_for(OnInventoryPage())


@when("I add the following items to the cart:")
def add_items_to_cart(customer: Actor, datatable) -> None:
    for item_name in _expected_items(datatable):
        customer.attempts_to(AddProductToCart.named(item_name))


@then(parsers.parse("the cart badge count should be {count:d}"))
def cart_badge_count_should_be(customer: Actor, count: int) -> None:
    if count == 0:
        customer.attempts_to(Ensure.that(AppShell.SHOPPING_CART_BADGE).to_have_count(0))
        return
    customer.attempts_to(Ensure.that(AppShell.SHOPPING_CART_BADGE).to_have_text(str(count)))


@when("I go to the cart")
def go_to_cart(customer: Actor) -> None:
    customer.attempts_to(GoToCart())


@then("the cart should contain the following items:")
def cart_should_contain_items(customer: Actor, datatable) -> None:
    expected_items = _expected_items(datatable)
    actual_items = customer.asks_for(TextsOf(CartPage.CART_ITEM_NAMES))
    assert Counter(actual_items) == Counter(expected_items)


@then(parsers.parse("the cart item count should be {count:d}"))
def cart_item_count_should_be(customer: Actor, count: int) -> None:
    customer.attempts_to(Ensure.that(CartPage.CART_ITEM_NAMES).to_have_count(count))


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
    actual_items = customer.asks_for(TextsOf(CheckoutOverviewPage.CHECKOUT_OVERVIEW_ITEM_NAMES))
    assert Counter(actual_items) == Counter(expected_items)


@then(parsers.parse('the payment information should be "{text}"'))
def payment_information_should_be(customer: Actor, text: str) -> None:
    customer.attempts_to(Ensure.that(CheckoutOverviewPage.CHECKOUT_PAYMENT_INFO).to_have_text(text))


@then(parsers.parse('the shipping information should be "{text}"'))
def shipping_information_should_be(customer: Actor, text: str) -> None:
    customer.attempts_to(
        Ensure.that(CheckoutOverviewPage.CHECKOUT_SHIPPING_INFO).to_have_text(text)
    )


@then("totals should match the computed sum")
def totals_should_match(customer: Actor) -> None:
    assert customer.asks_for(TotalsMatchComputedSum())


@when("I finish checkout")
def finish_checkout(customer: Actor) -> None:
    customer.attempts_to(CompleteCheckout())


@then("I should see a checkout complete confirmation")
def should_see_checkout_complete_confirmation(customer: Actor) -> None:
    customer.attempts_to(
        Ensure.that(CheckoutCompletePage.CHECKOUT_COMPLETE_TITLE).to_be_visible(),
        Ensure.that(CheckoutCompletePage.CHECKOUT_COMPLETE_TITLE).to_have_text(
            "Checkout: Complete!"
        ),
    )


@when("I return home to the inventory")
def return_home_to_inventory(customer: Actor) -> None:
    customer.attempts_to(
        ReturnToProducts(),
        Ensure.that(InventoryPage.INVENTORY_CONTAINER).to_be_visible(),
    )
