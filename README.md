# Playwright + Pytest Screenplay Framework

A Python UI automation framework using Playwright, pytest, and the Screenplay pattern,
with `pytest-bdd` as the primary behavior layer.

The repository demonstrates:
- business-readable BDD scenarios
- thin step definitions
- reusable Screenplay Tasks, Questions, and Interactions
- centralized locators and runtime configuration

## Setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m playwright install
pytest -q
```

## Test Reporting

Pytest generates test artifacts automatically into `test-results/`:
- `junit.xml` for CI parsing/integrations
- `report.html` as a shareable HTML report
- failure screenshots (`--screenshot=only-on-failure`)
- Playwright traces on failures (`--tracing=retain-on-failure`)

In GitHub Actions, `test-results/` is uploaded as a workflow artifact even when tests fail.

## Runtime Configuration

Runtime settings are environment-driven through `screenplay/config/runtime.py`.

| Variable | Default | Description |
| --- | --- | --- |
| `BASE_URL` | `https://www.saucedemo.com/` | Application base URL used by `OpenSauceDemo` and `Login`. |
| `BROWSER` | `chromium` | Default browser for pytest-playwright (`chromium`, `firefox`, `webkit`). |
| `HEADED` | `false` | Run tests headed when true (`true/false`, `1/0`, `yes/no`). |
| `SLOW_MO_MS` | `0` | Slow motion delay in milliseconds for browser actions. |
| `DEFAULT_TIMEOUT_MS` | `5000` | Default timeout for wait interactions (`WaitUntilVisible`/`WaitUntilHidden`). |

Example:

```powershell
$env:BASE_URL = "https://www.saucedemo.com"
$env:BROWSER = "firefox"
$env:HEADED = "true"
$env:SLOW_MO_MS = "150"
$env:DEFAULT_TIMEOUT_MS = "7000"
pytest -q
```

## Current Screenplay API

### Tasks
- `OpenSauceDemo.app()`
- `Login.with_credentials(username, password)`
- `EnterUsername.as_(username)`
- `EnterPassword.as_(password)`
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
- `BeginCheckout()` (POC flow)
- `ProvideCheckoutInformation.as_customer(first_name, last_name, postal_code)` (POC flow)
- `Logout()` (POC flow)

### Questions
- `OnLoginPage()`
- `OnInventoryPage()`
- `CartBadgeCount()`
- `TotalsMatchComputedSum()`
- `TextOf(target)`
- `TextsOf(target)`
- `IsVisible(target)`
- `IsFocused(target)`
- `FocusIndicatorVisible()`
- `AttributeOf(target, attribute_name)`
- `CurrentUrl()`

## Project Structure

```text
screenplay/
|-- abilities/      # Actor abilities (BrowseTheWeb)
|-- config/         # Runtime settings (env-driven)
|-- core/           # Actor, Task, Interaction, Question, Target
|-- interactions/   # Atomic UI operations
|-- questions/      # Reusable state queries
|-- tasks/          # Business-level actions
`-- ui/             # SauceDemo locators/targets

tests/
|-- features/       # Gherkin scenarios
|-- steps/          # pytest-bdd step definitions
|-- conftest.py     # fixture wiring + runtime defaults
`-- test_*.py       # scenario loaders + optional direct tests

docs/
|-- architecture.md
|-- design_decisions.md
|-- domain_model.md
|-- engine_flows.md
`-- step_vocabulary.md
```

## Test Modes

### 1. pytest-bdd + Screenplay (primary)
- Gherkin defines behavior.
- Step definitions map phrases to Tasks/Questions.
- Business intent stays separate from UI mechanics.

### 2. Direct pytest + Screenplay (supporting)
- Useful for focused workflow tests and refactoring safety.
- `tests/test_golden_path_poc.py` is an example.

## Documentation

- Domain model: `docs/domain_model.md`
- Step vocabulary: `docs/step_vocabulary.md`
- Architecture: `docs/architecture.md`
- Composed engine flows: `docs/engine_flows.md`
- Design rationale: `docs/design_decisions.md`
- Presentation guide: `docs/project_presentation.md`
