"""Unit tests for health check and root endpoints."""


def test_health_returns_200(client):
    """GET /health must return HTTP 200"""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_returns_ok_status(client):
    """GET /health must return {"status": "ok"}"""
    response = client.get("/health")
    assert response.json() == {"status": "ok"}


def test_root_returns_200(client):
    """GET / must return HTTP 200"""
    response = client.get("/")
    assert response.status_code == 200


def test_root_returns_message(client):
    """GET / must contain the app running message"""
    response = client.get("/")
    data = response.json()
    assert "message" in data
    assert data["message"] == "AI Study Pilot is running"


def test_root_returns_session_id(client):
    """GET / must return a session_id in the response"""
    response = client.get("/")
    data = response.json()
    assert "session_id" in data
    assert data["session_id"] is not None


def test_health_db_returns_200(client):
    """GET /health/db must return HTTP 200 when DB mock responds"""
    response = client.get("/health/db")
    assert response.status_code == 200


def test_health_gemini_returns_200(client):
    """GET /health/gemini must return HTTP 200 when Gemini mock responds"""
    response = client.get("/health/gemini")
    assert response.status_code == 200


def test_health_gemini_returns_success_status(client):
    """GET /health/gemini must return status: success from the mocked service"""
    response = client.get("/health/gemini")
    data = response.json()
    assert data["status"] == "success"

