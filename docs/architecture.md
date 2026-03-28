# Framework Architecture

This document is a deep-dive reference for the framework. It covers:

- the layered system architecture
- the core class hierarchy and dependencies
- how `Ensure` is implemented internally
- runtime execution sequences for each activity type
- architectural rules and the directory-to-responsibility map

---

## 1. Layered System Architecture

The framework is a strict 4-layer stack. Arrows show dependency direction (upper layers
depend on lower layers; lower layers never import from above).

```mermaid
flowchart TB
  subgraph TL["Test Layer — tests/"]
    SD["SauceDemo — test_*.py · features/ · conftest.py"]
    TH["Work Items — test_*.py · conftest.py"]
  end

  subgraph EL["Target Layer — examples/"]
    SDE["saucedemo/ — tasks · questions · ui/pages · ui/components"]
    THE["work_items/ — automation/tasks · automation/questions · automation/ui · app/"]
  end

  subgraph CL["Core — screenplay_core/"]
    CORE["core/ — Actor · Task · Interaction · Question · Consequence (pure Python)"]
    AB["playwright/ — Target · BrowseTheWeb · Ensure · interactions/ · questions/"]
    BI["http/ — CallTheApi"]
  end

  subgraph RT["Runtime"]
    PW["Playwright — browser automation"]
    HTTP["requests.Session — HTTP API calls"]
  end

  TL --> EL
  TL --> CL
  EL --> CL
  AB --> PW
  AB --> HTTP
```

| Layer | Responsibility |
|---|---|
| **Test layer** | Describes behavior — no `page`, `locator`, or `expect()` calls |
| **Example target layer** | App-specific vocabulary: Tasks, Questions, Targets, API clients |
| **Screenplay core** | Reusable building blocks split into `core/` (pure abstractions), `playwright/` (Playwright extension), and `http/` (HTTP extension) |
| **Runtime** | Playwright drives the browser; `requests` makes HTTP API calls |

---

## 2. Core Class Hierarchy

```mermaid
classDiagram
  class Activity {
    <<abstract>>
    +perform_as(actor) None
  }

  class Task {
    +perform_as(actor) None
    +perform_interactions(actor, *interactions) None
  }

  class Interaction {
    +perform_as(actor) None
  }

  class Consequence {
    +perform_as(actor) None
  }

  class Question {
    <<abstract>>
    +answered_by(actor)
  }

  class Actor {
    +name str
    +can(ability) Actor
    +ability_to(ability_class)
    +attempts_to(*activities Task|Consequence) None
    +_attempts_to_interactions(*interactions) None
    +asks_for(question)
  }

  class Target {
    +description str
    +locator_function Callable
    +resolve_for(actor) Locator
  }

  class BrowseTheWeb {
    +page Page
    +base_url str|None
    +using(page, base_url) BrowseTheWeb
  }

  class CallTheApi {
    +base_url str
    +session Session
    +at(base_url) CallTheApi
    +get(path) Response
    +post(path) Response
    +put(path) Response
    +patch(path) Response
    +delete(path) Response
    +close() None
  }

  class Ensure {
    +that(target) LocatorAssertions
  }

  class _EnsureTargetBuilder {
    +target Target
    +__getattr__(method_name) wrapper
  }

  class _EnsureCall {
    +target Target
    +method_name str
    +perform_as(actor) None
  }

  Activity <|-- Task
  Activity <|-- Interaction
  Activity <|-- Consequence
  Consequence <|-- _EnsureCall

  Actor --> Task : attempts_to
  Actor --> Consequence : attempts_to
  Actor --> Interaction : _attempts_to_interactions
  Actor --> Question : asks_for
  Actor "1" o-- "*" BrowseTheWeb : abilities
  Actor "1" o-- "*" CallTheApi : abilities

  Task --> Interaction : perform_interactions

  Target --> BrowseTheWeb : resolve_for
  Target --> Locator : returns

  Ensure ..> _EnsureTargetBuilder : builds
  _EnsureTargetBuilder ..> _EnsureCall : builds
  _EnsureCall --> Target : resolves
  _EnsureCall --> LocatorAssertions : delegates

  BrowseTheWeb --> Page : wraps
  CallTheApi --> Session : wraps
```

**Key points:**

- `Activity` is the abstract base. Everything the actor executes inherits from it.
- `Task` and `Interaction` both extend `Activity`; Tasks compose Interactions.
- `Consequence` extends `Activity`; `_EnsureCall` is the only built-in Consequence implementation.
- `Question` is separate from `Activity` — it returns a value rather than performing a side effect.
- An actor can hold multiple abilities. `ability_to()` resolves by exact class or base-class match.
- `_EnsureTargetBuilder` is an internal intermediate object; it is never used directly in tests.

---

## 3. The `Ensure` Implementation

`Ensure` is the most non-obvious part of the framework. Understanding it requires following
the construction chain before any actor is involved.

### Construction chain

