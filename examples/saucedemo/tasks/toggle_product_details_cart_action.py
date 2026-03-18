from examples.saucedemo.ui.pages.product_details_page import ProductDetailsPage
from screenplay_core.core.actor import Actor
from screenplay_core.core.task import Task
from screenplay_core.playwright.interactions.click import Click


class ToggleProductDetailsCartAction(Task):
    """Task: click the add/remove action button on product details page."""

    def perform_as(self, actor: Actor) -> None:
        self.perform_interactions(actor, Click(ProductDetailsPage.PRODUCT_DETAILS_ACTION_BUTTON))
