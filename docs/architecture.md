# Framework Architecture (Hierarchy + Dependencies)

This document is a deep-dive architecture map for the framework.
It shows:
- class hierarchy (inheritance model)
- class dependencies (who uses whom)
- runtime execution flow from feature/test to browser

## 1. System Architecture (Layered View)

```mermaid
flowchart TB
  subgraph Behavior["Behavior and Test Entry Layer"]
    F[tests/features/*.feature]
    BDD[tests/test_*_bdd.py]
    PYT[tests/test_*.py]
    CONF[tests/conftest.py]
  end

  subgraph Domain["Domain Layer: saucedemo/"]
    ST[saucedemo/tasks/*]
    SQ[saucedemo/questions/*]
    SUI[saucedemo/ui/saucedemo.py]
    SRC[saucedemo/config/runtime.py]
  end

  subgraph Core["Reusable Screenplay Layer: screenplay_core/"]
    CCORE[core/*]
    CAB[abilities/browse_the_web.py]
    CINT[interactions/*]
    CQUE[questions/*]
  end

  PW[Playwright Sync API]

  F --> BDD
  BDD --> ST
  BDD --> SQ
  PYT --> ST
  PYT --> SQ
  CONF --> SRC
  CONF --> CAB
  CONF --> PW

  ST --> SUI
  SQ --> SUI
  ST --> CINT
  SQ --> CQUE
  ST --> CCORE
  SQ --> CCORE
  SUI --> CCORE

  CINT --> CCORE
  CQUE --> CCORE
  CCORE --> CAB
  CAB --> PW
```

## 2. Core Class Hierarchy

```mermaid
classDiagram
  class Activity {
    <<abstract>>
    +perform_as(actor) None
  }

  class Task
  class Interaction

  class Question {
    <<abstract>>
    +answered_by(actor)
  }

  class Actor {
    +name str
    +can(ability) Actor
    +ability_to(ability_class)
    +attempts_to(*activities) None
    +asks_for(question)
    +expect(target) LocatorAssertions
  }

  class Target {
    +description str
    +locator_function(page) Locator
    +resolve_for(actor) Locator
  }

  class BrowseTheWeb {
    +page
    +base_url optional str
    +default_timeout_ms int
    +using(page, base_url, default_timeout_ms) BrowseTheWeb
  }

  class Page
  class Locator

  Activity <|-- Task
  Activity <|-- Interaction
  Actor --> Activity : performs
  Actor --> Question : asks
  Actor --> Target : expect(target)
  Actor "1" o-- "*" BrowseTheWeb : abilities
  Target --> BrowseTheWeb : resolve_for(actor)
  BrowseTheWeb --> Page : wraps
  Target --> Locator : returns
```

## 3. Reusable Implementation Classes (screenplay_core)

### 3.1 Interaction Hierarchy

```mermaid
classDiagram
  class Interaction
  class Click
  class Fill
  class Clear
  class Focus
  class NavigateTo
  class PressKey
  class RefreshPage
  class ScrollIntoView
  class SelectByValue
  class WaitUntilVisible
  class WaitUntilHidden

  Interaction <|-- Click
  Interaction <|-- Fill
  Interaction <|-- Clear
  Interaction <|-- Focus
  Interaction <|-- NavigateTo
  Interaction <|-- PressKey
  Interaction <|-- RefreshPage
  Interaction <|-- ScrollIntoView
  Interaction <|-- SelectByValue
  Interaction <|-- WaitUntilVisible
  Interaction <|-- WaitUntilHidden
```

### 3.2 Generic Question Hierarchy

```mermaid
classDiagram
  class Question
  class AttributeOf
  class CurrentUrl
  class FocusIndicatorVisible
  class IsFocused
  class IsVisible
  class TextOf
  class TextsOf

  Question <|-- AttributeOf
  Question <|-- CurrentUrl
  Question <|-- FocusIndicatorVisible
  Question <|-- IsFocused
  Question <|-- IsVisible
  Question <|-- TextOf
  Question <|-- TextsOf
```

## 4. Domain Class Hierarchy (saucedemo)

