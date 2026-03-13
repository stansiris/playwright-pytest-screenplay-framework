import pytest

from examples.saucedemo.questions.on_inventory_page import OnInventoryPage
from examples.saucedemo.questions.on_login_page import OnLoginPage
from examples.saucedemo.tasks.add_product_to_cart import AddProductToCart
from examples.saucedemo.tasks.begin_checkout import BeginCheckout
from examples.saucedemo.tasks.complete_checkout import CompleteCheckout
from examples.saucedemo.tasks.go_to_cart import GoToCart
from examples.saucedemo.tasks.login import Login
from examples.saucedemo.tasks.open_checkout_complete_page import OpenCheckoutCompletePage
from examples.saucedemo.tasks.open_saucedemo import OpenSauceDemo
from examples.saucedemo.tasks.provide_checkout_information import ProvideCheckoutInformation
from examples.saucedemo.tasks.refresh_browser import RefreshBrowser
from examples.saucedemo.tasks.return_to_products import ReturnToProducts
from examples.saucedemo.ui.components.app_shell import AppShell
from examples.saucedemo.ui.pages.cart_page import CartPage
from examples.saucedemo.ui.pages.checkout_complete_page import CheckoutCompletePage
from examples.saucedemo.ui.pages.inventory_page import InventoryPage
from examples.saucedemo.ui.pages.login_page import LoginPage
from screenplay_core.consequences.ensure import Ensure
from screenplay_core.core.actor import Actor
from screenplay_core.questions.current_url import CurrentUrl

PRODUCT_NAMES = ["Sauce Labs Backpack", "Sauce Labs Bike Light"]
FIRST_NAME = "John"
LAST_NAME = "Doe"
POSTAL_CODE = "08873"


@pytest.fixture
def customer_on_checkout_complete(customer: Actor) -> Actor:
    activities = [
        OpenSauceDemo.app(),
        Ensure.that(LoginPage.LOGIN_BUTTON).to_be_visible(),
        Login.with_credentials("standard_user", "secret_sauce"),
    ]
    for product_name in PRODUCT_NAMES:
        activities.append(AddProductToCart.named(product_name))
    activities.extend(
        [
            BeginCheckout(),
            ProvideCheckoutInformation.as_customer(FIRST_NAME, LAST_NAME, POSTAL_CODE),
            CompleteCheckout(),
            Ensure.that(CheckoutCompletePage.CHECKOUT_COMPLETE_TITLE).to_be_visible(),
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
    customer.attempts_to(
        Ensure.that(CheckoutCompletePage.CHECKOUT_COMPLETE_TITLE).to_have_text(
            "Checkout: Complete!"
        ),
        Ensure.that(CheckoutCompletePage.CHECKOUT_COMPLETE_HEADER).to_have_text(
            "Thank you for your order!"
        ),
        Ensure.that(CheckoutCompletePage.CHECKOUT_COMPLETE_TEXT).to_contain_text("dispatched"),
        Ensure.that(CheckoutCompletePage.CHECKOUT_COMPLETE_PONY_IMAGE).to_be_visible(),
    )


@pytest.mark.integration
def test_checkout_complete_has_empty_cart_badge(customer_on_checkout_complete: Actor) -> None:
    """Verify cart badge is empty after checkout is completed."""
    customer = customer_on_checkout_complete
    customer.attempts_to(Ensure.that(AppShell.SHOPPING_CART_BADGE).to_have_count(0))


@pytest.mark.integration
def test_checkout_complete_return_to_products_keeps_cart_empty(
    customer_on_checkout_complete: Actor,
) -> None:
    """Verify returning to inventory from complete page keeps cart empty."""
    customer = customer_on_checkout_complete
    customer.attempts_to(
        ReturnToProducts(),
        Ensure.that(InventoryPage.INVENTORY_CONTAINER).to_be_visible(),
    )
    assert customer.asks_for(OnInventoryPage())
    customer.attempts_to(Ensure.that(AppShell.SHOPPING_CART_BADGE).to_have_count(0))


@pytest.mark.integration
def test_checkout_complete_return_to_inventory_then_cart_is_empty(
    customer_on_checkout_complete: Actor,
) -> None:
    """Verify cart remains empty after returning to inventory and reopening cart."""
    customer = customer_on_checkout_complete
    customer.attempts_to(
        ReturnToProducts(),
        Ensure.that(InventoryPage.INVENTORY_CONTAINER).to_be_visible(),
        GoToCart(),
    )
    assert customer.asks_for(CurrentUrl()).endswith("/cart.html")
    customer.attempts_to(
        Ensure.that(AppShell.SHOPPING_CART_BADGE).to_have_count(0),
        Ensure.that(CartPage.CART_ITEM_NAMES).to_have_count(0),
    )


@pytest.mark.integration
def test_checkout_complete_refresh_keeps_confirmation_visible(
    customer_on_checkout_complete: Actor,
) -> None:
    """Verify browser refresh on complete page preserves completion state."""
    customer = customer_on_checkout_complete
    customer.attempts_to(
        RefreshBrowser(),
        Ensure.that(CheckoutCompletePage.CHECKOUT_COMPLETE_TITLE).to_be_visible(),
        Ensure.that(CheckoutCompletePage.CHECKOUT_COMPLETE_TITLE).to_have_text(
            "Checkout: Complete!"
        ),
        Ensure.that(AppShell.SHOPPING_CART_BADGE).to_have_count(0),
    )


@pytest.mark.integration
def test_checkout_complete_direct_url_redirects_to_login_when_logged_out(customer: Actor) -> None:
    """Verify logged-out access to complete page URL redirects to login page."""
    customer.attempts_to(OpenCheckoutCompletePage())
    assert customer.asks_for(OnLoginPage())
