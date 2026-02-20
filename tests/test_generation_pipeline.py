import json

from engine import build_intent_from_documentation, generate_from_documentation

DOCUMENTATION = """
page.goto("https://www.saucedemo.com/")
page.locator('[data-test="username"]').fill("standard_user")
page.locator('[data-test="password"]').fill("secret_sauce")
page.locator('[data-test="add-to-cart-test.allthethings()-t-shirt-(red)"]').click()
page.locator('[data-test="shopping-cart-link"]').click()
page.locator('[data-test="checkout"]').click()
page.locator('[data-test="firstName"]').fill("John")
page.locator('[data-test="lastName"]').fill("Doe")
page.locator('[data-test="postalCode"]').fill("12345")
page.locator('[data-test="continue"]').click()
page.locator('[data-test="finish"]').click()
expect(page.locator('[data-test="title"]')).to_contain_text("Checkout: Complete!")
page.locator('[data-test="back-to-products"]').click()
page.locator('[data-test="logout-sidebar-link"]').click()
expect(page.locator('[data-test="login-button"]')).to_contain_text("Login")
"""


def test_build_intent_from_documentation_maps_expected_flow():
    intent = build_intent_from_documentation(DOCUMENTATION, test_name="generated_purchase_flow")

    assert [step.action for step in intent.steps] == [
        "login",
        "add_product_to_cart",
        "begin_checkout",
        "provide_checkout_information",
        "complete_checkout",
        "wait_until_visible",
        "assert_text",
        "return_to_products",
        "logout",
        "wait_until_visible",
        "assert_text",
    ]

    assert intent.steps[0].params == {"username": "standard_user", "password": "secret_sauce"}
    assert intent.steps[3].params == {
        "first_name": "John",
        "last_name": "Doe",
        "postal_code": "12345",
    }
    assert intent.steps[6].params == {
        "target": "CHECKOUT_COMPLETE_TITLE",
        "expected": "Checkout: Complete!",
    }
    assert intent.steps[10].params == {"target": "LOGIN_BUTTON", "expected": "Login"}


def test_generate_from_documentation_writes_json_and_pytest(tmp_path):
    json_output = tmp_path / "intent" / "generated_purchase_flow.json"
    test_output = tmp_path / "tests" / "test_generated_purchase_flow.py"

    intent, generated_json, generated_test = generate_from_documentation(
        documentation=DOCUMENTATION,
        json_output_path=json_output,
        test_output_path=test_output,
        test_name="generated_purchase_flow",
    )

    assert intent.name == "generated_purchase_flow"
    assert generated_json.exists()
    assert generated_test.exists()

    payload = json.loads(generated_json.read_text(encoding="utf-8"))
    assert payload["name"] == "generated_purchase_flow"
    assert payload["steps"][0]["action"] == "login"

    rendered_test = generated_test.read_text(encoding="utf-8")
    assert "def test_generated_purchase_flow(customer):" in rendered_test
    assert 'Login.with_credentials("standard_user", "secret_sauce")' in rendered_test
    assert "AddProductToCart.red_t_shirt()" in rendered_test
    assert 'assert customer.asks_for(TextOf(SauceDemo.LOGIN_BUTTON)) == "Login"' in rendered_test
