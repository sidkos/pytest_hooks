import os
import random
from typing import Dict, List

from src.clients.redis_client.redis_client import RedisClient


def random_id(max_length: int = 3) -> int:
    length = random.randint(1, max_length)
    return random.randint(1, (10**length - 1))


def random_string(max_length: int = 5) -> str:
    length = random.randint(1, max_length)
    return "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=length))


def print_report() -> None:
    execution_id = os.getenv("EXECUTION_ID")

    with RedisClient() as redis_client:
        keys = redis_client.keys(f"{execution_id}:*")
        test_steps: Dict[str, List[str]] = {}

        # Group steps by test name
        for key in keys:
            if key.endswith(":step_number"):
                continue  # Skip step number keys

            # Extract test name from key
            parts = key.split(":")
            if len(parts) < 3:
                continue  # Skip invalid keys
            test_name = parts[1]

            if test_name not in test_steps:
                test_steps[test_name] = []

            # Add step content to test_steps
            step_content = redis_client.get(key)
            if step_content:
                test_steps[test_name].append(step_content)

        # Print the grouped steps in a structured format
        for test_name, steps in test_steps.items():
            print(f"\n{test_name}:")
            for idx, step in enumerate(steps, start=1):
                print(f"  Step {idx}: {step}")
