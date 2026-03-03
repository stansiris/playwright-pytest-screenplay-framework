# Step Vocabulary (Current)

This catalog lists the currently wired `pytest-bdd` step phrases.
Sources of truth:
- `tests/test_golden_path_bdd.py`
- `tests/test_login_bdd.py`

## Given Steps

- `Given I open the SauceDemo application`

## When Steps

- `When I log in with username "{username}" and password "{password}"`
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

## Login Mirror Steps (`tests/test_login_bdd.py`)

### Given Steps

- `Given I open the login page for login scenarios`

### When Steps

- `When I submit login credentials username "{username}" and password "{password}"`
- `When I log out from the inventory menu`

### Then Steps

- `Then I should be on the inventory page for login scenarios`
- `Then I should be back on the login page for login scenarios`
- `Then I should see login error message "{error_message}" for login scenarios`
- `Then I can dismiss the login error message`
