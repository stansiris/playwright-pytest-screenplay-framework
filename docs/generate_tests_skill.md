# Scaffolding a New Test Target with `/planner` and `/python-screenplay-generator`

> This document doubles as a LinkedIn post. See the plain-text version at the bottom.

---

## What the skills do

This repository now splits planning from code generation:

- `/planner` turns requirements, notes, or explored behavior into a Screenplay-oriented plan, Gherkin, or both
- `/python-screenplay-generator` turns the approved plan into the concrete Screenplay layer stack for the target app

Together they can produce target catalog updates, Tasks, Questions, actor fixture changes
when needed, and test files from a URL or a scenario description.

The generator respects the framework layer rules: no `Interaction` in test files, no raw
strings in `Target` lambdas, factory classmethods on every `Task`, and `pytestmark` on every
test module. After writing the files it runs `ruff` and `black` and fixes any issues before
reporting completion.

---

## Worked example: SauceDemo login errors

SauceDemo (`https://www.saucedemo.com/`) is one of the public targets already used in this
repository. It makes a compact worked example because the login page is small, the outcomes
are easy to verify, and the selectors are stable.

### Step 1 - Plan the scenario

Start with the planner so the behavior is reviewed before code is generated.

```text
/planner Generate negative login coverage for empty username, empty password, and locked out user for https://www.saucedemo.com/ SauceDemo format=both
```

For this scenario, the planner would produce:

- a Screenplay plan with candidate Tasks such as `OpenSauceDemo` and `Login.with_credentials(...)`
- candidate Questions and Consequences for reading and verifying the error banner
- matching Gherkin scenarios for the three negative paths

### Step 2 - Generate from the approved plan

Once the plan looks right, pass the approved scenario to the generator:

```text
/python-screenplay-generator Implement the approved SauceDemo negative login plan for https://www.saucedemo.com/ SauceDemo
```

### Step 3 - The generator discovers locators

The generator runs a headless Playwright script against the live page:

```python
from playwright.sync_api import sync_playwright

url = "https://www.saucedemo.com/"
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(url)
    page.wait_for_load_state("networkidle")
    elements = page.query_selector_all("[data-testid]")
    # -> 0 results. SauceDemo uses `data-test`, not `data-testid`.
```

No `data-testid` attributes were found. The generator falls back automatically to other
stable attributes and records:

| Element | Selector |
|---|---|
| Username field | `[data-test="username"]` |
| Password field | `[data-test="password"]` |
| Log In button | `[data-test="login-button"]` |
| Error message | `[data-test="error"]` |

It also confirms the error messages empirically by running three submissions against the live
app:

| Scenario | Result |
|---|---|
| Empty username | `"Epic sadface: Username is required"` |
| Empty password | `"Epic sadface: Password is required"` |
| Locked out user | `"Epic sadface: Sorry, this user has been locked out."` |

> This is a good example of why the generator should validate behavior, not only inspect
> markup. The page shape alone does not tell you which negative cases return distinct messages.

### Step 4 - Generated code (shown for review before writing)

**Target catalog** - `examples/saucedemo/ui/pages/login_page.py`

```python
from screenplay_core.playwright.target import Target


def login_button_locator(page):
    return page.locator('[data-test="login-button"]')


def login_username_locator(page):
    return page.locator('[data-test="username"]')


def login_password_locator(page):
    return page.locator('[data-test="password"]')


def login_error_message_locator(page):
    return page.locator('[data-test="error"]')


class LoginPage:
    LOGIN_BUTTON = Target("Login button", login_button_locator)
    LOGIN_USERNAME = Target("Login username", login_username_locator)
    LOGIN_PASSWORD = Target("Login password", login_password_locator)
    LOGIN_ERROR_MESSAGE = Target("Login error message", login_error_message_locator)
```

**Navigate task** - `examples/saucedemo/tasks/open_saucedemo.py`

```python
from screenplay_core.core.actor import Actor
from screenplay_core.core.task import Task
from screenplay_core.playwright.interactions.navigate_to import NavigateTo


class OpenSauceDemo(Task):
    """Task: open the SauceDemo application."""

    def perform_as(self, actor: Actor) -> None:
        self.perform_interactions(actor, NavigateTo("/"))

    @classmethod
    def app(cls) -> "OpenSauceDemo":
        return cls()
```

**Login task** - `examples/saucedemo/tasks/login.py`

