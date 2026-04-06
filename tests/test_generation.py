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


# ---------------------------------------------------------------------------
# Summary generation tests
# ---------------------------------------------------------------------------


def test_generate_summary_returns_200(client):
    """POST /generate-summary should return HTTP 200."""
    response = client.post("/generate-summary", json={"content": "Study text about FastAPI."})
    assert response.status_code == 200


def test_generate_summary_response_has_overview(client):
    """POST /generate-summary response must contain an 'overview' key."""
    response = client.post("/generate-summary", json={"content": "Study text about FastAPI."})
    data = response.json()
    assert "overview" in data
    assert isinstance(data["overview"], str)


def test_generate_summary_response_has_key_points(client):
    """POST /generate-summary response must contain a non-empty 'key_points' list."""
    response = client.post("/generate-summary", json={"content": "Study text about FastAPI."})
    data = response.json()
    assert "key_points" in data
    assert isinstance(data["key_points"], list)
    assert len(data["key_points"]) >= 3


# ---------------------------------------------------------------------------
# Flashcard generation tests
# ---------------------------------------------------------------------------


def test_generate_flashcards_returns_200(client):
    """POST /generate-flashcards should return HTTP 200."""
    response = client.post("/generate-flashcards", json={"content": "Study text about Docker."})
    assert response.status_code == 200


def test_generate_flashcards_response_has_flashcards_key(client):
    """POST /generate-flashcards response must contain a 'flashcards' key."""
    response = client.post("/generate-flashcards", json={"content": "Study text about Docker."})
    data = response.json()
    assert "flashcards" in data


def test_generate_flashcards_contains_at_least_one_card(client):
    """POST /generate-flashcards should return a non-empty list of cards."""
    response = client.post("/generate-flashcards", json={"content": "Study text about Docker."})
    data = response.json()
    assert isinstance(data["flashcards"], list)
    assert len(data["flashcards"]) > 0


def test_generate_flashcards_card_has_question_and_answer(client):
    """Each flashcard must have both a 'question' and an 'answer'."""
    response = client.post("/generate-flashcards", json={"content": "Study text about Docker."})
    card = response.json()["flashcards"][0]
    assert "question" in card
    assert "answer" in card
