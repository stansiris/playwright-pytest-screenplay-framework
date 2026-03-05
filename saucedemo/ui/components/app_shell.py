from screenplay_core.core.target import Target


def page_title_locator(page):
    return page.locator('[data-test="title"]')


def menu_button_locator(page):
    return page.get_by_role("button", name="Open Menu")


def logout_link_locator(page):
    return page.locator('[data-test="logout-sidebar-link"]')


def shopping_cart_link_locator(page):
    return page.locator('[data-test="shopping-cart-link"]')


def shopping_cart_badge_locator(page):
    return page.locator('[data-test="shopping-cart-badge"]')


class AppShell:
    PAGE_TITLE = Target("Page title", page_title_locator)
    MENU_BUTTON = Target("Open Menu button", menu_button_locator)
    LOGOUT_LINK = Target("Logout link", logout_link_locator)
    SHOPPING_CART_LINK = Target("Shopping cart link", shopping_cart_link_locator)
    SHOPPING_CART_BADGE = Target("Shopping cart badge", shopping_cart_badge_locator)
