from screenplay.config.runtime import runtime_settings
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


def login_error_message_locator(page):
    return page.locator('[data-test="error"]')


def login_error_close_button_locator(page):
    return page.locator('[data-test="error-button"]')


def inventory_container_locator(page):
    return page.locator('[data-test="inventory-container"]')


def inventory_sort_locator(page):
    return page.locator('[data-test="product-sort-container"]')


def inventory_item_names_locator(page):
    return page.locator('[data-test="inventory-item-name"]')


def inventory_item_prices_locator(page):
    return page.locator('[data-test="inventory-item-price"]')


def add_to_cart_red_tshirt_locator(page):
    return page.locator('[data-test="add-to-cart-test.allthethings()-t-shirt-(red)"]')


def add_to_cart_button_for_product_locator(product_name: str):
    """Build a locator function for the add-to-cart button of a named product."""

    def locator(page):
        # Find the inventory card by its visible product name, then pick its add button.
        product_card = page.locator('[data-test="inventory-item"]').filter(
            has=page.locator('[data-test="inventory-item-name"]', has_text=product_name)
        )
        return product_card.locator('button[data-test^="add-to-cart"]').first

    return locator


def shopping_cart_link_locator(page):
    return page.locator('[data-test="shopping-cart-link"]')


def shopping_cart_badge_locator(page):
    return page.locator('[data-test="shopping-cart-badge"]')


def cart_item_names_locator(page):
    return page.locator('[data-test="inventory-item-name"]')


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


def checkout_overview_item_names_locator(page):
    return page.locator('[data-test="inventory-item-name"]')


def checkout_payment_info_locator(page):
    return page.locator('[data-test="payment-info-value"]')


def checkout_shipping_info_locator(page):
    return page.locator('[data-test="shipping-info-value"]')


def checkout_subtotal_locator(page):
    return page.locator('[data-test="subtotal-label"]')


def checkout_tax_locator(page):
    return page.locator('[data-test="tax-label"]')


def checkout_total_locator(page):
    return page.locator('[data-test="total-label"]')


def checkout_complete_title_locator(page):
    return page.locator('[data-test="title"]')


def back_to_products_locator(page):
    return page.locator('[data-test="back-to-products"]')


class SauceDemo:
    PRODUCT_RED_TSHIRT = "Test.allTheThings() T-Shirt (Red)"

    MENU_BUTTON = Target("Open Menu button", menu_button_locator)
    LOGOUT_LINK = Target("Logout link", logout_link_locator)
    LOGIN_BUTTON = Target("Login button", login_button_locator)
    LOGIN_USERNAME = Target("Login username", login_username_locator)
    LOGIN_PASSWORD = Target("Login password", login_password_locator)
    LOGIN_ERROR_MESSAGE = Target("Login error message", login_error_message_locator)
    LOGIN_ERROR_CLOSE_BUTTON = Target("Login error close button", login_error_close_button_locator)
    INVENTORY_CONTAINER = Target("Inventory Products List", inventory_container_locator)
    INVENTORY_SORT = Target("Inventory sort dropdown", inventory_sort_locator)
    INVENTORY_ITEM_NAMES = Target("Inventory item names", inventory_item_names_locator)
    INVENTORY_ITEM_PRICES = Target("Inventory item prices", inventory_item_prices_locator)
    ADD_TO_CART_RED_TSHIRT = Target(
        "Add red t-shirt to cart button", add_to_cart_red_tshirt_locator
    )
    SHOPPING_CART_LINK = Target("Shopping cart link", shopping_cart_link_locator)
    SHOPPING_CART_BADGE = Target("Shopping cart badge", shopping_cart_badge_locator)
    CART_ITEM_NAMES = Target("Cart item names", cart_item_names_locator)
    CHECKOUT_BUTTON = Target("Checkout button", checkout_button_locator)
    CHECKOUT_FIRST_NAME = Target("Checkout first name", checkout_first_name_locator)
    CHECKOUT_LAST_NAME = Target("Checkout last name", checkout_last_name_locator)
    CHECKOUT_POSTAL_CODE = Target("Checkout postal code", checkout_postal_code_locator)
    CHECKOUT_CONTINUE = Target("Checkout continue button", checkout_continue_locator)
    CHECKOUT_FINISH = Target("Checkout finish button", checkout_finish_locator)
    CHECKOUT_OVERVIEW_ITEM_NAMES = Target(
        "Checkout overview item names", checkout_overview_item_names_locator
    )
    CHECKOUT_PAYMENT_INFO = Target("Checkout payment info", checkout_payment_info_locator)
    CHECKOUT_SHIPPING_INFO = Target("Checkout shipping info", checkout_shipping_info_locator)
    CHECKOUT_SUBTOTAL = Target("Checkout subtotal", checkout_subtotal_locator)
    CHECKOUT_TAX = Target("Checkout tax", checkout_tax_locator)
    CHECKOUT_TOTAL = Target("Checkout total", checkout_total_locator)
    CHECKOUT_COMPLETE_TITLE = Target("Checkout complete title", checkout_complete_title_locator)
    BACK_TO_PRODUCTS = Target("Back to products button", back_to_products_locator)
    URL = runtime_settings.base_url

    @staticmethod
    def add_to_cart_button_for(product_name: str) -> Target:
        return Target(
            f"Add '{product_name}' to cart button",
            add_to_cart_button_for_product_locator(product_name),
        )
