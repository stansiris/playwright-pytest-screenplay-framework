# Getting Started: Write Your First Test

This guide walks through the framework from the ground up using the SauceDemo example target.
By the end you will understand how the pieces connect and be able to add new tests confidently.

---

## Environment Setup

### Windows

```powershell
git clone https://github.com/stansiris/playwright-pytest-screenplay-framework.git
cd playwright-pytest-screenplay-framework

python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
playwright install
```

### macOS / Linux

```bash
git clone https://github.com/stansiris/playwright-pytest-screenplay-framework.git
cd playwright-pytest-screenplay-framework

python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
playwright install
```

Verify the setup:

```bash
pytest tests/saucedemo/test_login.py -q
```

---

## How the Pieces Connect

Before writing a test, understand what each layer provides.

### The Actor

The actor is the test user. Everything in a test flows through the actor.
An actor needs at least one **Ability** before it can do anything useful.

```python
Actor("Customer").can(BrowseTheWeb.using(page, base_url=base_url))
```

### Abilities

Abilities connect the actor to external systems.

| Ability | Wraps | Used for |
|---|---|---|
| `BrowseTheWeb` | Playwright `page` | UI navigation, clicks, fills, assertions |
| `CallTheApi` | `requests.Session` | JSON API calls |

### Tasks

A Task is a named, reusable business action. Tests call Tasks - not raw browser operations.
Tasks are composed of low-level **Interactions** (`Click`, `Fill`, `NavigateTo`, etc.).

```python
# examples/saucedemo/tasks/login.py
class Login(Task):
    def perform_as(self, actor) -> None:
        self.perform_interactions(
            actor,
            Fill(LoginPage.LOGIN_USERNAME, self.username),
            Fill(LoginPage.LOGIN_PASSWORD, self.password),
            Click(LoginPage.LOGIN_BUTTON),
        )

    @classmethod
    def with_credentials(cls, username: str, password: str) -> "Login":
        return cls(username, password)
```

### Targets

A Target is a named, lazy locator recipe. It stores *how* to find an element, not the
element itself. It is resolved at runtime through the actor's `BrowseTheWeb` ability.

```python
# examples/saucedemo/ui/pages/login_page.py
class LoginPage:
    LOGIN_BUTTON   = Target("Login button",   lambda page: page.locator('[data-test="login-button"]'))
    LOGIN_USERNAME = Target("Login username", lambda page: page.locator('[data-test="username"]'))
    LOGIN_PASSWORD = Target("Login password", lambda page: page.locator('[data-test="password"]'))
```

### Consequences (`Ensure`)

`Ensure` is the assertion DSL. It wraps Playwright's `expect()` so assertions stay inside
the actor's activity flow and benefit from Playwright's auto-waiting and retry behaviour.

```python
actor.attempts_to(
    Ensure.that(LoginPage.LOGIN_BUTTON).to_be_visible(),
    Ensure.that(InventoryPage.INVENTORY_CONTAINER).to_be_visible(),
)
```

---

## Step 1: Understand the `customer` Fixture

Open [`tests/saucedemo/conftest.py`](../tests/saucedemo/conftest.py):

```python
@pytest.fixture
def customer(page, base_url):
    return Actor("Customer").can(
        BrowseTheWeb.using(
            page,
            base_url=base_url,
        )
    )
```

- `page` is the Playwright page provided by `pytest-playwright`.
- `base_url` comes from pytest's `--base-url` option, with a fallback to `https://www.saucedemo.com/` in `tests/saucedemo/conftest.py`.
- `.can(BrowseTheWeb.using(...))` gives the actor browser capability.

Any test that receives `customer` has a ready-to-use actor with a live browser page.

---

## Step 2: Identify the Building Blocks You Need

For a login test these already exist:

| What you need | Where it lives |
|---|---|
| Open the app | [`examples/saucedemo/tasks/open_saucedemo.py`](../examples/saucedemo/tasks/open_saucedemo.py) |
| Enter credentials and click login | [`examples/saucedemo/tasks/login.py`](../examples/saucedemo/tasks/login.py) |
| Logout | [`examples/saucedemo/tasks/logout.py`](../examples/saucedemo/tasks/logout.py) |
| Login page targets | [`examples/saucedemo/ui/pages/login_page.py`](../examples/saucedemo/ui/pages/login_page.py) |
| Inventory page targets | [`examples/saucedemo/ui/pages/inventory_page.py`](../examples/saucedemo/ui/pages/inventory_page.py) |
| Assertions | [`screenplay_core/playwright/ensure.py`](../screenplay_core/playwright/ensure.py) |

When everything you need already exists, you only need to write the test itself.

---

## Step 3: Write the Test

Create `tests/saucedemo/test_login_get_started.py`:

