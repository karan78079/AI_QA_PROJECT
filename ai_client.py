import os
import re
import time

from dotenv import load_dotenv
from openai import APIStatusError, OpenAI


load_dotenv()


def _client() -> OpenAI:
	api_key = os.getenv("GEMINI_API_KEY")
	if not api_key:
		raise RuntimeError("GEMINI_API_KEY is not configured")

	return OpenAI(
		api_key=api_key,
		base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
	)


def _code_from_response(content: str) -> str:
	match = re.search(r"```(?:python)?\s*(.*?)```", content, re.DOTALL | re.IGNORECASE)
	return (match.group(1) if match else content).strip() + "\n"


def _request(messages: list[dict[str, str]], model: str):
	for attempt in range(3):
		try:
			return _client().chat.completions.create(
				model=model,
				messages=messages,
			)
		except APIStatusError as error:
			status_code = getattr(error, "status_code", None)
			if status_code == 429:
				raise RuntimeError(
					"Gemini quota is exhausted. Wait for the quota reset or use a Gemini "
					"API key/project with available billing or quota. No retry was attempted."
				) from error
			if status_code not in {500, 502, 503, 504} or attempt == 2:
				raise
			time.sleep(2 ** attempt)


def generate_test_code(test_case: str, browser_snapshot: str) -> str:
	model = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
	messages = [
		{
			"role": "system",
			"content": """
You generate executable Python pytest tests using Playwright's sync API.
Return only one complete Python source file, without Markdown fences or explanations.
Use the supplied browser snapshot as the source of truth for locators.
Use os.getenv('TEST_EMAIL') and os.getenv('TEST_PASSWORD') for credentials;
never copy credential values into the generated source.
Include `from dotenv import load_dotenv` and call `load_dotenv()` so the generated
test works when run directly from pytest. This application uses hash routing;
wait for URLs containing `/#/dashboard/`, `/#/dashboard/cart`,
`/#/dashboard/order`, `/#/dashboard/thanks`, or `/#/auth/login` as appropriate.
Use a specific locator such as `[role='alert']` or `.toast-error`, not a selector
that matches a container and its child at the same time.
Launch every Playwright browser with `headless=True`.
The generated file must contain at least one function named test_... and must be
self-contained, including a sync_playwright context and browser cleanup.
""",
		},
		{
			"role": "user",
			"content": f"USER TEST CASE:\n{test_case}\n\nBROWSER SNAPSHOT:\n{browser_snapshot}",
		},
	]

	response = _request(messages, model)

	content = response.choices[0].message.content or ""
	if not content.strip():
		raise RuntimeError("Gemini returned empty test code")
	return _code_from_response(content)


def repair_test_code(
	test_case: str,
	browser_snapshot: str,
	current_code: str,
	failure_output: str,
) -> str:
	messages = [
		{
			"role": "system",
			"content": """
You repair an executable Python pytest test that uses Playwright's sync API.
Return only the complete corrected Python source file, without Markdown fences or
explanations. Preserve the requested coverage, use the browser snapshot as the
source of truth, and do not hardcode credentials. Keep load_dotenv(), use
headless=True, and handle this application's hash-based URLs with /#/ patterns.
Fix the reported failure rather than removing the failing scenario. The result
must contain at least one function named test_... and be valid Python.
""",
		},
		{
			"role": "user",
			"content": (
				f"REQUIREMENT:\n{test_case}\n\n"
				f"BROWSER SNAPSHOT:\n{browser_snapshot}\n\n"
				f"CURRENT TEST CODE:\n{current_code}\n\n"
				f"PYTEST FAILURE:\n{failure_output}"
			),
		},
	]

	response = _request(messages, os.getenv("GEMINI_MODEL", "gemini-3.6-flash"))

	content = response.choices[0].message.content or ""
	if not content.strip():
		raise RuntimeError("Gemini returned empty repaired test code")
	return _code_from_response(content)
