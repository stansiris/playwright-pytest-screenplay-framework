---
name: python-screenplay-generator
description: Generate Python Screenplay Targets, Tasks, Questions, and test scaffolding from an approved plan, Gherkin, or scenario for this repository.
argument-hint: "<approved plan or scenario description> [AppName]"
---

You are generating **Python test code** for the
**playwright-pytest-screenplay-framework** portfolio project.

The project uses the **Screenplay Pattern** with a strict architecture.
This skill should generate Python code that matches the existing framework rather than inventing a new style.

Arguments provided: $ARGUMENTS

Parse the arguments as follows:
- **Plan / Scenario** - the approved Screenplay plan, Gherkin, or plain-English scenario to implement.
- **AppName** (optional) - a PascalCase app name such as `WorkItems` or `SauceDemo`. If omitted, derive it from context where possible.

If the scenario is too vague to implement safely, ask the user for clarification before proceeding.

If a live **URL** is provided inside the arguments, you may use it to inspect the page and discover locators.
If no URL is provided, generate code from the approved plan and existing repository patterns only.

---

## Accepted input formats

This skill accepts any of the following as approved input:

1. A Screenplay-oriented test plan
2. A Gherkin feature/scenario set
3. A combined document containing both Screenplay planning notes and Gherkin scenarios

Do not require a single planner-specific format if the intent is already clear and implementation-ready.

---

## Normalization rule

Before generating code, normalize the approved input into the repository's Screenplay architecture.

- If the input is Screenplay-oriented:
  - map Actor, Tasks, Questions, Consequences, and Scenarios directly into code structure

- If the input is Gherkin:
  - infer the Screenplay concepts needed to implement each scenario
  - identify likely Tasks from business actions
  - identify likely Questions or Ensure assertions from `Then` steps
  - identify reusable Targets from repeated UI references
  - preserve scenario intent without copying Gherkin mechanically into low-level code

- If the input contains both:
  - treat the Screenplay plan as implementation guidance
  - treat the Gherkin as behavioral specification
  - resolve minor wording differences in favor of the most testable and specific interpretation

Always generate repository-native Python Screenplay code, regardless of whether the approved
source material was written as Screenplay planning notes, Gherkin, or both.

---

## Hard architectural rules - never violate these

1. `actor.attempts_to()` accepts **only** `Task` or `Consequence`. Never pass an `Interaction` directly.
2. `Interaction` objects are created **only** inside `Task.perform_as()`, passed to `self.perform_interactions(actor, ...)`.
3. **Target** locator is always a `lambda page: page.locator(...)` or `lambda page: page.get_by_*(...)` - never a raw string.
4. Prefer `data-testid` attribute selectors: `page.locator('[data-testid="..."]')`.
5. Dynamic (parameterised) targets are `@classmethod` factory methods on the catalog class, not plain attributes.
6. Every Task has a readable factory classmethod such as `with_credentials(...)`, `named(...)`, or `for_(...)`.
7. Questions return a plain Python value (`bool`, `str`, `int`, `list`, etc.).
8. `Ensure.that(target).to_be_visible()` and similar checks are `Consequence`s, so they are valid inside `actor.attempts_to()`.
9. Test files use `pytest` functions, not classes.
10. Never import low-level Playwright interactions directly into test files.
11. Reuse existing framework abstractions before creating new ones.
12. Do not generate TypeScript.
13. Do not generate step-definition style automation unless explicitly requested.
14. Generate Screenplay Pattern code for this repository even when the input source is Gherkin.

---

## File placement conventions

| Artefact | Path |
|----------|------|
| Target catalog | `examples/<app_name>/automation/ui/targets.py` |
| UI Tasks | `examples/<app_name>/automation/tasks/<task_name>.py` |
| Questions | `examples/<app_name>/automation/questions/<question_name>.py` |
| UI tests | `tests/<app_name>/test_<app_name>_ui.py` |
| Feature files (if requested) | `tests/<app_name>/features/<feature_name>.feature` |

`<app_name>` is the snake_case application name.

---

## Input interpretation guidance

When the source is Gherkin:
- `Given` steps often imply setup Tasks or precondition helpers
- `When` steps usually map to Task execution
- `Then` steps usually map to Questions and/or Ensure consequences
- `And` should be interpreted according to the preceding step type
- repeated step phrases should be normalized into reusable abstractions rather than duplicated code

---

## Step-by-step workflow

### Step 1 - Read the approved plan and inspect existing patterns

Before generating code:
1. Read `AGENTS.md`
2. Inspect existing repository examples for the same app or a similar app
3. Reuse naming, layering, and style from the codebase
4. If relevant, inspect existing targets, tasks, questions, and tests before adding new ones

Reference examples when available:
- existing target catalog
- existing task
- existing question
- existing test

When in doubt, follow an existing pattern from the repository instead of inventing a new one.

### Step 2 - Discover or infer locators

If a URL is supplied, inspect the page and prefer:
1. `data-testid`
2. accessible role/name selectors
3. other stable attributes

If there is no URL:
- infer the needed targets from approved requirements and existing code
- do not invent brittle selectors without warning
- note assumptions where selectors cannot be safely confirmed

### Step 3 - Generate the Target catalog additions

Create or extend target catalogs using the repository's Target shape.

Rules:
- centralize selectors
- group targets by page or section
- do not duplicate existing targets
- use `@classmethod` for dynamic targets
- use default-argument capture inside lambdas when closing over parameters

### Step 4 - Generate Tasks

Read the approved plan and identify the user actions.

Create one Task file per meaningful action when that matches repository practice.

Rules:
- Tasks should be business-readable
- low-level mechanics stay inside `perform_as()`
- use existing interactions such as Click, Fill, SelectByValue, Navigate where applicable
- expose readable factory classmethods

### Step 5 - Generate Questions and Consequences

For each read of system state, create or reuse a Question.

Rules:
- use Questions for values, visibility reads, counts, text, or status
- use Ensure / Consequence style for direct checks where appropriate
- do not create Questions for things that are better expressed as a simple Ensure

### Step 6 - Generate the test file

Create or update pytest-based tests.

Rules:
- tests remain readable from the actor's point of view
- tests import Tasks, Questions, Targets, and Ensure
- tests do not import low-level interactions
- use the correct actor fixture from the relevant `conftest.py`
- apply markers appropriate to the suite

### Step 7 - Show before inserting

Before writing any file:
1. Print the generated Target snippet.
2. Print each Task file.
3. Print each Question file.
4. Print the test file.
5. Print any assumptions or unresolved selector concerns.
6. Ask the user to confirm before inserting.

After confirmation:
- append or insert into existing files where appropriate
- create new files only where needed
- avoid unrelated edits

### Step 8 - Lint and validate

After writing all files, run:

    ruff check . && black --check .

If either fails, fix the issues before reporting completion.

If relevant and safe, run the smallest meaningful pytest scope for the generated code.

---

## Output expectations

When presenting generated code, provide:
- file paths
- complete contents for new files
- targeted edits for existing files
- a short explanation of how the pieces fit together

---

## Reference expectations from this codebase

Before finalizing, inspect similar repository files and align with them.

When in doubt:
- prefer existing patterns
- prefer smaller reusable abstractions
- prefer centralized targets
- prefer actor-centered readability
- prefer maintainability over over-abstraction
