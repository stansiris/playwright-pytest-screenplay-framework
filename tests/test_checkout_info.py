import pytest

from saucedemo.tasks.add_product_to_cart import AddProductToCart
from saucedemo.tasks.continue_checkout import ContinueCheckout
from saucedemo.tasks.enter_checkout_information import EnterCheckoutInformation
from saucedemo.tasks.go_to_cart import GoToCart
from saucedemo.tasks.login import Login
from saucedemo.tasks.open_login_page import OpenLoginPage
from saucedemo.tasks.proceed_to_checkout import ProceedToCheckout
from saucedemo.tasks.provide_checkout_information import ProvideCheckoutInformation
from saucedemo.ui.saucedemo import SauceDemo
from screenplay_core.core.actor import Actor
from screenplay_core.interactions.click import Click
from screenplay_core.interactions.wait_until_visible import WaitUntilVisible
from screenplay_core.questions.current_url import CurrentUrl

PRODUCT_NAME = "Sauce Labs Backpack"
FIRST_NAME = "John"
LAST_NAME = "Doe"
POSTAL_CODE = "08873"


@pytest.fixture
def customer_on_checkout_info(customer: Actor) -> Actor:
    customer.attempts_to(
        OpenLoginPage(),
        Login.with_credentials("standard_user", "secret_sauce"),
        AddProductToCart.named(PRODUCT_NAME),
        GoToCart(),
        ProceedToCheckout(),
        WaitUntilVisible.for_(SauceDemo.CHECKOUT_FIRST_NAME),
    )
    assert customer.asks_for(CurrentUrl()).endswith("/checkout-step-one.html")
    return customer


@pytest.mark.smoke
@pytest.mark.integration
def test_checkout_info_page_loads(customer_on_checkout_info: Actor) -> None:
    """Verify checkout step-one page loads with required form controls visible."""
    customer = customer_on_checkout_info
    customer.expect(SauceDemo.CHECKOUT_FIRST_NAME).to_be_visible()
    customer.expect(SauceDemo.CHECKOUT_LAST_NAME).to_be_visible()
    customer.expect(SauceDemo.CHECKOUT_POSTAL_CODE).to_be_visible()
    customer.expect(SauceDemo.CHECKOUT_CONTINUE).to_be_visible()
    assert customer.asks_for(CurrentUrl()).endswith("/checkout-step-one.html")


@pytest.mark.integration
@pytest.mark.parametrize(
    "first_name,last_name,postal_code,expected_error_message",
    [
        ("", LAST_NAME, POSTAL_CODE, "Error: First Name is required"),
        (FIRST_NAME, "", POSTAL_CODE, "Error: Last Name is required"),
        (FIRST_NAME, LAST_NAME, "", "Error: Postal Code is required"),
    ],
)
def test_checkout_info_required_fields_validation(
    customer_on_checkout_info: Actor,
    first_name: str,
    last_name: str,
    postal_code: str,
    expected_error_message: str,
) -> None:
    """Verify required-field validation errors appear for missing checkout inputs."""
    customer = customer_on_checkout_info
    customer.attempts_to(
        EnterCheckoutInformation.as_customer(first_name, last_name, postal_code),
        ContinueCheckout(),
    )

    customer.expect(SauceDemo.CHECKOUT_INFO_ERROR_MESSAGE).to_contain_text(expected_error_message)
    assert customer.asks_for(CurrentUrl()).endswith("/checkout-step-one.html")

    customer.attempts_to(Click(SauceDemo.CHECKOUT_INFO_ERROR_CLOSE_BUTTON))
    customer.expect(SauceDemo.CHECKOUT_INFO_ERROR_MESSAGE).to_be_hidden()


@pytest.mark.integration
def test_checkout_info_valid_information_proceeds_to_overview(
    customer_on_checkout_info: Actor,
) -> None:
    """Verify valid checkout info submission proceeds to checkout overview."""
    customer = customer_on_checkout_info
    customer.attempts_to(
        EnterCheckoutInformation.as_customer(FIRST_NAME, LAST_NAME, POSTAL_CODE),
        ContinueCheckout(),
    )

    customer.expect(SauceDemo.CHECKOUT_FINISH).to_be_visible()
    assert customer.asks_for(CurrentUrl()).endswith("/checkout-step-two.html")


@pytest.mark.integration
def test_checkout_info_provide_checkout_information_task_proceeds_to_overview(
    customer_on_checkout_info: Actor,
) -> None:
    """Verify composite ProvideCheckoutInformation task navigates to overview."""
    customer = customer_on_checkout_info
    customer.attempts_to(
        ProvideCheckoutInformation.as_customer(FIRST_NAME, LAST_NAME, POSTAL_CODE),
    )

    customer.expect(SauceDemo.CHECKOUT_FINISH).to_be_visible()
    assert customer.asks_for(CurrentUrl()).endswith("/checkout-step-two.html")


@pytest.mark.integration
def test_checkout_info_cancel_returns_to_cart(customer_on_checkout_info: Actor) -> None:
    """Verify cancel on checkout step one returns the user to cart page."""
    customer = customer_on_checkout_info
    customer.attempts_to(Click(SauceDemo.CHECKOUT_INFO_CANCEL_BUTTON))

    customer.expect(SauceDemo.CHECKOUT_BUTTON).to_be_visible()
    assert customer.asks_for(CurrentUrl()).endswith("/cart.html")
