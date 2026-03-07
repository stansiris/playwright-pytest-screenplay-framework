# Design Decisions

This document explains the key architectural decisions behind the framework.

The framework is intentionally opinionated. Its goal is not only to automate a web application, but also to demonstrate how the **Screenplay Pattern** can be implemented in Python in a way that keeps tests readable, domain-focused, and scalable.

These decisions are meant to preserve the separation between:

- **business behavior**
- **UI mechanics**
- **assertion strategy**
- **automation runtime**

---

## Why Screenplay instead of Page Object Model?

The framework uses the **Screenplay Pattern** instead of the traditional **Page Object Model (POM)** because Screenplay scales more naturally as test suites grow.

Page Object Model organizes automation around **pages** and **page methods**. This works well for small projects, but over time page classes often become large, tightly coupled to the UI, and responsible for too many concerns. Tests also tend to drift toward calling page methods directly, which can make business intent less obvious.

Screenplay organizes automation around **actors**, **tasks**, **interactions**, **questions**, and **abilities**. This shifts the focus from page structure to **user behavior**.

Example:

Page Object Model style:

```python
login_page.login(username, password)
inventory_page.add_to_cart("backpack")
checkout_page.finish_checkout()
```

Screenplay style:

```python
customer.attempts_to(
    Login.with_credentials(username, password),
    AddProductToCart.named("Sauce Labs Backpack"),
    CompleteCheckout(),
)
```

The Screenplay version reads more like behavior and less like browser scripting.

### Why this matters

Screenplay provides several advantages for this framework:

- tests stay focused on **intent**
- reusable behavior is modeled as **Tasks**
- low-level browser operations are isolated in **Interactions**
- assertions and state retrieval are separated cleanly
- the framework is easier to grow without turning into a collection of page scripts

In short, the project chooses Screenplay because it provides a better architecture for demonstrating **test design**, not just test execution.

---

## Why `actor.attempts_to()` only accepts Tasks and Consequences

`actor.attempts_to()` is intentionally restricted to **Tasks** and **Consequences**.

This is a deliberate design choice to keep tests written at the **behavior level**.

A Task represents a meaningful user action:

- `Login.with_credentials(...)`
- `AddProductToCart.named(...)`
- `ProceedToCheckout()`

A Consequence represents an assertion or verification step:

- `Ensure.that(...).to_be_visible()`

This means that when reading a test, the reader sees **what the actor is doing**, not the low-level implementation details.

Example:

```python
customer.attempts_to(
    Login.with_credentials("standard_user", "secret_sauce"),
    ProceedToCheckout(),
)
```

This is preferred over allowing tests to execute raw UI mechanics such as:

```python
customer.attempts_to(
    Fill(LoginPage.USERNAME, "standard_user"),
    Fill(LoginPage.PASSWORD, "secret_sauce"),
    Click(LoginPage.LOGIN_BUTTON),
)
```

### Why this restriction exists

If `actor.attempts_to()` accepted every activity type directly, tests would gradually become more procedural and less expressive. The framework would begin drifting back toward:

- page-level scripting
- test-specific click chains
- leaking selectors and UI structure into tests

Restricting `attempts_to()` creates a guardrail that protects the DSL.

### Why Consequences are allowed

Assertions are still part of the actor’s behavior in the test flow. A consequence is something the actor verifies after acting on the system.

Example:

```python
customer.attempts_to(
    Login.with_credentials("standard_user", "secret_sauce"),
    Ensure.that(InventoryPage.CONTAINER).to_be_visible(),
)
```

This keeps assertions inside the same readable Screenplay flow while preserving architectural boundaries.

---

## Why direct Interactions are not used in tests

Direct **Interactions** are intentionally not used in tests because they operate at the wrong level of abstraction.

An Interaction is a low-level UI action such as:

- `Click`
- `Fill`
- `WaitUntilVisible`
- `SelectOption`

These are important internally, but they are not the language the tests should speak.

Tests should express **user intent**, not UI instructions.

Preferred:

```python
customer.attempts_to(
    Login.with_credentials("standard_user", "secret_sauce")
)
```

Not preferred:

```python
customer.attempts_to(
    Fill(LoginPage.USERNAME, "standard_user"),
    Fill(LoginPage.PASSWORD, "secret_sauce"),
    Click(LoginPage.LOGIN_BUTTON),
)
```

### Why this matters

Using direct Interactions in tests causes several problems:

- tests become harder to read
- tests become more tightly coupled to the UI
- business intent becomes harder to recognize
- duplication increases across test cases
- the framework loses the advantage of reusable domain actions

Interactions still exist and remain important, but they belong **inside Tasks**, where implementation details can be composed and reused safely.

This separation helps preserve the distinction between:

- **what the actor does** → Task
- **how the browser performs it** → Interaction

---

## Why `Ensure.that()` exists

`Ensure.that()` exists to bridge **Screenplay-style assertions** with **Playwright’s `expect()` API**.

Playwright provides powerful locator assertions such as:

- `to_be_visible()`
- `to_have_text()`
- `to_contain_text()`
- `to_have_count()`

These assertions provide important benefits:

