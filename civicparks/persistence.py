from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy import Engine, create_engine

from civicparks.maintenance import triage_maintenance_request
from civicparks.registration import RecreationProgram, draft_registration_assistance


metadata = sa.MetaData()
registration_records = sa.Table("registration_records", metadata, sa.Column("assistance_id", sa.String(36), primary_key=True), sa.Column("program_title", sa.String(255), nullable=False), sa.Column("registration_url", sa.Text(), nullable=False), sa.Column("assistance_text", sa.Text(), nullable=False), sa.Column("staff_review_required", sa.Boolean(), nullable=False), sa.Column("boundary", sa.Text(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), schema="civicparks")
maintenance_records = sa.Table("maintenance_records", metadata, sa.Column("triage_id", sa.String(36), primary_key=True), sa.Column("issue", sa.Text(), nullable=False), sa.Column("suggested_category", sa.String(160), nullable=False), sa.Column("civic311_handoff_ready", sa.Boolean(), nullable=False), sa.Column("staff_review_required", sa.Boolean(), nullable=False), sa.Column("boundary", sa.Text(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), schema="civicparks")


@dataclass(frozen=True)
class StoredRegistrationAssistance:
    assistance_id: str
    program_title: str
    registration_url: str
    assistance_text: str
    staff_review_required: bool
    boundary: str
    created_at: datetime


@dataclass(frozen=True)
class StoredMaintenanceTriage:
    triage_id: str
    issue: str
    suggested_category: str
    civic311_handoff_ready: bool
    staff_review_required: bool
    boundary: str
    created_at: datetime


class ParksWorkpaperRepository:
    def __init__(self, *, db_url: str | None = None, engine: Engine | None = None) -> None:
        base_engine = engine or create_engine(db_url or "sqlite+pysqlite:///:memory:", future=True)
        if base_engine.dialect.name == "sqlite":
            self.engine = base_engine.execution_options(schema_translate_map={"civicparks": None})
        else:
            self.engine = base_engine
            with self.engine.begin() as connection:
                connection.execute(sa.text("CREATE SCHEMA IF NOT EXISTS civicparks"))
        metadata.create_all(self.engine)

    def create_registration(self, *, program: RecreationProgram) -> StoredRegistrationAssistance:
        draft = draft_registration_assistance(program)
        stored = StoredRegistrationAssistance(str(uuid4()), draft.program_title, draft.registration_url, draft.assistance_text, draft.staff_review_required, draft.boundary, datetime.now(UTC))
        with self.engine.begin() as connection:
            connection.execute(registration_records.insert().values(**stored.__dict__))
        return stored

    def get_registration(self, assistance_id: str) -> StoredRegistrationAssistance | None:
        with self.engine.begin() as connection:
            row = connection.execute(sa.select(registration_records).where(registration_records.c.assistance_id == assistance_id)).mappings().first()
        return None if row is None else StoredRegistrationAssistance(**dict(row))

    def create_maintenance(self, *, issue: str, location: str) -> StoredMaintenanceTriage:
        draft = triage_maintenance_request(issue, location)
        stored = StoredMaintenanceTriage(str(uuid4()), draft.issue, draft.suggested_category, draft.civic311_handoff_ready, draft.staff_review_required, draft.boundary, datetime.now(UTC))
        with self.engine.begin() as connection:
            connection.execute(maintenance_records.insert().values(**stored.__dict__))
        return stored

    def get_maintenance(self, triage_id: str) -> StoredMaintenanceTriage | None:
        with self.engine.begin() as connection:
            row = connection.execute(sa.select(maintenance_records).where(maintenance_records.c.triage_id == triage_id)).mappings().first()
        return None if row is None else StoredMaintenanceTriage(**dict(row))
