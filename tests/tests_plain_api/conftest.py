from collections.abc import Generator

import pytest
import requests
from playwright.sync_api import Playwright, APIRequestContext

TASKHUB_URL =  "http://127.0.1:5001"

@pytest.fixture(scope="session")
def api(playwright: Playwright) -> Generator[APIRequestContext, None, None]:
    """Create a Playwright APIRequestContext for making API calls to TaskHub."""
    ctx = playwright.request.new_context(base_url=TASKHUB_URL)
    yield ctx
    ctx.dispose()

@pytest.fixture(autouse=True)
def reset_data(api: APIRequestContext) -> None:
    """Reset TaskHub data before each test by calling the API endpoint."""
    api.post("/api/test/reset")
    
@pytest.fixture
def auth_api(playwright: Playwright) -> Generator[APIRequestContext, None, None]:
    """Create an authenticated APIRequestContext for making API calls to TaskHub."""
    ctx = playwright.request.new_context(base_url=TASKHUB_URL)
    ctx.post("/api/auth/login", data={"username": "admin", "password": "admin123"})
    yield ctx
    ctx.dispose()