"""FastAPI runtime foundation for CivicParks."""

from civiccore import __version__ as CIVICCORE_VERSION
from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from civicparks import __version__
from civicparks.maintenance import triage_maintenance_request
from civicparks.policy import ParksPolicySource, answer_policy_question
from civicparks.programs import ParksProgram, answer_program_question
from civicparks.public_ui import render_public_lookup_page
from civicparks.registration import RecreationProgram, draft_registration_assistance

app = FastAPI(
    title="CivicParks",
    version=__version__,
    description="Parks and recreation policy, program, registration-link, and maintenance-triage foundation.",
)

@app.get("/favicon.ico", include_in_schema=False)
def favicon() -> Response:
    """Return an empty favicon response so browser QA has a clean console."""

    return Response(status_code=204)

POLICY_SOURCES = [
    ParksPolicySource(
        "policy-1",
        "Park rental policy",
        "Facility rentals require staff confirmation and published fee schedules.",
        "Parks Policy 1",
    )
]


class PolicyQuestionRequest(BaseModel):
    question: str


class ProgramQuestionRequest(BaseModel):
    question: str
    programs: list[ParksProgram]


class RegistrationAssistanceRequest(BaseModel):
    program: RecreationProgram


class MaintenanceTriageRequest(BaseModel):
    issue: str
    location: str


@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": "CivicParks",
        "version": __version__,
        "status": "parks and recreation support foundation",
        "message": (
            "CivicParks policy Q&A, program Q&A, registration-link assistance, "
            "maintenance triage, and public UI foundation are online; payments, "
            "registrations, participant records, reservation writes, crew dispatch, "
            "live LLM calls, and connector runtime are not implemented yet."
        ),
        "next_step": "Post-v0.1.1 roadmap: registration-system and Civic311 handoff adapter design",
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "civicparks",
        "version": __version__,
        "civiccore_version": CIVICCORE_VERSION,
    }


@app.get("/civicparks", response_class=HTMLResponse)
def public_page() -> str:
    return render_public_lookup_page()


@app.post("/api/v1/civicparks/policy-answer")
def policy_answer(request: PolicyQuestionRequest) -> dict[str, object]:
    return answer_policy_question(request.question, POLICY_SOURCES).__dict__


@app.post("/api/v1/civicparks/program-answer")
def program_answer(request: ProgramQuestionRequest) -> dict[str, object]:
    return answer_program_question(request.question, request.programs).__dict__


@app.post("/api/v1/civicparks/registration-assistance")
def registration_assistance(request: RegistrationAssistanceRequest) -> dict[str, object]:
    return draft_registration_assistance(request.program).__dict__


@app.post("/api/v1/civicparks/maintenance-triage")
def maintenance_triage(request: MaintenanceTriageRequest) -> dict[str, object]:
    return triage_maintenance_request(request.issue, request.location).__dict__
