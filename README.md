# AI Debugging Agent (Ollama + Llama3)

## Overview
Specialized AI agent for debugging Python errors using structured reasoning and execution validation.

## Features
- Root cause detection
- Minimal fixes
- JSON structured outputs
- Execution validation (sandboxed)

## Setup
```bash
pip install -r requirements.txt
cp .env.example .env
uvicorn src.main:app --reload
```

## Example
Input:
{
  "code": "print(x)",
  "error": "NameError"
}

Output:
{
  "root_cause": "x is not defined",
  "fix": "define x before use",
  "corrected_code": "x = 0\nprint(x)"
}

## Evaluation Method
Score =
(0.4 × Fix Accuracy) +
(0.2 × Execution Success) +
(0.2 × Token Efficiency) +
(0.2 × Latency)

Scaled to 10,000

## Benchmark vs Claude (Example)
| Case | Claude | Agent |
|------|--------|-------|
| IndexError | try/except | fixed loop bound |
| NameError | vague hint | explicit fix |
| ZeroDivision | explanation | safe guard |

## Design Decisions
- Ollama for local inference
- Structured JSON output for deterministic evaluation
- Execution-based validation to reduce hallucinations

## Cursor Integration
Uses `.cursorrules` to enforce minimal, safe, and testable fixes