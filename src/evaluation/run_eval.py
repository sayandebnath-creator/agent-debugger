import json
import os
from src.agent import DebugAgent

agent = DebugAgent()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
file_path = os.path.join(BASE_DIR, "tests", "benchmark_cases.json")

with open(file_path) as f:
    cases = json.load(f)

results = []

for case in cases:
    output = agent.debug_code(case["code"], case["error"])
    results.append({
        "input": case,
        "output": output
    })

print(results)