from screenplay_core.playwright.target import Target


def login_logo_locator(page):
    return page.locator(".login_logo")


def login_button_locator(page):
    return page.locator('[data-test="login-button"]')


def login_username_locator(page):
    return page.locator('[data-test="username"]')


def login_password_locator(page):
    return page.locator('[data-test="password"]')


def login_error_message_locator(page):
    return page.locator('[data-test="error"]')


def login_error_close_button_locator(page):
    return page.locator('[data-test="error-button"]')


class LoginPage:
    LOGIN_LOGO = Target("Login logo", login_logo_locator)
    LOGIN_BUTTON = Target("Login button", login_button_locator)
    LOGIN_USERNAME = Target("Login username", login_username_locator)
    LOGIN_PASSWORD = Target("Login password", login_password_locator)
    LOGIN_ERROR_MESSAGE = Target("Login error message", login_error_message_locator)
    LOGIN_ERROR_CLOSE_BUTTON = Target("Login error close button", login_error_close_button_locator)
