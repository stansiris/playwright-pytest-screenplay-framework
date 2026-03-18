from playwright.sync_api import Page, expect


def test_tasks_page_accessible_after_api_login(page: Page):
    """Login via page.request (shares BrowserContext session), then verify tasks page loads."""
    response = page.request.post("/api/login", data={"username": "admin", "password": "admin123"})
    assert response.ok

    page.goto("/tasks")
    expect(page.get_by_test_id("task-list-container")).to_be_visible()
