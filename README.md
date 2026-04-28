# CivicParks

CivicParks v0.1.1 ships the municipal parks and recreation support foundation for CivicSuite: cited parks policy Q&A, program and facility Q&A, registration assistance that links to existing systems, maintenance request triage for Civic311-style handoff, FastAPI runtime, public sample UI, docs, tests, browser QA, and release gates.

It is not a registration system, payment processor, reservation system, participant-record store, work-order system, live LLM runtime, or parks connector.

Install:

```bash
python -m pip install -e ".[dev]"
python -m uvicorn civicparks.main:app --host 127.0.0.1 --port 8143
```

CivicParks v0.1.1 is pinned to `civiccore==0.3.0`.

Apache 2.0 code. CC BY 4.0 docs.
