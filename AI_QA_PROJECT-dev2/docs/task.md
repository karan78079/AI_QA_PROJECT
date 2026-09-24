# Project Task Plan

## 1. Project Objective

Build an AI-powered self-healing test automation framework that can generate,
execute, repair, and report UI and REST API tests from Markdown requirements.

## 2. Completed Tasks

### Framework Foundation

- [x] Create the Python project structure.
- [x] Add environment-based configuration.
- [x] Add Gemini/OpenAI-compatible client integration.
- [x] Add pytest as the execution framework.
- [x] Add Playwright support for browser UI testing.
- [x] Add `requests` support for REST API testing.
- [x] Add Playwright MCP browser snapshot integration.

### UI Testing

- [x] Create the UI Markdown test suite.
- [x] Define login test scenarios.
- [x] Define login validation scenarios.
- [x] Define invalid login scenarios.
- [x] Define product listing scenarios.
- [x] Define product visibility scenarios.
- [x] Define cart scenarios.
- [x] Define checkout scenarios.
- [x] Define order placement scenarios.
- [x] Define orders-page scenarios.
- [x] Define logout scenarios.
- [x] Add UI-only generation instructions.

### API Testing

- [x] Create a separate API Markdown test suite.
- [x] Define API authentication requirements.
- [x] Define runtime token and user ID handling.
- [x] Define add-to-cart API validation.
- [x] Define cart-count validation.
- [x] Define create-order validation.
- [x] Define order-history validation.
- [x] Add API-only generation instructions.

### Mode Selection

- [x] Add interactive UI/API selection to `main.py`.
- [x] Automatically load the UI Markdown file for UI mode.
- [x] Automatically load the API Markdown file for API mode.
- [x] Skip browser snapshot collection in API mode.
- [x] Collect browser snapshot in UI mode.
- [x] Pass the selected mode explicitly to the AI generation layer.

### AI Test Generation

- [x] Add UI test generation with Playwright.
- [x] Add API test generation with `requests`.
- [x] Add explicit UI/API test-type detection.
- [x] Add response code-fence cleanup.
- [x] Add empty-response validation.
- [x] Add model configuration through environment variables.

### Self-Healing

- [x] Detect failed generated tests.
- [x] Capture failure output.
- [x] Save failed test versions.
- [x] Send requirements and failure details to Gemini.
- [x] Support UI test repair.
- [x] Support API test repair.
- [x] Retry repaired tests.
- [x] Add configurable retry limits.
- [x] Stop after the configured maximum attempts.

### Validation and Reporting

- [x] Validate generated Python syntax.
- [x] Confirm that generated tests contain pytest test functions.
- [x] Run pytest collection before execution.
- [x] Capture test duration.
- [x] Capture standard output.
- [x] Capture standard error.
- [x] Create JSON attempt reports.
- [x] Create HTML pytest reports.
- [x] Create JUnit XML reports.
- [x] Add failure classification.

### Documentation

- [x] Add [PRD.md](./PRD.md).
- [x] Add [architecture.md](./architecture.md).
- [x] Add [rules.md](./rules.md).
- [x] Add [design.md](./design.md).
- [x] Add this project task document.

## 3. Current Validation Status

- [x] Python source compilation completed successfully.
- [x] Test-type detection tests pass.
- [x] UI and API Markdown files exist.
- [x] Generated test file exists.
- [x] Reports directory exists.
- [x] `.env` is excluded from source control through `.gitignore`.
- [x] Required environment variable names are configured.

Focused validation result:

```text
2 passed
```

## 4. Required Setup Tasks

Before running the framework on a new machine:

- [ ] Install Python dependencies from `requirements.txt`.
- [ ] Install Node dependencies from `package.json`.
- [ ] Install Playwright browser binaries.
- [ ] Create a local `.env` file.
- [ ] Add an active `GEMINI_API_KEY`.
- [ ] Configure an approved `TEST_EMAIL`.
- [ ] Configure an approved `TEST_PASSWORD`.
- [ ] Configure `MAX_REPAIR_ATTEMPTS`.
- [ ] Confirm network access to Gemini and the target application.

