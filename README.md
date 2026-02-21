# playwright-pytest-screenplay-framework

Python Playwright + pytest project using the Screenplay pattern.

## Feature-to-Test Pipeline

The framework now consumes `.feature` files directly with a deterministic flow:
1. Parse Gherkin (`Feature`, `Background`, `Scenario`, `Scenario Outline`, `Examples`)
2. Expand scenario outlines into runnable scenario cases
3. Map supported step sentences into structured `IntentStep` actions
4. Generate a JSON bundle + pytest module

### Modules

- `intent/plans`: Gherkin parser + scenario outline expander.
- `intent/schemas`: `TestIntent` and `IntentStep` data structures.
- `mapper`: Deterministic mapping from supported login-feature steps to canonical actions.
- `engine`: Orchestrates parse -> map -> JSON -> pytest generation.

## Example Usage

```python
from engine import generate_from_feature_file

intents, json_path, test_path = generate_from_feature_file(
    feature_file_path="tests/login_page.feature",
    json_output_path="generated/intent/login_feature_bundle.json",
    test_output_path="generated/tests/test_generated_login_feature.py",
)
```

## Output

- JSON: one bundle file containing all expanded scenarios and mapped steps.
- Pytest: one module with one test function per expanded scenario.

The generated pytest tests expect the `customer` fixture from `tests/conftest.py`.
