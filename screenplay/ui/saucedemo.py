from screenplay.core.target import Target


def menu_button_locator(page):
    return page.get_by_role("button", name="Open Menu")


def logout_link_locator(page):
    return page.locator('[data-test="logout-sidebar-link"]')


def login_button_locator(page):
    return page.locator('[data-test="login-button"]')
    # return page.get_by_role("button", name="Login")


def login_username_locator(page):
    return page.locator('[data-test="username"]')


def login_password_locator(page):
    return page.locator('[data-test="password"]')


def inventory_container_locator(page):
    return page.locator('[data-test="inventory-container"]')


class SauceDemo:
    MENU_BUTTON = Target("Open Menu button", menu_button_locator)
    LOGOUT_LINK = Target("Logout link", logout_link_locator)
    LOGIN_BUTTON = Target("Login button", login_button_locator)
    LOGIN_USERNAME = Target("Login username", login_username_locator)
    LOGIN_PASSWORD = Target("Login password", login_password_locator)
    INVENTORY_CONTAINER = Target("Inventory Products List", inventory_container_locator)
    URL = "https://saucedemo.com/"
