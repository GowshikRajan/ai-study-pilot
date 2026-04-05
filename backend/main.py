import os
import uuid
from typing import Optional
from dotenv import load_dotenv
from pymongo import MongoClient
from fastapi import FastAPI, Response, Cookie, Depends
from pydantic import BaseModel
from backend.services.gemini_service import GeminiService

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
# Updated database name to 'project'
db = client["project"]
user_materials = db["user_materials"]

class StudyRequest(BaseModel):
    content: str

app = FastAPI()
gemini_service = GeminiService()

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

@app.get("/test-db")
def test_db():
    return {"message": "Database connected successfully"}

@app.get("/health/gemini")
def test_gemini():
    """Hidden test endpoint to verify Gemini API connectivity."""
    return gemini_service.test_connection()

@app.post("/generate-quiz")
def generate_quiz(request: StudyRequest):
    """Endpoint to generate a multiple-choice quiz from study content."""
    return gemini_service.generate_quiz(request.content)

@app.post("/generate-summary")
def generate_summary(request: StudyRequest):
    """Endpoint to generate a summary with key points from study content."""
    return gemini_service.generate_summary(request.content)

@app.post("/generate-flashcards")
def generate_flashcards(request: StudyRequest):
    """Endpoint to generate Q&A flashcards from study content."""
    return gemini_service.generate_flashcards(request.content)
