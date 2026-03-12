# Getting Started: Create Your First Test (Login Example)

This guide is for new users of this repository.
By the end, you will know how to add a new test case using the existing Screenplay setup.

## Environment Setup (Windows and macOS/Linux)

If you have not set up the project yet, do this first.

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

After setup passes, continue with the test-creation steps below.

## What You Need to Know First

In this framework:

- A test uses an `Actor` (for example, `Customer`) to perform high-level behavior.
- The actor needs `Ability` objects (for example, `BrowseTheWeb`) to interact with the app.
- Tests should call `Task` and `Consequence` objects, not low-level interactions directly.

The most important practical rule:

- Reuse the `customer` fixture for normal UI tests.
- If you need a new actor, create it in [`tests/conftest.py`](../tests/conftest.py) (not inline in a single test file).

## Step 1: Understand the `customer` Fixture

Open [`tests/conftest.py`](../tests/conftest.py).  
You already have this fixture:

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

Why this matters:

- `page` comes from `pytest-playwright`.
- `base_url` comes from `pytest.ini`.
- `Actor("Customer")` is the test user.
- `.can(BrowseTheWeb.using(...))` gives that actor browser capability.

If a test does not use an actor with `BrowseTheWeb`, UI tasks and assertions will fail.

## Step 2: Reuse Existing Login Building Blocks

For login tests, these pieces already exist:

- Targets: [`examples/saucedemo/ui/pages/login_page.py`](../examples/saucedemo/ui/pages/login_page.py)
- Task: [`examples/saucedemo/tasks/login.py`](../examples/saucedemo/tasks/login.py)
- Open app task: [`examples/saucedemo/tasks/open_saucedemo.py`](../examples/saucedemo/tasks/open_saucedemo.py)
- Assertions DSL: [`screenplay_core/consequences/ensure.py`](../screenplay_core/consequences/ensure.py)

This means you usually only need to write the test itself.

## Step 3: Create a New Login Test File

Create `tests/saucedemo/test_login_get_started.py`:

```python
import pytest

from examples.saucedemo.tasks.login import Login
from examples.saucedemo.tasks.open_saucedemo import OpenSauceDemo
from examples.saucedemo.ui.pages.inventory_page import InventoryPage
from examples.saucedemo.ui.pages.login_page import LoginPage
from screenplay_core.consequences.ensure import Ensure


@pytest.mark.smoke
def test_login_happy_path(customer) -> None:
    customer.attempts_to(
        OpenSauceDemo.app(),
        Ensure.that(LoginPage.LOGIN_BUTTON).to_be_visible(),
        Login.with_credentials(username="standard_user", password="secret_sauce"),
        Ensure.that(InventoryPage.INVENTORY_CONTAINER).to_be_visible(),
    )
```

What this test does:

1. Opens the app.
2. Confirms login page is visible.
3. Logs in with valid credentials.
4. Confirms inventory page is visible.

## Step 4: Run Just Your New Test

```powershell
pytest -q tests/saucedemo/test_login_get_started.py
```

If this passes, your first new Screenplay test is working correctly.

## When Should You Add a New Actor Fixture?

Create a new actor fixture when the role is truly different, such as:

- a second UI user in the same scenario (for example, `admin` and `customer`)
- a role with different abilities
- a role that needs different setup data

Add new actor fixtures in [`tests/conftest.py`](../tests/conftest.py) so all tests can share them consistently.

Example:

```python
@pytest.fixture
def admin(page, base_url):
    return Actor("Admin").can(
        BrowseTheWeb.using(
            page,
            base_url=base_url,
        )
    )
```

Why `conftest.py` is preferred:

- single place for shared setup
- consistent actor creation across tests
- easier maintenance when abilities/configuration change

## Common Mistakes and Fixes

`Exception: <ActorName> does not have ability BrowseTheWeb`

- Cause: actor was created without `.can(BrowseTheWeb.using(...))`
- Fix: use the `customer` fixture or add the ability in `conftest.py`

`TypeError: attempts_to() accepts Task/Consequence only`

- Cause: a test passed `Click(...)`/`Fill(...)` directly
- Fix: wrap low-level interactions in a `Task`, then call that task from the test

Assertion fails because target not found

- Cause: locator or page state is wrong
- Fix: verify target definitions in page files under [`examples/saucedemo/ui/pages/`](../examples/saucedemo/ui/pages/)

## Recommended Workflow for Any New Test

1. Start with an existing actor fixture (`customer`).
2. Reuse existing tasks and targets if possible.
3. Add new target(s) only if a locator is missing.
4. Add or update a task to express the business action.
5. Keep test code focused on behavior flow and assertions.
6. Run the new test, then run full suite if needed.

## One Rule to Remember

Tests describe behavior.  
Tasks implement behavior.  
Fixtures create actors and abilities.

If you follow that separation, your test suite stays easy to scale and maintain.
