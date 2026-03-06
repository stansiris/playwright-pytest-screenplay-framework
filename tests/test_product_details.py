import pytest

from saucedemo.questions.cart_badge_count import CartBadgeCount
from saucedemo.questions.on_inventory_page import OnInventoryPage
from saucedemo.questions.on_login_page import OnLoginPage
from saucedemo.tasks.add_product_to_cart import AddProductToCart
from saucedemo.tasks.go_to_cart import GoToCart
from saucedemo.tasks.login import Login
from saucedemo.tasks.open_login_page import OpenLoginPage
from saucedemo.tasks.open_product_details import OpenProductDetails
from saucedemo.tasks.open_product_details_by_id import OpenProductDetailsById
from saucedemo.tasks.return_to_products import ReturnToProducts
from saucedemo.tasks.toggle_product_details_cart_action import ToggleProductDetailsCartAction
from saucedemo.tasks.wait_for_inventory_page import WaitForInventoryPage
from saucedemo.ui.components.back_navigation import BackNavigation
from saucedemo.ui.pages.cart_page import CartPage
from saucedemo.ui.pages.inventory_page import InventoryPage
from saucedemo.ui.pages.product_details_page import ProductDetailsPage
from screenplay_core.core.actor import Actor
from screenplay_core.questions.current_url import CurrentUrl
from screenplay_core.questions.text_of import TextOf
from screenplay_core.questions.texts_of import TextsOf

PRODUCT_NAME = "Sauce Labs Backpack"
PRODUCT_ID = 4


@pytest.fixture
def customer_on_inventory(customer: Actor) -> Actor:
    customer.attempts_to(
        OpenLoginPage(),
        Login.with_credentials("standard_user", "secret_sauce"),
        WaitForInventoryPage(),
    )
    assert customer.asks_for(OnInventoryPage())
    return customer


def open_product_details(customer: Actor, product_name: str) -> None:
    customer.attempts_to(OpenProductDetails.named(product_name))
    customer.expect(ProductDetailsPage.PRODUCT_DETAILS_ACTION_BUTTON).to_be_visible()
    assert "inventory-item.html" in customer.asks_for(CurrentUrl())


@pytest.mark.smoke
@pytest.mark.integration
def test_product_details_open_from_inventory(customer_on_inventory: Actor) -> None:
    """Verify a product details page opens from inventory with expected primary elements."""
    customer = customer_on_inventory
    open_product_details(customer, PRODUCT_NAME)

    customer.expect(ProductDetailsPage.PRODUCT_DETAILS_NAME).to_be_visible()
    customer.expect(ProductDetailsPage.PRODUCT_DETAILS_ACTION_BUTTON).to_be_visible()
    assert customer.asks_for(TextOf(ProductDetailsPage.PRODUCT_DETAILS_NAME)) == PRODUCT_NAME


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

    assert customer.asks_for(TextOf(ProductDetailsPage.PRODUCT_DETAILS_NAME)) == expected_name
    assert customer.asks_for(TextOf(ProductDetailsPage.PRODUCT_DETAILS_PRICE)) == expected_price
    assert (
        customer.asks_for(TextOf(ProductDetailsPage.PRODUCT_DETAILS_DESCRIPTION))
        == expected_description
    )


@pytest.mark.integration
def test_product_details_add_to_cart_updates_badge(customer_on_inventory: Actor) -> None:
    """Verify adding item from details increments cart badge and toggles button to Remove."""
    customer = customer_on_inventory
    open_product_details(customer, PRODUCT_NAME)

    customer.attempts_to(ToggleProductDetailsCartAction())
    assert customer.asks_for(CartBadgeCount()) == 1
    customer.expect(ProductDetailsPage.PRODUCT_DETAILS_ACTION_BUTTON).to_have_text("Remove")


@pytest.mark.integration
def test_product_details_remove_from_cart_updates_badge(customer_on_inventory: Actor) -> None:
    """Verify removing item from details clears cart badge and restores Add to cart button."""
    customer = customer_on_inventory
    open_product_details(customer, PRODUCT_NAME)

    customer.attempts_to(ToggleProductDetailsCartAction())
    customer.attempts_to(ToggleProductDetailsCartAction())
    assert customer.asks_for(CartBadgeCount()) == 0
    customer.expect(ProductDetailsPage.PRODUCT_DETAILS_ACTION_BUTTON).to_have_text("Add to cart")


@pytest.mark.integration
def test_product_details_back_to_products_preserves_cart(customer_on_inventory: Actor) -> None:
    """Verify back-to-products returns to inventory while preserving cart state."""
    customer = customer_on_inventory
    open_product_details(customer, PRODUCT_NAME)
    customer.attempts_to(ToggleProductDetailsCartAction())

    customer.attempts_to(
        ReturnToProducts(),
        WaitForInventoryPage(),
    )
    assert customer.asks_for(OnInventoryPage())
    assert customer.asks_for(CartBadgeCount()) == 1
    customer.expect(InventoryPage.inventory_item_action_button_for(PRODUCT_NAME)).to_have_text(
        "Remove"
    )


@pytest.mark.integration
def test_product_details_reflect_inventory_cart_state(customer_on_inventory: Actor) -> None:
    """Verify details action button reflects cart state set from inventory page."""
    customer = customer_on_inventory
    customer.attempts_to(AddProductToCart.named(PRODUCT_NAME))
    assert customer.asks_for(CartBadgeCount()) == 1

    open_product_details(customer, PRODUCT_NAME)
    customer.expect(ProductDetailsPage.PRODUCT_DETAILS_ACTION_BUTTON).to_have_text("Remove")


@pytest.mark.integration
def test_product_details_add_then_cart_contains_item(customer_on_inventory: Actor) -> None:
    """Verify item added from details appears in the cart."""
    customer = customer_on_inventory
    open_product_details(customer, PRODUCT_NAME)
    customer.attempts_to(
        ToggleProductDetailsCartAction(),
        GoToCart(),
    )

    cart_items = customer.asks_for(TextsOf(CartPage.CART_ITEM_NAMES))
    assert PRODUCT_NAME in cart_items


@pytest.mark.integration
def test_product_details_direct_url_when_logged_in(
    customer_on_inventory: Actor,
) -> None:
    """Verify logged-in user can open product details directly by URL."""
    customer = customer_on_inventory
    customer.attempts_to(OpenProductDetailsById.with_id(PRODUCT_ID))

    customer.expect(BackNavigation.BACK_TO_PRODUCTS).to_be_visible()
    assert customer.asks_for(CurrentUrl()).endswith(f"/inventory-item.html?id={PRODUCT_ID}")


@pytest.mark.integration
def test_product_details_direct_url_redirects_to_login_when_logged_out(
    customer: Actor,
) -> None:
    """Verify logged-out access to details URL redirects to login page."""
    customer.attempts_to(OpenProductDetailsById.with_id(PRODUCT_ID))
    assert customer.asks_for(OnLoginPage())
