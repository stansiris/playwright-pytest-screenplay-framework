# Scaffolding a New Test Target with the `/generate-screenplay-tests` Skill

> This document doubles as a LinkedIn post. See the plain-text version at the bottom.

---

## What the skill does

The `/generate-screenplay-tests` Claude Code skill generates the complete Screenplay layer
stack for a new application target — Target catalog, Tasks, Questions, actor fixture, and
test file — from a URL or a scenario description.

It respects all framework layer rules: no `Interaction` in test files, no raw strings in
`Target` lambdas, factory classmethods on every `Task`, and `pytestmark` on every test
module. After writing the files it runs `ruff` and `black` and fixes any issues before
reporting completion.

---

## Worked example: ParaBank login page

ParaBank (`https://parabank.parasoft.com`) is a classic banking demo app used in testing
courses. It was not part of this framework originally. The example below shows how the skill
adds it end-to-end in one session.

### Step 1 — Invoke the skill

The skill requires two arguments: a **URL** (to navigate and discover locators) and a **scenario description** (to define what to test).

```
/generate-screenplay-tests https://parabank.parasoft.com/parabank/index.htm Generate negative test cases for the login page: empty credentials, username only, password only ParaBank
```

### Step 2 — The skill discovers locators

The skill runs a headless Playwright script against the live page:

```python
from playwright.sync_api import sync_playwright

url = "https://parabank.parasoft.com/parabank/index.htm"
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(url)
    page.wait_for_load_state("networkidle")
    elements = page.query_selector_all("[data-testid]")
    # → 0 results. ParaBank has no data-testid attributes.
```

No `data-testid` attributes found. The skill falls back automatically, querying by
`name`, `type`, and `class` instead, and records:

| Element | Selector |
|---|---|
| Username field | `input[name="username"]` |
| Password field | `input[name="password"]` |
| Log In button | `input[type="submit"]` |
| Error message | `p.error` |

It also confirms the error messages empirically by running three test submissions against
the live app:

| Scenario | Result |
|---|---|
| Both fields empty | `"Please enter a username and password."` |
| Username only | `"Please enter a username and password."` |
| Password only | `"Please enter a username and password."` |

> Note: ParaBank is a deliberately vulnerable demo — any non-empty username + password
> actually succeeds (logs in as the seeded demo user). "Wrong credentials" is therefore not
> a testable negative case on this app.

### Step 3 — Generated code (shown for review before writing)

**Target catalog** — `examples/parabank/automation/ui/targets.py`

```python
"""ParaBank UI target catalog used by Screenplay tasks and questions."""

from __future__ import annotations

from screenplay_core.playwright.target import Target


class ParaBankTargets:
    LOGIN_USERNAME_INPUT = Target(
        "ParaBank login username input",
        lambda page: page.locator('input[name="username"]'),
    )
    LOGIN_PASSWORD_INPUT = Target(
        "ParaBank login password input",
        lambda page: page.locator('input[name="password"]'),
    )
    LOGIN_SUBMIT_BUTTON = Target(
        "ParaBank login submit button",
        lambda page: page.locator('input[type="submit"]'),
    )
    LOGIN_ERROR_MESSAGE = Target(
        "ParaBank login error message",
        lambda page: page.locator("p.error"),
    )
```

**Navigate task** — `examples/parabank/automation/tasks/open_parabank.py`

```python
from screenplay_core.core.task import Task
from screenplay_core.playwright.interactions.navigate_to import NavigateTo


class OpenParaBank(Task):
    """Task: navigate to the ParaBank login page."""

    _LOGIN_URL = "https://parabank.parasoft.com/parabank/index.htm"

    def perform_as(self, actor) -> None:
        self.perform_interactions(actor, NavigateTo(self._LOGIN_URL))

    @classmethod
    def login_page(cls) -> "OpenParaBank":
        return cls()
```

**Login task** — `examples/parabank/automation/tasks/login_to_parabank.py`

```python
from examples.parabank.automation.ui.targets import ParaBankTargets
from screenplay_core.core.task import Task
from screenplay_core.playwright.interactions.click import Click
from screenplay_core.playwright.interactions.fill import Fill


class LoginToParaBank(Task):
    """Task: submit the ParaBank login form with given credentials."""

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def perform_as(self, actor) -> None:
        self.perform_interactions(
            actor,
            Fill(ParaBankTargets.LOGIN_USERNAME_INPUT, self.username),
            Fill(ParaBankTargets.LOGIN_PASSWORD_INPUT, self.password),
            Click(ParaBankTargets.LOGIN_SUBMIT_BUTTON),
        )

    @classmethod
    def with_credentials(cls, username: str, password: str) -> "LoginToParaBank":
        return cls(username=username, password=password)
```

