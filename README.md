# Playwright + Pytest Screenplay Framework

[![CI](https://github.com/stansiris/playwright-pytest-screenplay-framework/actions/workflows/ci.yml/badge.svg)](https://github.com/stansiris/playwright-pytest-screenplay-framework/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)

## Portfolio Project

**This repository is a public portfolio project, not a comprehensive SauceDemo test suite.**

This portfolio project demonstrates my automation and architecture skills by building a Python + Playwright framework around the Screenplay pattern. It shows that the same Screenplay model works cleanly with both 'pytest-bdd' scenarios and direct pytest tests.

This project highlights:
- a maintainable Screenplay-based architecture for UI testing
- reusable `screenplay_core` components with a separate `saucedemo` domain layer
- Codex-assisted implementation with human review and quality ownership
- business-readable BDD scenarios with concise step definitions
- support for both BDD and direct pytest styles on the same model
- marker-driven CI lanes (`smoke`, `integration`, `ui`, `e2e`) with artifacts
- centralized runtime configuration for project execution

## Table of Contents

- [Hybrid Assertion Model](#hybrid-assertion-model)
- [API and Design References](#api-and-design-references)
- [Project Structure](#project-structure)
- [Test Modes](#test-modes)
- [Documentation](#documentation)
- [AI-Assisted Development](#ai-assisted-development)
- [Current Test Coverage](#current-test-coverage)
- [Results and Impact](#results-and-impact)
- [Setup](#setup)
- [Troubleshooting](#troubleshooting)
- [Quick Run Commands](#quick-run-commands)
- [CI-Ready Formatting](#ci-ready-formatting)
- [CI Pipeline](#ci-pipeline)
- [Test Reporting](#test-reporting)
- [Demo and Evidence](#demo-and-evidence)
- [Runtime Configuration](#runtime-configuration)

## Hybrid Assertion Model

The framework intentionally supports a hybrid style:
- Playwright-native locator assertions through `Actor.expect(Target)` for strong UI synchronization and readable assertions.
- Screenplay Questions through `Actor.asks_for(...)` for domain/state assertions and reusable business checks.

Example:

```python
from saucedemo.questions.on_inventory_page import OnInventoryPage
from saucedemo.ui.pages.checkout_overview_page import CheckoutOverviewPage
from saucedemo.ui.pages.login_page import LoginPage


def test_example(customer):
    customer.expect(LoginPage.LOGIN_BUTTON).to_be_visible()
    customer.expect(CheckoutOverviewPage.CHECKOUT_TOTAL).to_contain_text("Total:")
    customer.expect(CheckoutOverviewPage.CHECKOUT_TOTAL).to_have_text(
        "Total: $60.45", timeout=3000
    )
    assert customer.asks_for(OnInventoryPage())
```

Timeout behavior:
- default `expect(...)` timeout is Playwright's built-in default
- pass `timeout=...` on any Playwright assertion call to override per assertion

## API and Design References

Detailed component model, task/question vocabulary, and architecture decisions are documented in:
- `docs/domain_model.md`
- `docs/architecture.md` (layered architecture, class hierarchy diagrams, dependency graphs, runtime sequence diagrams)
- `docs/ui_target_organization.md` (page/component target organization and usage conventions)
- `docs/design_decisions.md`

## Project Structure

```text
screenplay_core/
|-- abilities/      # Reusable abilities (BrowseTheWeb)
|-- core/           # Actor, Task, Interaction, Question, Target
|-- interactions/   # Reusable low-level browser interactions
`-- questions/      # Reusable generic questions

saucedemo/
|-- tasks/          # SauceDemo business-level actions
|-- questions/      # SauceDemo-specific queries
`-- ui/
    |-- pages/      # Page-level target catalogs
    `-- components/ # Shared target catalogs reused across pages

tests/
|-- features/       # Gherkin scenarios
|-- conftest.py     # fixture wiring + runtime defaults
`-- test_*.py       # BDD step adapters and direct pytest + Screenplay tests

docs/
|-- architecture.md
|-- codex_workflow.md
|-- design_decisions.md
|-- domain_model.md
|-- ui_target_organization.md
`-- engine_flows.md
```

## Test Modes

Both modes are first-class and share the same Tasks/Questions/Interactions model.

### 1. pytest-bdd + Screenplay
- Gherkin defines behavior.
- Step definitions (in `tests/test_golden_path_bdd.py` and `tests/test_login_bdd.py`) map phrases to Tasks/Questions.
- Business intent stays separate from UI mechanics.

### 2. Direct pytest + Screenplay
- Useful for focused workflow tests and refactoring safety.
- Current examples: `tests/test_login.py`, `tests/test_inventory.py`, `tests/test_product_details.py`, `tests/test_checkout_info.py`, `tests/test_checkout_complete.py`, and `tests/test_ui_pages.py`.

## Documentation

- Domain model: `docs/domain_model.md`
- Architecture: `docs/architecture.md`
- UI target organization: `docs/ui_target_organization.md`
- Composed engine flows: `docs/engine_flows.md`
- Design rationale: `docs/design_decisions.md`
- Codex generation workflow: `docs/codex_workflow.md`

## AI-Assisted Development

Most implementation artifacts in this repository were generated with Codex through iterative, conversational prompting by the project author, including both automation code and BDD feature files.

Final architecture, review decisions, and quality gates (lint/format/tests) were performed by the project author.

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

## Results and Impact

- Built a test model that supports both BDD and direct pytest styles on the same Screenplay primitives (Tasks/Questions/Interactions).
- Isolated UI selector change impact by organizing targets into page/component catalogs (`saucedemo/ui/pages/*`, `saucedemo/ui/components/*`).
- Established CI confidence coverage across environments:
  - fast lane on PR/push
  - matrix regression on `ubuntu/windows` x `chromium/firefox`
- Improved failure diagnosis through retained artifacts (`junit.xml`, HTML report, screenshots, traces).

## Setup

Use the shell block that matches your environment.

### PowerShell (Windows)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m playwright install
pytest -q
```

### Bash (macOS/Linux)

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m playwright install
pytest -q
```

## Troubleshooting

- Browser binaries missing:
  - run `python -m playwright install`
- `base_url` or navigation failures:
  - verify `pytest.ini` `base_url`
  - override per run with `--base-url="https://www.saucedemo.com"`
- Headed mode fails in remote/headless environments:
  - remove `--headed` for CI/server runs
- Slow/flaky local runs:
  - start with `pytest -q -m "smoke or e2e"`
  - use `--slowmo=150` only for debugging, not regular regression runs

## Quick Run Commands

```powershell
# smoke + e2e happy path
pytest -q -m "smoke or e2e"

# integration core (excluding smoke and ui overlap)
pytest -q -m "integration and not smoke and not ui"

# ui-focused page checks
pytest -q -m "ui"

# full regression marker union (keep `ui` explicit for future marker strategy changes)
pytest -q -m "smoke or integration or e2e or ui"
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

## CI Pipeline

GitHub Actions workflow: `.github/workflows/ci.yml`

Trigger model:
- `push`/`pull_request`: fast developer feedback
- `schedule`: unattended confidence runs
- `workflow_dispatch`: manual run

Current CI jobs:
- `lint`: `ruff` + `black --check`
- `tests_fast` (PR/push): `pytest -q -m "smoke or integration or e2e or ui"` on `ubuntu-latest` + `chromium`
- `full_matrix_regression` (schedule/manual): `pytest -q -m "smoke or integration or e2e or ui"` on `ubuntu/windows` x `chromium/firefox`

Marker-based pytest commands are shell-agnostic; only line-continuation syntax differs by shell.

Scheduled runs (UTC):
- Weekday nightly: `0 2 * * 1-5`
- Weekly full run: `0 3 * * 0`

## Test Reporting

Pytest generates test artifacts automatically into `test-results/`:
- `junit.xml` for CI parsing/integrations
- `report.html` as a shareable HTML report
- failure screenshots (`--screenshot=only-on-failure`)
- Playwright traces on failures (`--tracing=retain-on-failure`)

In GitHub Actions, `test-results/` is uploaded as a workflow artifact even when tests fail.
Retention policy:
- PR/push jobs: 14 days
- scheduled/manual full regression: 30 days

## Demo and Evidence

- CI workflow runs and job history: [`.github/workflows/ci.yml`](https://github.com/stansiris/playwright-pytest-screenplay-framework/actions/workflows/ci.yml)
- Local run output artifacts are written to `test-results/`:
  - `test-results/junit.xml`
  - `test-results/report.html`
- CI also uploads the same `test-results/` bundle as downloadable artifacts on each run.

## Runtime Configuration

Runtime defaults are defined in `pytest.ini` and consumed in `tests/conftest.py`.
Override them from the command line when needed.

| Setting | Default | Description |
| --- | --- | --- |
| `[pytest] base_url` | `https://www.saucedemo.com/` | Base URL used by navigation tasks. Override with `--base-url=...`. |
| `--browser` | `chromium` | Browser for pytest-playwright (`chromium`, `firefox`, `webkit`). Defaults to the plugin's Chromium when not provided. |
| `--headed` | `false` | Optional CLI flag to run headed. |
| `--slowmo` | plugin default | Optional CLI delay (ms) between browser actions. |

### Runtime Override Example (PowerShell)

```powershell
pytest -q `
  --browser=firefox `
  --headed `
  --slowmo=150 `
  --base-url="https://www.saucedemo.com"
```

### Runtime Override Example (Bash)

```bash
pytest -q \
  --browser=firefox \
  --headed \
  --slowmo=150 \
  --base-url="https://www.saucedemo.com"
```
