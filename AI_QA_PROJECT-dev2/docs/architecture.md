# System Architecture

## 1. Overview

The AI-powered self-healing test automation framework converts Markdown test
requirements into executable pytest tests. It supports two execution modes:

- UI testing with Playwright and Playwright MCP.
- API testing with Python `requests`.

The user selects the required mode when `main.py` starts. The framework then
loads the corresponding Markdown specification, asks Gemini to generate a
test, validates and executes the generated code, and attempts bounded
self-healing when failures occur.

## 2. Architecture Diagram

```text
                         +----------------------+
                         |        User          |
                         | Selects UI or API    |
                         +----------+-----------+
                                    |
                                    v
                         +----------------------+
                         |       main.py        |
                         | Orchestration layer  |
                         +----+------------+----+
                              |            |
              +---------------+            +----------------+
              |                                    |
              v                                    v
   +-----------------------+            +-----------------------+
        | Requirements File     |            | Gemini Classification |
        | requirements.txt      |            | API or UI             |
   +-----------+-----------+            +-----------+-----------+
               |                                    |
               v                                    v
   +-----------------------+            +-----------------------+
   | Playwright MCP        |            | Gemini API Client      |
   | Browser snapshot      |            | API test generation    |
   +-----------+-----------+            +-----------+-----------+
               |                                    |
               +----------------+-------------------+
                                v
                    +-------------------------+
                    |       ai_client.py      |
                    | Test generation/repair  |
                    +-----------+-------------+
                                |
                                v
                    +-------------------------+
                    | generated/tests/        |
                    | test_case.py            |
                    +-----------+-------------+
                                |
                                v
                    +-------------------------+
                    |   playwright_runner.py  |
                    | Validate, collect, run  |
                    +-----------+-------------+
                                |
                    +-----------+-----------+
                    |                       |
                    v                       v
          +-------------------+   +------------------------+
          | Test passed       |   | Test failed            |
          | Write reports     |   | Save history and repair |
          +-------------------+   +-----------+------------+
                                              |
                                              v
                                  +-------------------------+
                                  | Gemini repair request   |
                                  +------------+------------+
                                               |
                                               +----> Retry
```

## 3. Component Responsibilities

### 3.1 `main.py`

The orchestration layer is responsible for:

1. Asking the user to select UI or API testing.
2. Selecting the correct Markdown test suite.
3. Collecting a browser snapshot for UI mode.
4. Skipping browser collection for API mode.
5. Requesting generated test code from Gemini.
6. Writing the generated test to `generated/tests/test_case.py`.
7. Validating and executing the test.
8. Recording execution attempts.
9. Saving failed test versions.
10. Requesting repaired test code.
11. Retrying within `MAX_REPAIR_ATTEMPTS`.

### 3.2 `ai_client.py`

The AI client is responsible for:

- Loading the Gemini API key from environment variables.
- Selecting the configured Gemini model.
- Detecting or receiving the requested test type.
- Generating Playwright UI tests.
- Generating `requests` API tests.
- Repairing failed UI tests.
- Repairing failed API tests.
- Removing Markdown code fences from model responses.
- Handling transient model errors and quota errors.

Explicit mode selection from `main.py` is passed to the AI client so that UI
and API prompts are not confused.

### 3.3 `mcp_client.py`

The MCP client:

1. Starts the Playwright MCP server through `npx`.
2. Initializes an MCP client session.
3. Navigates to the target UI URL.
4. Requests a browser snapshot.
5. Converts the snapshot response into text.
6. Returns the snapshot to the AI generation layer.

The snapshot provides live UI context such as page text, roles, labels,
buttons, inputs, links, and visible application state.

### 3.4 `playwright_runner.py`

The runner provides:

- Python syntax validation.
- A check for at least one pytest test function.
- Pytest collection.
- Pytest execution.
- JUnit XML reporting.
- HTML reporting.
- Execution duration measurement.
- Failure classification.
- JSON report writing.

Although the module name references Playwright, it executes both generated
Playwright UI tests and generated `requests` API tests through pytest.

## 4. Test Specification Layer

The framework separates UI and API requirements into independent Markdown
files:

```text
test_cases/
└── requirements.txt
```

### UI specification

The UI specification describes browser actions and expected visible results,
including login, products, cart, checkout, orders, and logout.

### API specification

The API specification describes HTTP methods, endpoints, request data,
authentication, status codes, JSON fields, cart operations, and order
validation.

Separating the files avoids mixing browser instructions with REST API
instructions and makes the generated output more predictable.

## 5. Execution Modes

### 5.1 UI Mode

```text
User selects UI
        |
        v
Load requirements.txt
        |
        v
Extract application URL
        |
        v
Collect browser snapshot through MCP
        |
        v
Send requirements and snapshot to Gemini
        |
        v
Generate Playwright pytest code
        |
        v
Validate and execute generated test
```

UI mode is intended for browser-visible behavior. Generated tests should use
Playwright locators, page assertions, navigation checks, and browser cleanup.

