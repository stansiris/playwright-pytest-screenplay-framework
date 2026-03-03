# ToDo

## Existing

- [smoke] Keep the current golden path E2E as the build smoke test.

## Login Page (`https://www.saucedemo.com/`)

- [smoke] Valid login reaches inventory page.
- [integration] Invalid credentials show expected error message.
- [integration] Missing username/password validation cases.
- [integration] Dismiss login error behavior (`DismissLoginError`).

## Inventory Page (`/inventory.html`)

- [integration] Add/remove item updates cart badge correctly.
- [integration] Sort behavior checks (`SortInventory.by(...)`) including invalid option handling.
- [integration] Overlapping product-name locator test (`"Sauce Labs Bike"` vs `"Sauce Labs Bike Light"`).
- [integration] Harden `OnInventoryPage` to require exact path plus visible inventory container.
- [integration] Add negative-path `OnInventoryPage` tests (query contains `inventory.html` but page is not inventory).

## Product Details Page (`/inventory-item.html?id=<id>`)

- [integration] Navigate from inventory to details and verify name/price/description consistency.
- [integration] Add/remove from details page updates cart badge.
- [integration] Back-to-products returns to inventory list state.

## Cart Page (`/cart.html`)

- [integration] Cart contains expected items and count.
- [integration] Remove item from cart updates list and badge.
- [integration] Cart contents persist across refresh/navigation.

## Checkout Info Page (`/checkout-step-one.html`)

- [integration] Required-field validation for first/last/postal code.
- [integration] Valid checkout information proceeds to overview.
- [integration] `EnterCheckoutInformation` and `ProvideCheckoutInformation` task coverage.

## Checkout Overview Page (`/checkout-step-two.html`)

- [integration] Overview items match cart items.
- [integration] Payment/shipping info assertions.
- [integration] Totals math consistency with Decimal parser.
- [integration] Totals edge-case test (`0.10 + 0.20`) for precision safety.

## Checkout Complete Page (`/checkout-complete.html`)

- [integration] Checkout confirmation is visible after finish.
- [integration] Cart is reset after returning to inventory.
- [integration] Refresh/back behavior does not recreate stale checkout state.

## Cross-Cutting Framework Coverage

- [integration] Use `WaitUntilVisible.for_(SauceDemo.LOGIN_BUTTON)` in `OpenLoginPage` for timeout consistency.
- [integration] Add explicit tests for `Logout()`, `BeginCheckout()`, and other currently untested task compositions.
