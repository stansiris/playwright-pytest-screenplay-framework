import pytest

from saucedemo.tasks.dismiss_login_error import DismissLoginError
from saucedemo.tasks.login import Login
from saucedemo.tasks.logout import Logout
from saucedemo.tasks.open_saucedemo import OpenSauceDemo
from saucedemo.ui.pages.inventory_page import InventoryPage
from saucedemo.ui.pages.login_page import LoginPage
from screenplay_core.consequences.ensure import Ensure


@pytest.mark.parametrize(
    "username,password,expected_error_message",
    [
        ("", "secret_sauce", "Username is required"),
        ("standard_user", "", "Password is required"),
        (
            "invalid_user",
            "secret_sauce",
            "Username and password do not match any user in this service",
        ),
        (
            "standard_user",
            "wrong_password",
            "Username and password do not match any user in this service",
        ),
        ("locked_out_user", "secret_sauce", "Sorry, this user has been locked out."),
    ],
)
@pytest.mark.integration
def test_failed_login(customer, username, password, expected_error_message) -> None:
    """Verify invalid login inputs show the expected error and that the error can be dismissed."""
    customer.attempts_to(
        OpenSauceDemo.app(),
        Ensure.that(LoginPage.LOGIN_BUTTON).to_be_visible(),
        Login.with_credentials(username=username, password=password),
        Ensure.that(LoginPage.LOGIN_ERROR_MESSAGE).to_contain_text(expected_error_message),
        DismissLoginError(),
        Ensure.that(LoginPage.LOGIN_ERROR_MESSAGE).to_be_hidden(),
    )


@pytest.mark.parametrize(
    "username,password",
    [
        ("standard_user", "secret_sauce"),
        ("problem_user", "secret_sauce"),
        ("performance_glitch_user", "secret_sauce"),
    ],
)
@pytest.mark.smoke
def test_successful_login(customer, username, password) -> None:
    """Verify valid users can log in, reach inventory, and then log out back to login page."""
    customer.attempts_to(
        OpenSauceDemo.app(),
        Ensure.that(LoginPage.LOGIN_BUTTON).to_be_visible(),
        Login.with_credentials(username=username, password=password),
        Ensure.that(InventoryPage.INVENTORY_CONTAINER).to_be_visible(),
        Logout(),
        Ensure.that(LoginPage.LOGIN_BUTTON).to_be_visible(),
    )
