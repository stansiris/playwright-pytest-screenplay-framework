@integration
Feature: Login behavior (BDD mirror)
  This feature mirrors the direct pytest login tests using business-readable scenarios.

  Scenario: Successful login reaches inventory and user can log out
    Given I open the login page for login scenarios
    When I submit login credentials username "standard_user" and password "secret_sauce"
    Then I should be on the inventory page for login scenarios
    When I log out from the inventory menu
    Then I should be back on the login page for login scenarios

  Scenario Outline: Invalid login shows expected error message
    Given I open the login page for login scenarios
    When I submit login credentials username "<username>" and password "<password>"
    Then I should see login error message "<error_message>" for login scenarios
    And I can dismiss the login error message

    Examples:
      | username        | password       | error_message                                               |
      |                 | secret_sauce   | Username is required                                        |
      | standard_user   |                | Password is required                                        |
      | invalid_user    | secret_sauce   | Username and password do not match any user in this service |
      | standard_user   | wrong_password | Username and password do not match any user in this service |
      | locked_out_user | secret_sauce   | Sorry, this user has been locked out.                       |
