# UI Target Organization Guide

This document explains how UI targets are organized in the SauceDemo domain after the locator refactor.

## Why this structure exists

The project now separates targets by ownership:
- `pages`: targets that belong to a single page/screen
- `components`: targets shared across multiple pages

This keeps selector changes localized and avoids a single monolithic target file.

## Directory layout

```text
saucedemo/ui/
|-- pages/
|   |-- login_page.py
|   |-- inventory_page.py
|   |-- product_details_page.py
|   |-- cart_page.py
|   |-- checkout_info_page.py
|   |-- checkout_overview_page.py
|   `-- checkout_complete_page.py
`-- components/
    |-- app_shell.py
    `-- back_navigation.py
```

## Target catalogs

### Page catalogs

- `LoginPage`: login form, error banner
- `InventoryPage`: inventory grid, sort controls, product-level dynamic target factories
- `ProductDetailsPage`: details view content and action button
- `CartPage`: cart item rows, checkout button
- `CheckoutInfoPage`: checkout step one form and validation controls
- `CheckoutOverviewPage`: checkout step two summary and finish action
- `CheckoutCompletePage`: confirmation UI

### Component catalogs

- `AppShell`: global/shared shell controls (`PAGE_TITLE`, `MENU_BUTTON`, `LOGOUT_LINK`, `SHOPPING_CART_LINK`, `SHOPPING_CART_BADGE`)
- `BackNavigation`: shared back navigation (`BACK_TO_PRODUCTS`)

## Usage conventions

Import the narrowest catalog that owns the target you need.
`__init__.py` files are intentionally empty, so use direct module imports rather than package-level re-exports.

Task example:

```python
from saucedemo.ui.pages.login_page import LoginPage
from screenplay_core.interactions.fill import Fill

actor.attempts_to(
    Fill(LoginPage.LOGIN_USERNAME, username),
    Fill(LoginPage.LOGIN_PASSWORD, password),
)
```

Question example:

```python
from saucedemo.ui.components.app_shell import AppShell

badge = AppShell.SHOPPING_CART_BADGE.resolve_for(actor)
```

Test example:

```python
from saucedemo.ui.pages.checkout_overview_page import CheckoutOverviewPage

customer.expect(CheckoutOverviewPage.CHECKOUT_TOTAL).to_contain_text("Total:")
```

## Placement rules for new targets

1. Put a target in `pages/*` if it is specific to one page.
2. Put a target in `components/*` if reused across pages.
3. Keep dynamic target factories on the page that owns the domain concept.
4. Avoid inline selectors in tasks, questions, and tests.

## Naming conventions

- Module names: page modules use `<name>_page.py`; component modules use descriptive names (`app_shell.py`)
- Catalog classes: `PascalCase` (`LoginPage`, `AppShell`)
- Target constants: `UPPER_SNAKE_CASE`
- Dynamic target builders: intent-oriented names (`add_to_cart_button_for`)

## Change workflow

1. Add/adjust the target in its owning page/component module.
2. Update tasks/questions to use the target.
3. Update tests only when behavior or wording changes.
4. Run:
   - `python -m ruff check .`
   - `python -m black .`
   - `pytest -q`

## Migration note

The legacy single catalog (`SauceDemo` in `saucedemo/ui/saucedemo.py`) has been removed.
Use page/component catalogs directly in all new code.
