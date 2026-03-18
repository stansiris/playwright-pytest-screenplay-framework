from screenplay_core.playwright.target import Target


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


class ProductDetailsPage:
    PRODUCT_DETAILS_NAME = Target("Product details name", product_details_name_locator)
    PRODUCT_DETAILS_PRICE = Target("Product details price", product_details_price_locator)
    PRODUCT_DETAILS_DESCRIPTION = Target(
        "Product details description", product_details_description_locator
    )
    PRODUCT_DETAILS_ACTION_BUTTON = Target(
        "Product details add/remove button", product_details_action_button_locator
    )
    PRODUCT_DETAILS_IMAGE = Target("Product details image", product_details_image_locator)
