# playwright-pytest-screenplay-framework

Python Playwright + pytest project using the Screenplay pattern.

## Documentation-to-Test Pipeline (Minimal Scaffold)

This repository now includes a basic pipeline for:
1. Reading user documentation (plain text, markdown bullets, or Playwright-like steps)
2. Mapping it into structured JSON intent
3. Generating pytest Screenplay test code from that JSON

### Modules

- `intent/plans`: Extracts raw, actionable lines from documentation text.
- `intent/schemas`: Defines `TestIntent` and `IntentStep` data structures and JSON helpers.
- `mapper`: Maps extracted lines to canonical SauceDemo flow actions.
- `engine`: Orchestrates extract -> map -> JSON -> pytest test generation.

## Example Usage

```python
from engine import generate_from_documentation

documentation = """
1. Go to https://www.saucedemo.com/
2. Login with username "standard_user" and password "secret_sauce"
3. Add red t-shirt to cart
4. Start checkout
5. Fill first name "John", last name "Doe", and postal code "12345"
6. Finish checkout and verify "Checkout: Complete!"
7. Return to products, logout, and verify login button text "Login"
"""

intent, json_path, test_path = generate_from_documentation(
    documentation=documentation,
    json_output_path="generated/intent/golden_path.json",
    test_output_path="generated/tests/test_generated_golden_path.py",
    test_name="generated_golden_path",
)
```

The generated pytest test expects the `customer` fixture (already provided in `tests/conftest.py`).
