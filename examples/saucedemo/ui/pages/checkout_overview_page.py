from screenplay_core.playwright.target import Target


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


class CheckoutOverviewPage:
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
