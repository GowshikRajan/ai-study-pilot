"""Unit tests for AI generation endpoints: quiz, summary, and flashcards."""


# ---------------------------------------------------------------------------
# Quiz generation tests
# ---------------------------------------------------------------------------

def test_generate_quiz_returns_200(client):
    """POST /generate-quiz should return HTTP 200."""
    response = client.post("/generate-quiz", json={"content": "Study text about Python."})
    assert response.status_code == 200


def test_generate_quiz_response_has_quiz_key(client):
    """POST /generate-quiz response must contain a 'quiz' key."""
    response = client.post("/generate-quiz", json={"content": "Study text about Python."})
    data = response.json()
    assert "quiz" in data

def test_generate_quiz_contains_at_least_one_question(client):
    """POST /generate-quiz should return a non-empty list of questions."""
    response = client.post("/generate-quiz", json={"content": "Study text about Python."})
    data = response.json()
    assert isinstance(data["quiz"], list)
    assert len(data["quiz"]) > 0


def test_generate_quiz_question_has_required_fields(client):
    """Each quiz question must have 'question', 'options', and 'answer_index'."""
    response = client.post("/generate-quiz", json={"content": "Study text about Python."})
    question = response.json()["quiz"][0]
    assert "question" in question
    assert "options" in question
    assert "answer_index" in question
