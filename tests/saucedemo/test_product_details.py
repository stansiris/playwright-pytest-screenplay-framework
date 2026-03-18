import pytest

from examples.saucedemo.questions.on_inventory_page import OnInventoryPage
from examples.saucedemo.questions.on_login_page import OnLoginPage
from examples.saucedemo.tasks.add_product_to_cart import AddProductToCart
from examples.saucedemo.tasks.go_to_cart import GoToCart
from examples.saucedemo.tasks.login import Login
from examples.saucedemo.tasks.open_product_details import OpenProductDetails
from examples.saucedemo.tasks.open_product_details_by_id import OpenProductDetailsById
from examples.saucedemo.tasks.open_saucedemo import OpenSauceDemo
from examples.saucedemo.tasks.return_to_products import ReturnToProducts
from examples.saucedemo.tasks.toggle_product_details_cart_action import (
    ToggleProductDetailsCartAction,
)
from examples.saucedemo.ui.components.app_shell import AppShell
from examples.saucedemo.ui.components.back_navigation import BackNavigation
from examples.saucedemo.ui.pages.cart_page import CartPage
from examples.saucedemo.ui.pages.inventory_page import InventoryPage
from examples.saucedemo.ui.pages.login_page import LoginPage
from examples.saucedemo.ui.pages.product_details_page import ProductDetailsPage
from screenplay_core.playwright.ensure import Ensure
from screenplay_core.core.actor import Actor
from screenplay_core.playwright.questions.current_url import CurrentUrl
from screenplay_core.playwright.questions.text_of import TextOf

PRODUCT_NAME = "Sauce Labs Backpack"
PRODUCT_ID = 4


@pytest.fixture
def customer_on_inventory(customer: Actor) -> Actor:
    customer.attempts_to(
        OpenSauceDemo.app(),
        Ensure.that(LoginPage.LOGIN_BUTTON).to_be_visible(),
        Login.with_credentials("standard_user", "secret_sauce"),
        Ensure.that(InventoryPage.INVENTORY_CONTAINER).to_be_visible(),
    )
    assert customer.asks_for(OnInventoryPage())
    return customer


def open_product_details(customer: Actor, product_name: str) -> None:
    customer.attempts_to(
        OpenProductDetails.named(product_name),
        Ensure.that(ProductDetailsPage.PRODUCT_DETAILS_ACTION_BUTTON).to_be_visible(),
    )
    assert "inventory-item.html" in customer.asks_for(CurrentUrl())


@pytest.mark.smoke
@pytest.mark.integration
def test_product_details_open_from_inventory(customer_on_inventory: Actor) -> None:
    """Verify a product details page opens from inventory with expected primary elements."""
    customer = customer_on_inventory
    open_product_details(customer, PRODUCT_NAME)
    customer.attempts_to(
        Ensure.that(ProductDetailsPage.PRODUCT_DETAILS_NAME).to_be_visible(),
        Ensure.that(ProductDetailsPage.PRODUCT_DETAILS_ACTION_BUTTON).to_be_visible(),
        Ensure.that(ProductDetailsPage.PRODUCT_DETAILS_NAME).to_have_text(PRODUCT_NAME),
    )


@pytest.mark.integration
def test_product_details_content_matches_inventory_card(customer_on_inventory: Actor) -> None:
    """Verify name, price, and description on details page match the inventory card."""
    customer = customer_on_inventory
    expected_name = customer.asks_for(TextOf(InventoryPage.inventory_item_name_for(PRODUCT_NAME)))
    expected_price = customer.asks_for(TextOf(InventoryPage.inventory_item_price_for(PRODUCT_NAME)))
    expected_description = customer.asks_for(
        TextOf(InventoryPage.inventory_item_description_for(PRODUCT_NAME))
    )
    open_product_details(customer, PRODUCT_NAME)
    customer.attempts_to(
        Ensure.that(ProductDetailsPage.PRODUCT_DETAILS_NAME).to_have_text(expected_name),
        Ensure.that(ProductDetailsPage.PRODUCT_DETAILS_PRICE).to_have_text(expected_price),
        Ensure.that(ProductDetailsPage.PRODUCT_DETAILS_DESCRIPTION).to_have_text(
            expected_description
        ),
    )


