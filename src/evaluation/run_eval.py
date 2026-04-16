import json
import time  # used for extended evaluation if needed
from agent import DebugAgent
from executor import run_code  # execution validation integration
from metrics import calculate_score

agent = DebugAgent()

with open("../../tests/benchmark_cases.json") as f:
    cases = json.load(f)

success = 0
execution_success = 0
total_latency = 0
total_tokens = 0

for case in cases:
    result = agent.debug_code(case["code"], case["error"])

    total_latency += result.get("latency", 0)  # accumulate latency
    total_tokens += result.get("token_usage", 0)  # accumulate token usage

    # structured correctness check
    if "corrected_code" in result and result.get("error") != "Invalid JSON":
        success += 1

    ok, err = run_code(result.get("corrected_code", ""))  # actual execution test
    if ok:
        execution_success += 1

n = max(1, len(cases))
fix_accuracy = success / n
execution_rate = execution_success / n

# efficiency scoring (lower tokens = better)
token_efficiency = min(1.0, 500 / (total_tokens + 1))

# latency scoring (lower latency = better)
avg_latency = total_latency / n
latency_score = max(0.0, 1.0 - avg_latency)

final_score = calculate_score(
    fix_accuracy,
    execution_rate,
    token_efficiency,
    latency_score,
)

print({
    "avg_latency": avg_latency,
    "total_tokens": total_tokens,
    "fix_accuracy": fix_accuracy,
    "execution_rate": execution_rate,
    "final_score": final_score
})