```python
import pytest

from examples.saucedemo.tasks.login import Login
from examples.saucedemo.tasks.logout import Logout
from examples.saucedemo.tasks.open_saucedemo import OpenSauceDemo
from examples.saucedemo.ui.pages.inventory_page import InventoryPage
from examples.saucedemo.ui.pages.login_page import LoginPage
from screenplay_core.playwright.ensure import Ensure


@pytest.mark.smoke
def test_login_happy_path(customer) -> None:
    customer.attempts_to(
        OpenSauceDemo.app(),
        Ensure.that(LoginPage.LOGIN_BUTTON).to_be_visible(),
        Login.with_credentials(username="standard_user", password="secret_sauce"),
        Ensure.that(InventoryPage.INVENTORY_CONTAINER).to_be_visible(),
        Logout(),
        Ensure.that(LoginPage.LOGIN_BUTTON).to_be_visible(),
    )
```

What each step does:

1. Navigate to the SauceDemo URL.
2. Assert the login page has loaded.
3. Fill in credentials and click login.
4. Assert the inventory page is visible.
5. Open the menu and click logout.
6. Assert we are back on the login page.

---

## Step 4: Run the Test

```bash
pytest tests/saucedemo/test_login_get_started.py -q
```

---

## Shortcut: Generate the Scaffold Automatically

If you are adding tests for a brand-new application target, the `/generate-screenplay-tests`
Claude Code skill can generate the full Screenplay layer stack for you — Target catalog,
Tasks, Questions, conftest, and test file — from a single command:

```
/generate-screenplay-tests https://your-app-url.com
```

The skill discovers locators from the live page, shows you the generated code for review,
writes the files to the correct layer paths, and runs `ruff` + `black` before finishing.

See [generate_tests_skill.md](generate_tests_skill.md) for a worked example.

---

## When You Need Something New

### Adding a new Target

Add it to the relevant page file under `examples/saucedemo/ui/pages/`.

```python
# examples/saucedemo/ui/pages/login_page.py
class LoginPage:
    LOGIN_BUTTON        = Target("Login button",        lambda page: page.locator('[data-test="login-button"]'))
    LOGIN_ERROR_MESSAGE = Target("Login error message", lambda page: page.locator('[data-test="error"]'))
    # add a new target here
    LOGIN_LOGO          = Target("Login logo",          lambda page: page.locator(".login_logo"))
```

If a target is shared across multiple pages, add it to the relevant file under
[`examples/saucedemo/ui/components/`](../examples/saucedemo/ui/components/) instead.

### Adding a new Task

Create a new file under `examples/saucedemo/tasks/` and subclass `Task`.

```python
from screenplay_core.core.task import Task
from screenplay_core.playwright.interactions.click import Click
from examples.saucedemo.ui.pages.login_page import LoginPage


class DismissLoginError(Task):
    """Task: close the login error banner."""

    def perform_as(self, actor) -> None:
        self.perform_interactions(
            actor,
            Click(LoginPage.LOGIN_ERROR_CLOSE_BUTTON),
        )
```

Rules for Tasks:

- Use `self.perform_interactions(actor, ...)` for low-level browser actions.
- Use `actor.attempts_to(...)` inside `perform_as` only to compose other Tasks or Consequences.
- Never pass `Interaction` objects directly to `actor.attempts_to()`.

### Adding a new actor fixture

Add it to [`tests/saucedemo/conftest.py`](../tests/saucedemo/conftest.py) so all SauceDemo
tests can share it.

```python
@pytest.fixture
def admin(page, base_url):
    return Actor("Admin").can(
        BrowseTheWeb.using(page, base_url=base_url)
    )
```

Create a new actor fixture when the role is genuinely different — for example, a second
concurrent user, a role with different abilities, or a role that needs different setup data.
Do not create per-test actor fixtures inline in test files.

---

## Common Errors

**`Exception: Customer does not have ability BrowseTheWeb`**

The actor was created without `.can(BrowseTheWeb.using(...))`.
Fix: use the `customer` fixture, or register the ability when constructing the actor.

---

**`TypeError: Customer.attempts_to() accepts Task/Consequence only; got Interaction`**

A raw `Click(...)` or `Fill(...)` was passed directly to `attempts_to()`.
Fix: wrap the interaction(s) inside a `Task`, then call that task from the test.

---

**Assertion fails because element is not found**

Check the Target definition in the relevant page file under
[`examples/saucedemo/ui/pages/`](../examples/saucedemo/ui/pages/). Confirm the selector
matches the actual DOM using the Playwright inspector (`playwright codegen <url>`).

---

## The Rule to Remember

```
Tests     →  describe behavior
Tasks     →  implement behavior
Fixtures  →  create actors and abilities
```

Keep these responsibilities separate and the test suite stays easy to scale and maintain.
