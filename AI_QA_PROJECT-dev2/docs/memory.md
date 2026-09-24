# Memory and Project Context
+
+## 1. Project Summary
+
+This project is an AI-powered self-healing test automation framework that
+generates pytest tests from Markdown requirements. It supports both UI testing
+through Playwright and REST API testing through Python `requests`.
+
+The system is designed to reduce manual test authoring effort, accelerate QA
+automation, and repair failed generated tests automatically through Gemini.
+
+## 2. Current Project State
+
+- User requirements are in `test_cases/requirements.txt`; Gemini classifies API or UI.
+- The user reviews and approves generated scenarios before execution.
+- UI mode collects a browser snapshot using Playwright MCP.
+- API classification skips browser snapshot collection.
+- Generated tests are written to `generated/tests/test_case.py`.
+- Failed versions are saved in `generated/tests/history/`.
+- Reports are written to `reports/`.
+
+## 3. Important Design Decisions
+
+### Separate UI and API suites
+
+UI and API requirements are intentionally kept in separate Markdown files. This
+prevents mixing Playwright browser instructions with REST API instructions and
+reduces ambiguity for the model.
+
+### Explicit mode selection
+
+The user chooses UI or API mode before generation. This explicit selection is
+used to reduce misclassification and improve reliability.
+
+### Secret handling
+
+Secrets are expected to live in `.env` and not in source code or generated
+tests. The framework uses environment variables instead of hardcoded values.
+
+### Safety and repair
+
+The system retries only within a bounded limit. It stores failed versions and
+tries to repair them rather than silently deleting the failing scenario.
+
+## 4. Core Files
+
+- `main.py` — orchestrates user mode selection, generation, validation,
+  execution, repairs, and reports.
+- `ai_client.py` — generates and repairs UI/API tests via Gemini.
+- `mcp_client.py` — captures browser snapshots for UI mode.
+- `playwright_runner.py` — validates, runs, and reports pytest execution.
+- `test_cases/requirements.txt` — user-authored UI or API requirements.
+- `PRD.md` — product requirements.
+- `architecture.md` — system design.
+- `rules.md` — operational and governance rules.
+- `design.md` — engineering design rationale.
+- `task.md` — project task and status summary.
+
+## 5. Runtime Behavior
+
+When the framework starts:
+
+1. It asks the user whether they want UI or API testing.
+2. It loads the matching Markdown file.
+3. For UI mode, it gathers a browser snapshot.
+4. It sends requirements and snapshot to Gemini.
+5. It writes the generated test to `generated/tests/test_case.py`.
+6. It validates Python and pytest collection.
+7. It executes the generated tests.
+8. It writes reports to `reports/`.
+9. If tests fail, it saves the failing version and retries within the configured
+   repair limit.
+
+## 6. Important Constraints
+
+- The framework depends on Gemini API access.
+- UI mode requires Playwright MCP and browser support.
+- Live test execution depends on network access and working credentials.
+- Generated tests require review before being trusted for critical workflows.
+- Secrets must remain out of source control.
+
+## 7. Validation State
+
+The project has passed focused validation checks:
+
+- Python compilation of core files.
+- Detect_test_type unit tests for UI/API detection.
+
+This means the project is structurally sound and the mode-selection logic is
+working as expected.
+
+## 8. Recommended Future Work
+
+- Inject project rules into Gemini prompts for stronger enforcement.
+- Add stronger validation that generated code matches the selected mode.
+- Add a real end-to-end API run with approved test data.
+- Add a stable UI smoke test using a known test environment.
+- Add browser network-request capture for API discovery.
+- Add CI/CD integration.
+
+## 9. Manager Perspective
+
+This project is best understood as a prototype AI QA framework that combines:
+
+- natural-language requirements,
+- browser-state inspection,
+- API test generation,
+- pytest execution,
+- AI repair, and
+- structured reporting.
+
+It demonstrates strong engineering value and can serve as a useful portfolio or
+internship project, with further hardening required before production-level
+enterprise deployment.
