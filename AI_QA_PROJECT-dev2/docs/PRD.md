# Product Requirements Document

## Product Name

AI-Powered Self-Healing Test Automation Framework

## Document Purpose

This document explains the purpose, capabilities, workflow, scope, and
expected value of the AI-powered test automation framework for project
stakeholders and managers.

## Executive Summary

The framework converts natural-language testing requirements written in
Markdown into executable automated tests. It supports both web UI testing and
REST API testing.

The framework uses Gemini to generate pytest test code, Playwright MCP to
inspect live web application context for UI scenarios, and a self-healing
repair loop to improve failed generated tests. It validates the generated
code, executes the tests, classifies failures, stores test history, and
produces structured reports.

The objective is to reduce manual test-authoring effort, accelerate test
automation, and simplify maintenance when application behavior or selectors
change.

## Problem Statement

Traditional test automation requires engineers to:

- Understand the application manually.
- Write test code and selectors.
- Maintain tests when UI behavior changes.
- Create separate API test scripts.
- Analyze failures and repair broken tests.
- Prepare execution reports.

These activities are repetitive and can delay regression testing. Teams also
need a consistent way to convert business requirements into repeatable
automated validation.

## Product Vision

Provide a configurable testing assistant that allows a user to describe test
requirements in plain language and receive executable, validated, and
reportable UI or API tests with automatic repair support.

## Goals

1. Generate automated tests from Markdown-based requirements.
2. Support browser UI testing with Playwright.
3. Support REST API testing with Python `requests`.
4. Allow the user to select UI or API testing when starting the framework.
5. Use live browser context to improve UI locator generation.
6. Validate generated Python before execution.
7. Automatically repair failed generated tests within a configured retry limit.
8. Preserve failed test versions for debugging and comparison.
9. Produce useful execution reports for QA and engineering teams.
10. Keep credentials and API keys outside generated source code.

## Non-Goals

The framework is not intended to:

- Replace human QA judgment for critical business workflows.
- Guarantee that every AI-generated test is correct without review.
- Bypass CAPTCHA, OTP, MFA, or other security controls.
- Invent payment details, credentials, product IDs, or order IDs.
- Act as a complete performance-testing or load-testing platform.
- Automatically support native mobile or desktop applications.

## Target Users

- QA automation engineers
- Software developers
- Test engineers
- QA leads
- SDET teams
- Engineering managers
- Product teams preparing acceptance scenarios

## Key Capabilities

### 1. Markdown-Based Test Definition

Users describe test scenarios, test data, expected results, and execution
rules in Markdown files.

The project uses one user-authored specification at
`test_cases/requirements.txt`. Gemini classifies each requirement as API or UI
and creates independently reviewable test cases.

### 2. AI Test-Type Classification and Review

When `main.py` starts, Gemini classifies the requirements and presents test
cases for approval. The user can approve all, approve or reject specific IDs,
reject all, or add a manual test before code generation.

### 3. AI-Generated UI Tests

For UI mode, the framework:

- Opens the application through Playwright MCP.
- Captures a live browser snapshot.
- Sends the requirements and snapshot to Gemini.
- Generates executable Playwright pytest code.
- Uses visible page structure and application context to create locators.

Typical UI scenarios include:

- Login
- Form validation
- Product listing
- Add to cart
- Checkout
- Order placement
- Order history
- Logout

### 4. AI-Generated API Tests

For API mode, the framework:

- Reads API requirements from the API Markdown suite.
- Generates Python tests using `requests`.
- Validates status codes and JSON response fields.
- Supports authentication token and runtime identifier handling.
- Validates login, cart, product, order, and order-history workflows.

### 5. Self-Healing Test Repair

When a generated test fails, the framework:

1. Records the failure.
2. Saves a version of the failed test.
3. Sends the requirements, current code, and failure output to Gemini.
4. Generates a repaired test.
5. Executes the repaired test again.
6. Stops when the test passes or the retry limit is reached.

The retry limit is configured through:

```text
MAX_REPAIR_ATTEMPTS
```

### 6. Validation and Reporting

The framework:

- Compiles generated Python code.
- Runs pytest collection before execution.
- Executes the test suite.
- Captures stdout, stderr, duration, and status.
- Classifies common failure categories.
- Produces JSON, HTML, and JUnit XML reports.

## High-Level Workflow

```text
User selects UI or API mode
              |
              v
Framework selects the matching Markdown test suite
              |
              v
UI mode: collect browser snapshot
API mode: skip browser snapshot
              |
              v
Gemini generates pytest test code
              |
              v
Validate Python syntax and pytest collection
              |
              v
Execute generated tests
              |
       +------+- ------+
       |               |
     Pass            Fail
       |               |
       v               v
   Report       Save version and repair with Gemini
                       |
                       v
                  Retry execution
```

