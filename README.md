# Playwright + Pytest Screenplay Framework

Python UI automation framework using Playwright, pytest, and the Screenplay pattern, with an optional `pytest-bdd` layer for Gherkin-driven scenarios.

## New Direction

This project is moving toward a behavior-first, architecture-driven model:

- Keep automation logic in reusable Screenplay `Task` and `Interaction` classes.
- Use Gherkin as a collaboration/specification layer when needed.
- Treat each Gherkin step phrase as a stable contract mapped by step definitions.
- Prefer business-level steps for behavior tests, and UI-level steps only for UI mechanics.

## Core Principles

- **Screenplay stays primary**: step definitions should be thin wrappers that call Tasks/Questions.
- **Step contract discipline**: one step phrase should keep one meaning over time.
- **Reuse over duplication**: compose flows from reusable Tasks rather than raw page actions in tests.
- **Portability**: the core framework is generic; adapt to new sites by replacing app-specific Targets/Tasks.

## Project Structure

- `screenplay/core`: Actor, Task, Interaction, Question, Target abstractions.
- `screenplay/abilities`: actor abilities (for example `BrowseTheWeb`).
- `screenplay/interactions`: low-level browser actions (`Click`, `Fill`, `NavigateTo`, ...).
- `screenplay/tasks`: reusable business flows (`Login`, `Logout`, checkout tasks, ...).
- `screenplay/questions`: reusable assertions/query objects (`IsVisible`, `TextOf`).
- `screenplay/ui`: app-specific Targets and locators (`SauceDemo`).
- `tests`: pytest tests, fixtures, and feature files.

## Testing Modes

1. **Plain pytest + Screenplay (current baseline)**
   - Example: `tests/test_golden_path_poc.py`
   - Best for direct engineering feedback and fast refactoring.

2. **pytest-bdd + Screenplay (recommended for shared behavior language)**
   - Feature file: `tests/login_page.feature`
   - Step definitions map Gherkin steps to Screenplay Tasks/Questions.
   - Keeps business-readable specs without sacrificing framework design quality.

## Example Step Mapping (pytest-bdd)

```python
from pytest_bdd import parsers, when
from screenplay.tasks.login import Login


@when(parsers.parse('I log in with username "{username}" and password "{password}"'))
def login(customer, username, password):
    customer.attempts_to(Login.with_credentials(username, password))
```

## Practical Guidance for Gherkin

- Good behavior step: `When I log in with username "<username>" and password "secret_sauce"`
- Good UI-specific step: `When I press Tab`
- Avoid redefining the same phrase to do different actions.
- It is fine to scaffold step definitions with `print()` first, then replace with real Tasks/assertions.

## Getting Started

1. Install dependencies (pytest, playwright, pytest-playwright, and optionally pytest-bdd).
2. Install Playwright browser binaries:
   - `playwright install`
3. Run tests:
   - `pytest -q`

## Near-Term Roadmap

- Add first-class `pytest-bdd` step-definition module for `tests/login_page.feature`.
- Define an approved step vocabulary for login and checkout behavior.
- Add CI execution and test reporting (HTML/JUnit) for portfolio-grade presentation.
