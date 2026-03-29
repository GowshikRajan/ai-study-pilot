import os
from dotenv import load_dotenv
from pymongo import MongoClient
from fastapi import FastAPI
from services.gemini_service import GeminiService

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["ai_study_pilot"]

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

@app.get("/gemini-test")
def test_gemini():
    """Hidden test endpoint to verify Gemini API connectivity."""
    return gemini_service.test_connection()
