
# Playwright + Pytest Screenplay Framework

![Python](https://img.shields.io/badge/python-3.11+-blue)
![Playwright](https://img.shields.io/badge/playwright-testing-green)
[![codecov](https://codecov.io/gh/stansiris/playwright-pytest-screenplay-framework/branch/main/graph/badge.svg)](https://codecov.io/gh/stansiris/playwright-pytest-screenplay-framework)

A production-style test automation framework built with Python, Playwright, Pytest, and the
**Screenplay Pattern**. The repository ships two fully working example targets on top of a
reusable Screenplay core:

- **SauceDemo** — external public e-commerce app (UI + BDD)
- **Work Items** — bundled Flask app (UI, JSON API, and hybrid cross-boundary tests)

The primary goal is to demonstrate how the Screenplay Pattern can be implemented in Python
to produce readable, layered, and maintainable automation — not to be a large test suite.

---

## Quick Start

### Windows

```powershell
git clone https://github.com/stansiris/playwright-pytest-screenplay-framework.git
cd playwright-pytest-screenplay-framework

python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
playwright install

pytest -q
```

### macOS / Linux

```bash
git clone https://github.com/stansiris/playwright-pytest-screenplay-framework.git
cd playwright-pytest-screenplay-framework

python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
playwright install

pytest -q
```

---

## Key Concepts

| Concept | Description |
|---|---|
| Actor | Represents a user; orchestrates all actions and questions. |
| Ability | Grants the actor capability to reach an external system (`BrowseTheWeb`, `CallTheApi`). |
| Task | A high-level business action composed of interactions (`Login`, `CreateWorkItem`). |
| Interaction | A single low-level browser operation (`Click`, `Fill`, `NavigateTo`). |
| Target | A named, lazy locator recipe resolved through the actor's `BrowseTheWeb` ability. |
| Question | Reads and returns information from the system under test. |
| Consequence | Verifies system state; wraps Playwright `expect()` assertions (`Ensure`). |

---

## Architecture

The framework is a strict 4-layer stack. Each layer depends only on the layer below it.

```
Tests               →  describe behavior (thin, no browser details)
Example Target Layer →  app-specific Tasks, Questions, Targets, API tasks
Screenplay Core      →  Actor, Task, Interaction, Question, Target, Ensure
Playwright / requests →  browser and HTTP execution
```

`screenplay_core` is internally split into three modules reflecting their actual dependencies:

```
screenplay_core/core/        →  pure Python abstractions (Actor, Task, Interaction, Question, Consequence)
screenplay_core/playwright/  →  Playwright extension classes (Target, BrowseTheWeb, Ensure) plus interactions/ and questions/ subpackages
screenplay_core/http/        →  HTTP extension (CallTheApi)
```

```mermaid
graph TD

Actor["Actor"]
Ability["Ability<br/>(BrowseTheWeb, CallTheApi)"]
Task["Task<br/>(Login, CreateWorkItem)"]
Interaction["Interaction<br/>(Click, Fill, NavigateTo)"]
Question["Question<br/>(WorkItemVisible, TextOf)"]
Consequence["Consequence<br/>(Ensure.that)"]
Target["Target<br/>(UI Locator Recipe)"]
Playwright["Playwright / requests"]
System["Application Under Test"]

Actor -->|has ability| Ability
Actor -->|performs| Task
Task -->|composed of| Interaction
Interaction -->|acts on| Target
Target -->|resolved by| Playwright
Playwright -->|drives| System
Actor -->|asks| Question
Question -->|reads| Target
Actor -->|verifies| Consequence
Consequence -->|reads| Target
```

---

## Assertion Model

`Ensure` is a Screenplay-style DSL that wraps Playwright's `expect()` API. It gives tests
access to Playwright's full locator assertion set — auto-waiting, retry, and strong failure
diagnostics — without exposing `expect()` directly in test code.

```python
# Raw Playwright
expect(page.locator("#inventory_container")).to_be_visible()

# Screenplay equivalent
actor.attempts_to(
    Ensure.that(InventoryPage.INVENTORY_CONTAINER).to_be_visible()
)
```

`Ensure.that(target)` returns a `Consequence` object. The actor executes it, resolves the
`Target` into a Playwright `Locator`, and delegates to `expect(locator)`. IDE
autocompletion for all Playwright assertion methods is preserved via a `cast` to
`LocatorAssertions`.

---

## Example Tests

### SauceDemo — UI test with parametrize

```python
@pytest.mark.parametrize(
    "username,password",
    [
        ("standard_user", "secret_sauce"),
        ("problem_user", "secret_sauce"),
        ("performance_glitch_user", "secret_sauce"),
    ],
)
@pytest.mark.smoke
def test_successful_login(customer, username, password) -> None:
    customer.attempts_to(
        OpenSauceDemo.app(),
        Ensure.that(LoginPage.LOGIN_BUTTON).to_be_visible(),
        Login.with_credentials(username=username, password=password),
        Ensure.that(InventoryPage.INVENTORY_CONTAINER).to_be_visible(),
        Logout(),
        Ensure.that(LoginPage.LOGIN_BUTTON).to_be_visible(),
    )
```

### Work Items — hybrid test (create via API, verify in UI)

```python
@pytest.mark.hybrid
def test_create_work_item_via_api_verify_in_ui(work_items_api_actor, work_items_customer) -> None:
    title = "Hybrid API to UI work item"
    work_items_api_actor.attempts_to(
        LoginToWorkItemsApi.with_credentials("admin", "admin123"),
        CreateWorkItemViaApi.with_payload(
            {"title": title, "description": "Created via API", "priority": "HIGH"}
        ),
    )
    create_response = work_items_api_actor.ability_to(CallTheApi).last_response
    assert create_response is not None
    assert create_response.status_code == 201
    work_item_id = create_response.json()["id"]

    work_items_customer.attempts_to(
        OpenWorkItems.app(),
        LoginToWorkItems.with_credentials("admin", "admin123"),
        Ensure.that(WorkItemsTargets.work_item_for_id(work_item_id)).to_be_visible(),
        Ensure.that(WorkItemsTargets.work_item_title_text_for_id(work_item_id)).to_have_text(title),
    )
```

---

## SauceDemo

An external public e-commerce demo app used to show UI automation and BDD.

- Automation layer: `examples/saucedemo/`
- Tests: `tests/saucedemo/`
- BDD feature files: `tests/saucedemo/features/`

```bash
pytest tests/saucedemo -q
```

---

## Work Items

A lightweight Flask + SQLite work item management app bundled in this repository. It exists so
the framework can demonstrate UI, API, and hybrid automation without any external dependency.

### Where it lives

| Path | Purpose |
|---|---|
| `examples/work_items/app/` | Flask app source (routes, db, seed data) |
| `examples/work_items/automation/` | Tasks, Questions, Targets, API facade/helper |
| `tests/work_items/` | UI, API, hybrid, and BDD test suites |

### Default credentials

- Username: `admin`
- Password: `admin123`

### Run locally

```bash
python -m examples.work_items.app.app
# → http://127.0.0.1:5001/
```

### Run the tests

`tests/work_items/conftest.py` starts a Work Items server automatically on a free port for each
test session. No manual server start needed.

```bash
pytest tests/work_items -q                          # all Work Items tests
pytest tests/work_items/test_work_items_ui.py -q       # UI only
pytest tests/work_items/test_work_items_api.py -q      # API only
pytest tests/work_items/test_work_items_hybrid.py -q   # hybrid only
pytest tests/work_items/test_work_items_bdd.py -q      # BDD only
```

### Test markers

| Marker | Scope |
|---|---|
| `smoke` | Critical happy-path scenarios |
| `ui` | UI presentation and interaction |
| `api` | API-only scenarios |
| `hybrid` | Cross UI–API boundary scenarios |
| `integration` | Cross-component integration |
| `e2e` | Full end-to-end flows |

```bash
pytest -m "smoke or api" -q
```

---

## Project Structure

```
screenplay_core/
    core/               # Actor, Task, Interaction, Question, Consequence (pure Python)
    playwright/         # Target, BrowseTheWeb, Ensure, interactions/, questions/
    http/               # CallTheApi

examples/
    saucedemo/
        tasks/          # Login, Logout, AddProductToCart, …
        questions/      # OnInventoryPage, TotalsMatchComputedSum, …
        ui/
            pages/      # LoginPage, InventoryPage, CartPage, …
            components/ # AppShell, BackNavigation
    work_items/
        app/            # Flask app, db, seed
        automation/
            tasks/      # LoginToWorkItems, CreateWorkItem, EditWorkItem, …
            questions/  # WorkItemVisible, WorkItemCompleted, FlashMessages, …
            ui/         # WorkItemsTargets (all data-testid selectors)
            api/        # Work Items API helpers

tests/
    conftest.py         # Browser launch option overrides
    saucedemo/
        conftest.py     # customer actor fixture, base URL
        features/       # Gherkin feature files (pytest-bdd)
        test_*.py       # Direct pytest + BDD suites
    work_items/
        conftest.py     # Server lifecycle, per-test reset, actor fixtures
        test_*.py       # UI, API, hybrid suites

docs/
    api_testing.md     # API testing notes, design decisions, and open questions
    architecture.md     # Class hierarchy, dependency map, runtime sequences
    design_decisions.md # Q&A on key architectural choices
    get_started.md      # Step-by-step guide: write your first test
```

---

## How to Explore the Code

A good reading order for understanding the framework end to end:

1. [`tests/saucedemo/test_login.py`](tests/saucedemo/test_login.py) — smallest complete Screenplay test
2. [`screenplay_core/core/actor.py`](screenplay_core/core/actor.py) — how the actor executes tasks, consequences, and questions
3. [`examples/saucedemo/tasks/login.py`](examples/saucedemo/tasks/login.py) - domain behavior modeled as a reusable Task
4. [`screenplay_core/playwright/ensure.py`](screenplay_core/playwright/ensure.py) — how Playwright assertions are exposed through the Screenplay DSL
5. [`tests/work_items/test_work_items_hybrid.py`](tests/work_items/test_work_items_hybrid.py) — cross-boundary test using both `BrowseTheWeb` and `CallTheApi`
6. [`tests/work_items/test_work_items_bdd.py`](tests/work_items/test_work_items_bdd.py) — BDD scenarios wired to Screenplay steps via pytest-bdd

---

## CI Pipeline

GitHub Actions runs on push, pull request, and a nightly schedule.

| Job | Trigger | What it does |
|---|---|---|
| `lint` | push / PR | ruff check + black format check |
| `tests_fast` | push / PR | full marker union on Ubuntu / Chromium |
| `full_matrix_regression` | schedule / manual | Ubuntu + Windows × Chromium + Firefox |

Test artifacts (screenshots, traces, HTML report, JUnit XML) are uploaded on failure.

---

## Claude Code Skill

This repository ships a `/generate-screenplay-tests` Claude Code skill that scaffolds the full Screenplay layer stack for any new application target.

Running `/generate-screenplay-tests <url> <scenario description>` will:

1. Navigate to the URL and discover locators from the live page (preferring `data-testid`, falling back to `name`, `role`, or visible text selectors when the site has none).
2. Use the scenario description to decide which Tasks, Questions, and test cases to generate, then create a `Target` catalog, `Task` files, `Question` files, a `conftest.py` fixture, and a test file — all placed in the correct layer paths.
3. Show the generated code for review before writing any files.
4. Run `ruff` and `black` after writing and fix any formatting issues.

See [docs/generate_tests_skill.md](docs/generate_tests_skill.md) for a worked example using ParaBank.

---

## Further Reading

- [docs/api_testing.md](docs/api_testing.md) - API testing design notes, response ownership, and future discussion topics
- [docs/architecture.md](docs/architecture.md) — full class hierarchy and runtime sequence diagrams
- [docs/design_decisions.md](docs/design_decisions.md) — why Screenplay over Page Object Model, and other key choices
- [docs/get_started.md](docs/get_started.md) — step-by-step: write and run your first test
- [docs/generate_tests_skill.md](docs/generate_tests_skill.md) — using the Claude Code skill to scaffold a new target in minutes

---

## Portfolio Context

This repository demonstrates:

- Screenplay Pattern implementation in Python with clear layer boundaries
- Internal module split: runtime-agnostic `core/`, Playwright extension `playwright/`, HTTP extension `http/`
- Playwright integration exposed through a custom assertion DSL (`Ensure`)
- Dual-ability actors: `BrowseTheWeb` for UI and `CallTheApi` for JSON APIs
- Cross-boundary (hybrid) testing combining UI and API actors in a single test
- Support for both direct pytest and pytest-bdd test styles
- CI quality gates: lint, format check, and automated test execution
