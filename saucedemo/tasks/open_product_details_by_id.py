from screenplay_core.abilities.browse_the_web import BrowseTheWeb
from screenplay_core.core.actor import Actor
from screenplay_core.core.task import Task
from screenplay_core.interactions.navigate_to import NavigateTo


class OpenProductDetailsById(Task):
    """Task: open product details page directly by product id."""

    def __init__(self, product_id: int):
        self.product_id = product_id

    def __repr__(self) -> str:
        return f"OpenProductDetailsById(product_id={self.product_id})"

    def perform_as(self, actor: Actor) -> None:
        base_url = actor.ability_to(BrowseTheWeb).base_url
        if not base_url:
            raise ValueError(
                "BrowseTheWeb ability must include a base_url to open product details."
            )
        actor.attempts_to(NavigateTo(f"{base_url}inventory-item.html?id={self.product_id}"))

    @classmethod
    def with_id(cls, product_id: int) -> "OpenProductDetailsById":
        return cls(product_id)
