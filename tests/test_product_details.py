import re

import pytest

from saucedemo.questions.cart_badge_count import CartBadgeCount
from saucedemo.questions.on_inventory_page import OnInventoryPage
from saucedemo.questions.on_login_page import OnLoginPage
from saucedemo.tasks.add_product_to_cart import AddProductToCart
from saucedemo.tasks.login import Login
from saucedemo.tasks.open_login_page import OpenLoginPage
from saucedemo.ui.saucedemo import SauceDemo
from screenplay_core.core.actor import Actor
from screenplay_core.core.target import Target
from screenplay_core.interactions.click import Click
from screenplay_core.interactions.navigate_to import NavigateTo
from screenplay_core.interactions.wait_until_visible import WaitUntilVisible
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
        WaitUntilVisible.for_(SauceDemo.INVENTORY_CONTAINER),
    )
    assert customer.asks_for(OnInventoryPage())
    return customer


def inventory_item_name_target(product_name: str) -> Target:
    exact_name = re.compile(rf"^{re.escape(product_name)}$")
    return Target(
        f"Inventory item name '{product_name}'",
        lambda page: page.locator('[data-test="inventory-item-name"]', has_text=exact_name),
    )


def inventory_item_price_target(product_name: str) -> Target:
    exact_name = re.compile(rf"^{re.escape(product_name)}$")

    def locator(page):
        card = page.locator('[data-test="inventory-item"]').filter(
            has=page.locator('[data-test="inventory-item-name"]', has_text=exact_name),
        )
        return card.locator('[data-test="inventory-item-price"]')

    return Target(f"Inventory item price '{product_name}'", locator)


def inventory_item_description_target(product_name: str) -> Target:
    exact_name = re.compile(rf"^{re.escape(product_name)}$")

    def locator(page):
        card = page.locator('[data-test="inventory-item"]').filter(
            has=page.locator('[data-test="inventory-item-name"]', has_text=exact_name),
        )
        return card.locator('[data-test="inventory-item-desc"]')

    return Target(f"Inventory item description '{product_name}'", locator)


def inventory_item_action_button_target(product_name: str) -> Target:
    exact_name = re.compile(rf"^{re.escape(product_name)}$")

    def locator(page):
        card = page.locator('[data-test="inventory-item"]').filter(
            has=page.locator('[data-test="inventory-item-name"]', has_text=exact_name),
        )
        return card.locator("button")

    return Target(f"Inventory item action button '{product_name}'", locator)


PRODUCT_DETAILS_NAME = Target(
    "Product details name",
    lambda page: page.locator('[data-test="inventory-item-name"]'),
)
PRODUCT_DETAILS_PRICE = Target(
    "Product details price",
    lambda page: page.locator('[data-test="inventory-item-price"]'),
)
PRODUCT_DETAILS_DESCRIPTION = Target(
    "Product details description",
    lambda page: page.locator('[data-test="inventory-item-desc"]'),
)
PRODUCT_DETAILS_ACTION_BUTTON = Target(
    "Product details add/remove button",
    lambda page: page.locator('button[data-test^="add-to-cart"], button[data-test^="remove"]'),
)


def open_product_details(customer: Actor, product_name: str) -> None:
    customer.attempts_to(Click(inventory_item_name_target(product_name)))
    customer.expect(SauceDemo.BACK_TO_PRODUCTS).to_be_visible()
    assert "inventory-item.html" in customer.asks_for(CurrentUrl())


@pytest.mark.smoke
@pytest.mark.integration
def test_product_details_open_from_inventory(customer_on_inventory: Actor) -> None:
    customer = customer_on_inventory
    open_product_details(customer, PRODUCT_NAME)

    customer.expect(PRODUCT_DETAILS_NAME).to_be_visible()
    customer.expect(PRODUCT_DETAILS_ACTION_BUTTON).to_be_visible()
    assert customer.asks_for(TextOf(PRODUCT_DETAILS_NAME)) == PRODUCT_NAME


