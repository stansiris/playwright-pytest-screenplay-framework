import pytest

from saucedemo.questions.cart_badge_count import CartBadgeCount
from saucedemo.questions.on_inventory_page import OnInventoryPage
from saucedemo.questions.on_login_page import OnLoginPage
from saucedemo.tasks.add_product_to_cart import AddProductToCart
from saucedemo.tasks.begin_checkout import BeginCheckout
from saucedemo.tasks.complete_checkout import CompleteCheckout
from saucedemo.tasks.go_to_cart import GoToCart
from saucedemo.tasks.login import Login
from saucedemo.tasks.open_login_page import OpenLoginPage
from saucedemo.tasks.provide_checkout_information import ProvideCheckoutInformation
from saucedemo.tasks.return_to_products import ReturnToProducts
from saucedemo.ui.pages.cart_page import CartPage
from saucedemo.ui.pages.checkout_complete_page import CheckoutCompletePage
from saucedemo.ui.pages.inventory_page import InventoryPage
from screenplay_core.core.actor import Actor
from screenplay_core.interactions.navigate_to import NavigateTo
from screenplay_core.interactions.refresh_page import RefreshPage
from screenplay_core.interactions.wait_until_visible import WaitUntilVisible
from screenplay_core.questions.current_url import CurrentUrl
from screenplay_core.questions.text_of import TextOf
from screenplay_core.questions.texts_of import TextsOf

PRODUCT_NAMES = ["Sauce Labs Backpack", "Sauce Labs Bike Light"]
FIRST_NAME = "John"
LAST_NAME = "Doe"
POSTAL_CODE = "08873"


@pytest.fixture
def customer_on_checkout_complete(customer: Actor) -> Actor:
    activities = [
        OpenLoginPage(),
        Login.with_credentials("standard_user", "secret_sauce"),
    ]
    for product_name in PRODUCT_NAMES:
        activities.append(AddProductToCart.named(product_name))
    activities.extend(
        [
            BeginCheckout(),
            ProvideCheckoutInformation.as_customer(FIRST_NAME, LAST_NAME, POSTAL_CODE),
            CompleteCheckout(),
            WaitUntilVisible.for_(CheckoutCompletePage.CHECKOUT_COMPLETE_TITLE),
        ]
    )
    customer.attempts_to(*activities)

    assert customer.asks_for(CurrentUrl()).endswith("/checkout-complete.html")
    return customer


@pytest.mark.smoke
@pytest.mark.integration
def test_checkout_complete_confirmation_is_visible(customer_on_checkout_complete: Actor) -> None:
    """Verify checkout completion page shows confirmation text and image."""
    customer = customer_on_checkout_complete
    customer.expect(CheckoutCompletePage.CHECKOUT_COMPLETE_TITLE).to_have_text(
        "Checkout: Complete!"
    )
    customer.expect(CheckoutCompletePage.CHECKOUT_COMPLETE_HEADER).to_have_text(
        "Thank you for your order!"
    )
    customer.expect(CheckoutCompletePage.CHECKOUT_COMPLETE_TEXT).to_contain_text("dispatched")
    customer.expect(CheckoutCompletePage.CHECKOUT_COMPLETE_PONY_IMAGE).to_be_visible()


@pytest.mark.integration
def test_checkout_complete_has_empty_cart_badge(customer_on_checkout_complete: Actor) -> None:
    """Verify cart badge is empty after checkout is completed."""
    customer = customer_on_checkout_complete
    assert customer.asks_for(CartBadgeCount()) == 0


@pytest.mark.integration
def test_checkout_complete_return_to_products_keeps_cart_empty(
    customer_on_checkout_complete: Actor,
) -> None:
    """Verify returning to inventory from complete page keeps cart empty."""
    customer = customer_on_checkout_complete
    customer.attempts_to(
        ReturnToProducts(),
        WaitUntilVisible.for_(InventoryPage.INVENTORY_CONTAINER),
    )

    assert customer.asks_for(OnInventoryPage())
    assert customer.asks_for(CartBadgeCount()) == 0


@pytest.mark.integration
def test_checkout_complete_return_to_inventory_then_cart_is_empty(
    customer_on_checkout_complete: Actor,
) -> None:
    """Verify cart remains empty after returning to inventory and reopening cart."""
    customer = customer_on_checkout_complete
    customer.attempts_to(
        ReturnToProducts(),
        WaitUntilVisible.for_(InventoryPage.INVENTORY_CONTAINER),
        GoToCart(),
    )

    assert customer.asks_for(CurrentUrl()).endswith("/cart.html")
    assert customer.asks_for(CartBadgeCount()) == 0
    assert customer.asks_for(TextsOf(CartPage.CART_ITEM_NAMES)) == []


@pytest.mark.integration
def test_checkout_complete_refresh_keeps_confirmation_visible(
    customer_on_checkout_complete: Actor,
) -> None:
    """Verify browser refresh on complete page preserves completion state."""
    customer = customer_on_checkout_complete
    customer.attempts_to(
        RefreshPage(), WaitUntilVisible.for_(CheckoutCompletePage.CHECKOUT_COMPLETE_TITLE)
    )

    assert (
        customer.asks_for(TextOf(CheckoutCompletePage.CHECKOUT_COMPLETE_TITLE))
        == "Checkout: Complete!"
    )
    assert customer.asks_for(CartBadgeCount()) == 0


@pytest.mark.integration
def test_checkout_complete_direct_url_redirects_to_login_when_logged_out(
    customer: Actor, base_url: str
) -> None:
    """Verify logged-out access to complete page URL redirects to login page."""
    customer.attempts_to(NavigateTo(f"{base_url}checkout-complete.html"))
    assert customer.asks_for(OnLoginPage())
