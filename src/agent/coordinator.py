import os
import json
from google import genai
from utils.logger import log_trace
from agent.prompts import SYSTEM_PROMPT

class AgentCoordinator:
    def __init__(self):
        # We assume GEMINI_API_KEY is in the environment
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "your_gemini_api_key_here":
            raise ValueError("GEMINI_API_KEY is missing or invalid in .env")
        
        self.client = genai.Client(api_key=api_key)
        self.chat = self.client.chats.create(model="gemini-2.5-flash")
        
        # Initialize the chat with the system prompt context
        self.send_message(f"System Context:\n{SYSTEM_PROMPT}\n\nAcknowledge system context. Reply with 'OK'.")

    def send_message(self, message: str) -> str:
        """Send a message to the agent and maintain memory."""
        log_trace("Agent: Message IN", message)
        
        try:
            # We use gemini-2.5-flash for speed and cost-effectiveness
            response = self.chat.send_message(message)
            log_trace("Agent: Message OUT", response.text)
            return response.text
        except Exception as e:
            log_trace("Agent Error", str(e))
            raise Exception(f"LLM Error: {e}")

    def analyze_fit(self, cv_text: str, jd_text: str) -> dict:
        """Trigger the main analysis CoT flow."""
        prompt = (
            f"Please evaluate the candidate based on the following documents.\n\n"
            f"--- CV TEXT ---\n{cv_text}\n\n"
            f"--- JOB DESCRIPTION ---\n{jd_text}\n\n"
            f"Output the exact JSON required by the system prompt."
        )
        
        raw_response = self.send_message(prompt)
        
        try:
            # Strip markdown code blocks if any
            clean_json = raw_response.replace("```json", "").replace("```", "").strip()
            parsed = json.loads(clean_json)
            log_trace("Agent: JSON Parsed", "Successfully parsed the JSON output.")
            return parsed
        except json.JSONDecodeError:
            log_trace("Agent Error", f"Failed to parse JSON. Raw response: {raw_response}")
            return {"error": "Failed to generate structured JSON. Please try again."}
