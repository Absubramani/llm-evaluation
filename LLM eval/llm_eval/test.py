import sys
import os
import json

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from llm_agent.agent import Agent
from llm_eval.metrics import run_evaluation

agent = Agent()
summary = run_evaluation(agent, "llm_eval/test_cases/golden.json")

with open("llm_eval/dashboards/results.json", "w") as f:
    json.dump(summary, f, indent=2)

print(summary)
