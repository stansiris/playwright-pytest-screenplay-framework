from pytest_bdd import then

from screenplay.interactions.wait_until_visible import WaitUntilVisible
from screenplay.questions.on_inventory_page import OnInventoryPage
from screenplay.ui.saucedemo import SauceDemo


@then("I should be on the inventory page")
def should_be_on_inventory_page(customer) -> None:
    customer.attempts_to(WaitUntilVisible.for_(SauceDemo.INVENTORY_CONTAINER))
    assert customer.asks_for(OnInventoryPage())
