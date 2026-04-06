import os
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv


load_dotenv()


class DatabaseService:
    def __init__(self):
        self.mongo_uri = os.getenv("MONGO_URI")
        self.client = MongoClient(self.mongo_uri)
        # Database name is 'project' as requested
        self.db = self.client["project"]
        self.collection = self.db["user_materials"]


    def save_material(self, session_id: str, material_type: str, data: dict):
        """Saves generated study material to the database."""
        # Only save if there's no error in the AI response
        if "error" not in data:
            entry = {
                "session_id": session_id,
                "type": material_type,
                "data": data,
                "created_at": datetime.utcnow()
            }
            result = self.collection.insert_one(entry)
            return str(result.inserted_id)
        return None


    def get_user_history(self, session_id: str):
        """Retrieves all materials associated with a session ID."""
        # Find all entries for the session, sorted by newest first
        cursor = self.collection.find({"session_id": session_id}).sort("created_at", -1)
        
        history = []
        for doc in cursor:
            # Convert ObjectId and datetime to strings for JSON serialization
            doc["_id"] = str(doc["_id"])
            doc["created_at"] = doc["created_at"].isoformat()
            history.append(doc)
            
        return history
