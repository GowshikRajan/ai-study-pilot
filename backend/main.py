import os
import uuid
from typing import Optional
from dotenv import load_dotenv
from fastapi import FastAPI, Response, Cookie, Depends
from pydantic import BaseModel
from backend.services.gemini_service import GeminiService
from backend.services.database_service import DatabaseService

load_dotenv()

class StudyRequest(BaseModel):
    content: str

app = FastAPI()
gemini_service = GeminiService()
db_service = DatabaseService()

def get_session_id(response: Response, session_id: Optional[str] = Cookie(None)):
    """Dependency to get or create a session_id cookie."""
    if not session_id:
        session_id = str(uuid.uuid4())
        # Set cookie: httponly=True, max_age=30 days (in seconds)
        response.set_cookie(key="session_id", value=session_id, httponly=True, max_age=2592000)
    return session_id

@app.get("/")
def root(session_id: str = Depends(get_session_id)):
    return {"message": "AI Study Pilot is running", "session_id": session_id}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/health/db")
def test_db():
    # Simple check to see if we can reach the database
    try:
        db_service.client.server_info()
        return {"message": "Database connected successfully"}
    except Exception as e:
        return {"message": f"Database connection failed: {str(e)}"}

@app.get("/health/gemini")
def test_gemini():
    """Hidden test endpoint to verify Gemini API connectivity."""
    return gemini_service.test_connection()

@app.post("/generate-quiz")
def generate_quiz(request: StudyRequest, session_id: str = Depends(get_session_id)):
    """Generates a quiz and saves it to the database."""
    data = gemini_service.generate_quiz(request.content)
    db_service.save_material(session_id, "quiz", data)
    return data

@app.post("/generate-summary")
def generate_summary(request: StudyRequest, session_id: str = Depends(get_session_id)):
    """Generates a summary and saves it to the database."""
    data = gemini_service.generate_summary(request.content)
    db_service.save_material(session_id, "summary", data)
    return data

@app.post("/generate-flashcards")
def generate_flashcards(request: StudyRequest, session_id: str = Depends(get_session_id)):
    """Generates flashcards and saves them to the database."""
    data = gemini_service.generate_flashcards(request.content)
    db_service.save_material(session_id, "flashcards", data)
    return data

@app.get("/history")
def get_history(session_id: str = Depends(get_session_id)):
    """Retrieves the history of materials for the current session."""
    return {"history": db_service.get_user_history(session_id)}
