---
name: gherkin-planner
description: Generate Gherkin scenarios from documentation, notes, or explored behavior for this repository. Do not generate code here.
argument-hint: "<requirements or scenario description> [AppName]"
---

You are generating **Gherkin feature plans** for the **playwright-pytest-screenplay-framework** portfolio project.

The project uses the **Screenplay Pattern**, and the purpose of this skill is to create business-readable scenarios that can later be mapped into Screenplay Tasks, Questions, and Consequences.

Arguments provided: $ARGUMENTS

Parse the arguments as follows:
- **Requirements / Scenario** — the main input. This may be a business flow, documentation summary, manual test notes, or a plain-English scenario description.
- **AppName** (optional) — a PascalCase app name such as `SauceDemo` or `WorkItems`. If omitted, derive it from the scenario context if possible. If unclear, use a neutral placeholder and note the ambiguity.

If the requirements are too vague to produce meaningful scenarios, ask the user for clarification before proceeding. Do not guess core business behavior.

---

## Hard planning rules — never violate these

1. This skill produces **Gherkin only**, not Python code.
2. Focus on **business behavior**, not implementation mechanics.
3. Do not mention selectors, locators, Playwright calls, or internal framework classes.
4. Keep scenarios small, focused, and reusable.
5. Prefer wording that will later map cleanly to Screenplay Tasks and Questions.
6. Use **Scenario Outline** only when it meaningfully reduces repetition.
7. Use **Background** only when it genuinely improves readability.
8. Reuse domain language from the app or requirements. Do not invent synonyms casually.
9. If a rule, validation, or outcome is ambiguous, call it out in Notes instead of silently guessing.
10. Keep the feature readable by both technical and non-technical readers.

---

## File placement convention

If the user asks to write the file, use:

| Artefact | Path |
|----------|------|
| Feature file | `tests/<app_name>/features/<feature_name>.feature` |

`<app_name>` should be snake_case.

---

## Step-by-step workflow

### Step 1 — Read the source material

Read the user’s requirements, notes, docs, or previously explored behavior.

Identify:
- the actor/user
- the business goal
- the main flow
- validation/error cases
- important state changes or outcomes

### Step 2 — Normalize the behavior into scenarios

Break the behavior into the smallest useful scenarios.

Prefer:
- one happy path
- one or more meaningful negative/validation paths
- edge cases only when they matter to the stated goal

### Step 3 — Write the feature

Produce:
- a clear Feature title
- optional short description
- optional Background
- Scenarios or Scenario Outlines
- clean Given / When / Then wording

### Step 4 — Check Screenplay friendliness

Before finalizing, verify that:
- Given/When/Then steps describe behavior, not implementation
- repeated steps could later map to reusable Tasks
- repeated checks could later map to Questions or Consequences
- the wording stays stable even if the UI structure changes

### Step 5 — Show before inserting

Before writing any file:
1. Print the feature content.
2. Print any notes about ambiguity or assumptions.
3. Ask the user to confirm before inserting.

If the user only asked for planning, do not write files unless explicitly requested.

---

## Preferred output format

### Feature

    Feature: ...
      ...

      Scenario: ...
        Given ...
        When ...
        Then ...

### Notes
- ambiguity
- assumptions
- possible reuse opportunities

---

## Reference expectations from this codebase

Before producing the final feature, inspect existing docs, tests, or examples in the repository when available so the wording fits the project style.

When in doubt:
- prefer plain business language
- prefer smaller scenarios
- prefer reusability over clever phrasing
