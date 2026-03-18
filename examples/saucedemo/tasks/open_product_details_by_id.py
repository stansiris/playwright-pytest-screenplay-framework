from screenplay_core.core.actor import Actor
from screenplay_core.core.task import Task
from screenplay_core.playwright.interactions.navigate_to import NavigateTo


class OpenProductDetailsById(Task):
    """Task: open product details page directly by product id."""

    def __init__(self, product_id: int):
        self.product_id = product_id

    def __repr__(self) -> str:
        return f"OpenProductDetailsById(product_id={self.product_id})"

    def perform_as(self, actor: Actor) -> None:
        self.perform_interactions(actor, NavigateTo(f"/inventory-item.html?id={self.product_id}"))

    @classmethod
    def with_id(cls, product_id: int) -> "OpenProductDetailsById":
        return cls(product_id)
