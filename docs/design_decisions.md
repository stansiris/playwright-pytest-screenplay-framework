# Design Decisions

## Why checkout step one has no page-specific Questions

Checkout step one is an input form without business calculations.
Generic Questions (`TextOf`, `AttributeOf`, `IsVisible`) are enough.

## Why `TotalsMatchComputedSum` exists

Checkout overview contains business logic (subtotal + tax = total).
A dedicated Question keeps that calculation in one place and avoids duplicated assertions.

## Why `AddProductToCart` is context-aware

Tests should pass product names, not selector details.
`AddProductToCart.named(product_name)` resolves the right button from centralized targets.

## Why runtime settings are pytest-driven

Portfolio and CI runs need consistent, reproducible defaults without code edits.
Defaults live in `pytest.ini` (`base_url` and `--browser` via `addopts`) and can be overridden per run via CLI flags.

