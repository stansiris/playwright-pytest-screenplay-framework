# Engine-Layer Business Flows (Composed from Tasks + Questions)

> Engine flows are higher-level compositions of Screenplay Tasks.
> They should NOT introduce new locators.
> They may include lightweight verification using existing Questions.

---

## Auth Flows

### 1) `LoginSuccessfully(username, password)`
**Compose**
- `Login.with_credentials(username, password)`
**Verify (optional)**
- `OnInventoryPage()`

### 2) `LoginExpectingFailure(username, password, expected_error)`
**Compose**
- `Login.with_credentials(username, password)`
**Verify**
- `LoginErrorMessage.equals(expected_error)`

---

## Inventory Flows

### 3) `AddItemsFromInventory(item_names)`
**Compose**
- `AddItem.named(item)` for each item in `item_names`
**Verify (optional)**
- `CartBadgeCountIs(len(item_names))`

### 4) `RemoveItemsFromInventory(item_names)`
**Compose**
- `RemoveItem.named(item)` for each item in `item_names`
**Verify (optional)**
- `CartBadgeCountIs(0)` *(or expected count)*

### 5) `SortInventoryAndVerify(option)`
**Compose**
- `SortInventory.by(option)`
**Verify**
- `InventorySortedBy(option)`

### 6) `OpenItemAndValidateDetails(item_name, expected_name=None, expected_price=None, description_contains=None)`
**Compose**
- `OpenItemDetails.named(item_name)`
**Verify (optional, any combination)**
- `ItemName.is(expected_name)`
- `ItemPrice.is(expected_price)`
- `ItemDescription.contains(description_contains)`
**Compose**
- `ReturnToProducts()`

---

## Cart Flows

### 7) `GoToCartAndVerifyItems(item_names)`
**Compose**
- `GoToCart()`
**Verify**
- `CartContains.items(item_names)`
- `CartItemCountIs(len(item_names))`

### 8) `RemoveItemsInCartAndVerifyRemaining(remove_names, remaining_names)`
**Compose**
- `GoToCart()`
- `RemoveItems.named(remove_names)`
**Verify**
- `CartContains.items(remaining_names)`
- `CartItemCountIs(len(remaining_names))`

### 9) `EmptyCartFromCartPage()`
**Compose**
- `GoToCart()`
- `RemoveItems.named(all_item_names)` *(provided by test data)*
**Verify**
- `CartIsEmpty()`

*(Note: Engine layer can accept `all_item_names` as input; cart page itself doesn’t need to “discover” items.)*

---

## Checkout Flows (End-to-End)

### 10) `CheckoutSingleItem(item_name, first, last, zip)`
**Compose**
- `AddItem.named(item_name)`
- `GoToCart()`
- `ProceedToCheckout()`
- `EnterCheckoutInformation(first, last, zip)`
- `ContinueCheckout()`
**Verify (Step Two)**
- `OverviewContains.items([item_name])`
- `TotalsMatchComputedSum()`
**Compose**
- `FinishCheckout()`

### 11) `CheckoutMultipleItems(item_names, first, last, zip)`
**Compose**
- `AddItem.named(item)` for each in `item_names`
- `GoToCart()`
- `ProceedToCheckout()`
- `EnterCheckoutInformation(first, last, zip)`
- `ContinueCheckout()`
**Verify**
- `OverviewContains.items(item_names)`
- `TotalsMatchComputedSum()`
**Compose**
- `FinishCheckout()`

### 12) `CheckoutThenReturnHome(item_names, first, last, zip)`
**Compose**
- Use `CheckoutMultipleItems(...)`
- `ReturnHomeToInventory()`
**Verify (optional)**
- `OnInventoryPage()`
- `CartBadgeCountIs(0)`

---

## Checkout Negative / Abort Flows

### 13) `CancelCheckoutAtStepOne(item_names)`
**Compose**
- Add items (inventory)
- `GoToCart()`
- `ProceedToCheckout()`
- `CancelCheckout()`
**Verify (optional)**
- `CartItemCountIs(len(item_names))` *(still in cart)*

### 14) `CancelCheckoutAtStepTwo(item_names, first, last, zip)`
**Compose**
- Go through Step One:
  - `GoToCart()`
  - `ProceedToCheckout()`
  - `EnterCheckoutInformation(first, last, zip)`
  - `ContinueCheckout()`
- `CancelCheckout()`
**Verify (optional)**
- `OnInventoryPage()` *(SauceDemo cancel returns to inventory)*

---

## Post-Checkout Confirmation Flows

### 15) `VerifyOverviewMeta(payment_text, shipping_text)`
**Verify**
- `PaymentInformationIs(payment_text)`
- `ShippingInformationIs(shipping_text)`

### 16) `VerifyOrderTotalsAreCorrect(item_names)`
**Verify**
- `OverviewContains.items(item_names)`
- `TotalsMatchComputedSum()`

---

## Suggested “Golden Path” Engine Flow

### 17) `GoldenPathPurchase(item_names, first, last, zip)`
**Compose**
- `LoginSuccessfully(...)`
- `CheckoutMultipleItems(item_names, first, last, zip)`
- `ReturnHomeToInventory()`
**Verify**
- `CartBadgeCountIs(0)`
- `OnInventoryPage()`