"""Maps extracted documentation steps into canonical test intents."""

from __future__ import annotations

import re
from collections.abc import Sequence

from intent.schemas import IntentStep, TestIntent

_FILL_VALUE_RE = re.compile(r"\.fill\((['\"])(?P<value>.*?)\1\)")
_ASSERT_TEXT_RE = re.compile(r"to_contain_text\((['\"])(?P<value>.*?)\1\)", re.IGNORECASE)


def map_documentation_to_intent(
    documented_steps: Sequence[str],
    test_name: str = "test_generated_flow",
    actor_name: str = "Customer",
) -> TestIntent:
    """
    Map documentation lines to a structured SauceDemo test intent.

    This mapper is intentionally minimal and focused on the current
    SauceDemo purchase/logout flow.
    """

    normalized_steps = [step.strip() for step in documented_steps if step and step.strip()]
    if not normalized_steps:
        raise ValueError("No documented steps were provided for mapping.")

    joined_lower = "\n".join(step.lower() for step in normalized_steps)

    username = _extract_field_value(normalized_steps, "username")
    password = _extract_field_value(normalized_steps, "password")
    first_name = _extract_field_value(normalized_steps, "firstName", "first name", "firstname")
    last_name = _extract_field_value(normalized_steps, "lastName", "last name", "lastname")
    postal_code = _extract_field_value(normalized_steps, "postalCode", "postal code", "zipcode", "zip")

    checkout_complete_text = _extract_assertion_text(
        normalized_steps, "checkout: complete", "checkout complete", "data-test=\"title\""
    )
    login_button_text = _extract_assertion_text(
        normalized_steps, "data-test=\"login-button\"", "login button", "login"
    )

    steps: list[IntentStep] = []

    if username and password:
        steps.append(
            IntentStep(
                action="login",
                params={"username": username, "password": password},
                source="credentials extracted from documentation",
            )
        )

    if _contains_any(
        joined_lower,
        "add-to-cart-test.allthethings()-t-shirt-(red)",
        "add red t-shirt",
        "add red t shirt",
    ):
        steps.append(
            IntentStep(
                action="add_product_to_cart",
                params={"product": "red_t_shirt"},
                source="add-to-cart signal detected",
            )
        )

    if _contains_any(
        joined_lower,
        "shopping-cart-link",
        "data-test=\"checkout\"",
        "begin checkout",
        "start checkout",
        "click checkout",
    ):
        steps.append(IntentStep(action="begin_checkout", source="cart/checkout signal detected"))

    has_checkout_details = any([first_name, last_name, postal_code]) or _contains_any(
        joined_lower,
        "data-test=\"firstname\"",
        "data-test=\"lastname\"",
        "data-test=\"postalcode\"",
        "checkout information",
    )
    if has_checkout_details:
        steps.append(
            IntentStep(
                action="provide_checkout_information",
                params={
                    "first_name": first_name or "FIRST_NAME",
                    "last_name": last_name or "LAST_NAME",
                    "postal_code": postal_code or "POSTAL_CODE",
                },
                source="checkout form signal detected",
            )
        )

    if _contains_any(joined_lower, "data-test=\"finish\"", "click finish", "finish checkout"):
        steps.append(IntentStep(action="complete_checkout", source="finish signal detected"))

    if checkout_complete_text:
        steps.append(
            IntentStep(
                action="wait_until_visible",
                params={"target": "CHECKOUT_COMPLETE_TITLE"},
                source="checkout completion assertion detected",
            )
        )
        steps.append(
            IntentStep(
                action="assert_text",
                params={"target": "CHECKOUT_COMPLETE_TITLE", "expected": checkout_complete_text},
                source="checkout completion assertion detected",
            )
        )

    if _contains_any(joined_lower, "back-to-products", "back to products"):
        steps.append(IntentStep(action="return_to_products", source="back-to-products signal detected"))

    if _contains_any(joined_lower, "logout-sidebar-link", "log out", "logout"):
        steps.append(IntentStep(action="logout", source="logout signal detected"))

    if login_button_text:
        steps.append(
            IntentStep(
                action="wait_until_visible",
                params={"target": "LOGIN_BUTTON"},
                source="login assertion detected",
            )
        )
        steps.append(
            IntentStep(
                action="assert_text",
                params={"target": "LOGIN_BUTTON", "expected": login_button_text},
                source="login assertion detected",
            )
        )

    if not steps:
        raise ValueError(
            "No supported SauceDemo actions were recognized. "
            "Provide steps that include login, cart, checkout, or logout actions."
        )

    return TestIntent(
        name=test_name,
        actor_name=actor_name,
        steps=steps,
        metadata={"mapper": "saucedemo-v1", "source_steps": normalized_steps},
    )


def _contains_any(text: str, *tokens: str) -> bool:
    lower_text = text.lower()
    return any(token.lower() in lower_text for token in tokens)


def _extract_fill_value(step: str) -> str | None:
    match = _FILL_VALUE_RE.search(step)
    if match:
        return match.group("value").strip()
    return None


def _extract_field_value(steps: Sequence[str], *labels: str) -> str | None:
    for step in steps:
        lower_step = step.lower()
        if not any(label.lower() in lower_step for label in labels):
            continue

        fill_value = _extract_fill_value(step)
        if fill_value:
            return fill_value

        for label in labels:
            quoted_pattern = re.compile(
                rf"{re.escape(label)}[^\"']*['\"](?P<value>[^\"']+)['\"]", re.IGNORECASE
            )
            quoted_match = quoted_pattern.search(step)
            if quoted_match:
                return quoted_match.group("value").strip()

            plain_pattern = re.compile(
                rf"{re.escape(label)}\s*(?:is|=|:)\s*(?P<value>[A-Za-z0-9_.-]+)",
                re.IGNORECASE,
            )
            plain_match = plain_pattern.search(step)
            if plain_match:
                return plain_match.group("value").strip()

    return None


def _extract_assertion_text(steps: Sequence[str], *hints: str) -> str | None:
    for step in steps:
        lower_step = step.lower()
        if hints and not any(hint.lower() in lower_step for hint in hints):
            continue

        match = _ASSERT_TEXT_RE.search(step)
        if match:
            return match.group("value").strip()

    if any("checkout: complete!" in step.lower() for step in steps):
        return "Checkout: Complete!"
    if any("login button" in step.lower() for step in steps):
        return "Login"

    return None
