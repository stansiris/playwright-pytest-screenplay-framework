# Scaffolding a New Test Target with the `/generate-screenplay-tests` Skill

> This document doubles as a LinkedIn post. See the plain-text version at the bottom.

---

## What the skill does

The `/generate-screenplay-tests` Claude Code skill generates the complete Screenplay layer
stack for a new application target or focused scenario slice: Target catalog updates, Tasks,
Questions, actor fixture changes when needed, and test files from a URL or a scenario
description.

It respects all framework layer rules: no `Interaction` in test files, no raw strings in
`Target` lambdas, factory classmethods on every `Task`, and `pytestmark` on every test
module. After writing the files it runs `ruff` and `black` and fixes any issues before
reporting completion.

---

## Worked example: SauceDemo login errors

SauceDemo (`https://www.saucedemo.com/`) is one of the public targets already used in this
repository. It makes a compact worked example because the login page is small, the outcomes
are easy to verify, and the selectors are stable.

### Step 1 - Invoke the skill

The skill requires two arguments: a **URL** to navigate and discover locators, and a
**scenario description** to define what to test.

```
/generate-screenplay-tests https://www.saucedemo.com/ Generate negative login coverage for empty username, empty password, and locked out user SauceDemo
```

### Step 2 - The skill discovers locators

The skill runs a headless Playwright script against the live page:

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

No `data-testid` attributes were found. The skill falls back automatically to other stable
attributes and records:

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

### Step 3 - Generated code (shown for review before writing)

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

### Step 4 - Files written, lint passes

After confirmation, the skill writes or updates:

```
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

## What the skill handles automatically

- Falling back from `data-testid` to `data-test` or other stable attributes when a site has none
- Running test submissions against the live app to confirm actual error text before asserting
- Creating any missing `__init__.py` files so Python package imports resolve
- Placing every artefact in the correct layer path
- Enforcing all framework architectural rules: no `Interaction` in test files, lambda closures, factory classmethods
- Linting and formatting after writing

---
