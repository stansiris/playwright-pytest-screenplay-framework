# Assertion Model

This framework supports two complementary assertion approaches:

1. Ensure assertions for UI state (Playwright-powered)
2. Questions + Python assert for value checks

Both exist to keep tests readable, expressive, and flexible.

---

# When to Use Ensure

Use Ensure when verifying the state of UI elements.

Examples:

- element visibility
- text content
- element count
- enabled/disabled state

Example:

```python
customer.attempts_to(
    Ensure.that(InventoryPage.INVENTORY_CONTAINER).to_be_visible(),
    Ensure.that(AppShell.PAGE_TITLE).to_have_text("Products"),
)
```

These assertions internally use Playwright:

```python
expect(locator).to_be_visible()
```

Advantages:

- Playwright auto-waiting
- retry logic
- rich assertion messages

---

# When to Use Questions

Questions retrieve information from the system.

They return a value that can be used in logic or assertions.

Example Question:

```python
class TextOf(Question):

    def answered_by(self, actor):
        return self.target.resolve_for(actor).text_content() or ""
```

Usage:

```python
title = customer.asks_for(TextOf(AppShell.PAGE_TITLE))

assert title == "Products"
```

Questions are useful when:

- retrieving values
- performing calculations
- comparing business state

---

# Why Both Exist

UI assertions and value assertions serve different purposes.

| Tool | Purpose |
|---|---|
| Ensure | verify UI state using Playwright |
| Question | retrieve information from the system |
| assert | verify returned values |

This separation keeps the framework clean.

---

# Typical Pattern

A common test pattern looks like this:

```python
customer.attempts_to(
    Login.with_credentials("standard_user", "secret_sauce"),
    Ensure.that(InventoryPage.INVENTORY_CONTAINER).to_be_visible(),
)

title = customer.asks_for(TextOf(AppShell.PAGE_TITLE))

assert title == "Products"
```

Flow:

```
Task -> changes system state
Ensure -> verifies UI state
Question -> retrieves values
assert -> verifies logic
```

---

# Summary

Use the following rule of thumb:

```
Ensure -> UI assertions
Question -> retrieve values
assert -> verify values
```

This keeps tests:

- readable
- maintainable
- aligned with the Screenplay pattern.
