from pytest_bdd import given, parsers, scenario, then, when

from saucedemo.questions.on_inventory_page import OnInventoryPage
from saucedemo.questions.on_login_page import OnLoginPage
from saucedemo.tasks.click_login import ClickLogin
from saucedemo.tasks.dismiss_login_error import DismissLoginError
from saucedemo.tasks.enter_password import EnterPassword
from saucedemo.tasks.enter_username import EnterUsername
from saucedemo.tasks.open_saucedemo import OpenSauceDemo
from saucedemo.ui.saucedemo import SauceDemo
from screenplay_core.interactions.click import Click
from screenplay_core.interactions.focus import Focus
from screenplay_core.interactions.press_key import PressKey
from screenplay_core.interactions.refresh_page import RefreshPage
from screenplay_core.interactions.wait_until_visible import WaitUntilVisible
from screenplay_core.questions.attribute_of import AttributeOf
from screenplay_core.questions.focus_indicator_visible import FocusIndicatorVisible
from screenplay_core.questions.is_focused import IsFocused
from screenplay_core.questions.is_visible import IsVisible
from screenplay_core.questions.text_of import TextOf


@scenario(
    "features/login_page.feature",
    "Login succeeds with valid credentials for supported users",
)
def test_login_succeeds_with_valid_credentials_for_supported_users() -> None:
    pass


@scenario("features/login_page.feature", "Login form allows pressing Enter to submit")
def test_login_form_allows_pressing_enter_to_submit() -> None:
    pass


@scenario("features/login_page.feature", "Password input is masked")
def test_password_input_is_masked() -> None:
    pass


@scenario("features/login_page.feature", "Login fails when username is missing")
def test_login_fails_when_username_is_missing() -> None:
    pass


@scenario("features/login_page.feature", "Login fails when password is missing")
def test_login_fails_when_password_is_missing() -> None:
    pass


@scenario("features/login_page.feature", "Login fails when both username and password are missing")
def test_login_fails_when_both_username_and_password_are_missing() -> None:
    pass


@scenario("features/login_page.feature", "Login fails with an invalid username")
def test_login_fails_with_an_invalid_username() -> None:
    pass


@scenario("features/login_page.feature", "Login fails with an invalid password")
def test_login_fails_with_an_invalid_password() -> None:
    pass


@scenario("features/login_page.feature", "Login fails for locked_out_user")
def test_login_fails_for_locked_out_user() -> None:
    pass


@scenario("features/login_page.feature", "Error message can be dismissed")
def test_error_message_can_be_dismissed() -> None:
    pass


@scenario("features/login_page.feature", "Username and password fields are cleared on page refresh")
def test_username_and_password_fields_are_cleared_on_page_refresh() -> None:
    pass


@scenario("features/login_page.feature", "Login fails with blank and malformed credential inputs")
def test_login_fails_with_blank_and_malformed_credential_inputs() -> None:
    pass


@scenario("features/login_page.feature", "Clicking on username field gives it focus")
def test_clicking_on_username_field_gives_it_focus() -> None:
    pass


@scenario("features/login_page.feature", "Clicking on password field gives it focus")
def test_clicking_on_password_field_gives_it_focus() -> None:
    pass


@scenario("features/login_page.feature", "Login button can receive keyboard focus")
def test_login_button_can_receive_keyboard_focus() -> None:
    pass


@scenario(
    "features/login_page.feature", "User can navigate login form using Tab key in correct order"
)
def test_user_can_navigate_login_form_using_tab_key_in_correct_order() -> None:
    pass


@scenario("features/login_page.feature", "User can navigate backwards using Shift+Tab")
def test_user_can_navigate_backwards_using_shifttab() -> None:
    pass


@scenario("features/login_page.feature", "Login page state is preserved after failed login")
def test_login_page_state_is_preserved_after_failed_login() -> None:
    pass


@scenario("features/login_page.feature", "Focused element is visibly highlighted")
def test_focused_element_is_visibly_highlighted() -> None:
    pass


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


@then("I should be on the inventory page")
def should_be_on_inventory_page(customer) -> None:
    customer.attempts_to(WaitUntilVisible.for_(SauceDemo.INVENTORY_CONTAINER))
    assert customer.asks_for(OnInventoryPage())


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
