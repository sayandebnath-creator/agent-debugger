import os
import re
import requests
import time  # used for latency measurement
import json  # used to enforce structured parsing
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_BASE_URL")
MODEL = os.getenv("MODEL")

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
        - Ensure corrected_code is valid Python syntax
        - Do not use semicolons for loops or control structures
        - Use proper indentation and new lines for blocks (for, if, etc.)
        - Preserve existing variables and context unless necessary to change

        Code:
        {code}

        Error:
        {error}
        """
        raw = self._call_llm(prompt).strip()

        try:
            # fix unescaped newlines inside JSON strings
            raw = raw.replace('\r', '')

            raw = re.sub(
                r'("corrected_code"\s*:\s*")(.*?)(")',
                lambda m: m.group(1) + m.group(2).replace('\n', '\\n') + m.group(3),
                raw,
                flags=re.DOTALL
            )
            parsed = json.loads(raw)  # strict JSON parsing
            # clean triple-quoted code
            code_out = parsed.get("corrected_code", "")

            if isinstance(code_out, str):
                code_out = code_out.strip()
                if code_out.startswith('"""') and code_out.endswith('"""'):
                    code_out = code_out[3:-3].strip()

            parsed["corrected_code"] = code_out
            if not isinstance(parsed, dict) or "corrected_code" not in parsed:
                raise ValueError("Invalid schema")

            parsed.setdefault("root_cause", "unknown")  # schema safety
            parsed.setdefault("fix", "unknown")
            parsed.setdefault("corrected_code", code)
            parsed["latency"] = time.time() - start_time  # latency metric
            parsed["token_usage"] = estimate_tokens(code + error + raw)  # token metric

            return parsed
        except Exception:
            # attempt recovery from malformed JSON
            try:
                # extract JSON block if extra text exists
                json_match = re.search(r"\{.*\}", raw, re.DOTALL)
                # if json_match:
                #     parsed = json.loads(json_match.group())
                if not json_match:
                    raise ValueError("No JSON found")

                json_str = json_match.group()

                # fix unescaped newlines in corrected_code
                json_str = re.sub(
                    r'("corrected_code"\s*:\s*")(.*?)(")',
                    lambda m: m.group(1) + m.group(2).replace('\n', '\\n') + m.group(3),
                    json_str,
                    flags=re.DOTALL
                )

                parsed = json.loads(json_str)

                # repeat cleanup logic (same as main path)
                code_out = parsed.get("corrected_code", "")

                if isinstance(code_out, str):
                    code_out = code_out.strip()
                    if code_out.startswith('"""') and code_out.endswith('"""'):
                        code_out = code_out[3:-3].strip()

                parsed["corrected_code"] = code_out

                parsed.setdefault("root_cause", "unknown")
                parsed.setdefault("fix", "unknown")
                parsed.setdefault("corrected_code", code)
                parsed["latency"] = time.time() - start_time
                parsed["token_usage"] = estimate_tokens(code + error + raw)

                return parsed
                # else:
                #     raise ValueError("No JSON found")
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