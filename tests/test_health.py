"""Unit tests for health check and root endpoints."""


def test_root_returns_200(client):
    """GET / should always return HTTP 200."""
    response = client.get("/")
    assert response.status_code == 200


def test_root_returns_html(client):
    """GET / should return HTML content."""
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_root_contains_app_name(client):
    """Frontend should contain app title."""
    response = client.get("/")
    assert "AI Study Pilot" in response.text


def test_health_returns_200(client):
    """GET /health should return HTTP 200."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_returns_ok_status(client):
    """GET /health should return {"status": "ok"}."""
    response = client.get("/health")
    assert response.json() == {"status": "ok"}


def test_health_db_returns_200(client):
    """GET /health/db should return HTTP 200 when database mock is active."""
    response = client.get("/health/db")
    assert response.status_code == 200


def test_health_db_message_indicates_success(client):
    """GET /health/db response should contain a success message."""
    response = client.get("/health/db")
    data = response.json()
    assert "message" in data
    assert "successfully" in data["message"].lower()


def test_health_gemini_returns_200(client):
    """GET /health/gemini should return HTTP 200 when Gemini mock is active."""
    response = client.get("/health/gemini")
    assert response.status_code == 200


def test_health_gemini_returns_success_status(client):
    """GET /health/gemini response should indicate a successful connection."""
    response = client.get("/health/gemini")
    data = response.json()
    assert "status" in data
    assert data["status"] == "success"
