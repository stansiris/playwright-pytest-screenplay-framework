# Architecture Overview

This repository combines:
- Screenplay pattern for automation structure
- pytest-bdd for behavior specifications
- Playwright for browser execution

## Execution Flow

Gherkin scenario in `tests/features/*.feature`
-> step function in `tests/steps/*.py`
-> Screenplay `Task` or `Question`
-> low-level `Interaction`
-> Playwright API via `BrowseTheWeb`

## Layer Responsibilities

### `screenplay/core`
- `Actor`
- base abstractions: `Task`, `Interaction`, `Question`, `Target`

### `screenplay/abilities`
- `BrowseTheWeb` bridges Actor to Playwright `page`

### `screenplay/interactions`
- atomic UI actions (`Click`, `Fill`, `PressKey`, `WaitUntilVisible`, ...)

### `screenplay/tasks`
- intent-level workflows (`Login`, `AddProductToCart`, `ProceedToCheckout`, ...)

### `screenplay/questions`
- reusable state queries/assertions (`OnInventoryPage`, `TextOf`, `TotalsMatchComputedSum`, ...)

### `screenplay/ui`
- centralized `Target` locators for SauceDemo

### `tests/features`
- business-readable scenarios

### `tests/steps`
- thin adapters from natural language to Screenplay calls

## Runtime Configuration

Runtime behavior is configured by environment variables in `screenplay/config/runtime.py`:
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
- Targets should be declared once in `screenplay/ui/saucedemo.py`.
