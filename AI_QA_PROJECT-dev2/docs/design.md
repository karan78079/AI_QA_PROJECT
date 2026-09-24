# Software Design Document

## 1. Purpose

This document describes the software design of the AI-powered self-healing
test automation framework. It explains how the framework is organized, how
users interact with it, how data moves through the system, and why the main
design decisions were made.

## 2. Design Goals

The design aims to provide:

1. Simple test definition through Markdown.
2. Support for both UI and REST API testing.
3. Clear separation between UI and API workflows.
4. AI-assisted test generation.
5. Bounded self-healing after test failures.
6. Safe handling of credentials and runtime data.
7. Test validation before execution.
8. Useful reports for engineers and managers.
9. Easy extension to additional applications and test scenarios.

## 3. Design Overview

The framework follows a pipeline design:

```text
Test requirements
        |
        v
        Gemini classification and human review
        |
        v
Context collection
        |
        v
AI test generation
        |
        v
Source validation
        |
        v
Pytest collection and execution
        |
        v
Reporting
        |
        +----> Repair and retry when required
```

The framework is divided into five logical layers:

| Layer | Responsibility |
|---|---|
| Requirement layer | Stores UI and API scenarios in one user-authored requirements file |
| Orchestration layer | Classifies, reviews, and controls the complete lifecycle |
| Context layer | Collects browser context for UI generation |
| AI layer | Generates and repairs test code |
| Execution layer | Validates, runs, classifies, and reports test results |

## 4. Main Design Components

### 4.1 Requirement Layer

The requirement layer uses one user-authored file:

```text
test_cases/requirements.txt
```

Gemini classifies the requirements as API or UI and splits them into
independently reviewable scenarios. Set `TEST_REQUIREMENTS_FILE` to use a
different file. The root `requirements.txt` remains reserved for dependencies.

The UI file contains browser behavior such as:

- Login
- Product listing
- Cart
- Checkout
- Orders
- Logout

The API file contains HTTP behavior such as:

- Authentication
- Product selection
- Cart operations
- Cart count validation
- Order creation
- Order-history validation

The user can approve all scenarios, approve selected IDs, reject selected IDs,
reject the complete plan, or add a manual scenario before Gemini generates
executable code.

### 4.2 Orchestration Layer

[main.py](C:/Users/Jatin/OneDrive/Desktop/Final_project/AI_QA_AGENT/main.py)
controls the workflow.

Responsibilities:

- Load the single requirements file.
- Ask Gemini to classify and split the requirements.
- Review approved, rejected, and manually added scenarios.
- Collect a browser snapshot only in UI mode.
- Request generated test code.
- Save the latest generated test.
- Validate and execute the test.
- Record attempts.
- Start repair cycles when a test fails.

The orchestrator does not contain application-specific selectors or API
request details. Those details remain in the Markdown requirements and model
context.

### 4.3 Context Layer

[mcp_client.py](C:/Users/Jatin/OneDrive/Desktop/Final_project/AI_QA_AGENT/mcp_client.py)
provides browser context for UI generation.

The context flow is:

```text
UI application URL
        |
        v
Playwright MCP
        |
        v
Browser navigation
        |
        v
Browser snapshot
        |
        v
Gemini UI-generation prompt
```

API mode skips this layer because API tests do not require a browser snapshot.

### 4.4 AI Layer

[ai_client.py](C:/Users/Jatin/OneDrive/Desktop/Final_project/AI_QA_AGENT/ai_client.py)
provides generation and repair functions.

The AI layer has separate responsibilities for:

- UI test generation
- API test generation
- UI test repair
- API test repair
- Response cleanup
- Transient model error handling

The classified mode is passed explicitly to the generation function. This
keeps API and UI prompts separate after classification.

### 4.5 Execution Layer

[playwright_runner.py](C:/Users/Jatin/OneDrive/Desktop/Final_project/AI_QA_AGENT/playwright_runner.py)
provides mode-independent pytest execution.

Responsibilities:

- Compile generated Python.
- Confirm that pytest test functions exist.
- Run pytest collection.
- Execute collected tests.
- Capture output and duration.
- Generate HTML and JUnit reports.
- Classify failures.
- Write JSON attempt history.

The runner does not decide whether a test is UI or API. It executes the
generated pytest file produced by the selected mode.

## 5. User Interaction Design

The application uses a simple command-line review interaction:

```text
Review action: [a] approve all [p] approve specific [s] reject specific [m] add manual test [r] reject all [e] execute approved
```

### UI selection

When Gemini classifies the requirements as UI:

1. The user reviews the generated scenarios.
2. The application finds the application URL.
3. It collects a Playwright MCP snapshot.
4. It generates Playwright pytest code for approved scenarios.
5. It writes `reports/ui_testing_report.json` and executes the tests.

### API selection

When Gemini classifies the requirements as API:

1. The user reviews the generated scenarios.
2. Browser snapshot collection is skipped.
3. It generates `requests` pytest code for approved scenarios.
4. It writes `reports/api_testing_report.json` and executes the tests.

## 6. Data Flow Design

### 6.1 UI Data Flow

```text
requirements.txt
        +
browser snapshot
        |
        v
Gemini
        |
        v
generated/tests/test_case.py
        |
        v
pytest + Playwright
        |
        v
reports/
```

### 6.2 API Data Flow

```text
requirements.txt
        |
        v
Gemini
        |
        v
generated/tests/test_case.py
        |
        v
pytest + requests
        |
        v
reports/
```

### 6.3 Repair Data Flow