**Question** — `examples/parabank/automation/questions/login_error_message.py`

```python
from examples.parabank.automation.ui.targets import ParaBankTargets
from screenplay_core.core.actor import Actor
from screenplay_core.core.question import Question


class LoginErrorMessage(Question):
    """Question: the text content of the login error message paragraph."""

    def answered_by(self, actor: Actor) -> str:
        return ParaBankTargets.LOGIN_ERROR_MESSAGE.resolve_for(actor).inner_text()

    @classmethod
    def displayed(cls) -> "LoginErrorMessage":
        return cls()
```

**Test file** — `tests/parabank/test_parabank_login_ui.py`

```python
"""ParaBank login page negative UI tests expressed with Screenplay tasks and questions."""

import pytest

from examples.parabank.automation.questions.login_error_message import LoginErrorMessage
from examples.parabank.automation.tasks.login_to_parabank import LoginToParaBank
from examples.parabank.automation.tasks.open_parabank import OpenParaBank
from examples.parabank.automation.ui.targets import ParaBankTargets
from screenplay_core.playwright.ensure import Ensure

pytestmark = [pytest.mark.ui, pytest.mark.integration]

_EXPECTED_EMPTY_CREDS_ERROR = "Please enter a username and password."


def test_login_with_empty_credentials_shows_error(parabank_visitor) -> None:
    """Submitting the login form with both fields empty shows a validation error."""
    parabank_visitor.attempts_to(
        OpenParaBank.login_page(),
        Ensure.that(ParaBankTargets.LOGIN_SUBMIT_BUTTON).to_be_visible(),
        LoginToParaBank.with_credentials("", ""),
        Ensure.that(ParaBankTargets.LOGIN_ERROR_MESSAGE).to_be_visible(),
    )
    error = parabank_visitor.asks_for(LoginErrorMessage.displayed())
    assert error == _EXPECTED_EMPTY_CREDS_ERROR


def test_login_with_username_only_shows_error(parabank_visitor) -> None:
    """Submitting with a username but no password shows a validation error."""
    parabank_visitor.attempts_to(
        OpenParaBank.login_page(),
        Ensure.that(ParaBankTargets.LOGIN_SUBMIT_BUTTON).to_be_visible(),
        LoginToParaBank.with_credentials("john", ""),
        Ensure.that(ParaBankTargets.LOGIN_ERROR_MESSAGE).to_be_visible(),
    )
    error = parabank_visitor.asks_for(LoginErrorMessage.displayed())
    assert error == _EXPECTED_EMPTY_CREDS_ERROR


def test_login_with_password_only_shows_error(parabank_visitor) -> None:
    """Submitting with a password but no username shows a validation error."""
    parabank_visitor.attempts_to(
        OpenParaBank.login_page(),
        Ensure.that(ParaBankTargets.LOGIN_SUBMIT_BUTTON).to_be_visible(),
        LoginToParaBank.with_credentials("", "secret123"),
        Ensure.that(ParaBankTargets.LOGIN_ERROR_MESSAGE).to_be_visible(),
    )
    error = parabank_visitor.asks_for(LoginErrorMessage.displayed())
    assert error == _EXPECTED_EMPTY_CREDS_ERROR
```

### Step 4 — Files written, lint passes

After confirmation, the skill creates:

```
examples/parabank/
  __init__.py
  automation/
    __init__.py
    ui/
      __init__.py
      targets.py
    tasks/
      __init__.py
      open_parabank.py
      login_to_parabank.py
    questions/
      __init__.py
      login_error_message.py

tests/parabank/
  __init__.py
  conftest.py
  test_parabank_login_ui.py
```

`ruff check . && black --check .` — all checks pass.

---

## What the skill handles automatically

- Falling back from `data-testid` to `name`/`type`/`class` selectors when a site has none
- Running test submissions against the live app to confirm actual error text before asserting
- Creating all `__init__.py` files so Python package imports resolve
- Placing every artefact in the correct layer path
- Enforcing all framework architectural rules (no `Interaction` in test files, lambda closures, factory classmethods)
- Linting and formatting after writing

---