```mermaid
classDiagram
  class Task
  class Question
  class SauceDemo
  class Target
  class Click
  class Fill
  class NavigateTo

  class AddProductToCart
  class BeginCheckout
  class ClickLogin
  class CompleteCheckout
  class ContinueCheckout
  class DismissLoginError
  class EnterCheckoutInformation
  class GoToCart
  class Login
  class Logout
  class OpenLoginPage
  class OpenSauceDemo
  class ProceedToCheckout
  class ProvideCheckoutInformation
  class ReturnToProducts
  class SortInventory

  class CartBadgeCount
  class OnInventoryPage
  class OnLoginPage
  class TotalsMatchComputedSum

  Task <|-- AddProductToCart
  Task <|-- BeginCheckout
  Task <|-- ClickLogin
  Task <|-- CompleteCheckout
  Task <|-- ContinueCheckout
  Task <|-- DismissLoginError
  Task <|-- EnterCheckoutInformation
  Task <|-- GoToCart
  Task <|-- Login
  Task <|-- Logout
  Task <|-- OpenLoginPage
  Task <|-- OpenSauceDemo
  Task <|-- ProceedToCheckout
  Task <|-- ProvideCheckoutInformation
  Task <|-- ReturnToProducts
  Task <|-- SortInventory

  Question <|-- CartBadgeCount
  Question <|-- OnInventoryPage
  Question <|-- OnLoginPage
  Question <|-- TotalsMatchComputedSum

  SauceDemo --> Target : static targets
  AddProductToCart --> Click : uses
  ClickLogin --> Click : uses
  ContinueCheckout --> Click : uses
  CompleteCheckout --> Click : uses
  DismissLoginError --> Click : uses
  GoToCart --> Click : uses
  Logout --> Click : uses
  ProceedToCheckout --> Click : uses
  ReturnToProducts --> Click : uses
  Login --> Fill : uses
  OpenSauceDemo --> NavigateTo : uses
  Login --> ClickLogin : composes
  BeginCheckout --> GoToCart : composes
  BeginCheckout --> ProceedToCheckout : composes
  ProvideCheckoutInformation --> EnterCheckoutInformation : composes
  ProvideCheckoutInformation --> ContinueCheckout : composes
```

## 5. Module Dependency Graph

This graph focuses on import direction and responsibility boundaries.

```mermaid
flowchart LR
  subgraph Tests["tests/"]
    TCONF[conftest.py]
    TBDD[test_*_bdd.py]
    TPY[test_*.py]
  end

  subgraph Sauce["saucedemo/"]
    SCONF[config/runtime.py]
    STASK[tasks/*]
    SQUEST[questions/*]
    SUI[ui/saucedemo.py]
  end

  subgraph Core["screenplay_core/"]
    CACT[core/activity.py]
    CACTOR[core/actor.py]
    CTASK[core/task.py]
    CINTER[core/interaction.py]
    CQUEST[core/question.py]
    CTARGET[core/target.py]
    CABIL[abilities/browse_the_web.py]
    CINT[interactions/*]
    CQUE[questions/*]
    CTIME[interactions/_timeouts.py]
  end

  PWSYNC[playwright.sync_api]

  TBDD --> STASK
  TBDD --> SQUEST
  TPY --> STASK
  TPY --> SQUEST
  TCONF --> SCONF
  TCONF --> CABIL
  TCONF --> CACTOR
  TCONF --> PWSYNC

  STASK --> CTASK
  STASK --> CINT
  STASK --> SUI
  STASK --> CABIL
  STASK --> CACTOR

  SQUEST --> CQUEST
  SQUEST --> CQUE
  SQUEST --> SUI
  SQUEST --> CABIL
  SQUEST --> CACTOR

  SUI --> CTARGET

  CTASK --> CACT
  CINTER --> CACT
  CACTOR --> CACT
  CACTOR --> CQUEST
  CACTOR --> CTARGET
  CACTOR --> PWSYNC
  CTARGET --> CABIL
  CTARGET --> PWSYNC
  CINT --> CINTER
  CINT --> CTARGET
  CINT --> CABIL
  CINT --> CTIME
  CQUE --> CQUEST
  CQUE --> CTARGET
  CQUE --> CABIL
  CABIL --> PWSYNC
```

