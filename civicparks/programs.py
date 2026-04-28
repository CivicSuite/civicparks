"""Parks and recreation program Q&A helpers."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ParksProgram:
    title: str
    audience: str
    date: str
    accessibility_note: str


@dataclass(frozen=True)
class ProgramAnswer:
    answer: str
    programs: tuple[ParksProgram, ...]
    accessibility_review_required: bool
    registration_system_required: bool


def answer_program_question(question: str, programs: list[ParksProgram]) -> ProgramAnswer:
    return ProgramAnswer(
        answer=f"Draft parks and recreation program answer for: {question}",
        programs=tuple(programs),
        accessibility_review_required=True,
        registration_system_required=True,
    )
