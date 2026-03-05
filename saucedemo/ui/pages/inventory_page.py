import re

from screenplay_core.core.target import Target


def _inventory_card_for_product(page, product_name: str):
    exact_name = re.compile(rf"^{re.escape(product_name)}$")
    return page.locator('[data-test="inventory-item"]').filter(
        has=page.locator('[data-test="inventory-item-name"]', has_text=exact_name)
    )


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
    def locator(page):
        return _inventory_card_for_product(page, product_name).locator(
            'button[data-test^="add-to-cart"]'
        )

    return locator


class InventoryPage:
    PRODUCT_RED_TSHIRT = "Test.allTheThings() T-Shirt (Red)"

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
