"""Unit tests for the GET /history endpoint."""

def test_history_returns_200(client):
    """GET /history should return HTTP 200."""
    response = client.get("/history")
    assert response.status_code == 200
