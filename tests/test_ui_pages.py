import pytest

from saucedemo.questions.on_inventory_page import OnInventoryPage
from saucedemo.tasks.add_product_to_cart import AddProductToCart
from saucedemo.tasks.complete_checkout import CompleteCheckout
from saucedemo.tasks.go_to_cart import GoToCart
from saucedemo.tasks.login import Login
from saucedemo.tasks.open_login_page import OpenLoginPage
from saucedemo.tasks.open_product_details import OpenProductDetails
from saucedemo.tasks.proceed_to_checkout import ProceedToCheckout
from saucedemo.tasks.provide_checkout_information import ProvideCheckoutInformation
from saucedemo.tasks.wait_for_checkout_complete_page import WaitForCheckoutCompletePage
from saucedemo.tasks.wait_for_checkout_info_page import WaitForCheckoutInfoPage
from saucedemo.tasks.wait_for_inventory_page import WaitForInventoryPage
from saucedemo.ui.components.app_shell import AppShell
from saucedemo.ui.components.back_navigation import BackNavigation
from saucedemo.ui.pages.cart_page import CartPage
from saucedemo.ui.pages.checkout_complete_page import CheckoutCompletePage
from saucedemo.ui.pages.checkout_info_page import CheckoutInfoPage
from saucedemo.ui.pages.checkout_overview_page import CheckoutOverviewPage
from saucedemo.ui.pages.inventory_page import InventoryPage
from saucedemo.ui.pages.login_page import LoginPage
from saucedemo.ui.pages.product_details_page import ProductDetailsPage
from screenplay_core.core.actor import Actor
from screenplay_core.questions.attribute_of import AttributeOf
from screenplay_core.questions.current_url import CurrentUrl
from screenplay_core.questions.texts_of import TextsOf

PRODUCT_NAME = "Sauce Labs Backpack"
FIRST_NAME = "John"
LAST_NAME = "Doe"
POSTAL_CODE = "08873"


def login_as_standard_user(customer: Actor) -> None:
    customer.attempts_to(
        OpenLoginPage(),
        Login.with_credentials("standard_user", "secret_sauce"),
        WaitForInventoryPage(),
    )
    assert customer.asks_for(OnInventoryPage())


def add_item_and_open_checkout_info(customer: Actor) -> None:
    customer.attempts_to(
        AddProductToCart.named(PRODUCT_NAME),
        GoToCart(),
        ProceedToCheckout(),
        WaitForCheckoutInfoPage(),
    )


@pytest.mark.ui
@pytest.mark.integration
def test_login_page_ui_elements(customer: Actor) -> None:
    """Verify login page UI shows logo, credentials inputs, and placeholders."""
    customer.attempts_to(OpenLoginPage())

    customer.expect(LoginPage.LOGIN_LOGO).to_be_visible()
    customer.expect(LoginPage.LOGIN_USERNAME).to_be_visible()
    customer.expect(LoginPage.LOGIN_PASSWORD).to_be_visible()
    customer.expect(LoginPage.LOGIN_BUTTON).to_be_visible()
    assert customer.asks_for(AttributeOf(LoginPage.LOGIN_USERNAME, "placeholder")) == "Username"
    assert customer.asks_for(AttributeOf(LoginPage.LOGIN_PASSWORD, "placeholder")) == "Password"