```mermaid
sequenceDiagram
  participant Test as Test Function
  participant Ensure
  participant Builder as _EnsureTargetBuilder
  participant Call as _EnsureCall

  Test->>Ensure: Ensure.that(target)
  Ensure-->>Test: _EnsureTargetBuilder(target) [typed as LocatorAssertions]
  Test->>Builder: .to_be_visible()
  Builder->>Builder: __getattr__("to_be_visible")
  Builder-->>Test: _EnsureCall(target, "to_be_visible", args, kwargs)
```

`Ensure.that(target).to_be_visible()` is a two-step construction. The result is a
`_EnsureCall` object — a `Consequence` — that can be passed to `actor.attempts_to()`.

### Execution chain

```
actor.attempts_to(_EnsureCall)
  → _EnsureCall.perform_as(actor)
      ↓
  1. locator = target.resolve_for(actor)       # BrowseTheWeb.page → Playwright Locator
  2. assertion = expect(locator)               # Playwright assertion factory
  3. method = getattr(assertion, method_name)  # e.g. to_be_visible
  4. method(*args, **kwargs)                   # execute; raises on failure
```

### Why the cast to `LocatorAssertions`

`Ensure.that()` returns `_EnsureTargetBuilder` but declares its return type as
`LocatorAssertions`. This is a deliberate lie to the type checker. It lets IDEs offer full
Playwright assertion autocompletion (`.to_be_visible()`, `.to_have_text()`, etc.) while the
actual runtime object is the dynamic `_EnsureTargetBuilder`. The pattern is a pragmatic
trade-off: dynamic dispatch at runtime, static autocomplete in the IDE.

---

## 4. Runtime Sequences

### 4.1 Task and Interaction

```mermaid
sequenceDiagram
  participant Test as Test Function
  participant A as Actor
  participant DomainTask as Domain Task
  participant Interaction
  participant Target
  participant BrowseTheWeb
  participant Playwright as Playwright Page

  Test->>A: attempts_to(Task)
  A->>DomainTask: perform_as(actor)
  opt Task composes nested Tasks or Consequences
    DomainTask->>A: attempts_to(Task/Consequence)
    A-->>DomainTask: done
  end
  DomainTask->>A: perform_interactions(actor, Click/Fill/...)
  A->>Interaction: perform_as(actor)
  Interaction->>Target: resolve_for(actor)
  Target->>BrowseTheWeb: actor.ability_to(BrowseTheWeb)
  BrowseTheWeb-->>Target: page
  Target-->>Interaction: Locator
  Interaction->>Playwright: click / fill / navigate / ...
  Playwright-->>Interaction: done
  Interaction-->>A: done
  A-->>Test: done
```

### 4.2 Question

```mermaid
sequenceDiagram
  participant Test as Test Function
  participant A as Actor
  participant Question
  participant Target
  participant BrowseTheWeb
  participant Playwright as Playwright Page

  Test->>A: asks_for(Question)
  A->>Question: answered_by(actor)
  opt Question reads a Target
    Question->>Target: resolve_for(actor)
    Target->>BrowseTheWeb: actor.ability_to(BrowseTheWeb)
    BrowseTheWeb-->>Target: page
    Target-->>Question: Locator
  end
  Question->>Playwright: read text / url / visibility / ...
  Playwright-->>Question: raw value
  Question-->>A: computed answer
  A-->>Test: answer
```

### 4.3 Ensure Consequence

```mermaid
sequenceDiagram
  participant Test as Test Function
  participant Ensure
  participant A as Actor
  participant EnsureCall as _EnsureCall
  participant Target
  participant Playwright as expect(locator)

  Test->>Ensure: Ensure.that(Target).to_be_visible()
  Ensure-->>Test: _EnsureCall
  Test->>A: attempts_to(_EnsureCall)
  A->>EnsureCall: perform_as(actor)
  EnsureCall->>Target: resolve_for(actor)
  Target-->>EnsureCall: Locator
  EnsureCall->>Playwright: expect(locator).to_be_visible()
  Playwright-->>EnsureCall: pass / AssertionError
  EnsureCall-->>A: done
  A-->>Test: done
```

### 4.4 API Task with `CallTheApi`

```mermaid
sequenceDiagram
  participant Test as Test Function
  participant A as API Actor
  participant ApiTask as API Task
  participant CallTheApi
  participant HTTP as requests.Session

  Test->>A: attempts_to(ApiTask)
  A->>ApiTask: perform_as(actor)
  ApiTask->>CallTheApi: actor.ability_to(CallTheApi)
  CallTheApi-->>ApiTask: CallTheApi instance
  ApiTask->>HTTP: session.post / get / put / delete
  HTTP-->>ApiTask: Response
  ApiTask->>ApiTask: store result (self.result)
  ApiTask-->>A: done
  A-->>Test: done
  Test->>Test: assert task.result.status_code == 201
```

The API actor uses `CallTheApi` instead of `BrowseTheWeb`. There is no `Target` or
Playwright involvement. API Tasks store their response in `self.result` so tests can
inspect status codes and payloads after `attempts_to()` returns.

### 4.5 Hybrid test: two actors

