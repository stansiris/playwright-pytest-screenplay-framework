# SauceDemo Domain Model

This document is the source of truth for the automation language implemented in this repository.
App-specific names map to classes in `saucedemo/tasks` and `saucedemo/questions`.
Generic reusable questions live in `screenplay_core/questions`.

Current automated coverage includes:
- golden-path purchase scenario in `tests/features/golden_path.feature`
- login behavior BDD mirror scenarios in `tests/features/login.feature`
- direct pytest + Screenplay suites covering login, inventory, product details, checkout info, checkout complete, UI pages, and actor strictness

## Actor and Ability

- Actor fixture: `customer` in `tests/conftest.py`
- Ability: `BrowseTheWeb.using(page, base_url=base_url)`

## Task Model

### Entry and navigation
- `OpenSauceDemo.app()`
- `OpenLoginPage()`
- `OpenProductDetails.named(product_name)`
- `OpenProductDetailsById.with_id(product_id)`
- `OpenCheckoutCompletePage()`
- `GoToCart()`
- `ReturnToProducts()`
- `RefreshBrowser()`

### Login and session
- `Login.with_credentials(username, password)`
- `Login.with_username_only(username)`
- `Login.with_password_only(password)`
- `ClickLogin()`
- `DismissLoginError()`
- `Logout()`

### Inventory and product actions
- `SortInventory.by(option)`
- `AddProductToCart.named(product_name)`
- `RemoveProductFromCart.named(product_name)`
- `ToggleProductDetailsCartAction()`

### Checkout step one (information)
- `BeginCheckout()`
- `ProceedToCheckout()`
- `EnterCheckoutInformation.as_customer(first_name, last_name, postal_code)`
- `ContinueCheckout()`
- `ProvideCheckoutInformation.as_customer(first_name, last_name, postal_code)`
- `CancelCheckoutInfo()`
- `DismissCheckoutInfoError()`

### Checkout step two and completion
- `CompleteCheckout()`

### Synchronization helpers
- `WaitForInventoryPage()`
- `WaitForCheckoutInfoPage()`
- `WaitForCheckoutCompletePage()`

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

### Domain checks
- `CartBadgeCount()`
- `InventoryCount()`
- `TotalsMatchComputedSum()`

## Target Model

UI selectors are organized as `Target` objects by page and shared component:
- page targets in `saucedemo/ui/pages/*`
- shared targets in `saucedemo/ui/components/*`

Tasks, Questions, and tests/step definitions should reference these targets instead of inline selectors.
Detailed conventions and examples: `docs/ui_target_organization.md`.

## Usage in BDD

Feature files live under `tests/features`.
BDD step definitions in `tests/test_golden_path_bdd.py` and `tests/test_login_bdd.py` are thin wrappers that delegate to the Task and Question model above.