@pytest.mark.ui
@pytest.mark.integration
def test_inventory_page_ui_elements(customer: Actor) -> None:
    """Verify inventory page UI structure, product list, and sort options."""
    login_as_standard_user(customer)

    customer.expect(InventoryPage.INVENTORY_CONTAINER).to_be_visible()
    customer.expect(AppShell.PAGE_TITLE).to_have_text("Products")
    customer.expect(InventoryPage.INVENTORY_SORT).to_be_visible()
    customer.expect(AppShell.SHOPPING_CART_LINK).to_be_visible()
    customer.expect(InventoryPage.INVENTORY_ITEM_NAMES).to_have_count(6)
    customer.expect(InventoryPage.INVENTORY_ITEM_PRICES).to_have_count(6)
    assert customer.asks_for(TextsOf(InventoryPage.INVENTORY_SORT_OPTIONS)) == [
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
    customer.attempts_to(OpenProductDetails.named(PRODUCT_NAME))

    assert "inventory-item.html" in customer.asks_for(CurrentUrl())
    customer.expect(BackNavigation.BACK_TO_PRODUCTS).to_have_text("Back to products")
    customer.expect(ProductDetailsPage.PRODUCT_DETAILS_IMAGE).to_be_visible()
    customer.expect(InventoryPage.INVENTORY_ITEM_NAMES).to_have_text(PRODUCT_NAME)
    customer.expect(InventoryPage.INVENTORY_ITEM_PRICES).to_be_visible()
    customer.expect(BackNavigation.BACK_TO_PRODUCTS).to_be_visible()


@pytest.mark.ui
@pytest.mark.integration
def test_cart_page_ui_elements(customer: Actor) -> None:
    """Verify cart page UI elements render with an item present."""
    login_as_standard_user(customer)
    customer.attempts_to(AddProductToCart.named(PRODUCT_NAME), GoToCart())

    assert customer.asks_for(CurrentUrl()).endswith("/cart.html")
    customer.expect(AppShell.PAGE_TITLE).to_have_text("Your Cart")
    customer.expect(CartPage.CART_ITEM_NAMES).to_have_count(1)
    customer.expect(CartPage.CHECKOUT_BUTTON).to_be_visible()


@pytest.mark.ui
@pytest.mark.integration
def test_checkout_info_page_ui_elements(customer: Actor) -> None:
    """Verify checkout step-one UI controls are visible and labeled correctly."""
    login_as_standard_user(customer)
    add_item_and_open_checkout_info(customer)

    assert customer.asks_for(CurrentUrl()).endswith("/checkout-step-one.html")
    customer.expect(AppShell.PAGE_TITLE).to_have_text("Checkout: Your Information")
    customer.expect(CheckoutInfoPage.CHECKOUT_FIRST_NAME).to_be_visible()
    customer.expect(CheckoutInfoPage.CHECKOUT_LAST_NAME).to_be_visible()
    customer.expect(CheckoutInfoPage.CHECKOUT_POSTAL_CODE).to_be_visible()
    customer.expect(CheckoutInfoPage.CHECKOUT_CONTINUE).to_be_visible()
    customer.expect(CheckoutInfoPage.CHECKOUT_INFO_CANCEL_BUTTON).to_be_visible()


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
    customer.expect(AppShell.PAGE_TITLE).to_have_text("Checkout: Overview")
    customer.expect(CheckoutOverviewPage.CHECKOUT_OVERVIEW_ITEM_NAMES).to_have_count(1)
    customer.expect(CheckoutOverviewPage.CHECKOUT_PAYMENT_INFO).to_be_visible()
    customer.expect(CheckoutOverviewPage.CHECKOUT_SHIPPING_INFO).to_be_visible()
    customer.expect(CheckoutOverviewPage.CHECKOUT_SUBTOTAL).to_be_visible()
    customer.expect(CheckoutOverviewPage.CHECKOUT_TAX).to_be_visible()
    customer.expect(CheckoutOverviewPage.CHECKOUT_TOTAL).to_be_visible()
    customer.expect(CheckoutOverviewPage.CHECKOUT_FINISH).to_be_visible()


@pytest.mark.ui
@pytest.mark.integration
def test_checkout_complete_page_ui_elements(customer: Actor) -> None:
    """Verify checkout complete UI shows confirmation messaging and navigation control."""
    login_as_standard_user(customer)
    add_item_and_open_checkout_info(customer)
    customer.attempts_to(
        ProvideCheckoutInformation.as_customer(FIRST_NAME, LAST_NAME, POSTAL_CODE),
        CompleteCheckout(),
        WaitForCheckoutCompletePage(),
    )

    assert customer.asks_for(CurrentUrl()).endswith("/checkout-complete.html")
    customer.expect(CheckoutCompletePage.CHECKOUT_COMPLETE_TITLE).to_have_text(
        "Checkout: Complete!"
    )
    customer.expect(CheckoutCompletePage.CHECKOUT_COMPLETE_HEADER).to_have_text(
        "Thank you for your order!"
    )
    customer.expect(CheckoutCompletePage.CHECKOUT_COMPLETE_TEXT).to_be_visible()
    customer.expect(CheckoutCompletePage.CHECKOUT_COMPLETE_PONY_IMAGE).to_be_visible()
    customer.expect(BackNavigation.BACK_TO_PRODUCTS).to_be_visible()