## 5. Execution Tasks

### UI execution

- [ ] Start the project with `python main.py`.
- [ ] Select `1` for UI testing.
- [ ] Confirm that MCP connects successfully.
- [ ] Confirm that a browser snapshot is collected.
- [ ] Confirm that Playwright code is generated.
- [ ] Validate generated UI test syntax.
- [ ] Review the UI test report.
- [ ] Investigate any failed or blocked scenarios.

### API execution

- [ ] Start the project with `python main.py`.
- [ ] Select `2` for API testing.
- [ ] Confirm that browser snapshot collection is skipped.
- [ ] Confirm that `requests` code is generated.
- [ ] Validate generated API test syntax.
- [ ] Confirm valid API authentication.
- [ ] Confirm approved product and order test data.
- [ ] Review the API test report.
- [ ] Investigate any failed or blocked scenarios.

## 6. Pre-Commit Checklist

- [ ] Run Python compilation.
- [ ] Run focused pytest tests.
- [ ] Confirm the intended Markdown suites are present.
- [ ] Confirm no secrets are present in source files.
- [ ] Confirm `.env` is ignored.
- [ ] Confirm reports do not contain tokens or passwords.
- [ ] Review the latest generated test file.
- [ ] Remove temporary files that are not project deliverables.
- [ ] Confirm documentation matches the current implementation.
- [ ] Confirm live tests were either run successfully or clearly documented
  as environment-dependent.

## 7. Manager Demonstration Checklist

- [ ] Explain the problem solved by the framework.
- [ ] Show the UI/API mode selection.
- [ ] Show the separate Markdown test suites.
- [ ] Demonstrate UI test generation.
- [ ] Demonstrate API test generation.
- [ ] Show generated pytest code.
- [ ] Show syntax and collection validation.
- [ ] Explain the self-healing retry loop.
- [ ] Show test history versions.
- [ ] Show JSON, HTML, and JUnit reports.
- [ ] Explain secret handling.
- [ ] Explain current limitations and future enhancements.

## 8. Known Limitations

- [ ] Full live execution depends on Gemini availability.
- [ ] UI execution depends on Playwright MCP and browser binaries.
- [ ] Target websites may change selectors or workflows.
- [ ] API contracts may require application-specific request details.
- [ ] Generated code requires review for critical workflows.
- [ ] The latest generated UI or API test uses the same output path.
- [ ] Browser network requests are not automatically captured by the current
  MCP client.
- [ ] Self-healing is bounded and cannot guarantee a correct repair.

## 9. Recommended Future Tasks

### High Priority

- [ ] Inject approved AI-generation rules into Gemini prompts.
- [ ] Add stronger validation that generated code matches the selected mode.
- [ ] Add a real API integration test using approved test data.
- [ ] Add a complete UI smoke test using a stable test environment.
- [ ] Redact sensitive values from all reports and artifacts.

### Medium Priority

- [ ] Add automatic browser network-request capture.
- [ ] Add API schema validation.
- [ ] Add separate generated output paths for UI and API tests.
- [ ] Add CI/CD workflow integration.
- [ ] Add configurable test-suite registration.
- [ ] Add richer structured logging.

### Lower Priority

- [ ] Add parallel test execution.
- [ ] Add historical trend dashboards.
- [ ] Add additional model providers.
- [ ] Add test tagging and selective scenario execution.
- [ ] Add human approval before executing repaired code.

## 10. Definition of Done

The project task is complete when:

1. UI and API modes can be selected from `main.py`.
2. The correct Markdown suite is loaded for each mode.
3. The correct test framework is generated.
4. Generated code passes syntax validation.
5. Pytest collection succeeds.
6. Tests execute and produce reports.
7. Failures are classified.
8. Self-healing attempts are bounded and recorded.
9. Credentials remain outside committed files.
10. Documentation is available for managers, developers, and QA engineers.

