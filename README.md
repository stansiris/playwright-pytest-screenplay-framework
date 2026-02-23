# Playwright + Pytest Screenplay Framework

A Python UI automation framework using **Playwright**, **pytest**, and the **Screenplay pattern**, with `pytest-bdd` as the primary behavior layer.

This project demonstrates disciplined domain modeling, reusable Tasks and Questions, and clean separation between business intent and UI mechanics.

---

# Setup

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m playwright install
pytest -q
```

---

# Architecture Philosophy

This framework follows these principles:

- **Screenplay is the core abstraction**  
  Tests and step definitions call reusable `Task` and `Question` objects.

- **Behavior-first design with pytest-bdd**  
  Gherkin scenarios describe behavior. Step definitions remain thin wrappers.

- **Tasks represent intent**  
  Not clicks. Not locators. Not UI mechanics.

- **Questions represent state verification**  
  Assertions are encapsulated in reusable query objects.

- **Clear page responsibility separation**  
  Each page defines only the Tasks and Questions it truly owns.

---

# SauceDemo Domain Model

The following Tasks and Questions define the complete vocabulary used to model the SauceDemo application.

All tests and Gherkin steps compose from these primitives.

---

## Login Page

### Tasks
- `Login.with_credentials(username, password)`

### Questions
- `LoginErrorMessage.text()` *(or `LoginErrorMessage.equals(expected)`)*
- `OnInventoryPage()`

---

## Inventory Page

### Tasks
- `SortInventory.by(option)`
- `OpenItemDetails.named(item_name)`
- `AddItem.named(item_name)`
- `RemoveItem.named(item_name)`
- `GoToCart()`

### Questions
- `InventorySortedBy(option)`
- `CartBadgeCountIs(n)`

---

## Inventory Item / Item Details Page

### Tasks
- `ReturnToProducts()`
- `AddItem.named(item_name)`
- `RemoveItem.named(item_name)`

### Questions
- `ItemName.is(expected)`
- `ItemDescription.contains(text)`
- `ItemPrice.is(expected_price)`

---

## Cart Page

### Tasks
- `ContinueShopping()`
- `ProceedToCheckout()`
- `RemoveItem.named(item_name)`
- `RemoveItems.named(item_names)`

### Questions
- `CartContains.items(item_names)`
- `CartItemCountIs(n)`
- `CartIsEmpty()`

---

## Checkout Step One (Information Page)

### Tasks
- `EnterCheckoutInformation(first_name, last_name, postal_code)`
- `ContinueCheckout()`
- `CancelCheckout()`

*(No page-specific Questions — use generic text/value/error assertions.)*

---

## Checkout Step Two (Overview Page)

### Tasks
- `FinishCheckout()`
- `CancelCheckout()`

### Questions
- `OverviewContains.items(item_names)`
- `PaymentInformationIs(text)`
- `ShippingInformationIs(text)`
- `TotalsMatchComputedSum()`

---

## Checkout Complete Page

### Tasks
- `ReturnHomeToInventory()`

*(Use generic assertions for confirmation text or visibility checks.)*

---

# Project Structure
```
screenplay/
│
├── core/ # Actor, Task, Interaction, Question, Target
├── abilities/ # Actor abilities (e.g., BrowseTheWeb)
├── interactions/ # Low-level UI actions (Click, Fill, NavigateTo)
├── tasks/ # Business-level Tasks
├── questions/ # Reusable Questions (assertions)
├── ui/ # Application-specific Targets/locators
│
tests/
├── features/ # Gherkin feature files
├── steps/ # pytest-bdd step definitions
├── test_*.py # Optional direct pytest + Screenplay tests
```

---

# Testing Modes

## 1️⃣ pytest-bdd + Screenplay (Primary)

- Feature files define behavior.
- Step definitions call Tasks and Questions.
- Business-readable scenarios with strong architecture.

Example:

```py
from pytest_bdd import when, parsers
from screenplay.tasks.login import Login

@when(parsers.parse('I log in with username "{username}" and password "{password}"'))
def login(actor, username, password):
    actor.attempts_to(Login.with_credentials(username, password))
```
## 2️⃣ Direct pytest + Screenplay

Useful for:

* Fast refactoring
* Engineering feedback
* Lower-level interaction testing

Example:
```py
def test_successful_login(actor):
    actor.attempts_to(
        Login.with_credentials("standard_user", "secret_sauce")
    )

    assert actor.asks_for(OnInventoryPage())
```
