# Playwright + Pytest Screenplay Framework

A production-style UI automation framework built with:

- Python
- Playwright
- Pytest
- Screenplay Pattern

This repository demonstrates how the **Screenplay architecture** can be implemented in Python
to build maintainable and scalable UI automation frameworks that support both
**BDD (`pytest-bdd`) and direct pytest tests**.

The framework separates:

- test behavior
- domain vocabulary
- automation mechanics
- browser runtime

This approach keeps tests readable while preserving a reusable and extensible automation architecture.

---

## Example Screenplay Test

In the Screenplay pattern, tests interact with the system through an **Actor**.
The `customer` fixture represents a user interacting with the application through the browser.

```python
def test_login(customer):
    customer.attempts_to(
        Login.with_credentials("standard_user", "secret_sauce")
    )

    customer.expect(InventoryPage.INVENTORY_CONTAINER).to_be_visible()
```

Screenplay allows tests to read like **user behavior instead of browser instructions**.

---

## Quick Start

### Windows (PowerShell)

```powershell
git clone https://github.com/stansiris/playwright-pytest-screenplay-framework.git
cd playwright-pytest-screenplay-framework

python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m playwright install

pytest -q
```

### macOS / Linux

```bash
git clone https://github.com/stansiris/playwright-pytest-screenplay-framework.git
cd playwright-pytest-screenplay-framework

python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
python -m playwright install

pytest -q
```

---

## Framework Architecture

The framework follows a layered architecture separating behavior,
domain logic, and automation mechanics.

```
Tests / BDD
      |
      v
Domain Layer (tasks, questions, UI targets)
      |
      v
Reusable Screenplay Core
      |
      v
Playwright
```

| Layer | Responsibility |
|-----|-----|
| Tests | Behavior specification |
| Domain | Business vocabulary |
| Screenplay Core | Reusable automation primitives |
| Playwright | Browser automation runtime |

---

## Execution Flow

```
Test / Feature
    |
    v
Actor
    |
    v
Task (business intent)
    |
    v
Interaction (UI operation)
    |
    v
Target (locator abstraction)
    |
    v
Playwright Locator / Page
```

---

## Design Principles

The framework follows several principles to keep automation scalable
and maintainable.

### Behavior First

Tests describe **user behavior**, not browser mechanics.

```python
customer.attempts_to(Login.with_credentials(user, password))
```

Instead of:

```python
page.fill("#username", user)
page.fill("#password", password)
page.click("#login")
```

---

### Intent Over Implementation

Tasks represent **what the user does**, while interactions define
**how the browser performs it**.

```
Login Task
   |
   v
Fill interaction
Click interaction
```

---

### Thin Tests

Test files remain minimal and delegate work to reusable domain logic.

```python
customer.attempts_to(
    OpenLoginPage(),
    Login.with_credentials("standard_user", "secret_sauce"),
    Logout(),
)
```

---

### Domain Vocabulary

Automation should reflect **business language**, not UI mechanics.

Examples:

```
Login
AddItemToCart
Checkout
IsInventoryPageVisible
```

Instead of:

```
ClickLoginButton
FillUsername
ClickSubmit
```

---

### Single Responsibility

Each abstraction has a focused purpose.

| Component | Responsibility |
|---|---|
| Actor | orchestrates activities |
| Task | represents user intent |
| Interaction | performs browser operations |
| Question | reads system state |
| Target | resolves UI elements |
| Ability | connects external systems |

---

## Actor Abilities

Actors gain capabilities through abilities.

```python
customer = Actor("Customer").can(
    BrowseTheWeb.using(page)
)
```

Abilities isolate external systems from domain logic.

Potential abilities include:

- Browser automation
- REST API communication
- Database access
- Messaging systems

---

## Project Structure

The project is organized into reusable framework components and domain-specific automation.

```
screenplay_core/
    abilities/
    core/
    interactions/
    questions/

saucedemo/
    tasks/
    questions/
    ui/
        pages/
        components/

tests/
    features/
    test_*.py
    conftest.py

docs/
```

| Directory | Responsibility |
|---|---|
| screenplay_core | reusable framework primitives |
| saucedemo | domain-specific automation |
| tests | behavior specs and test suites |
| docs | architecture and design documentation |

---

## Extending the Framework

The framework is **domain-agnostic**.

To automate another application:

```
myapp/
    tasks/
    questions/
    ui/pages/
    ui/components/
```

The Screenplay engine remains unchanged.

---

## Documentation

The `/docs` directory contains deeper conceptual documentation:

- architecture diagrams
- domain modeling
- design decisions
- runtime flows

---

## Core API Reference

The framework exposes a small set of abstractions:

| Component | Purpose |
|---|---|
| Actor | orchestrates tasks and questions |
| Task | represents user intent |
| Interaction | performs browser operations |
| Question | reads system state |
| Target | resolves locators |
| BrowseTheWeb | browser ability |

---

## CI Pipeline

GitHub Actions provides continuous integration including:

- Ruff linting
- Black formatting checks
- automated test execution
- artifact retention (reports, traces)

---

## Runtime Configuration

Runtime defaults are defined in `pytest.ini`.

Common CLI overrides:

```
--browser
--headed
--slowmo
--base-url
```

Example:

```bash
pytest -q --browser=firefox --headed
```

---

## Portfolio Context

This repository demonstrates:

- automation architecture design
- Screenplay pattern implementation in Python
- Playwright integration
- CI pipelines
- BDD + pytest test strategies
