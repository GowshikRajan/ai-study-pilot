from pymongo import MongoClient

client = MongoClient("mongodb+srv://rehamsw20n:rrss2222@cluster0.y4syk.mongodb.net/?appName=Cluster0")
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
