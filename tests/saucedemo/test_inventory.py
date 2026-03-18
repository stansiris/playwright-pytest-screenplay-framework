from decimal import Decimal

import pytest

from examples.saucedemo.questions.on_inventory_page import OnInventoryPage
from examples.saucedemo.questions.on_login_page import OnLoginPage
from examples.saucedemo.tasks.add_product_to_cart import AddProductToCart
from examples.saucedemo.tasks.login import Login
from examples.saucedemo.tasks.logout import Logout
from examples.saucedemo.tasks.open_product_details import OpenProductDetails
from examples.saucedemo.tasks.open_saucedemo import OpenSauceDemo
from examples.saucedemo.tasks.remove_product_from_cart import RemoveProductFromCart
from examples.saucedemo.tasks.return_to_products import ReturnToProducts
from examples.saucedemo.tasks.sort_inventory import SortInventory
from examples.saucedemo.ui.components.app_shell import AppShell
from examples.saucedemo.ui.components.back_navigation import BackNavigation
from examples.saucedemo.ui.pages.inventory_page import InventoryPage
from examples.saucedemo.ui.pages.login_page import LoginPage
from screenplay_core.core.actor import Actor
from screenplay_core.playwright.ensure import Ensure
from screenplay_core.playwright.questions.current_url import CurrentUrl
from screenplay_core.playwright.questions.texts_of import TextsOf

INVENTORY_ITEM_COUNT = 6


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


def parse_price(text: str) -> Decimal:
    return Decimal(text.replace("$", "").strip())


def ensure_cart_badge_count(customer: Actor, count: int) -> None:
    if count == 0:
        customer.attempts_to(Ensure.that(AppShell.SHOPPING_CART_BADGE).to_have_count(0))
        return
    customer.attempts_to(Ensure.that(AppShell.SHOPPING_CART_BADGE).to_have_text(str(count)))


@pytest.mark.smoke
@pytest.mark.integration
def test_inventory_page_loads_after_successful_login(customer_on_inventory: Actor) -> None:
    """Verify login lands on inventory and key page shell elements are visible."""
    customer = customer_on_inventory
    customer.attempts_to(
        Ensure.that(InventoryPage.INVENTORY_CONTAINER).to_be_visible(),
        Ensure.that(AppShell.SHOPPING_CART_LINK).to_be_visible(),
    )
    assert customer.asks_for(CurrentUrl()).endswith("/inventory.html")


@pytest.mark.integration
def test_inventory_displays_expected_products_and_controls(customer_on_inventory: Actor) -> None:
    """Verify inventory renders expected item counts and add-to-cart controls."""
    customer = customer_on_inventory
    customer.attempts_to(
        Ensure.that(InventoryPage.INVENTORY_ITEM_NAMES).to_have_count(INVENTORY_ITEM_COUNT),
        Ensure.that(InventoryPage.INVENTORY_ITEM_PRICES).to_have_count(INVENTORY_ITEM_COUNT),
        Ensure.that(InventoryPage.INVENTORY_ADD_TO_CART_BUTTONS).to_have_count(
            INVENTORY_ITEM_COUNT
        ),
    )


@pytest.mark.integration
def test_inventory_add_and_remove_single_item_updates_badge(customer_on_inventory: Actor) -> None:
    """Verify adding then removing one item updates cart badge and button state."""
    customer = customer_on_inventory
    product_name = "Sauce Labs Backpack"
    product_button = InventoryPage.inventory_item_action_button_for(product_name)
    customer.attempts_to(AddProductToCart.named(product_name))
    ensure_cart_badge_count(customer, 1)
    customer.attempts_to(
        Ensure.that(product_button).to_have_text("Remove"),
        RemoveProductFromCart.named(product_name),
    )
    ensure_cart_badge_count(customer, 0)
    customer.attempts_to(Ensure.that(product_button).to_have_text("Add to cart"))


@pytest.mark.integration
@pytest.mark.parametrize(
    "product_names, expected_badge_count",
    [
        (["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"], 3),
        (["Sauce Labs Fleece Jacket", "Sauce Labs Onesie"], 2),
    ],
)
def test_inventory_add_multiple_items_updates_badge_count(
    customer_on_inventory: Actor, product_names: list[str], expected_badge_count: int
) -> None:
    """Verify adding multiple items sets cart badge to the expected count."""
    customer = customer_on_inventory
    for product_name in product_names:
        customer.attempts_to(AddProductToCart.named(product_name))
    ensure_cart_badge_count(customer, expected_badge_count)


@pytest.mark.integration
def test_inventory_sorting_by_name_and_price(customer_on_inventory: Actor) -> None:
    """Verify name and price sorting options order inventory items correctly."""
    customer = customer_on_inventory
    customer.attempts_to(SortInventory.by("Name (Z to A)"))
    names_z_to_a = customer.asks_for(TextsOf(InventoryPage.INVENTORY_ITEM_NAMES))
    assert names_z_to_a == sorted(names_z_to_a, reverse=True)
    customer.attempts_to(SortInventory.by("Price (low to high)"))
    price_texts_low_to_high = customer.asks_for(TextsOf(InventoryPage.INVENTORY_ITEM_PRICES))
    prices_low_to_high = [parse_price(text) for text in price_texts_low_to_high]
    assert prices_low_to_high == sorted(prices_low_to_high)
    customer.attempts_to(SortInventory.by("Price (high to low)"))
    price_texts_high_to_low = customer.asks_for(TextsOf(InventoryPage.INVENTORY_ITEM_PRICES))
    prices_high_to_low = [parse_price(text) for text in price_texts_high_to_low]
    assert prices_high_to_low == sorted(prices_high_to_low, reverse=True)


@pytest.mark.integration
def test_inventory_product_details_and_back_preserves_cart(customer_on_inventory: Actor) -> None:
    """Verify navigating to details and back keeps inventory state and cart contents."""
    customer = customer_on_inventory
    product_name = "Sauce Labs Bike Light"
    customer.attempts_to(
        AddProductToCart.named(product_name), OpenProductDetails.named(product_name)
    )
    assert "inventory-item.html" in customer.asks_for(CurrentUrl())
    customer.attempts_to(
        Ensure.that(BackNavigation.BACK_TO_PRODUCTS).to_be_visible(),
        ReturnToProducts(),
        Ensure.that(InventoryPage.INVENTORY_CONTAINER).to_be_visible(),
    )
    assert customer.asks_for(OnInventoryPage())
    ensure_cart_badge_count(customer, 1)


@pytest.mark.integration
def test_inventory_logout_returns_to_login_page(customer_on_inventory: Actor) -> None:
    """Verify logout from inventory returns the user to the login page."""
    customer = customer_on_inventory
    customer.attempts_to(Logout())
    assert customer.asks_for(OnLoginPage())
