from playwright.sync_api import APIRequestContext, Page, expect

def test_tasks_page(api_auth_admin: APIRequestContext, page: Page):
    """Example test using API authentication context to log in, then navigating with a Page to verify login success."""
    page.goto("/tasks")
    expect(page.get_by_text("Login successful.")).to_be_visible()