@pytest.mark.integration
def test_product_details_add_to_cart_updates_badge(customer_on_inventory: Actor) -> None:
    """Verify adding item from details increments cart badge and toggles button to Remove."""
    customer = customer_on_inventory
    open_product_details(customer, PRODUCT_NAME)
    customer.attempts_to(
        ToggleProductDetailsCartAction(),
        Ensure.that(AppShell.SHOPPING_CART_BADGE).to_have_text("1"),
        Ensure.that(ProductDetailsPage.PRODUCT_DETAILS_ACTION_BUTTON).to_have_text("Remove"),
    )


@pytest.mark.integration
def test_product_details_remove_from_cart_updates_badge(customer_on_inventory: Actor) -> None:
    """Verify removing item from details clears cart badge and restores Add to cart button."""
    customer = customer_on_inventory
    open_product_details(customer, PRODUCT_NAME)
    customer.attempts_to(
        ToggleProductDetailsCartAction(),
        ToggleProductDetailsCartAction(),
        Ensure.that(AppShell.SHOPPING_CART_BADGE).to_have_count(0),
        Ensure.that(ProductDetailsPage.PRODUCT_DETAILS_ACTION_BUTTON).to_have_text("Add to cart"),
    )


@pytest.mark.integration
def test_product_details_back_to_products_preserves_cart(customer_on_inventory: Actor) -> None:
    """Verify back-to-products returns to inventory while preserving cart state."""
    customer = customer_on_inventory
    open_product_details(customer, PRODUCT_NAME)
    customer.attempts_to(
        ToggleProductDetailsCartAction(),
        ReturnToProducts(),
        Ensure.that(InventoryPage.INVENTORY_CONTAINER).to_be_visible(),
    )
    assert customer.asks_for(OnInventoryPage())
    customer.attempts_to(
        Ensure.that(AppShell.SHOPPING_CART_BADGE).to_have_text("1"),
        Ensure.that(InventoryPage.inventory_item_action_button_for(PRODUCT_NAME)).to_have_text(
            "Remove"
        ),
    )


@pytest.mark.integration
def test_product_details_reflect_inventory_cart_state(customer_on_inventory: Actor) -> None:
    """Verify details action button reflects cart state set from inventory page."""
    customer = customer_on_inventory
    customer.attempts_to(
        AddProductToCart.named(PRODUCT_NAME),
        Ensure.that(AppShell.SHOPPING_CART_BADGE).to_have_text("1"),
    )
    open_product_details(customer, PRODUCT_NAME)
    customer.attempts_to(
        Ensure.that(ProductDetailsPage.PRODUCT_DETAILS_ACTION_BUTTON).to_have_text("Remove")
    )


@pytest.mark.integration
def test_product_details_add_then_cart_contains_item(customer_on_inventory: Actor) -> None:
    """Verify item added from details appears in the cart."""
    customer = customer_on_inventory
    open_product_details(customer, PRODUCT_NAME)
    customer.attempts_to(
        ToggleProductDetailsCartAction(),
        GoToCart(),
        Ensure.that(CartPage.CART_ITEM_NAMES).to_contain_text(PRODUCT_NAME),
    )


@pytest.mark.integration
def test_product_details_direct_url_when_logged_in(customer_on_inventory: Actor) -> None:
    """Verify logged-in user can open product details directly by URL."""
    customer = customer_on_inventory
    customer.attempts_to(
        OpenProductDetailsById.with_id(PRODUCT_ID),
        Ensure.that(BackNavigation.BACK_TO_PRODUCTS).to_be_visible(),
    )
    assert customer.asks_for(CurrentUrl()).endswith(f"/inventory-item.html?id={PRODUCT_ID}")


@pytest.mark.integration
def test_product_details_direct_url_redirects_to_login_when_logged_out(customer: Actor) -> None:
    """Verify logged-out access to details URL redirects to login page."""
    customer.attempts_to(OpenProductDetailsById.with_id(PRODUCT_ID))
    assert customer.asks_for(OnLoginPage())
