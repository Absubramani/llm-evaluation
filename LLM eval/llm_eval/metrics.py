import json
import re

def normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9.]", "", text.lower())

def exact_match(output: str, expected: str) -> bool:
    return normalize(expected) in normalize(output)
def heuristic_length(output: str, min_len=1, max_len=200) -> bool:
    return min_len <= len(output) <= max_len

def run_evaluation(agent, test_cases_path: str):
    with open(test_cases_path) as f:
        test_cases = json.load(f)

    results = []
    passed = 0

    for case in test_cases:
        output = agent.run(case["input"])
        exact_ok = exact_match(output, case["expected"])
        length_ok = heuristic_length(output)

        if exact_ok:
            passed += 1

        results.append({
            "id": case["id"],
            "input": case["input"],
            "output": output,
            "expected": case["expected"],
            "exact_match": exact_ok,
            "length_ok": length_ok
        })

    return {
        "total": len(test_cases),
        "exact_match_accuracy": passed / len(test_cases),
        "results": results
    }
