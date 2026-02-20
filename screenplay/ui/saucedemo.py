from screenplay.core.target import Target


def menu_button_locator(page):
    return page.get_by_role("button", name="Open Menu")


def logout_link_locator(page):
    return page.locator('[data-test="logout-sidebar-link"]')


def login_button_locator(page):
    return page.locator('[data-test="login-button"]')


def login_username_locator(page):
    return page.locator('[data-test="username"]')


def login_password_locator(page):
    return page.locator('[data-test="password"]')


def inventory_container_locator(page):
    return page.locator('[data-test="inventory-container"]')


def add_to_cart_red_tshirt_locator(page):
    return page.locator('[data-test="add-to-cart-test.allthethings()-t-shirt-(red)"]')


def shopping_cart_link_locator(page):
    return page.locator('[data-test="shopping-cart-link"]')


def checkout_button_locator(page):
    return page.locator('[data-test="checkout"]')


def checkout_first_name_locator(page):
    return page.locator('[data-test="firstName"]')


def checkout_last_name_locator(page):
    return page.locator('[data-test="lastName"]')


def checkout_postal_code_locator(page):
    return page.locator('[data-test="postalCode"]')


def checkout_continue_locator(page):
    return page.locator('[data-test="continue"]')


def checkout_finish_locator(page):
    return page.locator('[data-test="finish"]')


def checkout_complete_title_locator(page):
    return page.locator('[data-test="title"]')


def back_to_products_locator(page):
    return page.locator('[data-test="back-to-products"]')


class SauceDemo:
    MENU_BUTTON = Target("Open Menu button", menu_button_locator)
    LOGOUT_LINK = Target("Logout link", logout_link_locator)
    LOGIN_BUTTON = Target("Login button", login_button_locator)
    LOGIN_USERNAME = Target("Login username", login_username_locator)
    LOGIN_PASSWORD = Target("Login password", login_password_locator)
    INVENTORY_CONTAINER = Target("Inventory Products List", inventory_container_locator)
    ADD_TO_CART_RED_TSHIRT = Target(
        "Add red t-shirt to cart button", add_to_cart_red_tshirt_locator
    )
    SHOPPING_CART_LINK = Target("Shopping cart link", shopping_cart_link_locator)
    CHECKOUT_BUTTON = Target("Checkout button", checkout_button_locator)
    CHECKOUT_FIRST_NAME = Target("Checkout first name", checkout_first_name_locator)
    CHECKOUT_LAST_NAME = Target("Checkout last name", checkout_last_name_locator)
    CHECKOUT_POSTAL_CODE = Target("Checkout postal code", checkout_postal_code_locator)
    CHECKOUT_CONTINUE = Target("Checkout continue button", checkout_continue_locator)
    CHECKOUT_FINISH = Target("Checkout finish button", checkout_finish_locator)
    CHECKOUT_COMPLETE_TITLE = Target("Checkout complete title", checkout_complete_title_locator)
    BACK_TO_PRODUCTS = Target("Back to products button", back_to_products_locator)
    URL = "https://www.saucedemo.com/"
