@golden_path @checkout @ui
Feature: Golden Path Purchase (SauceDemo)
  A business-readable end-to-end purchase flow that demonstrates the framework design:
  - Screenplay Tasks for intent (login, add items, checkout)
  - Questions for verification (cart contents, totals math)
  - Thin pytest-bdd steps that delegate to Tasks/Questions

  Background:
    Given I open the SauceDemo application

  Scenario: Successful purchase of multiple items and cart resets after checkout
    When I log in with username "standard_user" and password "secret_sauce"
    Then I should be on the inventory page

    When I sort inventory by "Name (A to Z)"
    And I add the following items to the cart:
      | item_name               |
      | Sauce Labs Backpack     |
      | Sauce Labs Bike Light   |
      | Sauce Labs Bolt T-Shirt |
    Then the cart badge count should be 3

    When I go to the cart
    Then the cart should contain the following items:
      | item_name               |
      | Sauce Labs Backpack     |
      | Sauce Labs Bike Light   |
      | Sauce Labs Bolt T-Shirt |
    And the cart item count should be 3

    When I proceed to checkout
    And I enter checkout information:
      | first_name | last_name | postal_code |
      | Stan       | Siris     | 08873       |
    And I continue checkout

    Then the overview should contain the following items:
      | item_name               |
      | Sauce Labs Backpack     |
      | Sauce Labs Bike Light   |
      | Sauce Labs Bolt T-Shirt |
    And the payment information should be "SauceCard #31337"
    And the shipping information should be "Free Pony Express Delivery!"
    And totals should match the computed sum

    When I finish checkout
    Then I should see a checkout complete confirmation

    When I return home to the inventory
    Then the cart badge count should be 0
