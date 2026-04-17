# AGENTS.md

## What this repository is

This repository is the **playwright-pytest-screenplay-framework** portfolio project.

It demonstrates a Python-based Playwright + pytest automation framework built around the **Screenplay Pattern** with a strict layered architecture.

Primary goals:
- keep tests readable in business terms
- keep framework pieces small and composable
- show that the same architecture can support UI, API, and hybrid testing
- preserve maintainability over cleverness
- prefer reuse of existing abstractions over introducing parallel styles

## Core architectural vocabulary

Use these terms consistently:

- Actor: performs activities using abilities
- Ability: gives the actor access to an external system or tool
- Task: higher-level business action
- Interaction: lower-level technical action
- Question: reads system state
- Consequence: assertion/verifier step
- Target: central locator abstraction

## Hard architectural expectations

These rules are repository-defining and should not be violated:

1. `actor.attempts_to()` accepts **only** `Task` or `Consequence`.
2. `Interaction` objects are created **only inside** `Task.perform_as()`, usually via `self.perform_interactions(actor, ...)`.
3. **Target** locators are always lambdas like `lambda page: page.locator(...)` or `lambda page: page.get_by_*(...)`, never raw selector strings by themselves.
4. Prefer stable selectors in this order:
   - `data-testid`
   - accessible role/name selectors
   - other stable attributes
5. Dynamic targets belong in `@classmethod` factory methods on the target catalog, not plain constants.
6. Every Task should expose a readable factory classmethod such as `with_credentials(...)`, `named(...)`, or `for_(...)`.
7. Questions return plain Python values such as `bool`, `str`, `int`, or `list`.
8. Prefer `Ensure.that(...).to_*()` as the assertion/consequence style when the framework supports it.
9. Tests use `pytest` functions, not test classes.
10. Tests should not import low-level Playwright interactions directly.

## Selector and Target guidance

- Keep selectors centralized in target catalogs.
- Do not scatter raw selectors across tests.
- Avoid brittle CSS/XPath if a better selector exists.
- Group targets by page or section where that improves readability.

## Task design guidance

- Keep Tasks business-readable.
- Keep Interactions low-level and reusable.
- Avoid giant Tasks that hide too much behavior.
- Compose from smaller Tasks where that improves clarity.
- Prefer adding the smallest useful abstraction.

## Questions and Consequences

- Use Questions when reading state or values.
- Use Consequences / Ensure wrappers for direct verification.
- If a test repeatedly reads a value, visibility, count, or status, prefer adding or reusing a Question.

## API and hybrid testing

- Keep API work aligned with Screenplay where practical.
- Wrap meaningful API actions in Tasks/Questions when that improves consistency.
- Preserve separation between UI and API concerns while still supporting hybrid scenarios.

## File discipline

When adding or editing code:
- inspect similar existing files first
- preserve naming conventions
- preserve folder structure
- prefer targeted changes over broad refactors

## Validation discipline

Before finishing a code change, when relevant:
- run the smallest relevant pytest scope first
- then broader validation if shared code was touched
- run Ruff if configured
- run Black if configured
- update docs/examples when public behavior changes

## Documentation expectations

When producing docs or examples:
- keep explanations practical and plain-English
- prefer copy-friendly markdown
- include examples when introducing a new abstraction
- explain architectural tradeoffs simply

## Change discipline

- Do not rename major concepts casually.
- Do not introduce new dependencies without strong justification.
- Do not create a second framework beside the existing one.
- For larger refactors, explain the before/after in simple terms.
