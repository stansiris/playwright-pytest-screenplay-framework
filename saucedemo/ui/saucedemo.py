import re

from screenplay_core.core.target import Target

CHECKOUT_COMPLETE_TITLE_TEXT = re.compile(r"^Checkout: Complete!$")


def _inventory_card_for_product(page, product_name: str):
    exact_name = re.compile(rf"^{re.escape(product_name)}$")
    return page.locator('[data-test="inventory-item"]').filter(
        has=page.locator('[data-test="inventory-item-name"]', has_text=exact_name)
    )


def login_logo_locator(page):
    return page.locator(".login_logo")


def page_title_locator(page):
    return page.locator('[data-test="title"]')


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


def inventory_sort_options_locator(page):
    return page.locator('[data-test="product-sort-container"] option')


def inventory_item_names_locator(page):
    return page.locator('[data-test="inventory-item-name"]')


def inventory_item_prices_locator(page):
    return page.locator('[data-test="inventory-item-price"]')


def inventory_add_to_cart_buttons_locator(page):
    return page.locator('button[data-test^="add-to-cart"]')


def add_to_cart_red_tshirt_locator(page):
    return page.locator('[data-test="add-to-cart-test.allthethings()-t-shirt-(red)"]')


def inventory_item_name_for_product_locator(product_name: str):
    exact_name = re.compile(rf"^{re.escape(product_name)}$")

    def locator(page):
        return page.locator('[data-test="inventory-item-name"]', has_text=exact_name)

    return locator


def inventory_item_price_for_product_locator(product_name: str):
    def locator(page):
        return _inventory_card_for_product(page, product_name).locator(
            '[data-test="inventory-item-price"]'
        )

    return locator


def inventory_item_description_for_product_locator(product_name: str):
    def locator(page):
        return _inventory_card_for_product(page, product_name).locator(
            '[data-test="inventory-item-desc"]'
        )

    return locator


def inventory_item_action_button_for_product_locator(product_name: str):
    def locator(page):
        return _inventory_card_for_product(page, product_name).locator("button")

    return locator


def add_to_cart_button_for_product_locator(product_name: str):
    """Build a locator function for the add-to-cart button of a named product."""

    def locator(page):
        return _inventory_card_for_product(page, product_name).locator(
            'button[data-test^="add-to-cart"]'
        )

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


def checkout_info_cancel_locator(page):
    return page.locator('[data-test="cancel"]')


def checkout_info_error_message_locator(page):
    return page.locator('[data-test="error"]')


def checkout_info_error_close_button_locator(page):
    return page.locator('[data-test="error-button"]')


def checkout_finish_locator(page):
    return page.locator('[data-test="finish"]')


def checkout_overview_item_names_locator(page):
    return page.locator('[data-test="inventory-item-name"]')


def checkout_overview_item_prices_locator(page):
    return page.locator('[data-test="inventory-item-price"]')


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
    return page.locator('[data-test="title"]', has_text=CHECKOUT_COMPLETE_TITLE_TEXT)


def checkout_complete_header_locator(page):
    return page.locator('[data-test="complete-header"]')


def checkout_complete_text_locator(page):
    return page.locator('[data-test="complete-text"]')


def checkout_complete_pony_image_locator(page):
    return page.locator('[data-test="pony-express"]')


def product_details_name_locator(page):
    return page.locator('[data-test="inventory-item-name"]')


def product_details_price_locator(page):
    return page.locator('[data-test="inventory-item-price"]')


def product_details_description_locator(page):
    return page.locator('[data-test="inventory-item-desc"]')


def product_details_action_button_locator(page):
    return page.locator('button[data-test^="add-to-cart"], button[data-test^="remove"]')


def product_details_image_locator(page):
    return page.locator(".inventory_details_img")


def back_to_products_locator(page):
    return page.locator('[data-test="back-to-products"]')