@pytest.mark.integration
def test_product_details_content_matches_inventory_card(customer_on_inventory: Actor) -> None:
    customer = customer_on_inventory
    expected_name = customer.asks_for(TextOf(inventory_item_name_target(PRODUCT_NAME)))
    expected_price = customer.asks_for(TextOf(inventory_item_price_target(PRODUCT_NAME)))
    expected_description = customer.asks_for(
        TextOf(inventory_item_description_target(PRODUCT_NAME))
    )

    open_product_details(customer, PRODUCT_NAME)

    assert customer.asks_for(TextOf(PRODUCT_DETAILS_NAME)) == expected_name
    assert customer.asks_for(TextOf(PRODUCT_DETAILS_PRICE)) == expected_price
    assert customer.asks_for(TextOf(PRODUCT_DETAILS_DESCRIPTION)) == expected_description


@pytest.mark.integration
def test_product_details_add_to_cart_updates_badge(customer_on_inventory: Actor) -> None:
    customer = customer_on_inventory
    open_product_details(customer, PRODUCT_NAME)

    customer.attempts_to(Click(PRODUCT_DETAILS_ACTION_BUTTON))
    assert customer.asks_for(CartBadgeCount()) == 1
    customer.expect(PRODUCT_DETAILS_ACTION_BUTTON).to_have_text("Remove")


@pytest.mark.integration
def test_product_details_remove_from_cart_updates_badge(customer_on_inventory: Actor) -> None:
    customer = customer_on_inventory
    open_product_details(customer, PRODUCT_NAME)

    customer.attempts_to(Click(PRODUCT_DETAILS_ACTION_BUTTON))
    customer.attempts_to(Click(PRODUCT_DETAILS_ACTION_BUTTON))
    assert customer.asks_for(CartBadgeCount()) == 0
    customer.expect(PRODUCT_DETAILS_ACTION_BUTTON).to_have_text("Add to cart")


@pytest.mark.integration
def test_product_details_back_to_products_preserves_cart(customer_on_inventory: Actor) -> None:
    customer = customer_on_inventory
    open_product_details(customer, PRODUCT_NAME)
    customer.attempts_to(Click(PRODUCT_DETAILS_ACTION_BUTTON))

    customer.attempts_to(
        Click(SauceDemo.BACK_TO_PRODUCTS),
        WaitUntilVisible.for_(SauceDemo.INVENTORY_CONTAINER),
    )
    assert customer.asks_for(OnInventoryPage())
    assert customer.asks_for(CartBadgeCount()) == 1
    customer.expect(inventory_item_action_button_target(PRODUCT_NAME)).to_have_text("Remove")


@pytest.mark.integration
def test_product_details_reflect_inventory_cart_state(customer_on_inventory: Actor) -> None:
    customer = customer_on_inventory
    customer.attempts_to(AddProductToCart.named(PRODUCT_NAME))
    assert customer.asks_for(CartBadgeCount()) == 1

    open_product_details(customer, PRODUCT_NAME)
    customer.expect(PRODUCT_DETAILS_ACTION_BUTTON).to_have_text("Remove")


@pytest.mark.integration
def test_product_details_add_then_cart_contains_item(customer_on_inventory: Actor) -> None:
    customer = customer_on_inventory
    open_product_details(customer, PRODUCT_NAME)
    customer.attempts_to(Click(PRODUCT_DETAILS_ACTION_BUTTON), Click(SauceDemo.SHOPPING_CART_LINK))

    cart_items = customer.asks_for(TextsOf(SauceDemo.CART_ITEM_NAMES))
    assert PRODUCT_NAME in cart_items


@pytest.mark.integration
def test_product_details_direct_url_when_logged_in(
    customer_on_inventory: Actor, base_url: str
) -> None:
    customer = customer_on_inventory
    customer.attempts_to(NavigateTo(f"{base_url}inventory-item.html?id={PRODUCT_ID}"))

    customer.expect(SauceDemo.BACK_TO_PRODUCTS).to_be_visible()
    assert customer.asks_for(CurrentUrl()).endswith(f"/inventory-item.html?id={PRODUCT_ID}")


@pytest.mark.integration
def test_product_details_direct_url_redirects_to_login_when_logged_out(
    customer: Actor, base_url: str
) -> None:
    customer.attempts_to(NavigateTo(f"{base_url}inventory-item.html?id={PRODUCT_ID}"))
    assert customer.asks_for(OnLoginPage())