- auto-waiting
- retry behavior
- strong failure diagnostics
- expressive locator assertions

The framework preserves those benefits without exposing raw Playwright assertions directly in tests.

Playwright style:

```python
expect(page.locator("#inventory_container")).to_be_visible()
```

Screenplay style:

```python
customer.attempts_to(
    Ensure.that(InventoryPage.CONTAINER).to_be_visible()
)
```

### Why not `actor.expect(...)`

Adding `expect()` directly to the Actor would make the Actor feel more like a wrapper around Playwright than a Screenplay abstraction.

The Actor is intended to perform Tasks, verify Consequences, ask Questions, and use Abilities. `Ensure.that()` keeps assertions explicit and separate while still preserving access to Playwright’s assertion capabilities.

## Why `Ensure.that()` is modeled as a Consequence

`Ensure.that(...).to_be_visible()` is modeled as a **Consequence** because it represents a verification step in the actor’s flow.

In this framework, the actor performs two kinds of high-level activities:

- **Tasks** — actions that change or advance the system
- **Consequences** — verifications of the resulting system state

A Consequence is not a value query. It is an executable assertion step that the actor performs after acting on the application.

Example:

```python
customer.attempts_to(
    Login.with_credentials("standard_user", "secret_sauce"),  # Task
    Ensure.that(InventoryPage.CONTAINER).to_be_visible(),     # Consequence
)
```

This distinction keeps the test flow readable: the actor does something, then verifies the outcome.

This approach keeps the DSL readable while preserving access to Playwright’s strongest assertion features.

---

## Why Questions and Ensure both exist

Questions and Ensure both deal with system state, but they serve **different roles**.

### Questions

A **Question** retrieves information from the system.

Examples:

- `TextOf(...)`
- `CurrentUrl()`
- `InventoryCount()`
- `OnInventoryPage()`

Questions return values that can be used in assertions, conditions, calculations, or other logic.

Example:

```python
title = customer.asks_for(TextOf(AppHeader.TITLE))
assert title == "Products"
```

### Ensure

**Ensure** verifies UI state directly, usually through Playwright locator assertions.

Example:

```python
customer.attempts_to(
    Ensure.that(AppHeader.TITLE).to_have_text("Products")
)
```

### Why both are necessary

If the framework only had Questions, it would lose the advantages of Playwright’s assertion engine for locator state.

If the framework only had Ensure, it would be harder to:

- retrieve values for later use
- express computed assertions
- compare domain-level values
- use plain Python assertion logic where appropriate

### The intended rule of thumb

Use:

- **Ensure** for UI assertions backed by Playwright `expect()`
- **Question** for retrieving values from the system
- **assert** for checking returned values

Examples:

UI assertion:

```python
customer.attempts_to(
    Ensure.that(InventoryPage.CONTAINER).to_be_visible()
)
```

Value retrieval + assertion:

```python
title = customer.asks_for(TextOf(AppHeader.TITLE))
assert title == "Products"
```

This separation keeps the framework expressive without collapsing multiple responsibilities into a single abstraction.

---

## Why Targets are encapsulated instead of used directly in tests

**Targets** encapsulate UI locator logic so that tests do not depend directly on selectors or page structure.

A Target represents a named UI element and knows how to resolve itself for an Actor.

Example:

```python
LOGIN_BUTTON = Target(
    "login button",
    lambda page: page.get_by_role("button", name="Login")
)
```

### Why not use raw locators in tests

Without Targets, tests would end up containing automation details such as:

```python
page.locator("#user-name")
page.get_by_role("button", name="Login")
```

This would cause several problems:

- selectors leak into tests
- tests become less readable
- locator changes require broader updates
- the domain language becomes weaker

### Why Targets matter in Screenplay

Targets create a stable abstraction between:

- the **intent of the test**
- the **mechanics of locating elements**

This allows Tasks, Questions, and Ensure to work against named UI elements instead of raw selectors.

Example:

```python
Ensure.that(InventoryPage.CONTAINER).to_be_visible()
```

is more expressive than:

```python
expect(page.locator("#inventory_container")).to_be_visible()
```

### Where Targets belong

Targets are intentionally used by several Screenplay abstractions:

- **Interactions** use Targets directly to perform low-level UI operations
- **Tasks** typically work with Targets through the Interactions they compose
- **Questions** use Targets to retrieve information from the application
- **Consequences** such as `Ensure` use Targets to verify UI state

They are not meant to become the dominant language of tests. Tests should still prefer business-level Tasks and domain-level Questions whenever possible.

---

## Summary

The framework is intentionally opinionated.

Its design choices aim to preserve:

- **readable tests**
- **reusable behavior**
- **clear separation of concerns**
- **strong integration with Playwright**
- **a Screenplay DSL that stays at the behavior level**

In practice, that means:

- use **Screenplay** instead of Page Object Model
- keep tests focused on **Tasks** and **Consequences**
- keep **Interactions** inside Tasks
- use **Ensure** for Playwright-backed UI assertions
- use **Questions** to retrieve values
- keep **Targets** as UI abstractions rather than raw selectors in tests

These constraints are intentional. They make the framework slightly stricter, but they also help keep it consistent, scalable, and easier to understand.
