from screenplay.core.task import Task
from screenplay.interactions.click import Click
from screenplay.interactions.fill import Fill
from screenplay.ui.saucedemo import SauceDemo


class ProvideCheckoutInformation(Task):
    """Task: fill checkout customer details and continue."""

    def __init__(self, first_name: str, last_name: str, postal_code: str):
        self.first_name = first_name
        self.last_name = last_name
        self.postal_code = postal_code

    def __repr__(self) -> str:
        return (
            "ProvideCheckoutInformation("
            f"first_name='{self.first_name}', "
            f"last_name='{self.last_name}', "
            f"postal_code='{self.postal_code}')"
        )

    def perform_as(self, actor) -> None:
        actor.attempts_to(
            Fill(SauceDemo.CHECKOUT_FIRST_NAME, self.first_name),
            Fill(SauceDemo.CHECKOUT_LAST_NAME, self.last_name),
            Fill(SauceDemo.CHECKOUT_POSTAL_CODE, self.postal_code),
            Click(SauceDemo.CHECKOUT_CONTINUE),
        )

    @staticmethod
    def as_customer(first_name: str, last_name: str, postal_code: str):
        return ProvideCheckoutInformation(first_name, last_name, postal_code)
