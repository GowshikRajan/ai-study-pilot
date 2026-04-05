import os
from dotenv import load_dotenv
from pymongo import MongoClient
from fastapi import FastAPI
from pydantic import BaseModel
from backend.services.gemini_service import GeminiService

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["ai_study_pilot"]

class StudyRequest(BaseModel):
    content: str

app = FastAPI()
gemini_service = GeminiService()

@app.get("/")
def root():
    return {"message": "AI Study Pilot is running"}

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

@app.post("/generate-summary")
def generate_summary(request: StudyRequest):
    """Endpoint to generate a summary with key points from study content."""
    return gemini_service.generate_summary(request.content)

@app.post("/generate-flashcards")
def generate_flashcards(request: StudyRequest):
    """Endpoint to generate Q&A flashcards from study content."""
    return gemini_service.generate_flashcards(request.content)
