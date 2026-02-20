"""Engine for documentation -> intent JSON -> pytest generation."""

from __future__ import annotations

import json
import re
from pathlib import Path

from intent.plans import extract_documented_steps
from intent.schemas import IntentStep, TestIntent
from mapper import map_documentation_to_intent

_ACTION_IMPORTS = {
    "login": "from screenplay.tasks.login import Login",
    "add_product_to_cart": "from screenplay.tasks.add_product_to_cart import AddProductToCart",
    "begin_checkout": "from screenplay.tasks.begin_checkout import BeginCheckout",
    "provide_checkout_information": (
        "from screenplay.tasks.provide_checkout_information import ProvideCheckoutInformation"
    ),
    "complete_checkout": "from screenplay.tasks.complete_checkout import CompleteCheckout",
    "return_to_products": "from screenplay.tasks.return_to_products import ReturnToProducts",
    "logout": "from screenplay.tasks.logout import Logout",
    "wait_until_visible": "from screenplay.interactions.wait_until_visible import WaitUntilVisible",
    "assert_text": "from screenplay.questions.text_of import TextOf",
}

_TARGET_EXPRESSIONS = {
    "CHECKOUT_COMPLETE_TITLE": "SauceDemo.CHECKOUT_COMPLETE_TITLE",
    "LOGIN_BUTTON": "SauceDemo.LOGIN_BUTTON",
}


def build_intent_from_documentation(
    documentation: str,
    test_name: str = "test_generated_flow",
    actor_name: str = "Customer",
) -> TestIntent:
    """Extract and map documentation into a canonical test intent."""

    documented_steps = extract_documented_steps(documentation)
    return map_documentation_to_intent(
        documented_steps=documented_steps,
        test_name=test_name,
        actor_name=actor_name,
    )


def render_pytest_test(intent: TestIntent, test_function_name: str | None = None) -> str:
    """Render a pytest test function from a mapped intent."""

    imports = _required_imports(intent.steps)
    function_name = _test_function_name(test_function_name or intent.name)
    body_lines = _render_test_body(intent.steps)

    if not body_lines:
        body_lines = ["    pass"]

    rendered = []
    rendered.extend(sorted(imports))
    rendered.append("")
    rendered.append("")
    rendered.append(f"def {function_name}(customer):")
    rendered.extend(body_lines)
    rendered.append("")
    return "\n".join(rendered)


def generate_test_file_from_intent(
    intent: TestIntent,
    output_path: str | Path,
    test_function_name: str | None = None,
) -> Path:
    """Generate a pytest module from an intent and write it to disk."""

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_pytest_test(intent, test_function_name=test_function_name), encoding="utf-8")
    return path


def generate_from_documentation(
    documentation: str,
    json_output_path: str | Path,
    test_output_path: str | Path,
    test_name: str = "test_generated_flow",
    actor_name: str = "Customer",
) -> tuple[TestIntent, Path, Path]:
    """
    End-to-end helper:
    documentation -> mapped intent -> JSON + pytest file.
    """

    intent = build_intent_from_documentation(
        documentation=documentation,
        test_name=test_name,
        actor_name=actor_name,
    )
    json_path = intent.write_json(json_output_path)
    test_path = generate_test_file_from_intent(intent, output_path=test_output_path)
    return intent, json_path, test_path


def _required_imports(steps: list[IntentStep]) -> set[str]:
    imports = set()
    needs_saucedemo = False

    for step in steps:
        action_import = _ACTION_IMPORTS.get(step.action)
        if action_import:
            imports.add(action_import)

        if step.action in {"wait_until_visible", "assert_text"}:
            needs_saucedemo = True

    if needs_saucedemo:
        imports.add("from screenplay.ui.saucedemo import SauceDemo")

    return imports


def _render_test_body(steps: list[IntentStep]) -> list[str]:
    blocks: list[tuple[str, list[str] | str]] = []
    attempt_buffer: list[str] = []

    for step in steps:
        if step.action == "assert_text":
            if attempt_buffer:
                blocks.append(("attempts", attempt_buffer.copy()))
                attempt_buffer.clear()
            blocks.append(("assert", _render_assert_step(step)))
            continue

        attempt_buffer.append(_render_attempt_step(step))

    if attempt_buffer:
        blocks.append(("attempts", attempt_buffer))

    lines: list[str] = []
    for index, (block_type, payload) in enumerate(blocks):
        if block_type == "attempts":
            attempts = payload if isinstance(payload, list) else []
            lines.append("    customer.attempts_to(")
            for attempt in attempts:
                lines.append(f"        {attempt},")
            lines.append("    )")
        else:
            lines.append(f"    {payload}")

        if index < len(blocks) - 1:
            lines.append("")

    return lines


def _render_attempt_step(step: IntentStep) -> str:
    params = step.params

    if step.action == "login":
        return (
            "Login.with_credentials("
            f"{_quoted(params.get('username'))}, {_quoted(params.get('password'))})"
        )
    if step.action == "add_product_to_cart":
        product = str(params.get("product", "red_t_shirt"))
        if product != "red_t_shirt":
            raise ValueError(f"Unsupported product mapping: {product}")
        return "AddProductToCart.red_t_shirt()"
    if step.action == "begin_checkout":
        return "BeginCheckout()"
    if step.action == "provide_checkout_information":
        return (
            "ProvideCheckoutInformation.as_customer("
            f"{_quoted(params.get('first_name'))}, "
            f"{_quoted(params.get('last_name'))}, "
            f"{_quoted(params.get('postal_code'))})"
        )
    if step.action == "complete_checkout":
        return "CompleteCheckout()"
    if step.action == "return_to_products":
        return "ReturnToProducts()"
    if step.action == "logout":
        return "Logout()"
    if step.action == "wait_until_visible":
        target_expression = _target_expression(str(params.get("target")))
        return f"WaitUntilVisible.for_({target_expression})"

    raise ValueError(f"Unsupported action in attempt block: {step.action}")


def _render_assert_step(step: IntentStep) -> str:
    if step.action != "assert_text":
        raise ValueError(f"Unsupported assert action: {step.action}")

    target_expression = _target_expression(str(step.params.get("target")))
    expected = _quoted(step.params.get("expected"))
    return f"assert customer.asks_for(TextOf({target_expression})) == {expected}"


def _target_expression(target_name: str) -> str:
    expression = _TARGET_EXPRESSIONS.get(target_name)
    if not expression:
        raise ValueError(f"Unknown target name for generator: {target_name}")
    return expression


def _quoted(value: object) -> str:
    return json.dumps("" if value is None else str(value))


def _test_function_name(raw_name: str) -> str:
    normalized = re.sub(r"[^0-9a-zA-Z_]+", "_", raw_name).strip("_").lower()
    if not normalized:
        normalized = "generated_flow"
    if not normalized.startswith("test_"):
        normalized = f"test_{normalized}"
    if normalized[0].isdigit():
        normalized = f"test_{normalized}"
    return normalized
