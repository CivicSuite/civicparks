"""Registration-assistance helpers that link out to existing recreation systems."""

from dataclasses import dataclass


@dataclass(frozen=True)
class RecreationProgram:
    title: str
    audience: str
    registration_url: str
    accessibility_note: str


@dataclass(frozen=True)
class RegistrationAssistance:
    program_title: str
    registration_url: str
    assistance_text: str
    staff_review_required: bool
    boundary: str


def draft_registration_assistance(program: RecreationProgram) -> RegistrationAssistance:
    return RegistrationAssistance(
        program_title=program.title,
        registration_url=program.registration_url,
        assistance_text=(
            f"Draft registration guidance for {program.title}. Confirm fees, capacity, "
            "age rules, and accommodations in the city's registration system before sharing."
        ),
        staff_review_required=True,
        boundary=(
            "CivicParks links to existing registration systems only. It does not take "
            "payments, enroll participants, manage minor participant records, or replace "
            "RecTrac, CivicRec, or another system of record."
        ),
    )
