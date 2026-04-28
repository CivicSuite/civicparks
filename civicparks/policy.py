"""Parks policy and facility-rule Q&A helpers."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ParksPolicySource:
    source_id: str
    title: str
    text: str
    citation: str


@dataclass(frozen=True)
class ParksPolicyAnswer:
    answer: str
    citations: tuple[str, ...]
    staff_review_required: bool
    boundary: str


def answer_policy_question(question: str, sources: list[ParksPolicySource]) -> ParksPolicyAnswer:
    citations = tuple(source.citation for source in sources if source.text)
    return ParksPolicyAnswer(
        answer=(
            f"Draft parks policy or facility-rule answer for: {question}. "
            "Verify fees, rental terms, league rules, and posted park rules before sharing."
        ),
        citations=citations,
        staff_review_required=True,
        boundary=(
            "CivicParks supports policy and program information only. It does not process "
            "registrations, payments, reservations, participant records, or maintenance dispatch."
        ),
    )
