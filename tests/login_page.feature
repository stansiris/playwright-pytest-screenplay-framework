Feature: SauceDemo - Login

  The SauceDemo login page should allow successful authentication with valid users,
  show clear errors for invalid attempts, and support keyboard and mouse navigation
  (tab order, focus, enter-to-submit).

  Background:
    Given I am on the SauceDemo login page

  # ----------------------------
  # Positive - Authentication
  # ----------------------------

  Scenario Outline: Login succeeds with valid credentials for supported users
    When I enter username "<username>"
    And I enter password "secret_sauce"
    And I click the Login button
    Then I should be on the inventory page
    And I should see the inventory container

    Examples:
      | username                 |
      | standard_user            |
      | problem_user             |
      | performance_glitch_user  |
      | error_user               |
      | visual_user              |

  Scenario: Login form allows pressing Enter to submit
    When I enter username "standard_user"
    And I enter password "secret_sauce"
    And I press Enter
    Then I should be on the inventory page
    And I should see the inventory container

  Scenario: Password input is masked
    Then the password field should be of type "password"

  # ----------------------------
  # Negative - Authentication / Validation
  # ----------------------------

  Scenario: Login fails when username is missing
    When I enter password "secret_sauce"
    And I click the Login button
    Then I should see an error message "Epic sadface: Username is required"
    And I should remain on the login page

  Scenario: Login fails when password is missing
    When I enter username "standard_user"
    And I click the Login button
    Then I should see an error message "Epic sadface: Password is required"
    And I should remain on the login page

  Scenario: Login fails when both username and password are missing
    When I click the Login button
    Then I should see an error message "Epic sadface: Username is required"
    And I should remain on the login page

  Scenario: Login fails with an invalid username
    When I enter username "not_a_real_user"
    And I enter password "secret_sauce"
    And I click the Login button
    Then I should see an error message "Epic sadface: Username and password do not match any user in this service"
    And I should remain on the login page

  Scenario: Login fails with an invalid password
    When I enter username "standard_user"
    And I enter password "wrong_password"
    And I click the Login button
    Then I should see an error message "Epic sadface: Username and password do not match any user in this service"
    And I should remain on the login page

  Scenario: Login fails for locked_out_user
    When I enter username "locked_out_user"
    And I enter password "secret_sauce"
    And I click the Login button
    Then I should see an error message "Epic sadface: Sorry, this user has been locked out."
    And I should remain on the login page

  Scenario: Error message can be dismissed
    When I enter username "standard_user"
    And I click the Login button
    Then I should see an error message "Epic sadface: Password is required"
    When I dismiss the error message
    Then I should not see the error message

  Scenario: Username and password fields are cleared on page refresh
    When I enter username "standard_user"
    And I enter password "secret_sauce"
    And I refresh the page
    Then the username field should be empty
    And the password field should be empty

  Scenario Outline: Login fails with blank and malformed credential inputs
    When I enter username "<username>"
    And I enter password "<password>"
    And I click the Login button
    Then I should see an error message "<error>"
    And I should remain on the login page

    Examples:
      | username        | password        | error                                                     |
      |                 |                 | Epic sadface: Username is required                         |
      | invalid_user    | secret_sauce    | Epic sadface: Username and password do not match any user in this service |
      | standard_user   | wrong_password  | Epic sadface: Username and password do not match any user in this service |

  # ----------------------------
  # Navigation - Keyboard and Mouse
  # ----------------------------

  Scenario: Clicking on username field gives it focus
    When I click on the username field
    Then the username field should be focused

  Scenario: Clicking on password field gives it focus
    When I click on the password field
    Then the password field should be focused

  Scenario: Login button can receive keyboard focus
    Given I focus the Login button
    Then the Login button should be focused

  Scenario: User can navigate login form using Tab key in correct order
    When I press Tab
    Then the username field should be focused
    When I press Tab
    Then the password field should be focused
    When I press Tab
    Then the Login button should be focused

  Scenario: User can navigate backwards using Shift+Tab
    Given I focus the Login button
    When I press Shift+Tab
    Then the password field should be focused
    When I press Shift+Tab
    Then the username field should be focused

  Scenario: Login page state is preserved after failed login
    When I enter username "standard_user"
    And I click the Login button
    Then I should see an error message
    And I should remain on the login page

  Scenario: Focused element is visibly highlighted
    When I press Tab
    Then the focused element should have a visible focus indicator
