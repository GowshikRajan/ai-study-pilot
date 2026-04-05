import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["ai_study_pilot"]

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "AI Study Pilot is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/test-db")
def test_db():
    return {"message": "Database connected successfully"}
