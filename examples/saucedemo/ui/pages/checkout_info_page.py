from screenplay_core.playwright.target import Target


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


class CheckoutInfoPage:
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
