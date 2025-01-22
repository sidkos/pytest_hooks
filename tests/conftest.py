import linecache
import sys
import uuid
from types import FrameType
from typing import Callable, Dict, List, Optional

import pytest
from _pytest.main import Session
from _pytest.nodes import Item

from src.clients.petstore_client.petstore_client import PetStoreClient
from src.clients.redis_client.redis_client import RedisClient
from src.helpers.tool_box import random_id, random_string
from src.models.category import Category
from src.models.pet import Pet
from src.models.tag import Tag

# Define the type for the trace function
TraceFunctionType = Callable[[FrameType, str, object], Optional["TraceFunctionType"]]

# Global variables for Redis and execution tracking
execution_id: Optional[str] = None
current_test_case_id: Optional[str] = None


def trace_lines(redis_client: RedisClient, frame: FrameType, event: str, arg: object) -> Optional[TraceFunctionType]:
    global execution_id, current_test_case_id

    if event == "line" and execution_id and current_test_case_id:
        code = frame.f_code
        lineno = frame.f_lineno
        filename = code.co_filename
        function_name = code.co_name

        if function_name.startswith("test_"):
            line = linecache.getline(filename, lineno).strip()
            simple_filename = filename.split("/")[-1]

            key = f"{execution_id}:{current_test_case_id}"
            step_number = int(redis_client.get(f"{key}:step_number") or "0") + 1
            redis_client.post(f"{key}:step_number", str(step_number))
            redis_client.post(f"{key}:{step_number}", f"{simple_filename}:{line}")

    return lambda f, e, a: trace_lines(redis_client, f, e, a)


def pytest_runtest_call(item: Item) -> None:
    global current_test_case_id

    # Determine the test case ID
    current_test_case_id = item.name
    print(f"\n[pytest] Starting test case: {current_test_case_id}")

    # Use RedisClient and keep it active for the test's duration
    redis_client = RedisClient()
    redis_client.__enter__()
    sys.settrace(lambda f, e, a: trace_lines(redis_client, f, e, a))

    # Store the Redis client for teardown
    setattr(item, "_redis_client", redis_client)  # Dynamically add _redis_client


def pytest_runtest_teardown(item: Item, nextitem: Optional[Item]) -> None:
    sys.settrace(None)
    print(f"[pytest] Finished test case: {item.name}")

    # Close Redis connection after the test
    redis_client = getattr(item, "_redis_client", None)
    if redis_client:
        redis_client.__exit__(None, None, None)  # Explicitly close the RedisClient


def pytest_sessionstart(session: Session) -> None:
    global execution_id
    execution_id = str(uuid.uuid4())
    print(f"\n[pytest] Session execution UUID: {execution_id}")


def pytest_sessionfinish(session: Session, exitstatus: int) -> None:
    global execution_id

    print(f"\n[pytest] Finished session with execution ID: {execution_id}")
    print("\n[pytest] Final Report:")

    with RedisClient() as redis_client:
        keys = redis_client.keys(f"{execution_id}:*")
        test_steps: Dict[str, List[str]] = {}  # Explicit type annotation

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


@pytest.fixture(scope="function", name="random_pet")
def generate_pet(random_tag: Tag, random_category: Category, status: str = "available") -> Pet:
    return Pet(
        id=random_id(),
        name=f"pet_{random_string()}",
        category=random_category,
        photo_urls=["https://example.com/buddy1.jpg", "https://example.com/buddy2.jpg"],
        tags=[random_tag],
        status=status,
    )


@pytest.fixture(scope="function", name="random_tag")
def generate_tag() -> Tag:
    return Tag(
        id=random_id(),
        name=str(uuid.uuid4()),
    )


@pytest.fixture(scope="function", name="random_category")
def generate_category() -> Category:
    return Category(id=random_id(), name=str(uuid.uuid4()))


@pytest.fixture(scope="session", name="pet_store_client")
def pet_store_client() -> PetStoreClient:
    return PetStoreClient()
