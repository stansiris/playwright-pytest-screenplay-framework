import pytest

from saucedemo.questions.on_inventory_page import OnInventoryPage
from saucedemo.tasks.login import Login
from saucedemo.tasks.open_login_page import OpenLoginPage
from saucedemo.ui.components.app_shell import AppShell
from saucedemo.ui.pages.login_page import LoginPage
from screenplay_core.interactions.click import Click


@pytest.mark.parametrize(
    "username,password,expected_error_message",
    [
        ("", "secret_sauce", "Username is required"),  # missing username
        ("standard_user", "", "Password is required"),  # missing password
        (
            "invalid_user",
            "secret_sauce",
            "Username and password do not match any user in this service",
        ),  # invalid username
        (
            "standard_user",
            "wrong_password",
            "Username and password do not match any user in this service",
        ),  # invalid password
        (
            "locked_out_user",
            "secret_sauce",
            "Sorry, this user has been locked out.",
        ),  # locked out user
    ],
)
@pytest.mark.integration
def test_failed_login(customer, username, password, expected_error_message) -> None:
    """Verify invalid login inputs show the expected error and that the error can be dismissed."""
    customer.attempts_to(
        OpenLoginPage(), Login.with_credentials(username=username, password=password)
    )

    customer.expect(LoginPage.LOGIN_ERROR_MESSAGE).to_contain_text(expected_error_message)
    customer.attempts_to(Click(LoginPage.LOGIN_ERROR_CLOSE_BUTTON))
    customer.expect(LoginPage.LOGIN_ERROR_MESSAGE).to_be_hidden()


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
        OpenLoginPage(), Login.with_credentials(username=username, password=password)
    )
    assert customer.asks_for(OnInventoryPage())
    customer.attempts_to(Click(AppShell.MENU_BUTTON), Click(AppShell.LOGOUT_LINK))
    customer.expect(LoginPage.LOGIN_BUTTON).to_be_visible()
