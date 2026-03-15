from playwright.sync_api import APIRequestContext, APIResponse

from screenplay_core.abilities.browse_the_web import BrowseTheWeb
from screenplay_core.core.actor import Actor


def test_health(api: APIRequestContext):
    response = api.get("/health", timeout=50)

    assert response.ok
    assert response.json() == {"status": "ok"}


def test_successful_login(api: APIRequestContext):
    response = api.post("/api/login", data={"username": "admin", "password": "admin123"})

    assert response.ok
    assert response.json() == {"username": "admin"}


def test_failed_login(api: APIRequestContext):
    response = api.post("/api/login", data={"username": "admin", "password": "wrongpassword"})

    assert not response.ok
    assert response.status == 401
    assert response.json() == {"error": "Invalid credentials."}


def test_ui_login_session_shared_with_api(logged_in_taskhub_customer: Actor):
    """Verify that after UI login the session cookie is shared with page.request,
    allowing authenticated API calls without a separate login step."""
    # page.request uses the BrowserContext base_url (TASKHUB_URL), so relative paths work here
    request_ctx: APIRequestContext = logged_in_taskhub_customer.ability_to(
        BrowseTheWeb
    ).page.request  # noqa: E501

    response: APIResponse = request_ctx.get("/api/me")
    assert response.ok
    assert response.json() == {"username": "admin"}


def test_ui_logout(logged_in_taskhub_customer: Actor):
    """Verify that logout clears the session."""
    # page.request uses the BrowserContext base_url (TASKHUB_URL), so relative paths work here
    request_ctx: APIRequestContext = logged_in_taskhub_customer.ability_to(
        BrowseTheWeb
    ).page.request  # noqa: E501

    response: APIResponse = request_ctx.post("/api/logout")
    assert response.ok
    assert response.json() == {"message": "Logged out."}
