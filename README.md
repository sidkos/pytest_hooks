# pytest_hooks: Petstore API Testing

This project demonstrates how to use pytest hooks to create custom reports while testing the **Petstore Swagger API**. The goal is to provide an example of combining **pytest hooks** and **Redis-based tracing** to track the execution of test cases and generate detailed insights into API interactions.

---

## **Overview**
This project leverages publicly available APIs from the **Petstore Swagger API**, which is designed as an example for practicing API interactions. The test suite uses `pytest` for:

- Parametrized API testing.
- Tracing test execution line-by-line with custom tracking (Redis-based).
- Hooking into pytest events to generate a tailored testing report.

---

## **API Information**
- **Base URL:** `https://petstore.swagger.io/v2`
- **Endpoints Covered:**
  - `/pet` (Pet-related operations)
  - `/store/order` (Order-related operations)
  - `/user` (User-related operations)
- **Documentation:** [Petstore API Docs](https://petstore.swagger.io/)

---

## **Features**

### 1. **Custom Reporting with pytest Hooks**
- Utilizes the `pytest_runtest_call` hook to track test execution dynamically.
- Logs the following details into a Redis database:
  - Test case name.
  - Execution line number and content.
  - Test steps with associated Redis keys for easy retrieval.
- Custom tracing ensures detailed insights into what happens during each test execution.

### 2. **Integration with Redis**
- Logs each line executed during a test case to a Redis database for real-time tracking and reporting.
- Stores information in the format:
  - `execution_id:test_case_id:step_number` (for line content).

### 3. **Dynamic Test Parameterization**
- Uses `@pytest.mark.parametrize` to dynamically test various attributes of a pet, such as `name`, `category`, `photo_urls`, and `status`.
- Example parameterized test:
  ```python
  @pytest.mark.parametrize(
      "attribute, updated_value",
      [
          pytest.param("name", random_string(), marks=pytest.mark.sanity),
          ("category", Category(id=random_id(), name=random_string())),
          ("photo_urls", [f"https://example.com/{random_string()}.jpg"]),
          ("tags", [Tag(id=random_id(), name=random_string())]),
          ("status", "sold"),
      ],
      ids=[
          "Update name",
          "Update category",
          "Update photo URLs",
          "Update tags",
          "Update status",
      ],
  )
  def test_update_pet(attribute, updated_value):
      # Implementation of the test
      pass
  ```

### 4. **Test Tracing with `sys.settrace`**
- Hooks into Python’s tracing mechanism using:
  ```python
  sys.settrace(lambda f, e, a: trace_lines(redis_client, f, e, a))
  ```
- Tracks and logs each line executed during a test case using the `trace_lines` function.

### 5. **Detailed Reporting with Hooks**
- The `pytest_runtest_call` hook initializes Redis, sets up tracing, and attaches the Redis client to each test item.
- Example:
  ```python
  def pytest_runtest_call(item: Item) -> None:
      global current_test_case_id

      current_test_case_id = item.name
      print(f"\n[pytest] Starting test case: {current_test_case_id}")

      redis_client = RedisClient()
      redis_client.__enter__()
      sys.settrace(lambda f, e, a: trace_lines(redis_client, f, e, a))

      setattr(item, "_redis_client", redis_client)
  ```

---

## **Setup Instructions**

### Clone the Repository
```bash
git clone https://github.com/your-repo/pytest_hooks
cd pytest_hooks
```

### Prerequisites
- Python 3.11 or higher.
- Install required dependencies:
  ```bash
  pip install -r requirements.txt
  ```

### Environment Setup
1. Ensure Redis is running locally or provide a connection to a Redis instance.
2. Set up the required API credentials (if any).

---

## **Running Tests**

Run the tests with:
```bash
pytest
```

### Run Specific Tests
Run only sanity-marked tests:
```bash
pytest -m sanity
```

### Generate a Verbose Report
```bash
pytest -v
```

---

## **Continuous Integration and Continuous Deployment (CI/CD)**

This project includes CI/CD workflows to automate code quality checks, testing, and deployment using GitHub Actions. Below is a description of the workflows:

1. **Static Code Analysis**:
   - Ensures the codebase adheres to quality standards by running tools like `black`, `isort`, `pycodestyle`, `flake8`, `mypy`, and `yamllint`.
   - This helps catch formatting issues, syntax errors, and type inconsistencies before code is merged.

2. **Continuous Integration (CI)**:
   - Runs the static code analysis workflow automatically on every push or manual trigger.
   - Ensures that the codebase remains clean and compliant with coding standards.

3. **Test Workflow**:
   - Executes all test cases in the repository using pytest.
   - Uses Docker Compose to set up any required dependencies (e.g., Redis).
   - Logs the execution results and generates reports for debugging.

---

## **How It Works**

1. **Initialization**:
   - Redis is initialized and connected before each test case using the `pytest_runtest_call` hook.
2. **Test Execution**:
   - Each line executed in the test case is traced using `trace_lines` and logged to Redis.
3. **Custom Report**:
   - Test steps are logged with Redis keys for debugging or custom reporting purposes.

---

## **Contributing**
Feel free to fork the repository and contribute with pull requests. Suggestions and feedback are always welcome!

---

## **License**
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## **Acknowledgments**
- **Swagger Petstore API** for providing the example API.
- **pytest** for the powerful testing framework.
- **Redis** for enabling real-time tracing and logging.

