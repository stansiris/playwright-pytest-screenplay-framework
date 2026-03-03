# Playwright + Pytest Screenplay Framework

A Python UI automation framework using Playwright, pytest, and the Screenplay pattern,
with `pytest-bdd` as the primary behavior layer.

The repository demonstrates:
- business-readable BDD scenarios
- concise step definitions colocated with each feature test file
- reusable `screenplay_core` framework components
- SauceDemo-specific tasks/questions/locators in a separate `saucedemo` layer
- centralized runtime configuration for project execution

## Current Test Coverage

Current coverage includes both BDD and direct pytest modules:
- BDD flows:
  - end-to-end smoke flow: `tests/features/golden_path.feature` -> `tests/test_golden_path_bdd.py`
  - login behavior mirror flow: `tests/features/login.feature` -> `tests/test_login_bdd.py`
- direct pytest + Screenplay integration tests:
  - `tests/test_login.py`
  - `tests/test_inventory.py`
  - `tests/test_product_details.py`
  - `tests/test_checkout_info.py`
  - `tests/test_checkout_complete.py`
- UI presentation checks for each core page:
  - `tests/test_ui_pages.py`

## Setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m playwright install
pytest -q
```

## CI-Ready Formatting

CI validates code style before running tests:
- `python -m ruff check .`
- `python -m black --check .`

Use these locally before pushing:

```powershell
python -m ruff check .
python -m black .
```

If you want the same validation behavior as CI without modifying files:

```powershell
python -m ruff check .
python -m black --check .
```

## Test Reporting

Pytest generates test artifacts automatically into `test-results/`:
- `junit.xml` for CI parsing/integrations
- `report.html` as a shareable HTML report
- failure screenshots (`--screenshot=only-on-failure`)
- Playwright traces on failures (`--tracing=retain-on-failure`)

In GitHub Actions, `test-results/` is uploaded as a workflow artifact even when tests fail.

## Runtime Configuration

Runtime settings are environment-driven through `saucedemo/config/runtime.py`.

| Variable | Default | Description |
| --- | --- | --- |
| `BASE_URL` | `https://www.saucedemo.com/` | Application base URL used by `OpenSauceDemo`/`OpenLoginPage` navigation tasks. |
| `BROWSER` | `chromium` | Default browser for pytest-playwright (`chromium`, `firefox`, `webkit`). |
| `HEADED` | `false` | Run tests headed when true (`true/false`, `1/0`, `yes/no`). |
| `SLOW_MO_MS` | `0` | Slow motion delay in milliseconds for browser actions. |
| `DEFAULT_TIMEOUT_MS` | `5000` | Default timeout for waits. Reusable core also supports `SCREENPLAY_DEFAULT_TIMEOUT_MS`. |

Example:

```powershell
$env:BASE_URL = "https://www.saucedemo.com"
$env:BROWSER = "firefox"
$env:HEADED = "true"
$env:SLOW_MO_MS = "150"
$env:DEFAULT_TIMEOUT_MS = "7000"
$env:SCREENPLAY_DEFAULT_TIMEOUT_MS = "7000"
pytest -q
```

## Current API

### Reusable `screenplay_core`
- `Actor`
- `Task`
- `Interaction`
- `Question`
- `Target`
- `BrowseTheWeb`
- Interactions: `Click`, `Fill`, `Focus`, `NavigateTo`, `PressKey`, `RefreshPage`, `ScrollIntoView`, `SelectByValue`, `WaitUntilVisible`, `WaitUntilHidden`
- Questions: `TextOf`, `TextsOf`, `IsVisible`, `IsFocused`, `FocusIndicatorVisible`, `AttributeOf`, `CurrentUrl`

### SauceDemo Domain (`saucedemo`)
- Questions: `OnLoginPage`, `OnInventoryPage`, `CartBadgeCount`, `TotalsMatchComputedSum`
- Tasks:
- `OpenSauceDemo.app()`
- `OpenLoginPage()`
- `Login.with_credentials(username, password)`
- `Login.with_username_only(username)`
- `Login.with_password_only(password)`
- `ClickLogin()`
- `DismissLoginError()`
- `SortInventory.by(option)`
- `AddProductToCart.named(product_name)`
- `GoToCart()`
- `ProceedToCheckout()`
- `EnterCheckoutInformation.as_customer(first_name, last_name, postal_code)`
- `ContinueCheckout()`
- `CompleteCheckout()`
- `ReturnToProducts()`
- `BeginCheckout()`
- `ProvideCheckoutInformation.as_customer(first_name, last_name, postal_code)`
- `Logout()`

## Project Structure

```text
screenplay_core/
|-- abilities/      # Reusable abilities (BrowseTheWeb)
|-- core/           # Actor, Task, Interaction, Question, Target
|-- interactions/   # Reusable low-level browser interactions
`-- questions/      # Reusable generic questions

saucedemo/
|-- config/         # Project runtime settings (env-driven)
|-- tasks/          # SauceDemo business-level actions
|-- questions/      # SauceDemo-specific queries
`-- ui/             # SauceDemo locators/targets

tests/
|-- features/       # Gherkin scenarios
|-- conftest.py     # fixture wiring + runtime defaults
`-- test_*.py       # BDD step adapters and direct pytest + Screenplay tests

docs/
|-- architecture.md
|-- codex_workflow.md
|-- design_decisions.md
|-- domain_model.md
|-- engine_flows.md
|-- project_presentation.md
`-- step_vocabulary.md
```

## Test Modes

### 1. pytest-bdd + Screenplay (primary)
- Gherkin defines behavior.
- Step definitions (in `tests/test_golden_path_bdd.py` and `tests/test_login_bdd.py`) map phrases to Tasks/Questions.
- Business intent stays separate from UI mechanics.

### 2. Direct pytest + Screenplay (supported)
- Useful for focused workflow tests and refactoring safety.
- Current examples: `tests/test_login.py`, `tests/test_inventory.py`, `tests/test_product_details.py`, `tests/test_checkout_info.py`, `tests/test_checkout_complete.py`, and `tests/test_ui_pages.py`.

## Documentation

- Domain model: `docs/domain_model.md`
- Step vocabulary: `docs/step_vocabulary.md`
- Architecture: `docs/architecture.md`
- Composed engine flows: `docs/engine_flows.md`
- Design rationale: `docs/design_decisions.md`
- Codex generation workflow: `docs/codex_workflow.md`
- Presentation guide: `docs/project_presentation.md`


