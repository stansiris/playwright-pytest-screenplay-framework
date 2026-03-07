# Engine Flows (Composed from Implemented Tasks and Questions)

Engine flows are higher-level compositions of existing Screenplay Tasks and Questions.
They do not add new selectors.

Current executable coverage:
- BDD: golden-path purchase (`tests/features/golden_path.feature`) and login mirror (`tests/features/login.feature`)
- Direct pytest: login, inventory, product details, checkout info, checkout complete, and UI page suites

## 1) Login successfully

Compose:
- `OpenLoginPage()`
- `Login.with_credentials(username, password)`
- `WaitForInventoryPage()`

Verify:
- `OnInventoryPage()`
- `TextOf(AppShell.PAGE_TITLE) == "Products"`

## 2) Login expecting failure

Compose:
- `OpenLoginPage()`
- `Login.with_credentials(invalid_username, invalid_password)` or partial credentials (`with_username_only` / `with_password_only`)

Verify:
- `Ensure.that(LoginPage.LOGIN_ERROR_MESSAGE).to_contain_text(...)`
- `OnLoginPage()`
- optional cleanup: `DismissLoginError()`

## 3) Inventory cart operations

Compose:
- `AddProductToCart.named(item_name)`
- optional remove path: `RemoveProductFromCart.named(item_name)`

Verify:
- `CartBadgeCount() == expected_count`
- `Ensure.that(InventoryPage.inventory_item_action_button_for(item_name)).to_have_text(...)`

## 4) Product details behavior

Compose:
- `OpenProductDetails.named(item_name)` or `OpenProductDetailsById.with_id(id)`
- `ToggleProductDetailsCartAction()`
- optional: `ReturnToProducts()`

Verify:
- `CurrentUrl()` contains `inventory-item.html`
- `TextOf(ProductDetailsPage.PRODUCT_DETAILS_NAME)`
- cart state reflected via `CartBadgeCount()` and action button text

## 5) Checkout step-one validation

Compose:
- `GoToCart()`
- `ProceedToCheckout()`
- `WaitForCheckoutInfoPage()`
- `EnterCheckoutInformation.as_customer(...)`
- `ContinueCheckout()`

Verify:
- required-field errors via `Ensure.that(CheckoutInfoPage.CHECKOUT_INFO_ERROR_MESSAGE).to_contain_text(...)`
- dismiss path via `DismissCheckoutInfoError()`
- cancel path via `CancelCheckoutInfo()`

## 6) Checkout through completion

Compose:
- `BeginCheckout()` or (`GoToCart()` + `ProceedToCheckout()`)
- `ProvideCheckoutInformation.as_customer(...)`
- `CompleteCheckout()`
- `WaitForCheckoutCompletePage()`

Verify:
- completion text and visuals on `CheckoutCompletePage`
- `CartBadgeCount() == 0`

## 7) Return to inventory after checkout

Compose:
- `ReturnToProducts()`
- `WaitForInventoryPage()`

Verify:
- `OnInventoryPage()`
- `CartBadgeCount() == 0`

## 8) Logout and guarded direct URLs

Compose:
- `Logout()`
- direct URL tasks when logged out:
  - `OpenProductDetailsById.with_id(...)`
  - `OpenCheckoutCompletePage()`

Verify:
- `OnLoginPage()`
