# Getting Started with the Playwright Pytest Screenplay Framework

This guide is not about installation. It explains how to quickly understand the architecture and design of the framework.

The goal is to help readers navigate the repository efficiently and understand the Screenplay implementation.

---

# Suggested Reading Order

Follow this order to understand the framework progressively.

### 1. Start with a small complete test

```
tests/test_login.py
```

This file shows a complete Screenplay example using pytest.

Key things to observe:

- the Actor fixture (`customer`)
- how the actor performs Tasks
- how Ensure performs Playwright assertions
- how Questions retrieve values

Example structure:

```python
customer.attempts_to(
    OpenLoginPage(),
    Login.with_credentials("standard_user", "secret_sauce"),
    Ensure.that(InventoryPage.INVENTORY_CONTAINER).to_be_visible(),
)

assert customer.asks_for(TextOf(AppShell.PAGE_TITLE)) == "Products"
```

---

### 2. Understand the Actor

```
screenplay_core/core/actor.py
```

This file contains the execution model of the framework.

Important methods:

- `attempts_to()` -> executes `Task` and `Consequence` only
- `_attempts_to_interactions()` -> internal path used by `Task.perform_interactions(...)`
- `asks_for()` -> retrieves values from Questions
- `ability_to()` -> accesses Actor abilities

---

### 3. Look at a real Task

```
saucedemo/tasks/login.py
```

Tasks represent business-level actions.

Example:

```
Login.with_credentials(username, password)
```

Tasks internally compose interactions through `self.perform_interactions(...)`.

---

### 4. Look at Targets

```
saucedemo/ui/pages/
saucedemo/ui/components/
```

Targets represent UI elements.

Example:

```python
LOGIN_BUTTON = Target(
    "Login button",
    lambda page: page.locator('[data-test="login-button"]'),
)
```

Targets encapsulate locator logic so tests and tasks stay readable.

---

### 5. Understand the assertion bridge

```
screenplay_core/consequences/ensure.py
```

This module connects Screenplay assertions to Playwright's `expect()` API.

Example DSL:

```
Ensure.that(Target).to_be_visible()
```

Internally this executes:

```
expect(locator).to_be_visible()
```

---

# Direct pytest vs pytest-bdd

The framework supports both styles of testing.

## Direct pytest tests

Example:

```
tests/test_login.py
```

Characteristics:

- fast to write
- minimal adapter layer
- good for technical regression suites

Example:

```python
def test_login(customer):
    customer.attempts_to(
        OpenLoginPage(),
        Login.with_credentials("standard_user", "secret_sauce"),
    )
    assert customer.asks_for(OnInventoryPage())
```

## pytest-bdd tests

Examples:

```
tests/test_login_bdd.py
tests/test_golden_path_bdd.py
```

Characteristics:

- maps Gherkin scenarios to Screenplay actions
- good for collaboration with non-technical stakeholders
- preserves the same Screenplay primitives underneath

Example flow:

```
Given the user is on the login page
When the user logs in
Then the inventory page should be visible
```

Step definitions stay thin and delegate behavior to Tasks/Questions.

---

# Key Takeaway

The framework separates concerns clearly:

```
Tests
  -> Tasks / Questions / Consequences
  -> Screenplay Core
  -> Playwright
```

Tests remain thin orchestration layers, while behavior is implemented in reusable Screenplay components.
