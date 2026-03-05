# Design Decisions

## Why checkout step one has no page-specific Questions

Checkout step one is an input form without business calculations.
Generic Questions (`TextOf`, `AttributeOf`, `IsVisible`) are enough.

## Why `TotalsMatchComputedSum` exists

Checkout overview contains business logic (subtotal + tax = total).
A dedicated Question keeps that calculation in one place and avoids duplicated assertions.

## Why `AddProductToCart` is context-aware

Tests should pass product names, not selector details.
`AddProductToCart.named(product_name)` resolves the right button from page-level targets.

## Why targets are split into `pages` and `components`

The original single target catalog became harder to navigate as coverage grew.
Splitting targets by page ownership improves maintainability:
- page-specific selectors stay with their page vocabulary
- shared controls (`menu`, `cart`, `back`) stay in reusable component catalogs
- selector changes are isolated to the owner module instead of a global file

This keeps Tasks and Questions readable while reducing cross-page coupling.

## Why runtime settings are pytest-driven

Portfolio and CI runs need consistent, reproducible defaults without code edits.
Defaults live in `pytest.ini` (`base_url` and reporting/trace behavior), and browser selection can be overridden per run via CLI flags.