### 5.2 API Mode

```text
User selects API
        |
        v
Classify API requirements from requirements.txt
        |
        v
Skip browser snapshot collection
        |
        v
Send API requirements to Gemini
        |
        v
Generate requests pytest code
        |
        v
Validate and execute generated test
```

API mode is intended for HTTP behavior. Generated tests should use
`requests.Session`, runtime authentication data, status-code assertions, and
JSON response assertions.

## 6. Generated Test Lifecycle

The generated file is stored at:

```text
generated/tests/test_case.py
```

The lifecycle is:

1. Generate code from the selected Markdown suite.
2. Write the code to the generated test path.
3. Compile the source with Python.
4. Confirm that a `test_...` function exists.
5. Run pytest collection.
6. Run the collected tests.
7. Write execution results to reports.

The generated file is a working artifact and may contain either UI or API
tests depending on the mode selected for the latest run.

## 7. Self-Healing Architecture

The self-healing loop is bounded and controlled:

```text
Generate test
     |
     v
Validate and execute
     |
  Passed? -------- Yes --------> Finish successfully
     |
     No
     v
Save failed version
     |
     v
Send requirements, code, and failure to Gemini
     |
     v
Write repaired code
     |
     v
Retry until pass or retry limit
```

The retry count is configured by:

```env
MAX_REPAIR_ATTEMPTS=3
```

The framework does not retry indefinitely. This prevents uncontrolled model
usage, repeated identical repairs, and unexpected execution costs.

Failed versions are stored under:

```text
generated/tests/history/
```

## 8. Failure Classification

The runner classifies failures into categories including:

- `blocked_network`
- `blocked_ai_quota`
- `blocked_credentials`
- `failed_test`

This classification helps distinguish an application/test failure from an
environment or service availability problem.

## 9. Reporting Architecture

Reports are stored under:

```text
reports/
```

The framework produces:

| Report | Purpose |
|---|---|
| `test_report.json` | Attempt history, status, classification, output, and duration |
| `test-report.html` | Human-readable pytest HTML report |
| `test-results.xml` | JUnit-compatible report for CI systems |
| `artifacts/` | Screenshots and related test artifacts when produced |

Each repair attempt is recorded in the JSON report.

## 10. Configuration and Secret Flow

Secrets are loaded from `.env` through `python-dotenv`:

```text
.env
  |
  v
ai_client.py / generated tests
  |
  v
Gemini requests or application authentication
```

Expected configuration includes:

```env
GEMINI_API_KEY=<active-key>
GEMINI_MODEL=<model-name>
TEST_EMAIL=<test-account-email>
TEST_PASSWORD=<test-account-password>
API_BASE_URL=<optional-api-base-url>
MAX_REPAIR_ATTEMPTS=3
```

The `.env` file is excluded through `.gitignore` and must not be committed.
Generated tests should use environment variables rather than embedding
credentials or tokens.

## 11. External Dependencies

### Python dependencies

Defined in `requirements.txt`:

- `openai`
- `python-dotenv`
- `mcp`
- `pytest`
- `pytest-html`
- `playwright`
- `requests`

### Node dependency

Defined in `package.json`:

- `@playwright/mcp`

### External services

- Gemini-compatible API endpoint.
- Playwright MCP package.
- Target UI application or API.
- Network access to the application under test.

## 12. Runtime Sequence

```text
1. Start main.py
2. Select UI or API mode
3. Load the matching Markdown file
4. Collect UI snapshot if UI mode is selected
5. Request generated code from Gemini
6. Save generated test
7. Compile generated Python
8. Run pytest collection
9. Execute tests
10. Write reports
11. If failed, save history version
12. Request repair from Gemini
13. Retry within configured limit
14. Return final status
```

## 13. Design Principles

The architecture follows these principles:

- Requirements and orchestration are separated.
- UI and API test specifications are separated.
- Test generation is isolated in the AI client.
- Browser context is provided only when useful for UI testing.
- Generated code is validated before execution.
- Failures are visible and classified.
- Repair attempts are bounded.
- Secrets are externalized.
- Runtime identifiers are captured instead of fabricated.
- Test history is preserved for diagnosis.

## 14. Current Architectural Limitations

- Browser network requests are not automatically captured by the current MCP
  client; API testing relies on the API Markdown specification.
- Generated code still requires review for critical workflows.
- Live UI selectors and API contracts may change.
- Gemini availability and quota affect generation and repair.
- The generated test path contains only the latest selected mode's output.
- Full end-to-end execution requires valid credentials, network access, and
  active external services.

## 15. Future Architecture Enhancements

Possible future improvements include:

1. Automatic browser request and response capture.
2. HAR/network trace input for API test generation.
3. Separate generated output paths for UI and API suites.
4. CI/CD execution with environment-specific configuration.
5. Secure secret-manager integration.
6. Parallel test execution.
7. Persistent result storage and trend dashboards.
8. Stronger validation that generated code matches the selected mode.
9. Test tagging and selective scenario execution.
10. Pluggable model providers.
