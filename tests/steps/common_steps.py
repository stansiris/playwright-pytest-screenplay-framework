from pytest_bdd import then

from saucedemo.questions.on_inventory_page import OnInventoryPage
from saucedemo.ui.saucedemo import SauceDemo
from screenplay_core.interactions.wait_until_visible import WaitUntilVisible


@then("I should be on the inventory page")
def should_be_on_inventory_page(customer) -> None:
    customer.attempts_to(WaitUntilVisible.for_(SauceDemo.INVENTORY_CONTAINER))
    assert customer.asks_for(OnInventoryPage())
