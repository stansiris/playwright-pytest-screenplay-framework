---
name: planner
description: Generate a Screenplay-oriented plan, Gherkin scenarios, or both from documentation, notes, or explored behavior for this repository. Do not generate code here.
argument-hint: "<requirements or scenario description> [AppName] [format=screenplay|gherkin|both]"
---

You are generating **plain planning artefacts** for the
**playwright-pytest-screenplay-framework** portfolio project.

This skill turns requirements, docs, or explored behavior into output that is easy to map into:
- Targets
- Tasks
- Questions
- Consequences
- pytest or pytest-bdd tests

Arguments provided: $ARGUMENTS

Parse the arguments as follows:
- **Requirements / Scenario** - the main behavioral input.
- **AppName** (optional) - a PascalCase app name such as `SauceDemo` or `WorkItems`. If omitted, derive it from context if possible.
- **format** (optional) - one of:
  - `screenplay` - produce a Screenplay-oriented plan
  - `gherkin` - produce Gherkin scenarios only
  - `both` - produce both formats in one response

If no format is specified, default to `screenplay`.

If the requirements are too vague to create a meaningful plan, ask the user for clarification before proceeding.

---

## Hard planning rules - never violate these

1. This skill produces a **plan**, not Python code.
2. Focus on behavior and architecture, not low-level implementation.
3. Do not produce raw Playwright calls unless the user explicitly asks for them.
4. Prefer naming that naturally maps to Screenplay concepts.
5. Distinguish clearly between:
   - actions the actor performs
   - things the actor reads
   - things the actor verifies
6. A read of system state usually belongs in a **Question**.
7. A direct assertion/check usually belongs in a **Consequence**.
8. Keep the plan actor-centered and business-readable.
9. If behavior is ambiguous, note it instead of inventing details.
10. Prefer smaller, reusable scenario plans over giant end-to-end plans.
11. The planner **may perform light exploratory browser work** when a live URL or running app is available.
12. Any exploration must serve planning only. Do not generate final code in this skill.
13. If `format=gherkin`, produce Gherkin only.
14. If `format=screenplay`, produce a Screenplay-oriented plan only.
15. If `format=both`, produce the Screenplay plan first and the Gherkin rendering second.

---

## Exploration behavior

When a live URL or running application is available, this skill may use **Playwright CLI**
together with the user's input to improve the plan in real time.

Use exploration to:
- confirm the actual user flow
- identify important screens, forms, states, and transitions
- observe visible validation messages and outcome states
- discover where the scenario branches or fails
- validate whether the documented behavior matches the real app

Do **not** use exploration to:
- write final Python code
- over-focus on selectors or implementation details
- wander into unrelated flows
- replace the user's stated requirements with guesses based only on UI discovery

Treat exploration as a **planning aid**, not the final deliverable.

---

## Step-by-step workflow

### Step 1 - Read the source material

Read the requirements, docs, notes, or explored behavior.

Identify:
- who the actor is
- what the actor wants
- what actions are required
- what state must be read
- what must be verified

### Step 2 - Explore when useful

If a live URL or running application is available, perform light exploratory navigation with
**Playwright CLI** to confirm the flow.

Use the exploration to answer questions such as:
- what is the actual sequence of user actions?
- what states become visible after each action?
- where are the likely success, validation, or error outcomes?
- does the real UI behavior match the described requirement?

Stop once you have enough information to create a strong plan.

### Step 3 - Normalize the behavior

Break the behavior into the smallest useful scenarios.

Always identify:
- Preconditions
- Actor goal
- Candidate Tasks
- Candidate Questions
- Candidate Consequences

Do not turn everything into a Task.
If something is a read, consider a Question.
If something is a direct verification, consider Ensure / Consequence style.

### Step 4 - Render in the requested format

If `format=screenplay`:
- produce a Screenplay-oriented plan

If `format=gherkin`:
- produce:
  - a clear `Feature` title
  - optional short description
  - optional `Background`
  - `Scenario` or `Scenario Outline`
  - clean `Given / When / Then` wording

If `format=both`:
- produce:
  1. the Screenplay-oriented plan
  2. a Gherkin rendering of the same behavior

### Step 5 - Check architectural fit

Before finalizing, verify that:
- the Tasks are business-readable
- the Questions represent state reads
- the Consequences represent checks
- the plan does not leak low-level Playwright mechanics
- repeated pieces could later become reusable abstractions
- Gherkin steps stay behavioral rather than implementation-specific

### Step 6 - Show before inserting

Before writing any file:
1. Print the requested planning output.
2. Print assumptions or ambiguities.
3. Ask the user to confirm before inserting.

If the user asked only for a plan, do not write files unless explicitly requested.

---

## Preferred output formats

### For `format=screenplay`

#### Scenario
- title
- summary

#### Preconditions
- setup or assumptions

#### Actor
- who is performing the flow
- what the actor is trying to achieve

#### Candidate Tasks
- Task 1
- Task 2
- Task 3

#### Candidate Questions
- Question 1
- Question 2

#### Candidate Consequences
- check 1
- check 2

#### Notes
- ambiguity
- assumptions
- possible reuse opportunities

### For `format=gherkin`

```gherkin
Feature: ...
  ...

  Scenario: ...
    Given ...
    When ...
    Then ...
```

### For `format=both`

Produce:
1. the Screenplay-oriented plan
2. the matching Gherkin scenarios

---

## Reference expectations from this codebase

Before producing the final plan, inspect existing docs, tests, and framework files when available.

When in doubt:
- prefer actor-centered language
- prefer reusable Tasks
- prefer Questions for reads
- prefer Consequences for verification
- prefer plain business language in Gherkin
- keep the plan easy to turn into Python later
