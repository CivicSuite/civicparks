from fastapi.testclient import TestClient

from civicparks import __version__
from civicparks.main import app

client = TestClient(app)


def test_root_reports_honest_current_state():
    payload = client.get("/").json()
    assert payload["name"] == "CivicParks"
    assert payload["version"] == __version__
    assert "database-backed registration/maintenance workpapers" in payload["message"]
    assert "payments" in payload["message"]
    assert "not implemented yet" in payload["message"]


def test_health_reports_civiccore_pin():
    assert client.get("/health").json() == {
        "status": "ok",
        "service": "civicparks",
        "version": "0.1.1",
        "civiccore_version": "0.3.0",
    }


def test_public_ui_contains_version_boundaries_and_dependency():
    text = client.get("/civicparks").text
    assert "CivicParks v0.1.1" in text
    assert "No payments" in text
    assert "civiccore==0.3.0" in text


def test_api_endpoints_return_deterministic_payloads():
    policy = client.post(
        "/api/v1/civicparks/policy-answer",
        json={"question": "facility rental"},
    ).json()
    assert policy["staff_review_required"] is True

    program = client.post(
        "/api/v1/civicparks/program-answer",
        json={
            "question": "teen events",
            "programs": [
                {
                    "title": "Teen tennis",
                    "audience": "teens",
                    "date": "2026-05-10",
                    "accessibility_note": "Accessible courts",
                }
            ],
        },
    ).json()
    assert program["accessibility_review_required"] is True

    registration = client.post(
        "/api/v1/civicparks/registration-assistance",
        json={
            "program": {
                "title": "Swim lessons",
                "audience": "youth",
                "registration_url": "https://parks.example/register",
                "accessibility_note": "Ramp access",
            }
        },
    ).json()
    assert registration["assistance_id"] is None

    triage = client.post(
        "/api/v1/civicparks/maintenance-triage",
        json={"issue": "trash bin full", "location": "Oak Park"},
    ).json()
    assert triage["triage_id"] is None
