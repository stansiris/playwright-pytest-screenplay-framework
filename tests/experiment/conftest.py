import pytest
from playwright.sync_api import APIRequestContext, APIResponse, Browser, Playwright

TASKHUB_USERNAME = "admin"
TASKHUB_PASSWORD = "admin123"


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: dict) -> dict:
    """Override the browser_type_launch_args fixture to return custom launch arguments."""
    return {
        **browser_type_launch_args,
        # "headless": False,
        # "slow_mo": 500
    }


@pytest.fixture(scope="session")
def base_url(pytestconfig: pytest.Config) -> str:
    url = pytestconfig.getoption("base_url", default=None) or "http://127.0.0.1:5001"
    return url


@pytest.fixture(scope="session")
def auth_state_via_api(
    browser: Browser, base_url: str, tmp_path_factory, playwright: Playwright
) -> str:
    """
    Alternative to auth_state fixture that logs in via the API instead of the UI.
    This is faster and less brittle, but it doesn't test the login UI.
    """

    path = tmp_path_factory.getbasetemp() / "auth_state_api.json"

    context: APIRequestContext = playwright.request.new_context(base_url=base_url)
    response: APIResponse = context.post(
        url="/api/login", data={"username": TASKHUB_USERNAME, "password": TASKHUB_PASSWORD}
    )

    # context: APIRequestContext = browser.new_context(base_url=base_url)  # throw away context
    # response = context.request.post(
    #     url="/api/login", data={"username": TASKHUB_USERNAME, "password": TASKHUB_PASSWORD}
    # )

    assert response.ok, f"Login API request failed with status {response.status}"
    context.storage_state(path=path)
    # context.close()
    context.dispose()  # Dispose the APIRequestContext to free resources

    return str(path)


@pytest.fixture(scope="session")
def auth_state_via_ui(browser: Browser, base_url: str, tmp_path_factory) -> str:
    """
    Runs ONCE per session.
    Creates a throwaway context, drives the login UI, dumps storage state to
    a file, then closes the context.  The file outlives the context.
    """

    path = tmp_path_factory.getbasetemp() / "auth_state_ui.json"

    context = browser.new_context(base_url=base_url)  # throw away context
    page = context.new_page()

    page.goto("/login")
    page.get_by_test_id("login-username-input").fill(TASKHUB_USERNAME)
    page.get_by_test_id("login-password-input").fill(TASKHUB_PASSWORD)
    page.get_by_test_id("login-submit-button").click()
    page.wait_for_url("/tasks")
    page.close()

    context.storage_state(path=path)
    context.close()

    return str(path)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict, auth_state_via_api: str) -> dict:
    """Override the browser_context_args fixture to include the path to the auth state file."""
    return {**browser_context_args, "storage_state": auth_state_via_api}
