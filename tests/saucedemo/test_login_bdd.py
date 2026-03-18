from pytest_bdd import given, parsers, scenario, then, when

from examples.saucedemo.questions.on_inventory_page import OnInventoryPage
from examples.saucedemo.questions.on_login_page import OnLoginPage
from examples.saucedemo.tasks.dismiss_login_error import DismissLoginError
from examples.saucedemo.tasks.login import Login
from examples.saucedemo.tasks.logout import Logout
from examples.saucedemo.tasks.open_saucedemo import OpenSauceDemo
from examples.saucedemo.ui.pages.inventory_page import InventoryPage
from examples.saucedemo.ui.pages.login_page import LoginPage
from screenplay_core.core.actor import Actor
from screenplay_core.playwright.ensure import Ensure


@scenario("features/login.feature", "Successful login reaches inventory and user can log out")
def test_successful_login_reaches_inventory_and_user_can_log_out() -> None:
    """Run the BDD login success flow and verify logout returns to login."""
    pass


@scenario("features/login.feature", "Invalid login shows expected error message")
def test_invalid_login_shows_expected_error_message() -> None:
    """Run the BDD invalid login flow and verify expected error handling."""
    pass


@given("I open the login page for login scenarios")
def open_login_page_for_login_scenarios(customer: Actor) -> None:
    customer.attempts_to(
        OpenSauceDemo.app(),
        Ensure.that(LoginPage.LOGIN_BUTTON).to_be_visible(),
    )


@when(
    parsers.re(
        '^I submit login credentials username "(?P<username>.*)" and password "(?P<password>.*)"$'
    )
)
def submit_login_credentials(customer: Actor, username: str, password: str) -> None:
    customer.attempts_to(Login.with_credentials(username=username, password=password))


@then("I should be on the inventory page for login scenarios")
def should_be_on_inventory_page_for_login_scenarios(customer: Actor) -> None:
    customer.attempts_to(Ensure.that(InventoryPage.INVENTORY_CONTAINER).to_be_visible())
    assert customer.asks_for(OnInventoryPage())


@when("I log out from the inventory menu")
def log_out_from_inventory_menu(customer: Actor) -> None:
    customer.attempts_to(Logout())


@then("I should be back on the login page for login scenarios")
def should_be_back_on_login_page_for_login_scenarios(customer: Actor) -> None:
    customer.attempts_to(Ensure.that(LoginPage.LOGIN_BUTTON).to_be_visible())
    assert customer.asks_for(OnLoginPage())


@then(parsers.parse('I should see login error message "{error_message}" for login scenarios'))
def should_see_login_error_message_for_login_scenarios(customer: Actor, error_message: str) -> None:
    customer.attempts_to(Ensure.that(LoginPage.LOGIN_ERROR_MESSAGE).to_contain_text(error_message))


@then("I can dismiss the login error message")
def can_dismiss_login_error_message(customer: Actor) -> None:
    customer.attempts_to(
        DismissLoginError(),
        Ensure.that(LoginPage.LOGIN_ERROR_MESSAGE).to_be_hidden(),
    )
