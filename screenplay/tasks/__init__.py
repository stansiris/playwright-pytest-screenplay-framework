"""Screenplay tasks package."""

from screenplay.tasks.add_product_to_cart import AddProductToCart
from screenplay.tasks.begin_checkout import BeginCheckout
from screenplay.tasks.click_login import ClickLogin
from screenplay.tasks.complete_checkout import CompleteCheckout
from screenplay.tasks.continue_checkout import ContinueCheckout
from screenplay.tasks.dismiss_login_error import DismissLoginError
from screenplay.tasks.enter_checkout_information import EnterCheckoutInformation
from screenplay.tasks.enter_password import EnterPassword
from screenplay.tasks.enter_username import EnterUsername
from screenplay.tasks.go_to_cart import GoToCart
from screenplay.tasks.login import Login
from screenplay.tasks.logout import Logout
from screenplay.tasks.open_saucedemo import OpenSauceDemo
from screenplay.tasks.proceed_to_checkout import ProceedToCheckout
from screenplay.tasks.provide_checkout_information import ProvideCheckoutInformation
from screenplay.tasks.return_to_products import ReturnToProducts
from screenplay.tasks.sort_inventory import SortInventory

__all__ = [
    "AddProductToCart",
    "BeginCheckout",
    "ClickLogin",
    "CompleteCheckout",
    "ContinueCheckout",
    "DismissLoginError",
    "EnterCheckoutInformation",
    "EnterPassword",
    "EnterUsername",
    "GoToCart",
    "Login",
    "Logout",
    "OpenSauceDemo",
    "ProceedToCheckout",
    "ProvideCheckoutInformation",
    "ReturnToProducts",
    "SortInventory",
]
