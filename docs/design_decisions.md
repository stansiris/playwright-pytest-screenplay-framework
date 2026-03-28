# Design Decisions (Q&A)

This document explains the key architectural decisions behind the framework
in a question-and-answer format.

The framework is intentionally opinionated. Its goal is not only to automate
a web application, but also to demonstrate how the Screenplay Pattern can be
implemented in Python in a way that keeps tests readable, domain-focused,
and scalable.

These decisions are meant to preserve separation between:

- business behavior
- UI mechanics
- assertion strategy
- automation runtime

## Table of Questions

- [Q1. Why use Screenplay instead of Page Object Model](#q1-why-use-screenplay-instead-of-page-object-model)
- [Q2. Why does `actor.attempts_to()` only accept Tasks and Consequences](#q2-why-does-actorattempts_to-only-accept-tasks-and-consequences)
- [Q3. Why does `Ensure.that()` exist](#q3-why-does-ensurethat-exist)
- [Q4. Why is `Ensure.that()` modeled as a Consequence](#q4-why-is-ensurethat-modeled-as-a-consequence)
- [Q5. What is the difference between `Question` and `Ensure`](#q5-what-is-the-difference-between-question-and-ensure)
- [Q6. Where does the raw API `Response` live after `attempts_to()`](#q6-where-does-the-raw-api-response-live-after-attempts_to)
- [Q7. What is the practical summary of these decisions](#q7-what-is-the-practical-summary-of-these-decisions)

---

## Q1. Why use Screenplay instead of Page Object Model

Screenplay scales more naturally as test suites grow.

Page Object Model organizes automation around pages and page methods.
That works well for smaller projects, but page classes often become large,
tightly coupled to UI details, and responsible for too many concerns.

Screenplay organizes automation around actors, tasks, interactions,
questions, and abilities. This shifts the design from page structure
to user behavior.

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

Why this matters:

- tests stay focused on intent
- reusable behavior is modeled as Tasks
- low-level browser operations are isolated in Interactions
- assertions and state retrieval are separated cleanly
- the framework can grow without becoming a collection of page scripts

---

## Q2. Why does `actor.attempts_to()` only accept Tasks and Consequences

`actor.attempts_to()` only accepts Tasks and Consequences to keep tests at the behavior level.

A Task represents a meaningful user action, for example:

- `Login.with_credentials(...)`
- `AddProductToCart.named(...)`
- `ProceedToCheckout()`

A Consequence represents a verification step, for example:

- `Ensure.that(...).to_be_visible()`

This keeps tests focused on what the actor is doing and verifying,
rather than on implementation details.

Preferred:

```python
customer.attempts_to(
    Login.with_credentials("standard_user", "secret_sauce"),
    Ensure.that(InventoryPage.CONTAINER).to_be_visible(),
)
```

---

## Q3. Why does `Ensure.that()` exist

`Ensure.that()` bridges Screenplay-style assertions with Playwright's
`expect()` API.

Playwright provides strong locator assertions, such as:

- `to_be_visible()`
- `to_have_text()`
- `to_contain_text()`
- `to_have_count()`

These assertions provide:

- auto-waiting
- retry behavior
- strong failure diagnostics
- expressive locator checks

The framework keeps those benefits without exposing raw Playwright assertions
directly in tests.

Raw Playwright call:

```python
expect(page.locator("#inventory_container")).to_be_visible()
```

Screenplay wrapped Playwright call:

```python
customer.attempts_to(
    Ensure.that(InventoryPage.CONTAINER).to_be_visible()
)
```

---

## Q4. Why is `Ensure.that()` modeled as a Consequence

`Ensure.that()` is modeled as a Consequence because it verifies system state
after an action rather than changing that state.

- **Tasks** perform actions
- **Consequences** verify results

```python
customer.attempts_to(
    Login.with_credentials("standard_user", "secret_sauce"),  # Task
    Ensure.that(InventoryPage.CONTAINER).to_be_visible(),     # Consequence
)
```

Modeling verification as an executable activity keeps it inside the same
actor flow as the Task that produced the result. The actor does something,
then verifies the outcome.

---

## Q5. What is the difference between `Question` and `Ensure`

Both `Question` and `Ensure` deal with system state, but they serve
different roles.

Question role:

- retrieves information from the system
- encapsulates transformation or comparison logic
- returns values for assertions, conditions, or calculations

Ensure role:

- uses Playwright's `expect()` to assert locator-based UI state
- keeps Playwright's auto-waiting and retry behavior
- expresses verification as part of the actor's activity flow

Why both are necessary:

- using only `Question` would lose the benefits of Playwright's locator
  assertion engine for UI state checks
- using only `Ensure` would make value retrieval and computed assertions
  harder and less flexible

Rule of thumb:

- use `Ensure` for UI assertions backed by `expect()`
- use `Question` to retrieve values or derive information
- use `assert` to check returned values when appropriate

---

## Q6. Where does the raw API `Response` live after `attempts_to()`

API tests in this project still use the Screenplay pattern.

- Tasks perform API actions
- Questions read API state
- `Actor.attempts_to(...)` returns `None`

That creates a practical problem: a test may still need the raw HTTP
`requests.Response` for assertions such as status code or error payload.

The framework solves this by storing the latest raw response on the generic
HTTP ability, `CallTheApi`, as `last_response`.

Why this location:

- not on the `Actor`, because `Actor` should remain a generic orchestrator
- not on Task objects, because Tasks should model actions rather than become
  mutable result containers
- not in a separate memory helper, because that adds another layer and makes
  the API flow harder to follow

`CallTheApi` is the object that actually performs the HTTP request, so it is
the narrowest and most natural owner for the latest raw response.

Example:

```python
work_items_api_actor.attempts_to(
    LoginToWorkItemsApi.with_credentials("admin", "admin123"),
    CreateWorkItemViaApi.with_payload({"title": "Example"}),
)

response = work_items_api_actor.ability_to(CallTheApi).last_response
assert response is not None
assert response.status_code == 201
```

Important subtlety:

API Questions also make HTTP calls through `CallTheApi`, so they overwrite
`last_response` too. If a test needs the raw response from a specific API Task,
it should assert on `last_response` immediately after that Task runs, before
asking an API Question.

For the longer-running record of API-testing-specific issues and follow-up
decisions, see `docs/api_testing.md`.

This means `last_response` is intentionally a latest-wins value.

---

## Q7. What is the practical summary of these decisions

The framework is intentionally strict in order to preserve readable tests,
reusable behavior, clean separation of concerns, and strong Playwright
integration.

In practice:

- use Screenplay instead of Page Object Model
- keep tests focused on Tasks and Consequences
- use `Ensure` for Playwright-backed UI assertions
- use `Question` to retrieve values

These constraints are intentional. They make the framework stricter,
but also more consistent, scalable, and easier to understand.

The result is a tighter, more readable, and more maintainable test DSL.
