from civicparks import __version__
from civicparks.maintenance import triage_maintenance_request
from civicparks.policy import ParksPolicySource, answer_policy_question
from civicparks.programs import ParksProgram, answer_program_question
from civicparks.registration import RecreationProgram, draft_registration_assistance


def test_version_is_release_version():
    assert __version__ == "0.1.0"


def test_policy_answer_is_cited_and_reviewed():
    answer = answer_policy_question(
        "Can we rent the pavilion?",
        [ParksPolicySource("p1", "Rental Policy", "Rentals need approval.", "Parks Policy 4")],
    )
    assert answer.citations == ("Parks Policy 4",)
    assert answer.staff_review_required is True
    assert "registrations" in answer.boundary


def test_program_answer_keeps_registration_and_accessibility_review():
    response = answer_program_question(
        "What events are for teens?",
        [ParksProgram("Teen tennis", "teens", "2026-05-10", "Accessible courts")],
    )
    assert response.accessibility_review_required is True
    assert response.registration_system_required is True
    assert response.programs[0].title == "Teen tennis"


def test_registration_assistance_links_out_without_enrolling():
    assistance = draft_registration_assistance(
        RecreationProgram("Swim lessons", "youth", "https://parks.example/register", "Ramp access")
    )
    assert assistance.registration_url == "https://parks.example/register"
    assert assistance.staff_review_required is True
    assert "does not take payments" in assistance.boundary


def test_maintenance_triage_is_civic311_ready_without_dispatch():
    triage = triage_maintenance_request("Broken playground swing", "Oak Park")
    assert triage.suggested_category == "playground-equipment"
    assert triage.civic311_handoff_ready is True
    assert "does not dispatch crews" in triage.boundary
