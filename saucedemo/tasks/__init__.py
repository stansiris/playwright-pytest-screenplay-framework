"""Screenplay tasks package."""

from saucedemo.tasks.add_product_to_cart import AddProductToCart
from saucedemo.tasks.begin_checkout import BeginCheckout
from saucedemo.tasks.click_login import ClickLogin
from saucedemo.tasks.complete_checkout import CompleteCheckout
from saucedemo.tasks.continue_checkout import ContinueCheckout
from saucedemo.tasks.dismiss_login_error import DismissLoginError
from saucedemo.tasks.enter_checkout_information import EnterCheckoutInformation
from saucedemo.tasks.go_to_cart import GoToCart
from saucedemo.tasks.login import Login
from saucedemo.tasks.logout import Logout
from saucedemo.tasks.open_saucedemo import OpenSauceDemo
from saucedemo.tasks.proceed_to_checkout import ProceedToCheckout
from saucedemo.tasks.provide_checkout_information import ProvideCheckoutInformation
from saucedemo.tasks.return_to_products import ReturnToProducts
from saucedemo.tasks.sort_inventory import SortInventory

__all__ = [
    "AddProductToCart",
    "BeginCheckout",
    "ClickLogin",
    "CompleteCheckout",
    "ContinueCheckout",
    "DismissLoginError",
    "EnterCheckoutInformation",
    "GoToCart",
    "Login",
    "Logout",
    "OpenSauceDemo",
    "ProceedToCheckout",
    "ProvideCheckoutInformation",
    "ReturnToProducts",
    "SortInventory",
]