## Main Components

| Component | Responsibility |
|---|---|
| `main.py` | Orchestrates mode selection, generation, execution, repair, and reporting |
| `ai_client.py` | Detects test type and communicates with Gemini |
| `mcp_client.py` | Connects to Playwright MCP and captures browser snapshots |
| `playwright_runner.py` | Validates, executes, and reports pytest results |
| `test_cases/requirements.txt` | User-authored UI or API requirements |
| `generated/tests/test_case.py` | Latest generated test file |
| `generated/tests/history/` | Previous generated test versions |
| `reports/` | JSON, HTML, XML, and test artifact output |

## Configuration Requirements

The framework uses environment variables for configuration and secrets:

```env
GEMINI_API_KEY=<active Gemini API key>
GEMINI_MODEL=gemini-2.5-flash
TEST_EMAIL=<approved test account email>
TEST_PASSWORD=<approved test account password>
API_BASE_URL=<optional API base URL>
MAX_REPAIR_ATTEMPTS=3
```

Secrets must not be committed to source control or included in generated
tests, reports, screenshots, or documentation.

## Functional Requirements

### FR-1: Mode Selection

The system shall ask the user to choose UI testing or API testing when
`main.py` starts.

### FR-2: Test Suite Selection

The system shall load the correct Markdown test suite based on the selected
mode.

### FR-3: UI Generation

The system shall provide UI requirements and browser context to Gemini and
generate Playwright pytest code for UI mode.

### FR-4: API Generation

The system shall provide API requirements to Gemini and generate `requests`
pytest code for API mode.

### FR-5: Generated-Code Validation

The system shall validate Python syntax and confirm that at least one pytest
test function exists before execution.

### FR-6: Test Execution

The system shall run pytest collection before executing the generated test.

### FR-7: Failure Repair

The system shall send failed test context to Gemini and retry within the
configured repair limit.

### FR-8: History

The system shall preserve failed generated versions in the test history
directory.

### FR-9: Reporting

The system shall record execution status, classification, duration, standard
output, and standard error.

### FR-10: Secret Protection

The system shall use environment variables for credentials and API keys and
shall not intentionally hardcode secrets in generated source.

## Non-Functional Requirements

### Reliability

- Generated code must be syntactically valid before execution.
- Failures must be visible in reports.
- Repair attempts must be bounded.

### Security

- Secrets must remain outside source code.
- Tokens and passwords must not be printed in logs.
- Test accounts and test data must be approved for automation.

### Maintainability

- Test requirements should be editable without changing orchestration code.
- UI and API suites should remain separate.
- Failed generated versions should be available for diagnosis.

### Usability

- A user should be able to select a test mode from the command line.
- Test requirements should be understandable by both technical and
  non-technical stakeholders.
- Reports should clearly communicate pass, failure, and blocked states.

## Success Criteria

The product is successful when:

1. A user can select UI or API testing from `main.py`.
2. The correct Markdown suite is loaded automatically.
3. Gemini generates the appropriate Playwright or `requests` test type.
4. Generated code passes syntax and collection validation.
5. The test runner executes the generated suite.
6. Failed tests receive bounded AI repair attempts.
7. Test history and reports are created.
8. Credentials remain external to generated source.
9. A manager can understand the result from the generated reports.

## Risks and Limitations

- Gemini availability, quota, and model behavior affect generation.
- Live websites may change selectors or page behavior.
- Network failures may prevent browser or API execution.
- Generated tests require review for critical workflows.
- API request bodies may vary between applications.
- Some scenarios require approved test data that cannot be safely invented.
- Infinite self-healing is intentionally avoided to prevent uncontrolled
  retries and API usage.

## Future Enhancements

Potential future improvements include:

- Automatic browser network-request capture.
- API request generation from observed browser traffic.
- Better test-type and test-suite metadata validation.
- CI/CD pipeline integration.
- Secure secret-manager integration.
- Parallel test execution.
- Trend dashboards for historical results.
- Test tagging and selective execution.
- Stronger generated-code policy validation.
- Support for additional API authentication schemes.

## Business Value

The framework can help teams:

- Reduce repetitive test-authoring effort.
- Accelerate regression coverage.
- Improve consistency between requirements and automated tests.
- Reduce maintenance time for locator and assertion failures.
- Enable developers and QA engineers to create tests using natural language.
- Obtain structured evidence from automated test execution.

## Current Project Status

The project is an AI-assisted testing framework prototype with working support
for:

- Playwright UI test generation
- REST API test generation
- Interactive UI/API mode selection
- Browser snapshot input for UI generation
- Pytest execution
- Self-healing repair attempts
- Test history
- JSON, HTML, and JUnit reporting

Live end-to-end results depend on valid credentials, active Gemini access,
network availability, the target application's current behavior, and approved
test data.
