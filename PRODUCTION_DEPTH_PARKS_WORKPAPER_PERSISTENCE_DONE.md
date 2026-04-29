# Production Depth: Parks Workpaper Persistence

## Summary

CivicParks now supports optional SQLAlchemy-backed registration assistance and maintenance triage records through `CIVICPARKS_WORKPAPER_DB_URL`.

## Shipped

- `ParksWorkpaperRepository` with schema-aware SQLAlchemy tables.
- Persisted registration assistance records with `assistance_id`.
- Persisted maintenance triage records with `triage_id`.
- Retrieval endpoints for both persisted workpapers.
- Actionable `503` guidance when persistence is not configured.

## Still Not Shipped

- Payments.
- Registrations or participant records.
- Reservation writes.
- Crew dispatch.
- Live LLM calls.
- Parks connector runtime.
