import re

import pytest

from saucedemo.questions.on_inventory_page import OnInventoryPage
from saucedemo.tasks.add_product_to_cart import AddProductToCart
from saucedemo.tasks.complete_checkout import CompleteCheckout
from saucedemo.tasks.go_to_cart import GoToCart
from saucedemo.tasks.login import Login
from saucedemo.tasks.open_login_page import OpenLoginPage
from saucedemo.tasks.proceed_to_checkout import ProceedToCheckout
from saucedemo.tasks.provide_checkout_information import ProvideCheckoutInformation
from saucedemo.ui.saucedemo import SauceDemo
from screenplay_core.core.actor import Actor
from screenplay_core.core.target import Target
from screenplay_core.interactions.click import Click
from screenplay_core.interactions.wait_until_visible import WaitUntilVisible
from screenplay_core.questions.attribute_of import AttributeOf
from screenplay_core.questions.current_url import CurrentUrl
from screenplay_core.questions.texts_of import TextsOf

PRODUCT_NAME = "Sauce Labs Backpack"
FIRST_NAME = "John"
LAST_NAME = "Doe"
POSTAL_CODE = "08873"

LOGIN_LOGO = Target("Login logo", lambda page: page.locator(".login_logo"))
PAGE_TITLE = Target("Page title", lambda page: page.locator('[data-test="title"]'))
INVENTORY_SORT_OPTIONS = Target(
    "Inventory sort options",
    lambda page: page.locator('[data-test="product-sort-container"] option'),
)
PRODUCT_DETAILS_IMAGE = Target(
    "Product details image",
    lambda page: page.locator(".inventory_details_img"),
)
CHECKOUT_INFO_CANCEL_BUTTON = Target(
    "Checkout info cancel button",
    lambda page: page.locator('[data-test="cancel"]'),
)
CHECKOUT_COMPLETE_HEADER = Target(
    "Checkout complete header",
    lambda page: page.locator('[data-test="complete-header"]'),
)
CHECKOUT_COMPLETE_TEXT = Target(
    "Checkout complete text",
    lambda page: page.locator('[data-test="complete-text"]'),
)
CHECKOUT_COMPLETE_PONY_IMAGE = Target(
    "Checkout complete pony image",
    lambda page: page.locator('[data-test="pony-express"]'),
)


def inventory_item_name_target(product_name: str) -> Target:
    exact_name = re.compile(rf"^{re.escape(product_name)}$")
    return Target(
        f"Inventory item name '{product_name}'",
        lambda page: page.locator('[data-test="inventory-item-name"]', has_text=exact_name),
    )


def login_as_standard_user(customer: Actor) -> None:
    customer.attempts_to(
        OpenLoginPage(),
        Login.with_credentials("standard_user", "secret_sauce"),
        WaitUntilVisible.for_(SauceDemo.INVENTORY_CONTAINER),
    )
    assert customer.asks_for(OnInventoryPage())


def add_item_and_open_checkout_info(customer: Actor) -> None:
    customer.attempts_to(
        AddProductToCart.named(PRODUCT_NAME),
        GoToCart(),
        ProceedToCheckout(),
        WaitUntilVisible.for_(SauceDemo.CHECKOUT_FIRST_NAME),
    )


@pytest.mark.ui
@pytest.mark.integration
def test_login_page_ui_elements(customer: Actor) -> None:
    """Verify login page UI shows logo, credentials inputs, and placeholders."""
    customer.attempts_to(OpenLoginPage())

    customer.expect(LOGIN_LOGO).to_be_visible()
    customer.expect(SauceDemo.LOGIN_USERNAME).to_be_visible()
    customer.expect(SauceDemo.LOGIN_PASSWORD).to_be_visible()
    customer.expect(SauceDemo.LOGIN_BUTTON).to_be_visible()
    assert customer.asks_for(AttributeOf(SauceDemo.LOGIN_USERNAME, "placeholder")) == "Username"
    assert customer.asks_for(AttributeOf(SauceDemo.LOGIN_PASSWORD, "placeholder")) == "Password"


@pytest.mark.ui
@pytest.mark.integration
def test_inventory_page_ui_elements(customer: Actor) -> None:
    """Verify inventory page UI structure, product list, and sort options."""
    login_as_standard_user(customer)

    customer.expect(SauceDemo.INVENTORY_CONTAINER).to_be_visible()
    customer.expect(PAGE_TITLE).to_have_text("Products")
    customer.expect(SauceDemo.INVENTORY_SORT).to_be_visible()
    customer.expect(SauceDemo.SHOPPING_CART_LINK).to_be_visible()
    customer.expect(SauceDemo.INVENTORY_ITEM_NAMES).to_have_count(6)
    customer.expect(SauceDemo.INVENTORY_ITEM_PRICES).to_have_count(6)
    assert customer.asks_for(TextsOf(INVENTORY_SORT_OPTIONS)) == [
        "Name (A to Z)",
        "Name (Z to A)",
        "Price (low to high)",
        "Price (high to low)",
    ]


