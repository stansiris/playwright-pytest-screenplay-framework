@integration @ui
Feature: Work Item Management
  Business-readable scenarios for the Work Items lifecycle.
  Demonstrates Screenplay Pattern automation across login, create, complete, filter, and delete.

  Scenario: Successful login reaches the work items page
    Given I open the Work Items application
    When I log in to Work Items with username "admin" and password "admin123"
    Then I should be on the Work Items page

  Scenario: Create a work item and verify it appears in the list
    Given I am logged in to Work Items
    When I create a work item titled "BDD created work item" with priority "HIGH"
    Then the work item titled "BDD created work item" should be visible

  Scenario: Complete a work item and filter to see only completed items
    Given I am logged in to Work Items
    When I create a work item titled "BDD work item to complete" with priority "MEDIUM"
    And I mark the work item titled "BDD work item to complete" as complete
    And I filter work items by "completed"
    Then the work item titled "BDD work item to complete" should be visible

  Scenario: Delete a work item and verify it is removed
    Given I am logged in to Work Items
    When I create a work item titled "BDD work item to delete" with priority "LOW"
    And I delete the work item titled "BDD work item to delete"
    Then the work item titled "BDD work item to delete" should not be visible
