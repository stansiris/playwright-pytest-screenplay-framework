from playwright.sync_api import APIRequestContext

def test_health(api: APIRequestContext):
    response = api.get("/health",timeout=50)

    assert response.ok
    assert response.json() == {
        "status": "ok"
    }

def test_successful_login(api: APIRequestContext):
    response = api.post("/api/login", data={"username": "admin", "password": "admin123"})

    assert response.ok
    assert response.json() == {
        "username": "admin"
    }

def test_failed_login(api: APIRequestContext):
    response = api.post("/api/login", data={"username": "admin", "password": "wrongpassword"})

    assert not response.ok
    assert response.status == 401
    assert response.json() == {
        "error": "Invalid credentials."
    }