import os
import requests
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL = os.getenv("MODEL", "llama3")

class DebugAgent:
    def __init__(self):
        self.model = MODEL

    def _call_llm(self, prompt):
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
        )
        return response.json()["response"]

    def debug_code(self, code, error):
        prompt = f"""
You are an expert debugging assistant.

Code:
{code}

Error:
{error}

Tasks:
1. Identify root cause
2. Suggest minimal fix
3. Provide corrected code
4. Explain briefly
"""
        return self._call_llm(prompt)