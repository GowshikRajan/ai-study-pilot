import os
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

# Set dummy environment variables BEFORE importing the app.
# This prevents GeminiService from raising ValueError on missing key
# and prevents MongoClient from failing on an empty URI.
os.environ.setdefault("GEMINI_API_KEY", "test-dummy-key-for-ci")
os.environ.setdefault("MONGO_URI", "mongodb://localhost:27017/testdb")

# ---------------------------------------------------------------------------
# Shared mock data — used by fixtures below
# ---------------------------------------------------------------------------


MOCK_QUIZ_RESPONSE = {
    "quiz": [
        {
            "question": "What is the capital of France?",
            "options": ["Berlin", "Madrid", "Paris", "Rome"],
            "answer_index": 2,
            "explanation": "Paris is the capital of France since 987 AD.",
        }
    ]
}


MOCK_SUMMARY_RESPONSE = {
    "overview": "This is a test overview of the provided study material.",
    "key_points": [
        "Key concept number one.",
        "Key concept number two.",
        "Key concept number three.",
    ],
}


MOCK_FLASHCARD_RESPONSE = {
    "flashcards": [
        {
            "question": "What is FastAPI?",
            "answer": "A modern, high-performance Python web framework.",
        }
    ]
}


MOCK_HISTORY = [
    {
        "_id": "507f1f77bcf86cd799439011",
        "session_id": "test-session-abc",
        "type": "quiz",
        "data": MOCK_QUIZ_RESPONSE,
        "created_at": "2026-01-01T00:00:00",
    }
]

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_gemini():
    """Replace the module-level gemini_service instance with a mock."""
    with patch("backend.main.gemini_service") as mock:
        mock.test_connection.return_value = {"status": "success", "message": "Hello"}
        mock.generate_quiz.return_value = MOCK_QUIZ_RESPONSE
        mock.generate_summary.return_value = MOCK_SUMMARY_RESPONSE
        mock.generate_flashcards.return_value = MOCK_FLASHCARD_RESPONSE
        yield mock


@pytest.fixture
def mock_db():
    """Replace the module-level db_service instance with a mock."""
    with patch("backend.main.db_service") as mock:
        mock.client.server_info.return_value = {"version": "6.0"}
        mock.save_material.return_value = "507f1f77bcf86cd799439011"
        mock.get_user_history.return_value = MOCK_HISTORY
        yield mock


@pytest.fixture
def client(mock_gemini, mock_db):
    """Provide a FastAPI test client with all external services mocked."""
    from backend.main import app
    with TestClient(app) as test_client:
        yield test_client
