import os
import json
import logging
import requests
from dotenv import load_dotenv

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        # Using GEMINI_API_KEY as requested
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logger.error("GEMINI_API_KEY not found in environment variables.")
            raise ValueError("GEMINI_API_KEY is missing")
        
        # REST API Configuration
        self.model = "gemini-3-flash-preview"
        # Based on user script: https://aiplatform.googleapis.com/v1/publishers/google/models/{MODEL}:generateContent
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"

    def test_connection(self) -> dict:
        """
        Ping test to verify API connectivity using requests.
        """
        try:
            payload = {
                "contents": [{"parts": [{"text": "Say 'Hello' for a connection test."}]}]
            }
            response = requests.post(self.url, json=payload, headers={"Content-Type": "application/json"})
            response.raise_for_status()
            
            result = response.json()
            message = result["candidates"][0]["content"]["parts"][0]["text"].strip()
            return {"status": "success", "message": message}
        except Exception as e:
            logger.error(f"Ping failed: {str(e)}")
            return {"status": "error", "message": str(e)}

    def clean_json_response(self, raw_response: str) -> dict:
        """
        Helper to ensure Gemini returns clean JSON.
        Removes markdown code blocks and attempts to parse the string.
        """
        try:
            cleaned = raw_response.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            
            return json.loads(cleaned.strip())
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {str(e)}")
            return {"error": "Invalid JSON format", "raw": raw_response}

    def call_gemini(self, prompt: str, expect_json: bool = False):
        """
        Generic wrapper for Gemini API calls using requests.
        """
        try:
            payload = {
                "contents": [{"parts": [{"text": prompt}]}]
            }
            response = requests.post(self.url, json=payload, headers={"Content-Type": "application/json"})
            
            if response.status_code == 429:
                logger.warning("Quota exceeded (429)")
                return {"error": "API quota exceeded. Try again later."}
            
            response.raise_for_status()
            
            result = response.json()
            text_response = result["candidates"][0]["content"]["parts"][0]["text"]
            
            if expect_json:
                return self.clean_json_response(text_response)
            return text_response
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error: {str(e)}")
            return {"error": f"API returned error: {response.status_code}"}
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return {"error": "An unexpected error occurred with the AI service."}
