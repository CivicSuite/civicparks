from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from civicparks.main import app, _dispose_workpaper_repository
from civicparks.persistence import ParksWorkpaperRepository
from civicparks.registration import RecreationProgram


client = TestClient(app)
PROGRAM = RecreationProgram("Swim lessons", "youth", "https://parks.example/register", "Ramp access")


def test_repository_persists_registration_and_maintenance(tmp_path: Path) -> None:
    db_path = tmp_path / "civicparks.db"
    repo = ParksWorkpaperRepository(db_url=f"sqlite+pysqlite:///{db_path.as_posix()}")
    reg = repo.create_registration(program=PROGRAM)
    triage = repo.create_maintenance(issue="trash bin full", location="Oak Park")
    repo.engine.dispose()
    reloaded = ParksWorkpaperRepository(db_url=f"sqlite+pysqlite:///{db_path.as_posix()}")
    assert reloaded.get_registration(reg.assistance_id).program_title == "Swim lessons"
    assert reloaded.get_maintenance(triage.triage_id).suggested_category == "park-cleanup"
    reloaded.engine.dispose()
    db_path.unlink()


def test_parks_persistence_api_round_trip(monkeypatch, tmp_path: Path) -> None:
    db_path = tmp_path / "civicparks-api.db"
    monkeypatch.setenv("CIVICPARKS_WORKPAPER_DB_URL", f"sqlite+pysqlite:///{db_path.as_posix()}")
    _dispose_workpaper_repository()
    reg = client.post("/api/v1/civicparks/registration-assistance", json={"program": PROGRAM.__dict__})
    fetched_reg = client.get(f"/api/v1/civicparks/registration-assistance/{reg.json()['assistance_id']}")
    triage = client.post("/api/v1/civicparks/maintenance-triage", json={"issue":"trash bin full","location":"Oak Park"})
    fetched_triage = client.get(f"/api/v1/civicparks/maintenance-triage/{triage.json()['triage_id']}")
    _dispose_workpaper_repository()
    monkeypatch.delenv("CIVICPARKS_WORKPAPER_DB_URL")
    assert fetched_reg.status_code == 200
    assert fetched_reg.json()["staff_review_required"] is True
    assert fetched_triage.status_code == 200
    assert fetched_triage.json()["suggested_category"] == "park-cleanup"
    db_path.unlink()


def test_get_registration_without_persistence_returns_actionable_503(monkeypatch) -> None:
    monkeypatch.delenv("CIVICPARKS_WORKPAPER_DB_URL", raising=False)
    _dispose_workpaper_repository()
    response = client.get("/api/v1/civicparks/registration-assistance/example")
    assert response.status_code == 503
    assert "Set CIVICPARKS_WORKPAPER_DB_URL" in response.json()["detail"]["fix"]


def test_get_maintenance_missing_id_returns_actionable_404(monkeypatch, tmp_path: Path) -> None:
    db_path = tmp_path / "civicparks-missing.db"
    monkeypatch.setenv("CIVICPARKS_WORKPAPER_DB_URL", f"sqlite+pysqlite:///{db_path.as_posix()}")
    _dispose_workpaper_repository()
    response = client.get("/api/v1/civicparks/maintenance-triage/missing")
    _dispose_workpaper_repository()
    monkeypatch.delenv("CIVICPARKS_WORKPAPER_DB_URL")
    assert response.status_code == 404
    assert "POST /api/v1/civicparks/maintenance-triage" in response.json()["detail"]["fix"]
    db_path.unlink()