```mermaid
sequenceDiagram
  participant Test as Test Function
  participant ApiActor as API Actor (CallTheApi)
  participant UiActor as UI Actor (BrowseTheWeb)
  participant Server as Work Items Server

  Test->>ApiActor: attempts_to(LoginToWorkItemsApi, CreateWorkItemViaApi)
  ApiActor->>Server: POST /api/login, POST /api/work-items
  Server-->>ApiActor: 200, 201
  ApiActor-->>Test: done
  Test->>Test: assert create_work_item.result.status_code == 201

  Test->>UiActor: attempts_to(OpenWorkItems, LoginToWorkItems)
  UiActor->>Server: browser GET /login, POST /login
  Server-->>UiActor: 200

  Test->>UiActor: attempts_to(Ensure.that(task_item).to_be_visible())
  UiActor->>Server: browser renders /work-items
  Server-->>UiActor: page with task visible
  UiActor-->>Test: done
```

Two independent actors — one with `CallTheApi`, one with `BrowseTheWeb` — operate against
the same server in a single test. They share no state; the test coordinates them.

---

## 5. Architectural Rules

- **Test files stay thin.** Tests express behavior using Tasks, Consequences, and Questions.
  No `page`, `locator`, or `expect()` calls appear in test code.
- **`actor.attempts_to()` accepts only `Task | Consequence`.** Passing an `Interaction`
  directly raises `TypeError`. This is enforced at runtime in `Actor.attempts_to()`.
- **Interactions live inside Tasks.** They are dispatched through
  `Task.perform_interactions()` → `Actor._attempts_to_interactions()`, never called
  directly by tests.
- **Target resolution flows through an Ability.** `Target.resolve_for(actor)` always goes
  through `actor.ability_to(BrowseTheWeb)`. There is no direct `page` access outside of
  Interactions and `BrowseTheWeb`.
- **Tasks may compose other Tasks or Consequences** by calling `actor.attempts_to(...)`
  inside `perform_as()`. This is the only supported nesting pattern.
- **Questions return values; they do not assert.** Use `Ensure` for Playwright-backed UI
  assertions. Use `Question` + `assert` for value-based checks.

---

## 6. Directory-to-Responsibility Map

| Directory | Responsibility |
|---|---|
| `screenplay_core/core` | Runtime-agnostic abstractions — zero external dependencies: `Activity`, `Task`, `Interaction`, `Consequence`, `Question`, `Actor`. |
| `screenplay_core/playwright` | Playwright extension: `Target` (locator recipe), `BrowseTheWeb` (page wrapper), `Ensure` (`expect()` DSL adapter). |
| `screenplay_core/playwright/interactions` | Reusable low-level browser actions: `Click`, `Fill`, `NavigateTo`, `PressKey`, `ScrollIntoView`, etc. |
| `screenplay_core/playwright/questions` | Generic read-model queries reusable across domains: `TextOf`, `CurrentUrl`, `IsVisible`, `AttributeOf`, etc. |
| `screenplay_core/http` | HTTP extension: `CallTheApi` (requests session wrapper). |
| `examples/saucedemo/ui/pages` | Page-level Target catalogs for SauceDemo (one class per page). |
| `examples/saucedemo/ui/components` | Shared Targets used across multiple SauceDemo pages. |
| `examples/saucedemo/tasks` | SauceDemo business Tasks: `Login`, `Logout`, `AddProductToCart`, `CompleteCheckout`, etc. |
| `examples/saucedemo/questions` | SauceDemo Questions: inventory state, totals, login page state. |
| `examples/work_items/app` | Flask app-under-test: routes, SQLite db, seed data. |
| `examples/work_items/automation/ui` | `WorkItemsTargets` — all `data-testid` and `data-work-item-id` selectors for Work Items. |
| `examples/work_items/automation/tasks` | Work Items UI Tasks (`CreateWorkItem`, `EditWorkItem`, `DeleteWorkItem`, …) and API Tasks (`CreateWorkItemViaApi`, `LoginToWorkItemsApi`, …). |
| `examples/work_items/automation/questions` | Work Items Questions: work item visibility, completion state, flash messages, API-based lookups. |
| `examples/work_items/automation/api` | Work Items API helper layer built on top of `CallTheApi`. |
| `tests/conftest.py` | Shared browser launch option overrides (applies to all test suites). |
| `tests/saucedemo/conftest.py` | `customer` actor fixture and `base_url` normalization for SauceDemo. |
| `tests/saucedemo/features` | Gherkin feature files for SauceDemo pytest-bdd suites. |
| `tests/saucedemo/test_*.py` | SauceDemo pytest and pytest-bdd test suites. |
| `tests/work_items/conftest.py` | Work Items session-scoped server lifecycle, per-test data reset, and actor fixtures (`work_items_customer`, `work_items_logged_in_customer`, `work_items_api_actor`). |
| `tests/work_items/features` | Gherkin feature files for Work Items pytest-bdd suites. |
| `tests/work_items/test_*.py` | Work Items UI, API, hybrid, and BDD test suites. |
