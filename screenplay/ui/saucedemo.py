class SauceDemo:
    """
    Central place for SauceDemo selectors.
    Keep selectors here so Tasks/Interactions stay clean.
    """

    # URL
    URL = "https://www.saucedemo.com/"

    # Login page
    USERNAME = "#user-name"
    PASSWORD = "#password"
    LOGIN_BUTTON = "#login-button"

    # Post-login (inventory page)
    INVENTORY_CONTAINER = "[data-test='inventory-container']"
