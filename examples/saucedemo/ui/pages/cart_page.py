from screenplay_core.playwright.target import Target


def cart_item_names_locator(page):
    return page.locator('[data-test="inventory-item-name"]')


def checkout_button_locator(page):
    return page.locator('[data-test="checkout"]')


class CartPage:
    CART_ITEM_NAMES = Target("Cart item names", cart_item_names_locator)
    CHECKOUT_BUTTON = Target("Checkout button", checkout_button_locator)
