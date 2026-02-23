# Step Vocabulary (Current)

This catalog lists every implemented pytest-bdd step phrase.
Source of truth: `tests/steps/common_steps.py`, `tests/steps/login_page_steps.py`, and `tests/steps/golden_path_steps.py`.

## Given Steps

- `Given I am on the SauceDemo login page`
- `Given I open the SauceDemo application`
- `Given I focus the Login button`

## When Steps

- `When I enter username "{username}"`
- `When I enter password "{password}"`
- `When I click the Login button`
- `When I press Enter`
- `When I dismiss the error message`
- `When I refresh the page`
- `When I click on the username field`
- `When I click on the password field`
- `When I press Tab`
- `When I press Shift+Tab`
- `When I log in with username "{username}" and password "{password}"`
- `When I sort inventory by "{option}"`
- `When I add the following items to the cart:`

```gherkin
When I add the following items to the cart:
  | item_name               |
  | Sauce Labs Backpack     |
  | Sauce Labs Bike Light   |
```

- `When I go to the cart`
- `When I proceed to checkout`
- `When I enter checkout information:`

```gherkin
When I enter checkout information:
  | first_name | last_name | postal_code |
  | John       | Doe       | 08873       |
```

- `When I continue checkout`
- `When I finish checkout`
- `When I return home to the inventory`

## Then Steps

- `Then I should be on the inventory page`
- `Then I should see the inventory container`
- `Then the password field should be of type "{field_type}"`
- `Then I should see an error message "{error_message}"`
- `Then I should see an error message`
- `Then I should remain on the login page`
- `Then I should not see the error message`
- `Then the username field should be empty`
- `Then the password field should be empty`
- `Then the username field should be focused`
- `Then the password field should be focused`
- `Then the Login button should be focused`
- `Then the focused element should have a visible focus indicator`
- `Then the cart badge count should be {count:d}`
- `Then the cart should contain the following items:`

```gherkin
Then the cart should contain the following items:
  | item_name               |
  | Sauce Labs Backpack     |
  | Sauce Labs Bike Light   |
```

- `Then the cart item count should be {count:d}`
- `Then the overview should contain the following items:`

```gherkin
Then the overview should contain the following items:
  | item_name               |
  | Sauce Labs Backpack     |
  | Sauce Labs Bike Light   |
```

- `Then the payment information should be "{text}"`
- `Then the shipping information should be "{text}"`
- `Then totals should match the computed sum`
- `Then I should see a checkout complete confirmation`
