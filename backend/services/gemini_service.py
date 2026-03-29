import os
import json
import logging
from google import genai
from google.genai import errors
from dotenv import load_dotenv

load_dotenv()

# Set up logging for error tracking
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logger.error("GEMINI_API_KEY not found in environment variables.")
            raise ValueError("GEMINI_API_KEY is missing")
        
        # Initialize the new Google GenAI client
        self.client = genai.Client(api_key=self.api_key)
        self.model_id = 'gemini-3-flash-preview'

    def test_connection(self) -> dict:
        """
        Ping test using the new SDK to verify the API key and connection.
        """
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents="Say 'Hello' for a connection test."
            )
            if response and response.text:
                return {"status": "success", "message": response.text.strip()}
            return {"status": "error", "message": "Empty response from Gemini"}
        except errors.ClientError as e:
            logger.error(f"Client error: {str(e)}")
            return {"status": "error", "message": "Invalid API Key or Client error"}
        except Exception as e:
            logger.error(f"Unexpected error during ping: {str(e)}")
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
        Wrapped call to Gemini with centralized error handling using the new SDK.
        """
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            if expect_json:
                return self.clean_json_response(response.text)
            return response.text
        except errors.ClientError as e:
            logger.warning(f"Gemini Client Error (likely quota or auth): {str(e)}")
            return {"error": "AI service limit reached or authentication failed."}
        except Exception as e:
            logger.error(f"Gemini API Error: {str(e)}")
            return {"error": "An unexpected error occurred with the AI service."}
