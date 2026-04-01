---
name: generate-screenplay-tests
description: Generate Screenplay Targets, Tasks, Questions, and test scaffolding for a new app or scenario
argument-hint: "<url-or-scenario> [AppName]"
---

You are generating test code for the **playwright-pytest-screenplay-framework** portfolio project.
The project uses the **Screenplay Pattern** with a strict 4-layer architecture.
Arguments provided: $ARGUMENTS

---

## Hard architectural rules — never violate these

1. `actor.attempts_to()` accepts **only** `Task` or `Consequence`. Never pass an `Interaction` directly.
2. `Interaction` objects are created **only** inside `Task.perform_as()`, passed to `self.perform_interactions(actor, ...)`.
3. **Target** locator is always a `lambda page: page.locator(...)` or `lambda page: page.get_by_*(...)` — never a raw string.
4. Prefer `data-testid` attribute selectors: `page.locator('[data-testid="..."]')`.
5. Dynamic (parameterised) targets are `@classmethod` factory methods on the catalog class, not plain attributes.
6. Every Task has a readable factory classmethod (e.g. `LoginToWorkItems.with_credentials(u, p)`, `CreateWorkItem.named(title=...)`).
7. Questions return a plain Python value (bool, str, int, list). The actor calls `actor.asks_for(QuestionInstance())`.
8. `Ensure.that(target).to_be_visible()` etc. is a `Consequence`, so it is valid inside `actor.attempts_to()`.
9. Test files use `pytest` functions, not classes. Apply `pytestmark = [pytest.mark.<type>, pytest.mark.integration]`.
10. Never import from `screenplay_core.playwright.interactions` in test files. Tests only see Tasks, Questions, Targets, and Ensure.

---

## File placement conventions

| Artefact | Path |
|----------|------|
| Target catalog | `examples/<app_name>/automation/ui/targets.py` |
| UI Tasks | `examples/<app_name>/automation/tasks/<task_name>.py` |
| Questions | `examples/<app_name>/automation/questions/<question_name>.py` |
| UI tests | `tests/<app_name>/test_<app_name>_ui.py` |

`<app_name>` is the snake_case application name (e.g. `work_items`, `saucedemo`).

---

## Step-by-step workflow

### Step 1 — Discover locators

**If a URL was provided:**
Run the following to capture `data-testid` attributes directly from the live page:

```python
# Execute this via Bash (requires the app to be running)
python - <<'EOF'
from playwright.sync_api import sync_playwright

url = "<URL_FROM_ARGUMENTS>"
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(url)
    page.wait_for_load_state("networkidle")
    elements = page.query_selector_all("[data-testid]")
    for el in elements:
        tid = el.get_attribute("data-testid")
        tag = el.evaluate("el => el.tagName.toLowerCase()")
        print(f'{tid}  // <{tag}>')
    browser.close()
EOF
```

Use the discovered `data-testid` values to hand-craft `Target` lambdas using the pattern in Step 2.

**If the page has no `data-testid` attributes:**
Fall back to `name`, `id`, `type`, `role`, or visible text selectors. Extract them with a broader query and hand-craft the lambdas.

**If you must infer from HTML source:**
Read the HTML, extract every `data-testid` value, and hand-craft the `Target` lambdas using the pattern below.

---

### Step 2 — Generate the Target catalog

Use the output from Step 1. Every target follows this shape:

```python
# Static target (stable selector)
LOGIN_BUTTON = Target(
    "<AppName> login button",
    lambda page: page.locator('[data-testid="login-button"]'),
)

# Dynamic target (parameterised — use @classmethod)
@classmethod
def item_card_for_id(cls, item_id: int) -> Target:
    return Target(
        f"<AppName> item card for id {item_id}",
        lambda page, _id=item_id: page.locator(
            f'[data-testid="item-card"][data-item-id="{_id}"]'
        ),
    )
```

**Important:** use a default-argument capture (`_id=item_id`) inside the lambda whenever the lambda closes over a loop variable or parameter.

Insert new targets into the existing `targets.py` file, grouped by page/section. Do not duplicate targets that already exist.

---

### Step 3 — Scaffold Tasks