```text
Generated test
        +
Failure output
        +
Original requirements
        +
Browser snapshot when applicable
        |
        v
Gemini repair request
        |
        v
Repaired generated test
        |
        v
Retry execution
```

## 7. Generated-Test Design

The framework intentionally stores the latest generated test in one standard
location:

```text
generated/tests/test_case.py
```

This gives the runner a stable path regardless of the selected mode. The
latest file may contain either:

- Playwright UI tests, or
- `requests` API tests.

Failed versions are preserved separately:

```text
generated/tests/history/
```

This makes the latest output easy to execute while retaining repair history
for diagnosis.

## 8. Configuration Design

Configuration is externalized through environment variables:

```env
GEMINI_API_KEY=<active-key>
GEMINI_MODEL=<model-name>
TEST_EMAIL=<approved-test-email>
TEST_PASSWORD=<approved-test-password>
API_BASE_URL=<optional-api-url>
MAX_REPAIR_ATTEMPTS=3
```

Design rationale:

- Prevent secrets from entering source code.
- Allow the same code to run in different environments.
- Support local development and CI/CD execution.
- Make test credentials replaceable without editing requirements.

## 9. Error-Handling Design

The framework separates errors into:

### Generation errors

Examples:

- Missing Gemini API key
- Empty model response
- Gemini quota exhaustion
- Temporary model service errors

### Validation errors

Examples:

- Invalid Python syntax
- Missing pytest test function
- Failed pytest collection

### Runtime test failures

Examples:

- Locator or assertion failure
- API status-code failure
- Invalid response structure
- Authentication failure

### Environment blocking conditions

Examples:

- Network unavailable
- Test environment unavailable
- Required credentials missing
- Approved test data unavailable

The final report records the status and classification rather than hiding the
failure behind a successful-looking fallback.

## 10. Self-Healing Design

The self-healing feature is designed as bounded feedback:

```text
Execute
  |
  +-- Pass --> Finish
  |
  +-- Fail --> Save version
                 |
                 v
              Repair
                 |
                 v
              Retry
```

The repair request contains:

- Original test requirements
- Current generated code
- Failure output
- Browser snapshot for UI scenarios

The repair process must preserve:

- Test objective
- Required scenario coverage
- Security rules
- Important assertions
- Runtime identifier relationships

The process stops after the configured maximum repair attempts.

## 11. Reporting Design

Reports are designed for both automation and human review:

| Output | Consumer |
|---|---|
| JSON report | Frameworks, scripts, diagnostics |
| HTML report | QA engineers and managers |
| JUnit XML | CI/CD systems |
| Test history | Developers investigating repairs |
| Screenshots/artifacts | UI failure analysis |

Each attempt should communicate:

- Attempt number
- Pass/fail status
- Failure classification
- Duration
- Standard output
- Standard error

## 12. Security Design

Security principles:

1. Secrets are loaded from environment variables.
2. `.env` is excluded from source control.
3. Generated tests must not hardcode credentials.
4. Tokens must not be printed in output.
5. Test accounts should have limited permissions.
6. Generated code should be reviewed before use against sensitive systems.
7. External model sharing must follow organizational policy.
8. Exposed credentials must be rotated immediately.

## 13. Extensibility Design

The framework can be extended by:

- Adding more Markdown test suites.
- Adding additional test modes.
- Supporting more authentication strategies.
- Adding different model providers.
- Adding API contract validators.
- Adding test tagging and selection.
- Adding CI/CD adapters.
- Adding persistent report storage.
- Adding browser network capture.
- Adding additional failure classifiers.

The preferred extension pattern is to add a focused component rather than
placing more mode-specific logic directly into the orchestration layer.

## 14. Design Trade-Offs

### Markdown requirements

**Benefit:** Easy for humans to read and edit.  
**Trade-off:** Natural-language requirements may be ambiguous.

### LLM-generated tests

**Benefit:** Reduces authoring effort and adapts to requirements.  
**Trade-off:** Generated code must be validated and reviewed.

### Browser snapshot input

**Benefit:** Gives the model current UI context.  
**Trade-off:** A snapshot may not capture every dynamic state or network event.

### Self-healing

**Benefit:** Reduces maintenance for recoverable failures.  
**Trade-off:** Repairs may be incorrect, so retry limits and review are needed.

### Single generated output path

**Benefit:** Keeps execution simple and predictable.  
**Trade-off:** The latest UI or API run replaces the previous generated file.

## 15. Design Constraints

The framework depends on:

- Active Gemini API access.
- Correct model configuration.
- Python dependencies.
- Node/npm and Playwright MCP for UI mode.
- Playwright browser binaries for UI execution.
- Reachable target applications and APIs.
- Approved credentials and test data.

## 16. Design Success Criteria

The design is considered successful when:

1. Users can select UI or API mode without editing orchestration code.
2. The correct test suite is loaded for the selected mode.
3. UI mode receives browser context.
4. API mode avoids unnecessary browser startup.
5. Gemini receives requirements appropriate to the selected mode.
6. Generated code is validated before execution.
7. Failed tests enter a bounded repair workflow.
8. Reports provide enough detail for diagnosis.
9. Secrets remain outside committed files.
10. New applications can be supported primarily through new requirements and
    environment configuration.

## 17. Future Design Direction

Future versions may introduce:

- A configuration file for registering multiple test suites.
- Separate generated output paths for UI and API modes.
- Automatic network-request discovery.
- Schema validation for API responses.
- Stronger generated-code policy checks.
- CI/CD pipeline integrations.
- Historical quality dashboards.
- Human approval before executing repaired code.

