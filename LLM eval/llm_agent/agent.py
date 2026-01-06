import re
from llm_agent.tools import TOOL_REGISTRY
from llm_agent.memory import Memory


def extract_numbers(text: str):
    return list(map(int, re.findall(r"-?\d+", text)))


class Agent:
    def __init__(self):
        self.memory = Memory()

    def decide_next_action(self, user_input: str):
        numbers = extract_numbers(user_input)
        text = user_input.lower()

        if not numbers:
            return None

        # CASE 1: sqrt of a single number
        if "square root" in text and len(numbers) == 1:
            if "done" not in self.memory.short_term:
                return {
                    "tool": "square_root",
                    "args": {"value": numbers[0]},
                    "state_flag": "done"
                }

        # CASE 2: sqrt of expression (25 + 75)
        if "square root" in text and len(numbers) > 1:
            if "add_done" not in self.memory.short_term:
                expr = " + ".join(map(str, numbers))
                return {
                    "tool": "calculate_expression",
                    "args": {"expression": expr},
                    "state_flag": "add_done"
                }

            if "add_done" in self.memory.short_term and "sqrt_done" not in self.memory.short_term:
                return {
                    "tool": "square_root",
                    "args": {"value": self.memory.get_stm("last_result")},
                    "state_flag": "sqrt_done"
                }

        return None

    def run(self, user_input: str):
        steps = 0

        while True:
            decision = self.decide_next_action(user_input)

            if decision is None:
                result = self.memory.get_stm("last_result")
                self.memory.clear_stm()

                if result is None:
                    return "Cannot compute the result"

                return f"Final Answer: {result}"

            try:
                tool_fn = TOOL_REGISTRY[decision["tool"]]
                result = tool_fn(**decision["args"])
            except Exception as e:
                self.memory.clear_stm()
                return str(e)

            self.memory.set_stm("last_result", result)
            self.memory.set_stm(decision["state_flag"], True)

            steps += 1
            if steps > 5:
                raise RuntimeError("Agent exceeded max steps")
