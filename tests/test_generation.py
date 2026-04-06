"""Unit tests for AI generation endpoints: quiz, summary, and flashcards."""


# ---------------------------------------------------------------------------
# Quiz generation tests
# ---------------------------------------------------------------------------

def test_generate_quiz_returns_200(client):
    """POST /generate-quiz should return HTTP 200."""
    response = client.post("/generate-quiz", json={"content": "Study text about Python."})
    assert response.status_code == 200