@pytest.mark.ui
@pytest.mark.integration
def test_product_details_page_ui_elements(customer: Actor) -> None:
    """Verify product details page UI elements render after opening an item."""
    login_as_standard_user(customer)
    customer.attempts_to(Click(inventory_item_name_target(PRODUCT_NAME)))

    assert "inventory-item.html" in customer.asks_for(CurrentUrl())
    customer.expect(SauceDemo.BACK_TO_PRODUCTS).to_have_text("Back to products")
    customer.expect(PRODUCT_DETAILS_IMAGE).to_be_visible()
    customer.expect(SauceDemo.INVENTORY_ITEM_NAMES).to_have_text(PRODUCT_NAME)
    customer.expect(SauceDemo.INVENTORY_ITEM_PRICES).to_be_visible()
    customer.expect(SauceDemo.BACK_TO_PRODUCTS).to_be_visible()


@pytest.mark.ui
@pytest.mark.integration
def test_cart_page_ui_elements(customer: Actor) -> None:
    """Verify cart page UI elements render with an item present."""
    login_as_standard_user(customer)
    customer.attempts_to(AddProductToCart.named(PRODUCT_NAME), GoToCart())

    assert customer.asks_for(CurrentUrl()).endswith("/cart.html")
    customer.expect(PAGE_TITLE).to_have_text("Your Cart")
    customer.expect(SauceDemo.CART_ITEM_NAMES).to_have_count(1)
    customer.expect(SauceDemo.CHECKOUT_BUTTON).to_be_visible()


@pytest.mark.ui
@pytest.mark.integration
def test_checkout_info_page_ui_elements(customer: Actor) -> None:
    """Verify checkout step-one UI controls are visible and labeled correctly."""
    login_as_standard_user(customer)
    add_item_and_open_checkout_info(customer)

    assert customer.asks_for(CurrentUrl()).endswith("/checkout-step-one.html")
    customer.expect(PAGE_TITLE).to_have_text("Checkout: Your Information")
    customer.expect(SauceDemo.CHECKOUT_FIRST_NAME).to_be_visible()
    customer.expect(SauceDemo.CHECKOUT_LAST_NAME).to_be_visible()
    customer.expect(SauceDemo.CHECKOUT_POSTAL_CODE).to_be_visible()
    customer.expect(SauceDemo.CHECKOUT_CONTINUE).to_be_visible()
    customer.expect(CHECKOUT_INFO_CANCEL_BUTTON).to_be_visible()


@pytest.mark.ui
@pytest.mark.integration
def test_checkout_overview_page_ui_elements(customer: Actor) -> None:
    """Verify checkout overview UI shows item, summary, totals, and finish action."""
    login_as_standard_user(customer)
    add_item_and_open_checkout_info(customer)
    customer.attempts_to(
        ProvideCheckoutInformation.as_customer(FIRST_NAME, LAST_NAME, POSTAL_CODE),
    )

    assert customer.asks_for(CurrentUrl()).endswith("/checkout-step-two.html")
    customer.expect(PAGE_TITLE).to_have_text("Checkout: Overview")
    customer.expect(SauceDemo.CHECKOUT_OVERVIEW_ITEM_NAMES).to_have_count(1)
    customer.expect(SauceDemo.CHECKOUT_PAYMENT_INFO).to_be_visible()
    customer.expect(SauceDemo.CHECKOUT_SHIPPING_INFO).to_be_visible()
    customer.expect(SauceDemo.CHECKOUT_SUBTOTAL).to_be_visible()
    customer.expect(SauceDemo.CHECKOUT_TAX).to_be_visible()
    customer.expect(SauceDemo.CHECKOUT_TOTAL).to_be_visible()
    customer.expect(SauceDemo.CHECKOUT_FINISH).to_be_visible()


@pytest.mark.ui
@pytest.mark.integration
def test_checkout_complete_page_ui_elements(customer: Actor) -> None:
    """Verify checkout complete UI shows confirmation messaging and navigation control."""
    login_as_standard_user(customer)
    add_item_and_open_checkout_info(customer)
    customer.attempts_to(
        ProvideCheckoutInformation.as_customer(FIRST_NAME, LAST_NAME, POSTAL_CODE),
        CompleteCheckout(),
        WaitUntilVisible.for_(SauceDemo.CHECKOUT_COMPLETE_TITLE),
    )

    assert customer.asks_for(CurrentUrl()).endswith("/checkout-complete.html")
    customer.expect(SauceDemo.CHECKOUT_COMPLETE_TITLE).to_have_text("Checkout: Complete!")
    customer.expect(CHECKOUT_COMPLETE_HEADER).to_have_text("Thank you for your order!")
    customer.expect(CHECKOUT_COMPLETE_TEXT).to_be_visible()
    customer.expect(CHECKOUT_COMPLETE_PONY_IMAGE).to_be_visible()
    customer.expect(SauceDemo.BACK_TO_PRODUCTS).to_be_visible()
