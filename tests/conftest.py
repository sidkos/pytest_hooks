import linecache
import sys
import uuid
from types import FrameType
from typing import Callable, Dict, List, Optional

import pytest
from _pytest.main import Session
from _pytest.nodes import Item

from src.clients.petstore_client.petstore_client import PetStoreClient
from src.helpers.tool_box import random_id, random_string
from src.models.category import Category
from src.models.pet import Pet
from src.models.tag import Tag

# Define the type for the trace function
TraceFunctionType = Callable[[FrameType, str, object], Optional["TraceFunctionType"]]

# Data structure to store the trace logs for each execution ID
execution_traces: Dict[str, Dict[str, List[Dict[str, str]]]] = {}

# Global variable to store the current execution ID
execution_id: Optional[str] = None
current_test_case_id: Optional[str] = None


def trace_lines(frame: FrameType, event: str, arg: object) -> Optional[TraceFunctionType]:
    global execution_id, current_test_case_id

    if event == "line" and execution_id and current_test_case_id:
        code = frame.f_code
        lineno = frame.f_lineno
        filename = code.co_filename
        function_name = code.co_name

        # Filter to trace only lines within the current test function
        if function_name.startswith("test_"):
            line = linecache.getline(filename, lineno).strip()

            # Simplify the filename (remove full path)
            simple_filename = filename.split("/")[-1]

            # Initialize the test case trace logs
            if current_test_case_id not in execution_traces[execution_id]:
                execution_traces[execution_id][current_test_case_id] = []

            # Append the line to the test case traces
            execution_traces[execution_id][current_test_case_id].append(
                {
                    "line_number": str(
                        len(execution_traces[execution_id][current_test_case_id]) + 1
                    ),  # Convert to string
                    "filename": simple_filename,
                    "code": line,
                }
            )

    return trace_lines


def pytest_runtest_call(item: Item) -> None:
    """
    Hook called before running a test.

    Args:
        item (Item): The pytest test item object.
    """
    global current_test_case_id

    # Determine the test case ID
    current_test_case_id = item.name  # Use the test function name with parameters for uniqueness
    print(f"\n[pytest] Starting test case: {current_test_case_id}")
    sys.settrace(trace_lines)


def pytest_runtest_teardown(item: Item, nextitem: Optional[Item]) -> None:
    """
    Hook called after finishing a test.

    Args:
        item (Item): The pytest test item object.
        nextitem (Optional[Item]): The next test item object or None if it's the last test.
    """
    sys.settrace(None)
    print(f"[pytest] Finished test case: {item.name}")


def pytest_sessionstart(session: Session) -> None:
    """
    Hook to generate a unique execution ID for the pytest session.

    Args:
        session (Session): The pytest session object.
    """
    global execution_id
    execution_id = str(uuid.uuid4())
    setattr(session.config, "execution_id", execution_id)
    print(f"\n[pytest] Session execution UUID: {execution_id}")
    execution_traces[execution_id] = {}


def pytest_sessionfinish(session: Session, exitstatus: int) -> None:
    """
    Hook called after the entire test session ends.

    Args:
        session (Session): The pytest session object.
        exitstatus (int): The exit status of the test session.
    """
    global execution_id
    print(f"\n[pytest] Finished session with execution ID: {execution_id}")
    print(f"\n[pytest] Final Trace Data for Execution ID {execution_id}:")
    print(execution_traces)


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
