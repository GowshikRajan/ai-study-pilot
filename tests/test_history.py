"""Unit tests for the GET /history endpoint."""

def test_history_returns_200(client):
    """GET /history should return HTTP 200."""
    response = client.get("/history")
    assert response.status_code == 200

def test_history_response_has_history_key(client):
    """GET /history response must contain a 'history' key."""
    response = client.get("/history")
    data = response.json()
    assert "history" in data
