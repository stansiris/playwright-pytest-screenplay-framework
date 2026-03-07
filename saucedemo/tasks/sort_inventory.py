from saucedemo.ui.pages.inventory_page import InventoryPage
from screenplay_core.core.actor import Actor
from screenplay_core.core.task import Task
from screenplay_core.interactions.select_by_value import SelectByValue

SORT_OPTION_VALUE = {
    "Name (A to Z)": "az",
    "Name (Z to A)": "za",
    "Price (low to high)": "lohi",
    "Price (high to low)": "hilo",
}


class SortInventory(Task):
    """Task: sort the inventory list by a human-readable option."""

    def __init__(self, option: str):
        if option not in SORT_OPTION_VALUE:
            supported = ", ".join(SORT_OPTION_VALUE)
            raise ValueError(f"Unsupported sort option '{option}'. Supported values: {supported}")
        self.option = option

    def __repr__(self) -> str:
        return f"SortInventory(option='{self.option}')"

    def perform_as(self, actor: Actor) -> None:
        self.perform_interactions(
            actor,
            SelectByValue(InventoryPage.INVENTORY_SORT, SORT_OPTION_VALUE[self.option]),
        )

    @classmethod
    def by(cls, option: str) -> "SortInventory":
        return cls(option)