```python
from examples.saucedemo.ui.pages.login_page import LoginPage
from screenplay_core.core.task import Task
from screenplay_core.playwright.interactions.click import Click
from screenplay_core.playwright.interactions.fill import Fill


class Login(Task):
    """Task: log into SauceDemo."""

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def perform_as(self, actor) -> None:
        self.perform_interactions(
            actor,
            Fill(LoginPage.LOGIN_USERNAME, self.username),
            Fill(LoginPage.LOGIN_PASSWORD, self.password),
            Click(LoginPage.LOGIN_BUTTON),
        )

    @classmethod
    def with_credentials(cls, username: str, password: str) -> "Login":
        return cls(username=username, password=password)
```

**Question** - `examples/saucedemo/questions/login_error_message.py`

```python
from examples.saucedemo.ui.pages.login_page import LoginPage
from screenplay_core.core.actor import Actor
from screenplay_core.core.question import Question


class LoginErrorMessage(Question):
    """Question: the text content of the login error message banner."""

    def answered_by(self, actor: Actor) -> str:
        return LoginPage.LOGIN_ERROR_MESSAGE.resolve_for(actor).inner_text()

    @classmethod
    def displayed(cls) -> "LoginErrorMessage":
        return cls()
```

**Test file** - `tests/saucedemo/test_login_errors.py`

```python
"""SauceDemo login error coverage expressed with Screenplay tasks and questions."""

import pytest

from examples.saucedemo.questions.login_error_message import LoginErrorMessage
from examples.saucedemo.tasks.login import Login
from examples.saucedemo.tasks.open_saucedemo import OpenSauceDemo
from examples.saucedemo.ui.pages.login_page import LoginPage
from screenplay_core.playwright.ensure import Ensure

pytestmark = [pytest.mark.ui, pytest.mark.integration]

_EMPTY_USERNAME_ERROR = "Epic sadface: Username is required"
_EMPTY_PASSWORD_ERROR = "Epic sadface: Password is required"
_LOCKED_OUT_ERROR = "Epic sadface: Sorry, this user has been locked out."


def test_login_with_empty_username_shows_error(customer) -> None:
    """Submitting without a username shows the required-username message."""
    customer.attempts_to(
        OpenSauceDemo.app(),
        Ensure.that(LoginPage.LOGIN_BUTTON).to_be_visible(),
        Login.with_credentials("", "secret_sauce"),
        Ensure.that(LoginPage.LOGIN_ERROR_MESSAGE).to_be_visible(),
    )
    error = customer.asks_for(LoginErrorMessage.displayed())
    assert error == _EMPTY_USERNAME_ERROR


def test_login_with_empty_password_shows_error(customer) -> None:
    """Submitting without a password shows the required-password message."""
    customer.attempts_to(
        OpenSauceDemo.app(),
        Ensure.that(LoginPage.LOGIN_BUTTON).to_be_visible(),
        Login.with_credentials("standard_user", ""),
        Ensure.that(LoginPage.LOGIN_ERROR_MESSAGE).to_be_visible(),
    )
    error = customer.asks_for(LoginErrorMessage.displayed())
    assert error == _EMPTY_PASSWORD_ERROR


def test_locked_out_user_sees_expected_message(customer) -> None:
    """Submitting locked-out credentials shows the locked user error."""
    customer.attempts_to(
        OpenSauceDemo.app(),
        Ensure.that(LoginPage.LOGIN_BUTTON).to_be_visible(),
        Login.with_credentials("locked_out_user", "secret_sauce"),
        Ensure.that(LoginPage.LOGIN_ERROR_MESSAGE).to_be_visible(),
    )
    error = customer.asks_for(LoginErrorMessage.displayed())
    assert error == _LOCKED_OUT_ERROR
```

### Step 5 - Files written, lint passes

After confirmation, the generator writes or updates:

```text
examples/saucedemo/
  tasks/
    open_saucedemo.py
    login.py
  questions/
    login_error_message.py
  ui/
    pages/
      login_page.py

tests/saucedemo/
  test_login_errors.py
```

`ruff check . && black --check .` - all checks pass.

---

## What the generator handles automatically

- Falling back from `data-testid` to `data-test` or other stable attributes when a site has none
- Running test submissions against the live app to confirm actual error text before asserting
- Creating any missing `__init__.py` files so Python package imports resolve
- Preserving the existing structure for the target app instead of forcing a second folder layout
- Enforcing all framework architectural rules: no `Interaction` in test files, lambda closures, factory classmethods
- Linting and formatting after writing

---
