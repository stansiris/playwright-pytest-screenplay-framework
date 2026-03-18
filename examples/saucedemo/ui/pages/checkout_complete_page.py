import re

from screenplay_core.playwright.target import Target

CHECKOUT_COMPLETE_TITLE_TEXT = re.compile(r"^Checkout: Complete!$")


def checkout_complete_title_locator(page):
    return page.locator('[data-test="title"]', has_text=CHECKOUT_COMPLETE_TITLE_TEXT)


def checkout_complete_header_locator(page):
    return page.locator('[data-test="complete-header"]')


def checkout_complete_text_locator(page):
    return page.locator('[data-test="complete-text"]')


def checkout_complete_pony_image_locator(page):
    return page.locator('[data-test="pony-express"]')


class CheckoutCompletePage:
    CHECKOUT_COMPLETE_TITLE = Target("Checkout complete title", checkout_complete_title_locator)
    CHECKOUT_COMPLETE_HEADER = Target("Checkout complete header", checkout_complete_header_locator)
    CHECKOUT_COMPLETE_TEXT = Target("Checkout complete text", checkout_complete_text_locator)
    CHECKOUT_COMPLETE_PONY_IMAGE = Target(
        "Checkout complete pony image", checkout_complete_pony_image_locator
    )