## 6. Runtime Sequence (How a Step Executes)

### 6.1 Task + Interaction Path

```mermaid
sequenceDiagram
  participant TestStep as "Step/Test Function"
  participant ScreenActor as "Actor"
  participant DomainTask as "Domain Task"
  participant UiInteraction as "Interaction"
  participant UiTarget as "Target"
  participant WebAbility as "BrowseTheWeb"
  participant PWRuntime as "Playwright Page/Locator"

  TestStep->>ScreenActor: attempts_to(Task)
  ScreenActor->>DomainTask: perform_as(actor)
  DomainTask->>ScreenActor: attempts_to(Interaction...)
  ScreenActor->>UiInteraction: perform_as(actor)
  UiInteraction->>UiTarget: resolve_for(actor)
  UiTarget->>WebAbility: actor.ability_to(BrowseTheWeb)
  WebAbility-->>UiTarget: page
  UiTarget-->>UiInteraction: Locator
  UiInteraction->>PWRuntime: click/fill/wait_for/etc.
  PWRuntime-->>UiInteraction: success/failure
  UiInteraction-->>ScreenActor: done
  ScreenActor-->>TestStep: done
```

### 6.2 Question Path

```mermaid
sequenceDiagram
  participant TestStep as "Step/Test Function"
  participant ScreenActor as "Actor"
  participant DomainQuestion as "Domain/Generic Question"
  participant UiTarget as "Target"
  participant WebAbility as "BrowseTheWeb"
  participant PWRuntime as "Playwright Page/Locator"

  TestStep->>ScreenActor: asks_for(Question)
  ScreenActor->>DomainQuestion: answered_by(actor)
  DomainQuestion->>UiTarget: resolve_for(actor) (optional)
  UiTarget->>WebAbility: actor.ability_to(BrowseTheWeb)
  WebAbility-->>UiTarget: page
  DomainQuestion->>PWRuntime: read url/text/visibility
  PWRuntime-->>DomainQuestion: raw value
  DomainQuestion-->>ScreenActor: computed answer
  ScreenActor-->>TestStep: answer
```

## 7. Timeout and Assertion Architecture

Two wait/assertion paths are intentionally supported:

1. Interaction wait path:
- `WaitUntilVisible` / `WaitUntilHidden`
- timeout resolved via `screenplay_core/interactions/_timeouts.py`
- source of default timeout: `BrowseTheWeb.default_timeout_ms`

2. Playwright assertion path:
- `Actor.expect(Target)` returns Playwright locator assertions
- global default assertion timeout is set in `tests/conftest.py` using `expect.set_options(timeout=runtime_settings.default_timeout_ms)`
- any assertion can still override timeout explicitly

## 8. Architectural Rules (Current Conventions)

- Steps in `tests/test_*.py` should stay thin and delegate behavior to Tasks/Questions.
- Tasks should express user intent and compose reusable interactions/tasks.
- Questions should read state or compute business checks, then return values.
- Selectors live in one place: `saucedemo/ui/saucedemo.py`.
- `Target` resolution must flow through actor ability (`BrowseTheWeb`) to keep browser access centralized.

## 9. Directory-to-Responsibility Map

| Directory | Responsibility |
| --- | --- |
| `screenplay_core/core` | Actor orchestration and base abstractions (`Activity`, `Task`, `Interaction`, `Question`, `Target`). |
| `screenplay_core/abilities` | External system capability wrapper (`BrowseTheWeb`). |
| `screenplay_core/interactions` | Reusable low-level actions against Playwright locators/pages. |
| `screenplay_core/questions` | Generic read-model queries reusable across domains. |
| `saucedemo/ui` | Domain target catalog and dynamic target factories. |
| `saucedemo/tasks` | Domain intent operations and composed workflows. |
| `saucedemo/questions` | Domain-specific assertions/state checks. |
| `tests/features` | Business-readable behavior specs (Gherkin). |
| `tests/test_*.py` | Thin BDD adapters plus direct pytest + Screenplay suites. |
| `tests/conftest.py` | Runtime wiring: actor fixture, browser defaults, assertion timeout defaults. |


