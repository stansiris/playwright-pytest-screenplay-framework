import pytest

from saucedemo.questions.on_inventory_page import OnInventoryPage
from saucedemo.tasks.login import Login
from saucedemo.ui.saucedemo import SauceDemo


@pytest.mark.parametrize(
    "username,password,expected_error_message",
    [
        ("standard_user", "secret_sauce", None),  # valid credentials
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
    ],
)
def test_login(customer, username, password, expected_error_message) -> None:
    customer.attempts_to(Login.with_credentials(username=username, password=password))

    if expected_error_message:
        customer.expect(SauceDemo.LOGIN_ERROR_MESSAGE).to_contain_text(expected_error_message)
    else:
        assert customer.asks_for(OnInventoryPage())
