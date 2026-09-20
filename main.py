import asyncio
import os
import re
import shutil
from pathlib import Path

from ai_client import generate_test_code, repair_test_code
from mcp_client import get_page_snapshot
from playwright_runner import classify_failure, run_pytest, validate_python, write_report


ROOT = Path(__file__).resolve().parent
GENERATED_TEST = ROOT / "generated" / "tests" / "test_case.py"
HISTORY_DIR = GENERATED_TEST.parent / "history"
REPORT_PATH = ROOT / "reports" / "test_report.json"


def read_test_case():

    with open("test_cases/full_test_cases.md", "r", encoding="utf-8") as file:
        return file.read()


async def main():
    test_case = read_test_case()
    url_match = re.search(r"https?://\S+", test_case)
    url = url_match.group(0) if url_match else "http://localhost"
    print("Connecting to MCP and collecting browser snapshot...")
    snapshot = await get_page_snapshot(url)
    print("Generating pytest code with Gemini...")
    try:
        generated_code = generate_test_code(test_case, snapshot)
    except RuntimeError as error:
        print(f"Gemini unavailable: {error}")
        return
    GENERATED_TEST.parent.mkdir(parents=True, exist_ok=True)
    GENERATED_TEST.write_text(generated_code, encoding="utf-8")
    max_repairs = int(os.getenv("MAX_REPAIR_ATTEMPTS", "3"))
    attempts = []
    for attempt in range(max_repairs + 1):
        try:
            validate_python(GENERATED_TEST)
            collection = run_pytest(GENERATED_TEST, collect_only=True)
            result = collection if collection.exit_code != 0 else run_pytest(GENERATED_TEST)
        except Exception as error:
            result = None
            failure_output = str(error)
        else:
            failure_output = result.traceback

        status = result.status if result is not None else "failed"
        attempts.append({
            "attempt": attempt + 1,
            "status": status,
            "classification": "passed" if status == "passed" else classify_failure(failure_output),
            "duration": result.duration if result is not None else 0,
            "stdout": result.stdout if result is not None else "",
            "stderr": result.stderr if result is not None else failure_output,
        })
        write_report(REPORT_PATH, attempts)

        if result is not None:
            print(result.stdout)
            if result.stderr:
                print(result.stderr)
            print(f"Attempt {attempt + 1}: {result.status} ({result.duration:.2f}s)")
            if result.exit_code == 0:
                print("Final status: passed")
                return

        if attempt == max_repairs:
            print(f"Final status: failed after {max_repairs} repair attempt(s)")
            raise SystemExit(1)

        HISTORY_DIR.mkdir(parents=True, exist_ok=True)
        version = attempt + 1
        shutil.copy2(GENERATED_TEST, HISTORY_DIR / f"test_case_v{version}.py")
        print(f"Test failed. Sending failure to Gemini for repair {version}/{max_repairs}...")
        repaired_code = repair_test_code(
            test_case,
            snapshot,
            GENERATED_TEST.read_text(encoding="utf-8"),
            failure_output,
        )
        GENERATED_TEST.write_text(repaired_code, encoding="utf-8")


if __name__ == "__main__":
    asyncio.run(main())