class SauceDemo:
    PRODUCT_RED_TSHIRT = "Test.allTheThings() T-Shirt (Red)"

    LOGIN_LOGO = Target("Login logo", login_logo_locator)
    MENU_BUTTON = Target("Open Menu button", menu_button_locator)
    LOGOUT_LINK = Target("Logout link", logout_link_locator)
    LOGIN_BUTTON = Target("Login button", login_button_locator)
    LOGIN_USERNAME = Target("Login username", login_username_locator)
    LOGIN_PASSWORD = Target("Login password", login_password_locator)
    LOGIN_ERROR_MESSAGE = Target("Login error message", login_error_message_locator)
    LOGIN_ERROR_CLOSE_BUTTON = Target("Login error close button", login_error_close_button_locator)
    PAGE_TITLE = Target("Page title", page_title_locator)
    INVENTORY_CONTAINER = Target("Inventory Products List", inventory_container_locator)
    INVENTORY_SORT = Target("Inventory sort dropdown", inventory_sort_locator)
    INVENTORY_SORT_OPTIONS = Target("Inventory sort options", inventory_sort_options_locator)
    INVENTORY_ITEM_NAMES = Target("Inventory item names", inventory_item_names_locator)
    INVENTORY_ITEM_PRICES = Target("Inventory item prices", inventory_item_prices_locator)
    INVENTORY_ADD_TO_CART_BUTTONS = Target(
        "Inventory add-to-cart buttons", inventory_add_to_cart_buttons_locator
    )
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
    CHECKOUT_INFO_CANCEL_BUTTON = Target(
        "Checkout info cancel button", checkout_info_cancel_locator
    )
    CHECKOUT_INFO_ERROR_MESSAGE = Target(
        "Checkout info error message", checkout_info_error_message_locator
    )
    CHECKOUT_INFO_ERROR_CLOSE_BUTTON = Target(
        "Checkout info error close button", checkout_info_error_close_button_locator
    )
    CHECKOUT_FINISH = Target("Checkout finish button", checkout_finish_locator)
    CHECKOUT_OVERVIEW_ITEM_NAMES = Target(
        "Checkout overview item names", checkout_overview_item_names_locator
    )
    CHECKOUT_OVERVIEW_ITEM_PRICES = Target(
        "Checkout overview item prices", checkout_overview_item_prices_locator
    )
    CHECKOUT_PAYMENT_INFO = Target("Checkout payment info", checkout_payment_info_locator)
    CHECKOUT_SHIPPING_INFO = Target("Checkout shipping info", checkout_shipping_info_locator)
    CHECKOUT_SUBTOTAL = Target("Checkout subtotal", checkout_subtotal_locator)
    CHECKOUT_TAX = Target("Checkout tax", checkout_tax_locator)
    CHECKOUT_TOTAL = Target("Checkout total", checkout_total_locator)
    CHECKOUT_COMPLETE_TITLE = Target("Checkout complete title", checkout_complete_title_locator)
    CHECKOUT_COMPLETE_HEADER = Target("Checkout complete header", checkout_complete_header_locator)
    CHECKOUT_COMPLETE_TEXT = Target("Checkout complete text", checkout_complete_text_locator)
    CHECKOUT_COMPLETE_PONY_IMAGE = Target(
        "Checkout complete pony image", checkout_complete_pony_image_locator
    )
    BACK_TO_PRODUCTS = Target("Back to products button", back_to_products_locator)
    PRODUCT_DETAILS_NAME = Target("Product details name", product_details_name_locator)
    PRODUCT_DETAILS_PRICE = Target("Product details price", product_details_price_locator)
    PRODUCT_DETAILS_DESCRIPTION = Target(
        "Product details description", product_details_description_locator
    )
    PRODUCT_DETAILS_ACTION_BUTTON = Target(
        "Product details add/remove button", product_details_action_button_locator
    )
    PRODUCT_DETAILS_IMAGE = Target("Product details image", product_details_image_locator)

    @staticmethod
    def add_to_cart_button_for(product_name: str) -> Target:
        return Target(
            f"Add '{product_name}' to cart button",
            add_to_cart_button_for_product_locator(product_name),
        )

    @staticmethod
    def inventory_item_name_for(product_name: str) -> Target:
        return Target(
            f"Inventory item name '{product_name}'",
            inventory_item_name_for_product_locator(product_name),
        )

    @staticmethod
    def inventory_item_price_for(product_name: str) -> Target:
        return Target(
            f"Inventory item price '{product_name}'",
            inventory_item_price_for_product_locator(product_name),
        )

    @staticmethod
    def inventory_item_description_for(product_name: str) -> Target:
        return Target(
            f"Inventory item description '{product_name}'",
            inventory_item_description_for_product_locator(product_name),
        )

    @staticmethod
    def inventory_item_action_button_for(product_name: str) -> Target:
        return Target(
            f"Inventory item action button '{product_name}'",
            inventory_item_action_button_for_product_locator(product_name),
        )
