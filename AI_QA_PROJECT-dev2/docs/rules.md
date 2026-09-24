# Framework Rules

## 1. Purpose

These rules define how the AI-powered test automation framework must generate,
execute, repair, and report UI and API tests.

## 2. Test Mode Rules

1. `main.py` loads the single requirements file and Gemini classifies it.
2. The requirements file is:

   ```text
   test_cases/requirements.txt
   ```

3. Users must review generated cases before execution.
4. UI and API behavior may be described in the same requirements file.
5. The generated code must match the selected mode.
6. UI mode must generate Playwright tests.
7. API mode must generate `requests` tests.

## 3. UI Testing Rules

1. Use Playwright with pytest.
2. Use the live browser snapshot as the source of truth for page structure,
   controls, labels, roles, placeholders, and visible text.
3. Use specific locators based on the live application.
4. Do not invent selectors, product names, order IDs, page text, or controls.
5. Use `headless=True` for generated browser tests.
6. Wait for navigation and dynamic content where required.
7. Validate visible page state, not only URL changes.
8. Use independent browser contexts where possible.
9. Close pages, contexts, and browsers during teardown.
10. Do not use API calls in a suite explicitly marked `UI TESTING ONLY`.

## 4. API Testing Rules

1. Use Python `requests` and pytest.
2. Use `requests.Session()` where a reusable authenticated session is useful.
3. Validate HTTP status codes.
4. Validate JSON response structure and required fields.
5. Capture authentication tokens at runtime.
6. Use the authorization format required by the API:

   ```text
   Authorization: Bearer <runtime_token>
   ```

7. Use runtime user IDs, product IDs, cart IDs, and order IDs.
8. Do not hardcode tokens, passwords, order IDs, or user IDs.
9. Do not invent request fields or response values.
10. Preserve API-to-UI identifiers when a flow requires cross-layer
    validation.

## 5. Authentication and Secret Rules

1. Store secrets in environment variables or an approved secret manager.
2. Use `python-dotenv` to load local development configuration.
3. Never commit `.env`.
4. Never place API keys, passwords, bearer tokens, or private credentials in:
   - Source code
   - Markdown requirements
   - Generated test files
   - Screenshots
   - HTML reports
   - JSON reports
   - Logs
5. Never print authentication tokens or passwords.
6. Use approved test accounts only.
7. Rotate credentials immediately if they are exposed.
8. Do not use production credentials for test execution unless explicitly
   approved.

## 6. Test Requirement Rules

1. Each Markdown suite must declare its test type explicitly:

   ```text
   UI TESTING ONLY
   ```

   or:

   ```text
   API TESTING ONLY
   ```

2. Requirements must state the application or API base URL.
3. Requirements must define expected results.
4. Requirements must identify required test data.
5. Requirements must clearly distinguish required and optional steps.
6. Requirements must state when a scenario should be blocked.
7. Requirements must not require fabricated data.
8. Requirements must not contain live secrets.
9. Requirements should use one clear scenario per test case where possible.
10. Requirements should be understandable to both QA engineers and managers.

## 7. AI Generation Rules

1. Gemini must return a complete Python source file.
2. Gemini must return executable pytest code.
3. Generated code must contain at least one function named `test_...`.
4. Generated code must use the library required by the selected mode.
5. Generated UI code must use Playwright.
6. Generated API code must use `requests`.
7. Generated code must load environment-based configuration where required.
8. Generated code must not hardcode secrets.
9. Generated code must preserve the requested scenario.
10. Generated code must not remove assertions merely to make a test pass.
11. Generated code must not replace runtime identifiers with invented values.
12. Markdown code fences must be removed before the test file is executed.

## 8. Generated-Code Validation Rules

Before execution, the framework must:

1. Read the generated source.
2. Compile the source with Python.
3. Confirm that at least one pytest test function exists.
4. Run pytest collection.
5. Execute tests only after successful collection.
6. Record validation or collection errors in the report.

Invalid generated code must not be treated as a successful test result.

## 9. Execution Rules

1. Execute tests through pytest.
2. Capture stdout and stderr.
3. Capture execution duration.
4. Generate JUnit XML for CI compatibility.
5. Generate an HTML test report.
6. Write attempt history to the JSON report.
7. Use approved test environments and test data.
8. Avoid destructive actions unless explicitly required by the test case.
9. Do not run tests against production systems without approval.
10. Do not repeat a test indefinitely.

