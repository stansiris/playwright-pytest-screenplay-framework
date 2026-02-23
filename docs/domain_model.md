# SauceDemo Domain Model

This document is the source of truth for the automation language implemented in this repository.
All names below map to real classes in `screenplay/tasks` and `screenplay/questions`.

## Actor and Ability

- Actor: `Actor("Customer")` in `tests/conftest.py`
- Ability: `BrowseTheWeb.using(page)`

## Page-Level Task Model

### Entry
- `OpenSauceDemo.app()`

### Login
- `Login.with_credentials(username, password)`
- `EnterUsername.as_(username)`
- `EnterPassword.as_(password)`
- `ClickLogin()`
- `DismissLoginError()`

### Inventory
- `SortInventory.by(option)`
- `AddProductToCart.named(product_name)`
- `GoToCart()`

### Cart
- `GoToCart()`
- `ProceedToCheckout()`

### Checkout Information (step one)
- `EnterCheckoutInformation.as_customer(first_name, last_name, postal_code)`
- `ContinueCheckout()`

### Checkout Overview (step two)
- `CompleteCheckout()`

### Checkout Complete
- `ReturnToProducts()`

### Supporting/POC Flows
- `BeginCheckout()`
- `ProvideCheckoutInformation.as_customer(first_name, last_name, postal_code)`
- `Logout()`

## Question Model

### Navigation and page state
- `OnLoginPage()`
- `OnInventoryPage()`
- `CurrentUrl()`

### Visibility and focus
- `IsVisible(target)`
- `IsFocused(target)`
- `FocusIndicatorVisible()`

### Text and attributes
- `TextOf(target)`
- `TextsOf(target)`
- `AttributeOf(target, attribute_name)`

### Cart and checkout business assertions
- `CartBadgeCount()`
- `TotalsMatchComputedSum()`

## Target Model

All UI selectors are centralized in `screenplay/ui/saucedemo.py` as `Target` objects.
Tasks and Questions must reference these targets instead of inline selectors.

## Usage in BDD

Feature files live under `tests/features`.
Step definitions in `tests/steps` are thin wrappers that delegate to the Task and Question model above.
