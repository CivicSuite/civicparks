# CivicParks Architecture

CivicParks v0.1.0 is a deterministic FastAPI module over CivicCore. It supports parks policy answers, program and facility questions, registration-link guidance, and maintenance request triage while explicitly avoiding payment processing, participant records, registration writes, facility reservation writes, crew dispatch, live connectors, and live LLM calls.

![CivicParks architecture](architecture-civicparks.svg)

## Shipped

- Parks policy and facility-rule answer drafts with citations and staff-review language.
- Program and event answer drafts with accessibility review prompts.
- Registration assistance that links to existing systems without writing to them.
- Maintenance request triage with Civic311-style handoff categories and staff review.
- Public sample UI and release gates.

## Not Shipped

- Payment processing, registrations, enrollments, or participant records.
- Facility reservation writes.
- Work-order creation or crew dispatch.
- Replacement for RecTrac, CivicRec, Civic311, or another system of record.
- Live parks connectors.
- Live LLM calls.
