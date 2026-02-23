# Architecture Overview

This repository implements a **Playwright + pytest** UI automation
framework using the **Screenplay pattern**, with **pytest-bdd** as the
primary behavior/specification layer.

The goal is to keep Gherkin readable and stable while ensuring
automation code remains **composable, reusable, and maintainable**.

------------------------------------------------------------------------

## High-Level Concept

**Screenplay is the automation engine.**\
**pytest-bdd is the collaboration/specification layer.**

Execution path:

Gherkin Scenario → Step Definitions (thin wrappers) → Screenplay Tasks
(business intent) → Interactions (UI mechanics) → Playwright API
(page.locator(), click(), fill(), etc.)

Key separation:

-   **Feature files** describe behavior
-   **Step definitions** translate phrases into Screenplay calls
-   **Tasks** express user intent and workflow composition
-   **Interactions** perform atomic UI actions
-   **Questions** query the UI state for assertions
-   **Targets** define how to locate elements (selectors)

------------------------------------------------------------------------

## Core Screenplay Concepts

### Actor

An **Actor** represents a user interacting with the system.

Responsibilities: - Holds **Abilities** (e.g., browsing the web) -
Executes Tasks and Interactions via `attempts_to(...)` - Evaluates
Questions via `asks_for(...)`

Example:

``` python
actor.attempts_to(
    Login.with_credentials("standard_user", "secret_sauce"),
    AddItem.named("Sauce Labs Backpack"),
    GoToCart(),
)

assert actor.asks_for(CartItemCountIs(1))
```

------------------------------------------------------------------------

### Ability

An **Ability** provides the Actor with capabilities required to interact
with the system.

Typical ability: - `BrowseTheWeb.using(page)`

Why: - Keeps Tasks/Interactions independent from the raw Playwright
fixture - Improves portability and test readability

------------------------------------------------------------------------

### Task

A **Task** represents a meaningful unit of user intent.

Rules: - Tasks are **business-level**, not click-level - Tasks can be
composed of multiple Interactions - Tasks should not expose selectors or
UI structure to tests

Examples: - `Login.with_credentials(username, password)` -
`AddItem.named(item_name)` - `ProceedToCheckout()`

------------------------------------------------------------------------

### Interaction

An **Interaction** is a single atomic UI operation.

Examples: - `Click.on(Target)` - `Fill.in(Target, value)` -
`Select.option(Target, value)`

Rules: - Interactions know how to use Playwright through Actor
Abilities - Interactions should be reusable across Tasks and apps

------------------------------------------------------------------------

### Question

A **Question** queries application state to support assertions.

Rules: - Questions do not perform meaningful state changes - Questions
return values (bool/string/number/list) for assertions - Prefer
page-specific Questions only when they represent real business logic

Examples: - `OnInventoryPage()` - `CartItemCountIs(n)` -
`TotalsMatchComputedSum()`

------------------------------------------------------------------------

### Target

A **Target** encapsulates an element locator (selector) and its meaning.

Rules: - Tasks/Interactions reference Targets, not raw selectors -
Targets live in `screenplay/ui` - Centralizing selectors makes
refactoring safe

------------------------------------------------------------------------

## pytest-bdd Integration

### Why pytest-bdd

-   Creates a shared behavior language (Gherkin)
-   Scenarios remain readable for non-technical reviewers
-   Step definitions call Screenplay code, keeping logic out of steps

### Step Definition Discipline

Step definitions should be thin and stable.

Good:

``` python
@when(parsers.parse('I add "{item_name}" to the cart'))
def add_item(actor, item_name):
    actor.attempts_to(AddItem.named(item_name))
```

Avoid: - Embedding locators inside steps - Performing multiple business
actions in a single step without intent - Creating multiple steps that
mean the same thing

------------------------------------------------------------------------

## Layer Responsibilities

### screenplay/core

Framework primitives: - Actor - Task, Interaction, Question interfaces -
Target abstraction

### screenplay/abilities

-   `BrowseTheWeb`

### screenplay/interactions

Generic atomic actions: - Click - Fill - NavigateTo - Select

### screenplay/tasks

Reusable business intent and workflows: - Login, AddItem, Checkout tasks

### screenplay/questions

Reusable assertions / UI queries: - Visibility checks - Text/value
extraction - Domain-specific validations (e.g., totals math)

### screenplay/ui

Application-specific Targets and locators

### tests/features

Gherkin specifications

### tests/steps

Step definitions mapping step phrases to Screenplay Tasks/Questions

------------------------------------------------------------------------

## Design Goals

-   **Readability**
-   **Reusability**
-   **Maintainability**
-   **Portability**
-   **Behavior focus**
