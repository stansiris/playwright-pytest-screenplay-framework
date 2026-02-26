# Step Vocabulary (Current)

This catalog lists every currently wired `pytest-bdd` step phrase.
Source of truth: `tests/test_golden_path_bdd.py`.

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
