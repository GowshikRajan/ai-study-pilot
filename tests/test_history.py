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


def test_history_returns_a_list(client):
    """GET /history 'history' value must be a list."""
    response = client.get("/history")
    data = response.json()
    assert isinstance(data["history"], list)


def test_history_entry_has_required_fields(client):
    """Each history entry must have 'type', 'data', and 'session_id' fields."""
    response = client.get("/history")
    data = response.json()
    assert len(data["history"]) > 0
    entry = data["history"][0]
    assert "type" in entry
    assert "data" in entry
    assert "session_id" in entry


def test_history_entry_type_is_string(client):
    """The 'type' field in a history entry must be a non-empty string."""
    response = client.get("/history")
    entry = response.json()["history"][0]
    assert isinstance(entry["type"], str)
    assert len(entry["type"]) > 0
