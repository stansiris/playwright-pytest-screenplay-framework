from pytest_bdd import given, parsers, then, when

from screenplay.interactions.click import Click
from screenplay.interactions.focus import Focus
from screenplay.interactions.press_key import PressKey
from screenplay.interactions.refresh_page import RefreshPage
from screenplay.interactions.wait_until_visible import WaitUntilVisible
from screenplay.questions.attribute_of import AttributeOf
from screenplay.questions.focus_indicator_visible import FocusIndicatorVisible
from screenplay.questions.is_focused import IsFocused
from screenplay.questions.is_visible import IsVisible
from screenplay.questions.on_login_page import OnLoginPage
from screenplay.questions.text_of import TextOf
from screenplay.tasks.click_login import ClickLogin
from screenplay.tasks.dismiss_login_error import DismissLoginError
from screenplay.tasks.enter_password import EnterPassword
from screenplay.tasks.enter_username import EnterUsername
from screenplay.tasks.open_saucedemo import OpenSauceDemo
from screenplay.ui.saucedemo import SauceDemo


@given("I am on the SauceDemo login page")
def open_login_page(customer) -> None:
    customer.attempts_to(
        OpenSauceDemo.app(),
        WaitUntilVisible.for_(SauceDemo.LOGIN_BUTTON),
    )


@when(parsers.re(r'^I enter username "(?P<username>.*)"$'))
def enter_username(customer, username: str) -> None:
    customer.attempts_to(EnterUsername.as_(username))


@when(parsers.re(r'^I enter password "(?P<password>.*)"$'))
def enter_password(customer, password: str) -> None:
    customer.attempts_to(EnterPassword.as_(password))


@when("I click the Login button")
def click_login_button(customer) -> None:
    customer.attempts_to(ClickLogin())


@then("I should see the inventory container")
def should_see_inventory_container(customer) -> None:
    customer.attempts_to(WaitUntilVisible.for_(SauceDemo.INVENTORY_CONTAINER))
    assert customer.asks_for(IsVisible(SauceDemo.INVENTORY_CONTAINER))


@when("I press Enter")
def press_enter(customer) -> None:
    customer.attempts_to(PressKey("Enter"))


@then(parsers.parse('the password field should be of type "{field_type}"'))
def password_field_type_should_be(customer, field_type: str) -> None:
    assert customer.asks_for(AttributeOf(SauceDemo.LOGIN_PASSWORD, "type")) == field_type


@then(parsers.parse('I should see an error message "{error_message}"'))
def should_see_error_message(customer, error_message: str) -> None:
    customer.attempts_to(WaitUntilVisible.for_(SauceDemo.LOGIN_ERROR_MESSAGE))
    assert customer.asks_for(TextOf(SauceDemo.LOGIN_ERROR_MESSAGE)) == error_message


@then("I should remain on the login page")
def should_remain_on_login_page(customer) -> None:
    customer.attempts_to(WaitUntilVisible.for_(SauceDemo.LOGIN_BUTTON))
    assert customer.asks_for(OnLoginPage())


@when("I dismiss the error message")
def dismiss_error_message(customer) -> None:
    customer.attempts_to(DismissLoginError())


@then("I should not see the error message")
def should_not_see_error_message(customer) -> None:
    assert not customer.asks_for(IsVisible(SauceDemo.LOGIN_ERROR_MESSAGE))


@when("I refresh the page")
def refresh_page(customer) -> None:
    customer.attempts_to(
        RefreshPage(),
        WaitUntilVisible.for_(SauceDemo.LOGIN_BUTTON),
    )


@then("the username field should be empty")
def username_field_should_be_empty(customer) -> None:
    assert customer.asks_for(TextOf(SauceDemo.LOGIN_USERNAME)) == ""


@then("the password field should be empty")
def password_field_should_be_empty(customer) -> None:
    assert customer.asks_for(TextOf(SauceDemo.LOGIN_PASSWORD)) == ""


@when("I click on the username field")
def click_username_field(customer) -> None:
    customer.attempts_to(Click(SauceDemo.LOGIN_USERNAME))


@then("the username field should be focused")
def username_field_should_be_focused(customer) -> None:
    assert customer.asks_for(IsFocused(SauceDemo.LOGIN_USERNAME))


@when("I click on the password field")
def click_password_field(customer) -> None:
    customer.attempts_to(Click(SauceDemo.LOGIN_PASSWORD))


@then("the password field should be focused")
def password_field_should_be_focused(customer) -> None:
    assert customer.asks_for(IsFocused(SauceDemo.LOGIN_PASSWORD))


@given("I focus the Login button")
def focus_login_button(customer) -> None:
    customer.attempts_to(Focus(SauceDemo.LOGIN_BUTTON))


@then("the Login button should be focused")
def login_button_should_be_focused(customer) -> None:
    assert customer.asks_for(IsFocused(SauceDemo.LOGIN_BUTTON))


@when("I press Tab")
def press_tab(customer) -> None:
    customer.attempts_to(PressKey("Tab"))


@when("I press Shift+Tab")
def press_shift_tab(customer) -> None:
    customer.attempts_to(PressKey("Shift+Tab"))


@then("I should see an error message")
def should_see_any_error_message(customer) -> None:
    assert customer.asks_for(IsVisible(SauceDemo.LOGIN_ERROR_MESSAGE))


@then("the focused element should have a visible focus indicator")
def focused_element_should_have_visible_indicator(customer) -> None:
    assert customer.asks_for(FocusIndicatorVisible())