## 10. Self-Healing Rules

1. Self-healing starts only after a generated test fails.
2. The current test code, requirements, and failure output must be supplied to
   the repair request.
3. The repair must preserve the original test objective.
4. The repair must preserve required assertions.
5. The repair must preserve API-to-UI identifier correlation.
6. The repair must not remove a failing scenario without an explicit
   blocked-data reason.
7. The repair must not add hardcoded credentials or tokens.
8. The repair must produce complete executable Python.
9. Each failed version must be saved before repair.
10. Repairs must stop at `MAX_REPAIR_ATTEMPTS`.
11. Infinite repair loops are prohibited.
12. A passing repair must still be reviewed for correctness in critical flows.

## 11. Failure Classification Rules

Classify failures consistently:

- `blocked_network`: network or target application is unavailable.
- `blocked_ai_quota`: Gemini quota or rate limit is exhausted.
- `blocked_credentials`: credentials are missing, invalid, or unauthorized.
- `failed_test`: the application or generated test violates an assertion.

Do not classify an ordinary assertion failure as blocked unless the failure
output supports that classification.

## 12. Blocking Rules

Mark a scenario as blocked when:

1. Required environment variables are missing.
2. Approved test data is unavailable.
3. The target environment cannot be reached.
4. Authentication cannot be established because the test environment is
   unavailable.
5. A required API contract or payment test value is not available.
6. The scenario would require inventing a value.

Do not silently skip ordinary functional failures.

## 13. Reporting Rules

Reports must include, where applicable:

- Test attempt number
- Final status
- Failure classification
- Duration
- Standard output
- Standard error
- Collection result
- Repair history
- Blocked reason

Reports must not contain:

- Passwords
- API keys
- Bearer tokens
- Private authentication headers
- Unapproved personal information

## 14. Test History Rules

1. Save failed generated versions before requesting repair.
2. Store history under:

   ```text
   generated/tests/history/
   ```

3. Use clear version names.
4. Do not overwrite historical versions during a retry.
5. Review historical versions when diagnosing repeated repair failures.

## 15. File and Directory Rules

The expected project organization is:

```text
AI_QA_AGENT/
├── main.py
├── ai_client.py
├── mcp_client.py
├── playwright_runner.py
├── PRD.md
├── architecture.md
├── rules.md
├── requirements.txt
├── package.json
├── test_cases/
│   └── requirements.txt
├── generated/
│   └── tests/
├── reports/
└── tests/
```

Generated files, reports, caches, and secrets should remain excluded from
source control when they are not intended as deliverables.

## 16. Change Management Rules

1. Keep UI and API changes isolated where possible.
2. Update the relevant Markdown requirement when behavior changes.
3. Update documentation when architecture or workflow changes.
4. Run focused tests after code changes.
5. Compile changed Python files before committing.
6. Do not commit secrets or temporary artifacts.
7. Review generated test output before relying on it.
8. Do not change unrelated files while addressing a test-generation issue.

## 17. Security Rules

1. Treat generated code as untrusted until reviewed.
2. Do not execute generated code against sensitive environments without
   approval.
3. Use least-privilege test accounts.
4. Restrict API keys to the required services and projects.
5. Rotate exposed credentials.
6. Redact secrets from diagnostic output.
7. Do not send confidential application data to an external model without
   organizational approval.
8. Review model-generated requests before using them against real systems.

## 18. Review and Approval Rules

Before a test suite is used by a team:

1. Confirm the correct test mode.
2. Review the Markdown requirements.
3. Review generated code.
4. Confirm test credentials are approved.
5. Run syntax validation and pytest collection.
6. Review the first complete execution report.
7. Confirm failures are correctly classified.
8. Confirm self-healing did not weaken assertions.
9. Confirm no secrets appear in source, reports, or artifacts.
10. Obtain environment approval for scheduled or CI execution.

## 19. Completion Criteria

A test execution is complete only when:

1. The selected Markdown suite was loaded.
2. The correct test type was generated.
3. Generated Python passed syntax validation.
4. Pytest collection completed.
5. Tests executed or were explicitly blocked.
6. Results were written to reports.
7. Repair attempts stopped at the configured limit.
8. The final status is clearly reported.

