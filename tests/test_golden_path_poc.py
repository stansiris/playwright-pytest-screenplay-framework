from screenplay.interactions.wait_until_visible import WaitUntilVisible
from screenplay.questions.text_of import TextOf
from screenplay.tasks.add_product_to_cart import AddProductToCart
from screenplay.tasks.begin_checkout import BeginCheckout
from screenplay.tasks.complete_checkout import CompleteCheckout
from screenplay.tasks.login import Login
from screenplay.tasks.logout import Logout
from screenplay.tasks.provide_checkout_information import ProvideCheckoutInformation
from screenplay.tasks.return_to_products import ReturnToProducts
from screenplay.ui.saucedemo import SauceDemo


def test_golden_path_purchase_and_logout(customer):
    customer.attempts_to(
        Login.with_credentials("standard_user", "secret_sauce"),
        AddProductToCart.red_t_shirt(),
        BeginCheckout(),
        ProvideCheckoutInformation.as_customer("John", "Doe", "12345"),
        CompleteCheckout(),
        WaitUntilVisible.for_(SauceDemo.CHECKOUT_COMPLETE_TITLE),
    )

    assert customer.asks_for(TextOf(SauceDemo.CHECKOUT_COMPLETE_TITLE)) == "Checkout: Complete!"

    customer.attempts_to(
        ReturnToProducts(),
        Logout(),
        WaitUntilVisible.for_(SauceDemo.LOGIN_BUTTON),
    )

    assert customer.asks_for(TextOf(SauceDemo.LOGIN_BUTTON)) == "Login"
