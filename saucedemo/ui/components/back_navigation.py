from screenplay_core.core.target import Target


def back_to_products_locator(page):
    return page.locator('[data-test="back-to-products"]')


class BackNavigation:
    BACK_TO_PRODUCTS = Target("Back to products button", back_to_products_locator)
