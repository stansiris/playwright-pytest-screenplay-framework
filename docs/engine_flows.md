# Engine Flows (Composed from Implemented Tasks and Questions)

Engine flows are higher-level compositions of existing Screenplay Tasks and Questions.
They do not add new selectors.

The current checked-in BDD automation covers the golden-path purchase flow.
The additional flows below document supported compositions from the available
task/question API, even when they are not yet represented by a dedicated feature file.

## 1) Login successfully

Compose:
- `OpenSauceDemo.app()`
- `Login.with_credentials(username, password)`

Verify:
- `OnInventoryPage()`

## 2) Login expecting failure

Compose:
- `OpenSauceDemo.app()`
- `EnterUsername.as_(username)` (optional for missing-user case)
- `EnterPassword.as_(password)` (optional for missing-pass case)
- `ClickLogin()`

Verify:
- `TextOf(SauceDemo.LOGIN_ERROR_MESSAGE)`
- `OnLoginPage()`

## 3) Add multiple items and verify cart badge

Compose:
- `SortInventory.by(option)` (optional)
- `AddProductToCart.named(item_name)` for each item

Verify:
- `CartBadgeCount() == expected_count`

## 4) Checkout multiple items

Compose:
- `GoToCart()`
- `ProceedToCheckout()`
- `EnterCheckoutInformation.as_customer(first_name, last_name, postal_code)`
- `ContinueCheckout()`
- `CompleteCheckout()`

Verify:
- `TextsOf(SauceDemo.CHECKOUT_OVERVIEW_ITEM_NAMES)`
- `TextOf(SauceDemo.CHECKOUT_PAYMENT_INFO)`
- `TextOf(SauceDemo.CHECKOUT_SHIPPING_INFO)`
- `TotalsMatchComputedSum()`

## 5) Return to inventory after checkout

Compose:
- `ReturnToProducts()`

Verify:
- `OnInventoryPage()`
- `CartBadgeCount() == 0`

## 6) Alternative end-to-end with logout

Compose:
- `Login.with_credentials(...)`
- `AddProductToCart.named(...)`
- `BeginCheckout()`
- `ProvideCheckoutInformation.as_customer(...)`
- `CompleteCheckout()`
- `ReturnToProducts()`
- `Logout()`

Verify:
- `TextOf(SauceDemo.LOGIN_BUTTON) == "Login"`
