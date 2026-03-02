# ToDo

- Add a regression test for overlapping inventory names (for example, `"Sauce Labs Bike"` vs `"Sauce Labs Bike Light"`) to ensure product selection stays exact.
- Update `TotalsMatchComputedSum` to use `Decimal` instead of `float` for money calculations.
- Add a checkout-specific price target (for example, `CHECKOUT_OVERVIEW_ITEM_PRICES`) and use it in totals assertions.
- Harden `OnInventoryPage` to require exact inventory path and visible inventory container.
- Use `WaitUntilVisible.for_(SauceDemo.LOGIN_BUTTON)` inside `OpenLoginPage` for timeout consistency.
- Add a totals edge-case test covering decimal precision values (for example, `0.10 + 0.20`).
- Add negative-path tests for `OnInventoryPage` (for example, URL contains `inventory.html` in query but is not inventory page).
- Add coverage for currently untested flows: `SortInventory.by(...)` (valid/invalid), `Logout()`, and checkout helper tasks.
