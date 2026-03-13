@integration @ui
Feature: TaskHub Task Management
  Business-readable scenarios for TaskHub task lifecycle flows.
  Demonstrates Screenplay Pattern automation across login, create, complete, filter, and delete.

  Scenario: Successful login reaches the task list
    Given I open the TaskHub application
    When I log in to TaskHub with username "admin" and password "admin123"
    Then I should be on the TaskHub task list

  Scenario: Create a task and verify it appears in the list
    Given I am logged in to TaskHub
    When I create a TaskHub task titled "BDD created task" with priority "HIGH"
    Then the TaskHub task titled "BDD created task" should be visible

  Scenario: Complete a task and filter to see only completed tasks
    Given I am logged in to TaskHub
    When I create a TaskHub task titled "BDD task to complete" with priority "MEDIUM"
    And I mark the TaskHub task titled "BDD task to complete" as complete
    And I filter the TaskHub task list by "completed"
    Then the TaskHub task titled "BDD task to complete" should be visible

  Scenario: Delete a task and verify it is removed
    Given I am logged in to TaskHub
    When I create a TaskHub task titled "BDD task to delete" with priority "LOW"
    And I delete the TaskHub task titled "BDD task to delete"
    Then the TaskHub task titled "BDD task to delete" should not be visible
