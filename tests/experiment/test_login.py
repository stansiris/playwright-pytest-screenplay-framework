import pytest
from playwright.sync_api import Page


@pytest.mark.skip(
    reason="This test is now covered by the auth_state fixture in conftest.py, "
    "which logs in once per session and saves the auth state to a file. This test can be removed."
)
def test_login(page: Page):
    page.goto("/login")
    page.get_by_test_id("login-username-input").fill("admin")
    page.get_by_test_id("login-password-input").fill("admin123")
    page.get_by_test_id("login-submit-button").click()
    # Verify that the user is redirected to the dashboard after successful login
    page.wait_for_url("/tasks")
    assert page.url.endswith("/tasks")


@pytest.mark.parametrize(
    "title, description, priority, due_date",
    [
        ("Drink Coffee", "Hazelnut flavor.", "HIGH", "2026-03-27"),
        ("Drink Tea", "Black currant", "MEDIUM", "2026-03-28"),
    ],
)
def test_add_task(page: Page, title: str, description: str, priority: str, due_date: str):
    page.goto("/tasks")
    page.get_by_test_id("task-title-input").fill(title)
    page.get_by_test_id("task-description-input").fill(description)
    page.get_by_test_id("task-priority-input").select_option(priority)
    page.get_by_test_id("task-due-date-input").fill(due_date)
    page.get_by_test_id("add-task-button").click()

    page.get_by_test_id("taskhub-logout-button").click()
