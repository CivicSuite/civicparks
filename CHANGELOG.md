# Changelog

## [0.1.1] - 2026-04-28

### Added

- Optional SQLAlchemy-backed registration assistance and maintenance triage workpaper records via `CIVICPARKS_WORKPAPER_DB_URL`.
- Registration assistance and maintenance triage retrieval endpoints for persisted records.

### Changed

- Dependency-alignment release: moved CivicParks to `civiccore==0.3.0` while preserving the existing v0.1.0 runtime foundation behavior.
- Updated CI, verification gates, package metadata, docs, runtime tests, landing page, and public UI labels for the v0.1.1 release.

## [0.1.0] - 2026-04-27

### Added

- CivicParks runtime foundation with FastAPI health, root, public UI, and deterministic API endpoints.
- Parks policy Q&A, program/facility Q&A, registration-link assistance, and maintenance request triage helpers.
- Professional docs, browser QA artifacts, GitHub community templates, placeholder-import gate, release gate, and package build.