For each user action identified in the scenario, create one Task file.

```python
# examples/<app_name>/automation/tasks/<task_name>.py
from examples.<app_name>.automation.ui.targets import <AppName>Targets
from screenplay_core.core.task import Task
from screenplay_core.playwright.interactions.click import Click
from screenplay_core.playwright.interactions.fill import Fill


class <TaskName>(Task):
    """Task: <one-line description of the user goal>."""

    def __init__(self, param: str):
        self.param = param

    def __repr__(self) -> str:
        return f"<TaskName>(param='{self.param}')"

    def perform_as(self, actor) -> None:
        self.perform_interactions(
            actor,
            Fill(<AppName>Targets.SOME_INPUT, self.param),
            Click(<AppName>Targets.SUBMIT_BUTTON),
        )

    @classmethod
    def with_param(cls, param: str) -> "<TaskName>":
        return cls(param=param)
```

Available interactions (import from `screenplay_core.playwright.interactions.*`):
- `Click(target)` — left-click
- `Fill(target, text)` — clear + type
- `SelectByValue(target, value)` — `<select>` element
- `Navigate(url)` — navigate to URL

---

### Step 4 — Scaffold Questions

For each assertion that reads state (not just `Ensure.that(target).to_be_visible()`), create a Question.

```python
# examples/<app_name>/automation/questions/<question_name>.py
from screenplay_core.core.actor import Actor
from screenplay_core.core.question import Question
from examples.<app_name>.automation.ui.targets import <AppName>Targets


class <QuestionName>(Question):
    """Question: <what boolean/value this answers>."""

    def __init__(self, identifier: str):
        self.identifier = identifier

    def answered_by(self, actor: Actor) -> bool:
        target = <AppName>Targets.some_target_for(self.identifier)
        return target.resolve_for(actor).is_visible()

    def __repr__(self) -> str:
        return f"<QuestionName>(identifier='{self.identifier}')"

    @classmethod
    def for_identifier(cls, identifier: str) -> "<QuestionName>":
        return cls(identifier=identifier)
```

Use `target.resolve_for(actor)` to get the underlying Playwright `Locator`.
Use `actor.ability_to(BrowseTheWeb).page` only when you need the raw page object (e.g. for URL checks).

---

### Step 5 — Scaffold the test file

```python
# tests/<app_name>/test_<app_name>_ui.py
"""<AppName> UI integration tests expressed with Screenplay tasks and questions."""

import pytest

from examples.<app_name>.automation.questions.<question_module> import <QuestionName>
from examples.<app_name>.automation.tasks.<task_module> import <TaskName>
from examples.<app_name>.automation.ui.targets import <AppName>Targets
from screenplay_core.playwright.ensure import Ensure

pytestmark = [pytest.mark.ui, pytest.mark.integration]


def test_<scenario_name>(<actor_fixture>) -> None:
    """<Plain-English description of what this test proves>."""
    <actor_fixture>.attempts_to(
        <TaskName>.with_param("value"),
        Ensure.that(<AppName>Targets.SOME_TARGET).to_be_visible(),
    )
    result = <actor_fixture>.asks_for(<QuestionName>.for_identifier("value"))
    assert result
```

The actor fixture name comes from `conftest.py` in `tests/<app_name>/`. Check that file before naming the fixture.

---

### Step 6 — Show before inserting

Before writing any file:
1. Print the generated Target snippet.
2. Print each Task file.
3. Print each Question file.
4. Print the test file.
5. Ask the user to confirm before inserting.

After confirmation, insert the code into the correct files. For Target catalogs, append new entries inside the existing class. For Tasks/Questions/Tests, create new files.

---

### Step 7 — Lint

After writing all files, run:
```bash
ruff check . && black --check .
```

If either fails, fix the issues before reporting completion.

---

## Reference examples from this codebase

**Existing target catalog:** `examples/work_items/automation/ui/targets.py`
**Existing task:** `examples/work_items/automation/tasks/login.py`
**Existing question:** `examples/work_items/automation/questions/work_item_visible.py`
**Existing test:** `tests/work_items/test_work_items_ui.py`

When in doubt about a pattern, read one of these files before generating code.
