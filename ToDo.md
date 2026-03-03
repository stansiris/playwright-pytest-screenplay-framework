# ToDo

## Coverage Snapshot (Implemented)

- [done] BDD flows for golden path and login mirror.
- [done] Direct pytest integration suites for login, inventory, product details, checkout info, and checkout complete.
- [done] UI page suites for login, inventory, product details, cart, checkout info, checkout overview, and checkout complete.

## Remaining High-Value Gaps

### Inventory Page

- [integration] Add invalid sort-option handling test (`SortInventory.by(...)` negative path).
- [integration] Add explicit overlapping product-name locator regression test (`"Sauce Labs Bike"` vs `"Sauce Labs Bike Light"`).
- [integration] Harden `OnInventoryPage` to require exact path plus visible inventory container.
- [integration] Add negative-path `OnInventoryPage` tests (query contains `inventory.html` but page is not inventory).

### Cart Page

- [integration] Remove item from cart updates both list and badge.
- [integration] Cart contents persist across refresh/navigation.
- [ui] Empty cart state coverage for expected controls and layout.

### Checkout Overview Page

- [integration] Add dedicated non-BDD checkout-overview totals test using `TotalsMatchComputedSum`.
- [integration] Add totals precision edge-case coverage (`0.10 + 0.20`) for parser/rounding safety.

### Cross-Cutting Framework Coverage

- [integration] Use `WaitUntilVisible.for_(SauceDemo.LOGIN_BUTTON)` in `OpenLoginPage` for timeout consistency.
- [integration] Add explicit task-level test for `DismissLoginError()`.
