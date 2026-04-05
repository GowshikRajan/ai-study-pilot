import os
import pytest
from unittest.mock import MagicMock

# ── Must set env vars BEFORE importing app ──────────────────────────────────
# GeminiService.__init__ raises ValueError if GEMINI_API_KEY is missing.
# MongoClient is lazy (doesn't actually connect until a query), so a fake URI is fine.
os.environ["GEMINI_API_KEY"] = "test-key-for-ci"
os.environ["MONGO_URI"] = "mongodb://localhost:27017/test"

from fastapi.testclient import TestClient
from app import app, gemini_service, db_service


@pytest.fixture
def client():
    """Provides a FastAPI test client for each test."""
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def mock_gemini(monkeypatch):
    """
    Patches all GeminiService methods with fake return values.
    This prevents any real Gemini API calls during testing.
    autouse=True means this runs automatically for every test.
    """
    monkeypatch.setattr(
        gemini_service,
        "generate_quiz",
        MagicMock(return_value={
            "quiz": [
                {
                    "question": "What is FastAPI?",
                    "options": ["A web framework", "A database", "A cloud provider", "A test tool"],
                    "answer_index": 0,
                    "explanation": "FastAPI is a modern Python web framework."
                }
            ]
        })
    )
    monkeypatch.setattr(
        gemini_service,
        "generate_summary",
        MagicMock(return_value={
            "overview": "This is a mocked overview for testing.",
            "key_points": ["Key point one.", "Key point two.", "Key point three."]
        })
    )
    monkeypatch.setattr(
        gemini_service,
        "generate_flashcards",
        MagicMock(return_value={
            "flashcards": [
                {"question": "What is Python?", "answer": "A high-level programming language."},
                {"question": "What is Docker?", "answer": "A containerisation platform."}
            ]
        })
    )
    monkeypatch.setattr(
        gemini_service,
        "test_connection",
        MagicMock(return_value={"status": "success", "message": "Hello"})
    )


@pytest.fixture(autouse=True)
def mock_db(monkeypatch):
    """
    Patches all DatabaseService methods with fake return values.
    This prevents any real MongoDB calls during testing.
    """
    monkeypatch.setattr(
        db_service,
        "save_material",
        MagicMock(return_value="fake-object-id-123")
    )
    monkeypatch.setattr(
        db_service,
        "get_user_history",
        MagicMock(return_value=[
            {
                "_id": "fake-id-1",
                "session_id": "test-session",
                "type": "summary",
                "data": {"overview": "mocked", "key_points": []},
                "created_at": "2026-01-01T00:00:00"
            }
        ])
    )
    # The /health/db endpoint calls db_service.client.server_info()
    monkeypatch.setattr(
        db_service.client,
        "server_info",
        MagicMock(return_value={"version": "6.0"})
    )