# Architecture Overview

This repository combines:
- Screenplay pattern for automation structure
- pytest-bdd for behavior specifications
- Playwright for browser execution

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
- one file per feature with scenario loader and thin step adapters

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


