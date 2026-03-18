from examples.saucedemo.ui.pages.checkout_info_page import CheckoutInfoPage
from screenplay_core.core.actor import Actor
from screenplay_core.core.task import Task
from screenplay_core.playwright.interactions.fill import Fill


class EnterCheckoutInformation(Task):
    """Task: fill checkout customer details."""

    def __init__(self, first_name: str, last_name: str, postal_code: str):
        self.first_name = first_name
        self.last_name = last_name
        self.postal_code = postal_code

    def __repr__(self) -> str:
        return (
            "EnterCheckoutInformation("
            f"first_name='{self.first_name}', "
            f"last_name='{self.last_name}', "
            f"postal_code='{self.postal_code}')"
        )

    def perform_as(self, actor: Actor) -> None:
        self.perform_interactions(
            actor,
            Fill(CheckoutInfoPage.CHECKOUT_FIRST_NAME, self.first_name),
            Fill(CheckoutInfoPage.CHECKOUT_LAST_NAME, self.last_name),
            Fill(CheckoutInfoPage.CHECKOUT_POSTAL_CODE, self.postal_code),
        )

    @classmethod
    def as_customer(
        cls, first_name: str, last_name: str, postal_code: str
    ) -> "EnterCheckoutInformation":
        return cls(first_name, last_name, postal_code)
