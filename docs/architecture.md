# Architecture Overview

This repository combines:
- Screenplay pattern for automation structure
- pytest-bdd for behavior specifications
- Playwright for browser execution

## Current Automated Coverage

The current checked-in coverage includes:
- one end-to-end BDD flow:
  - feature: `tests/features/golden_path.feature`
  - step module: `tests/test_golden_path_bdd.py`
- one focused BDD login mirror flow:
  - feature: `tests/features/login.feature`
  - step module: `tests/test_login_bdd.py`
- direct pytest + Screenplay integration suites for login, inventory, product details, checkout info, and checkout complete
- direct pytest + Screenplay UI suites for all core pages (`tests/test_ui_pages.py`)

## CI Strategy

CI is marker-driven to balance feedback speed and confidence:
- `lint` runs first on all CI triggers.
- `smoke_e2e` (push/PR): `pytest -m "smoke or e2e"` on Ubuntu + Chromium.
- `integration_core` (push/PR): `pytest -m "integration and not smoke and not ui"` on Ubuntu + Chromium.
- `ui` (main/master push): `pytest -m "ui"` on Ubuntu + Chromium.
- `full_matrix_regression` (schedule/manual): `pytest -m "smoke or integration or e2e"` on Ubuntu/Windows and Chromium/Firefox.

Artifact retention in CI:
- push/PR jobs: 14 days
- scheduled/manual matrix job: 30 days

## Execution Flow

Gherkin scenario in `tests/features/*.feature`
-> step function in `tests/test_*.py`
-> Screenplay `Task` or `Question`
-> low-level `Interaction`
-> Playwright API via `BrowseTheWeb`

## Layer Responsibilities

### `screenplay_core/core`
- `Actor`
- base abstractions: `Task`, `Interaction`, `Question`, `Target`

### `screenplay_core/abilities`
- `BrowseTheWeb` bridges Actor to Playwright `page`

### `screenplay_core/interactions`
- atomic UI actions (`Click`, `Fill`, `PressKey`, `WaitUntilVisible`, ...)

### `screenplay_core/questions`
- reusable generic queries (`TextOf`, `TextsOf`, `IsVisible`, ...)

### `saucedemo/tasks`
- intent-level workflows (`Login`, `AddProductToCart`, `ProceedToCheckout`, ...)

### `saucedemo/questions`
- SauceDemo-specific state queries/assertions (`OnInventoryPage`, `OnLoginPage`, `CartBadgeCount`, `TotalsMatchComputedSum`)

### `saucedemo/ui`
- centralized `Target` locators for SauceDemo

### `tests/features`
- business-readable scenarios

### `tests/test_*.py`
- mixed suite files: thin BDD step adapters plus direct pytest + Screenplay tests

## Runtime Configuration

Runtime behavior is configured by environment variables in `saucedemo/config/runtime.py`:
- `BASE_URL`
- `BROWSER`
- `HEADED`
- `SLOW_MO_MS`
- `DEFAULT_TIMEOUT_MS`

`tests/conftest.py` applies these settings to pytest-playwright defaults.

## Design Rules Enforced

- Step functions should not contain locators.
- Tasks should describe user intent, not DOM mechanics.
- Questions should read state and return values for assertions.
- Targets should be declared once in `saucedemo/ui/saucedemo.py`.


