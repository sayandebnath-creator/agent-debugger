import os
import requests
import time  # used for latency measurement
import json  # used to enforce structured parsing
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL = os.getenv("MODEL", "llama3")

def estimate_tokens(text: str) -> int:
    # heuristic token estimator for efficiency scoring
    return max(1, len(text) // 4)

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
            }, timeout=60, # prevent hanging requests
        )
        # return response.json()["response"]
        response.raise_for_status()  # fail fast on API issues
        data = response.json()
        return data.get("response", "")

    def debug_code(self, code:str, error:str) -> dict: # type define
        start_time = time.time()  # start latency tracking
        prompt = f"""
        You are a senior software engineer debugging Python code.
        Think step-by-step internally but output ONLY valid JSON.

        Return schema strictly:
        {{
        "root_cause": "...",
        "fix": "...",
        "corrected_code": "..."
        }}

        Rules:
        - Minimal fix only
        - Do not rewrite entire code
        - Ensure corrected_code runs without error
        - No markdown, no backticks

        Code:
        {code}

        Error:
        {error}
        """
        raw = self._call_llm(prompt).strip()

        try:
            parsed = json.loads(raw)  # strict JSON parsing
            if not isinstance(parsed, dict) or "corrected_code" not in parsed:
                raise ValueError("Invalid schema")

            parsed.setdefault("root_cause", "unknown")  # schema safety
            parsed.setdefault("fix", "unknown")
            parsed.setdefault("corrected_code", code)
            parsed["latency"] = time.time() - start_time  # latency metric
            parsed["token_usage"] = estimate_tokens(code + error + raw)  # token metric
            return parsed
        except Exception:
            return {
                "error": "Invalid JSON",
                "raw": raw,
                "root_cause": "parse_failed",
                "fix": "retry_prompt",
                "corrected_code": code,
                "latency": time.time() - start_time,  # still track latency
                "token_usage": estimate_tokens(code + error),
            }