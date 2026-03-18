import logging

from playwright.sync_api import APIRequestContext

logger = logging.getLogger(__name__)


def test_health(api: APIRequestContext):
    response = api.get("/health")

    assert response.ok
    assert response.json() == {"status": "ok"}


def test_successful_login(api: APIRequestContext):
    response = api.post("/api/login", json={"username": "admin", "password": "admin123"})

    assert response.ok
    assert response.json() == {"username": "admin"}


def test_failed_login_400(api: APIRequestContext):
    response = api.post("/api/login", json={"username": "admin", "password": ""})

    assert not response.ok
    assert response.status == 400
    assert response.json() == {"error": "Username and password are required."}


def test_failed_login_401(api: APIRequestContext):
    response = api.post("/api/login", json={"username": "admin", "password": "wrongpassword"})

    assert not response.ok
    assert response.status == 401
    assert response.json() == {"error": "Invalid credentials."}


def test_resource_authorization_403(
    api_auth_admin: APIRequestContext, api_auth_guest: APIRequestContext
):
    admin_create_task_response = api_auth_admin.post(
        "/api/tasks",
        data={
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "status": "ACTIVE",
            "priority": "MEDIUM",
            "due_date": "2026-03-20",
        },
    )

    assert admin_create_task_response.ok and admin_create_task_response.status == 201, (
        f"Admin task creation failed with status "
        f"{admin_create_task_response.status}: {admin_create_task_response.text()}"
    )

    logger.info(f"Admin created task with ID: {admin_create_task_response.json()}")

    admin_task_id = admin_create_task_response.json().get("id")

    guest_get_task_response = api_auth_guest.get(f"/api/tasks/{admin_task_id}")
    assert not guest_get_task_response.ok and guest_get_task_response.status == 403, (
        f"Guest should not access admin task, but got status "
        f"{guest_get_task_response.status}: {guest_get_task_response.text()}"
    )

    logger.info(
        f"Guest access to admin task correctly denied with status "
        f"{guest_get_task_response.status}, response: {guest_get_task_response.text()}"
    )
