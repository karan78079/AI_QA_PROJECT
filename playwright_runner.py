import os
import subprocess
import sys
import time
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class TestExecutionResult:
	status: str
	exit_code: int
	duration: float
	stdout: str
	stderr: str
	report_path: str = ""

	@property
	def traceback(self) -> str:
		return self.stderr or self.stdout


def validate_python(test_file: Path) -> None:
	source = test_file.read_text(encoding="utf-8")
	compile(source, str(test_file), "exec")
	if "def test_" not in source:
		raise ValueError("Generated test does not contain a pytest test function")


def run_pytest(test_file: Path, collect_only: bool = False) -> TestExecutionResult:
	test_path = test_file.resolve()
	command = [sys.executable, "-m", "pytest", str(test_path)]
	if collect_only:
		command.append("--collect-only")
	else:
		reports_dir = test_path.parents[2] / "reports"
		reports_dir.mkdir(parents=True, exist_ok=True)
		command.extend([
			"--junitxml", str(reports_dir / "test-results.xml"),
			"--html", str(reports_dir / "test-report.html"),
			"--self-contained-html",
		])

	started = time.perf_counter()
	if os.name == "nt":
		python_command = ["python", "-m", "pytest", str(test_path), *command[4:]] if not collect_only else ["python", "-m", "pytest", str(test_path), "--collect-only"]
		command = [
			os.environ.get("COMSPEC", "cmd.exe"),
			"/d",
			"/s",
			"/c",
			subprocess.list2cmdline(python_command),
		]
	completed = subprocess.run(
		command,
		capture_output=True,
		text=True,
		cwd=test_path.parents[2],
	)
	duration = time.perf_counter() - started
	return TestExecutionResult(
		status="passed" if completed.returncode == 0 else "failed",
		exit_code=completed.returncode,
		duration=duration,
		stdout=completed.stdout,
		stderr=completed.stderr,
		report_path=str(test_path.parents[2] / "reports" / "test-results.xml") if not collect_only else "",
	)


def classify_failure(output: str) -> str:
	text = output.lower()
	if any(value in text for value in ("connection_timed_out", "network_changed", "net::err_")):
		return "blocked_network"
	if "quota" in text or "rate limit" in text or "429" in text:
		return "blocked_ai_quota"
	if "credential" in text or "unauthorized" in text:
		return "blocked_credentials"
	return "failed_test"


def write_report(path: Path, attempts: list[dict]) -> None:
	path.parent.mkdir(parents=True, exist_ok=True)
	path.write_text(json.dumps({"attempts": attempts}, indent=2), encoding="utf-8")
