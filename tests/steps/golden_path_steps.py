from collections import Counter

from pytest_bdd import given, parsers, then, when

from screenplay.interactions.wait_until_visible import WaitUntilVisible
from screenplay.questions.cart_badge_count import CartBadgeCount
from screenplay.questions.text_of import TextOf
from screenplay.questions.texts_of import TextsOf
from screenplay.questions.totals_match_computed_sum import TotalsMatchComputedSum
from screenplay.tasks.add_product_to_cart import AddProductToCart
from screenplay.tasks.complete_checkout import CompleteCheckout
from screenplay.tasks.continue_checkout import ContinueCheckout
from screenplay.tasks.enter_checkout_information import EnterCheckoutInformation
from screenplay.tasks.go_to_cart import GoToCart
from screenplay.tasks.login import Login
from screenplay.tasks.open_saucedemo import OpenSauceDemo
from screenplay.tasks.proceed_to_checkout import ProceedToCheckout
from screenplay.tasks.return_to_products import ReturnToProducts
from screenplay.tasks.sort_inventory import SortInventory
from screenplay.ui.saucedemo import SauceDemo
from tests.steps.table_utils import as_row_dicts


def _expected_items(datatable) -> list[str]:
    return [row["item_name"] for row in as_row_dicts(datatable)]


@given("I open the SauceDemo application")
def open_saucedemo(customer) -> None:
    customer.attempts_to(
        OpenSauceDemo.app(),
        WaitUntilVisible.for_(SauceDemo.LOGIN_BUTTON),
    )


@when(parsers.parse('I log in with username "{username}" and password "{password}"'))
def login_with_credentials(customer, username: str, password: str) -> None:
    customer.attempts_to(Login.with_credentials(username, password))


@when(parsers.parse('I sort inventory by "{option}"'))
def sort_inventory(customer, option: str) -> None:
    customer.attempts_to(SortInventory.by(option))


@when("I add the following items to the cart:")
def add_items_to_cart(customer, datatable) -> None:
    for item_name in _expected_items(datatable):
        customer.attempts_to(AddProductToCart.named(item_name))


@then(parsers.parse("the cart badge count should be {count:d}"))
def cart_badge_count_should_be(customer, count: int) -> None:
    assert customer.asks_for(CartBadgeCount()) == count


@when("I go to the cart")
def go_to_cart(customer) -> None:
    customer.attempts_to(GoToCart())


@then("the cart should contain the following items:")
def cart_should_contain_items(customer, datatable) -> None:
    expected_items = _expected_items(datatable)
    actual_items = customer.asks_for(TextsOf(SauceDemo.CART_ITEM_NAMES))
    assert Counter(actual_items) == Counter(expected_items)


@then(parsers.parse("the cart item count should be {count:d}"))
def cart_item_count_should_be(customer, count: int) -> None:
    assert len(customer.asks_for(TextsOf(SauceDemo.CART_ITEM_NAMES))) == count


@when("I proceed to checkout")
def proceed_to_checkout(customer) -> None:
    customer.attempts_to(ProceedToCheckout())


@when("I enter checkout information:")
def enter_checkout_information(customer, datatable) -> None:
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
def continue_checkout(customer) -> None:
    customer.attempts_to(ContinueCheckout())


@then("the overview should contain the following items:")
def overview_should_contain_items(customer, datatable) -> None:
    expected_items = _expected_items(datatable)
    actual_items = customer.asks_for(TextsOf(SauceDemo.CHECKOUT_OVERVIEW_ITEM_NAMES))
    assert Counter(actual_items) == Counter(expected_items)


@then(parsers.parse('the payment information should be "{text}"'))
def payment_information_should_be(customer, text: str) -> None:
    assert customer.asks_for(TextOf(SauceDemo.CHECKOUT_PAYMENT_INFO)) == text


@then(parsers.parse('the shipping information should be "{text}"'))
def shipping_information_should_be(customer, text: str) -> None:
    assert customer.asks_for(TextOf(SauceDemo.CHECKOUT_SHIPPING_INFO)) == text


@then("totals should match the computed sum")
def totals_should_match(customer) -> None:
    assert customer.asks_for(TotalsMatchComputedSum())


@when("I finish checkout")
def finish_checkout(customer) -> None:
    customer.attempts_to(CompleteCheckout())


@then("I should see a checkout complete confirmation")
def should_see_checkout_complete_confirmation(customer) -> None:
    customer.attempts_to(WaitUntilVisible.for_(SauceDemo.CHECKOUT_COMPLETE_TITLE))
    assert customer.asks_for(TextOf(SauceDemo.CHECKOUT_COMPLETE_TITLE)) == "Checkout: Complete!"


@when("I return home to the inventory")
def return_home_to_inventory(customer) -> None:
    customer.attempts_to(
        ReturnToProducts(),
        WaitUntilVisible.for_(SauceDemo.INVENTORY_CONTAINER),
    )
