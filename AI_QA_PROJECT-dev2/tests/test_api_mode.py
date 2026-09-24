from ai_client import _json_from_response, detect_test_type
from main import requirements_for_generation, review_test_cases


def test_detect_api_case():
    case = """
    Validate POST /api/auth/login endpoint with email and password.
    Check 200 status and JWT token in response.
    """
    assert detect_test_type(case) == "api"


def test_detect_ui_case():
    case = """
    Login through the browser using visible email and password fields.
    Verify dashboard page is shown after clicking login.
    """
    assert detect_test_type(case) == "ui"


def test_parse_json_test_plan():
    plan = _json_from_response('```json\n{"test_type":"api","test_cases":[]}\n```')

    assert plan["test_type"] == "api"


def test_format_approved_requirements():
    requirements = requirements_for_generation([
        {"id": "TC001", "title": "Login", "requirement": "Accept valid credentials"},
        {"id": "MANUAL001", "title": "Logout", "requirement": "End the session"},
    ])

    assert "TC001: Login" in requirements
    assert "MANUAL001: Logout" in requirements


def test_review_can_approve_specific_test(monkeypatch):
    answers = iter(["p", "TC002", "e"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    cases = [
        {"id": "TC001", "title": "Login", "requirement": "Log in", "priority": "high"},
        {"id": "TC002", "title": "Logout", "requirement": "Log out", "priority": "medium"},
    ]

    approved = review_test_cases(cases)

    assert [test_case["id"] for test_case in approved] == ["TC002"]
