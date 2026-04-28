"""Maintenance request triage helpers for Civic311-compatible handoff."""

from dataclasses import dataclass


@dataclass(frozen=True)
class MaintenanceTriage:
    issue: str
    suggested_category: str
    civic311_handoff_ready: bool
    staff_review_required: bool
    boundary: str


def triage_maintenance_request(issue: str, location: str) -> MaintenanceTriage:
    normalized = f"{issue} {location}".lower()
    if "light" in normalized or "lamp" in normalized:
        category = "park-lighting"
    elif "trash" in normalized or "litter" in normalized:
        category = "park-cleanup"
    elif "playground" in normalized or "swing" in normalized:
        category = "playground-equipment"
    else:
        category = "parks-general"

    return MaintenanceTriage(
        issue=issue,
        suggested_category=category,
        civic311_handoff_ready=True,
        staff_review_required=True,
        boundary=(
            "Draft triage only. CivicParks does not dispatch crews, create work orders, "
            "or write into Civic311 in v0.1.1."
        ),
    )
