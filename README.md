# AI Debugging Agent (Ollama + Llama3)

## Overview
Specialized AI agent for debugging Python errors using structured reasoning and execution validation.

## Features
- Root cause detection
- Minimal fixes
- JSON structured outputs
- Execution validation (sandboxed)

## Problem Specialization

This agent is specialized for debugging runtime errors in Python code.

### Why this problem?
Debugging consumes a significant portion of developer time and is highly repetitive.

### Why prioritize it?
- High frequency in real-world development
- Measurable outcomes (code runs or fails)
- Existing LLMs are generic and not execution-validated

This agent focuses on:
- Root cause identification
- Minimal code fixes
- Execution validation

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

## API Usage

```bash
curl -X POST http://127.0.0.1:8000/debug \
-H "Content-Type: application/json" \
-d '{"code":"print(x)","error":"NameError"}'

---

# 📂 4. Create `.gitignore` (root folder) or already given in this repo

Paste:

```gitignore
.env
__pycache__/
*.pyc
evaluation_results.json
detailed_results.json