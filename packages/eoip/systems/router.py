"""FastAPI router for Systems Registry — register, configure, onboard, and manage connected systems."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from eoip.systems.registry import (
    SystemsRegistry, SystemStatus, KNOWN_SYSTEM_TYPES,
)
from eoip.systems.schema_generator import AutoSchemaGenerator
from eoip.systems.pipeline_factory import PipelineFactory
from eoip.systems.auto_onboard import AutoOnboardOrchestrator

router = APIRouter(prefix="/systems", tags=["Systems Registry"])

_CONFIG_PATH = Path("config/systems-registry.json")
_registry = SystemsRegistry(str(_CONFIG_PATH))
_schema_gen = AutoSchemaGenerator()
_pipeline_factory = PipelineFactory()
_orchestrator = AutoOnboardOrchestrator(_registry, _schema_gen, _pipeline_factory)


# ── Request / Response Models ────────────────────────────────────────

class RegisterSystemRequest(BaseModel):
    system_type: str = Field(..., description="e.g. jira, gitlab, postgresql")
    name: str = Field(..., min_length=1, max_length=256)
    base_url: str = Field(..., min_length=1)
    auth_type: str = "token"
    credentials: dict[str, Any] = Field(default_factory=dict)
    entity_types: list[str] = Field(default_factory=list)
    ingestion_mode: str = "auto"
    poll_interval_minutes: int = 60
    batch_size: int = 500
    tags: list[str] = Field(default_factory=list)
    auto_onboard: bool = True


class UpdateSystemRequest(BaseModel):
    name: str | None = None
    base_url: str | None = None
    auth_type: str | None = None
    credentials: dict[str, Any] | None = None
    entity_types: list[str] | None = None
    ingestion_mode: str | None = None
    poll_interval_minutes: int | None = None
    batch_size: int | None = None
    tags: list[str] | None = None


class OnboardRequest(BaseModel):
    sample_data: list[dict[str, Any]] | dict[str, Any] | None = None
    skip_ingestion: bool = False


class SchemaFromDataRequest(BaseModel):
    system_id: str
    system_type: str
    data: list[dict[str, Any]] | dict[str, Any]
    dataset_name: str | None = None


# ── Endpoints ────────────────────────────────────────────────────────

@router.get("/known-types")
def list_known_types() -> dict[str, Any]:
    return {"known_types": KNOWN_SYSTEM_TYPES}


@router.get("/")
def list_systems(
    status: str | None = None,
    category: str | None = None,
) -> dict[str, Any]:
    systems = _registry.list_systems()
    if status:
        systems = [s for s in systems if s.status.value == status]
    if category:
        systems = [s for s in systems if s.category.value == category]
    return {
        "count": len(systems),
        "systems": [_system_summary(s) for s in systems],
    }


@router.get("/{system_id}")
def get_system(system_id: str) -> dict[str, Any]:
    s = _registry.get_system(system_id)
    if not s:
        raise HTTPException(404, f"System {system_id} not found")
    return _system_detail(s)


@router.post("/register")
def register_system(req: RegisterSystemRequest) -> dict[str, Any]:
    entry = _registry.register_system(
        name=req.name,
        system_type=req.system_type,
        connection={"base_url": req.base_url},
        auth={"auth_type": req.auth_type, "credentials": req.credentials},
        ingestion={
            "mode": req.ingestion_mode,
            "entity_types": req.entity_types,
            "poll_interval_minutes": req.poll_interval_minutes,
            "batch_size": req.batch_size,
        },
        tags=req.tags,
    )

    result: dict[str, Any] = {
        "system_id": entry.system_id,
        "status": "REGISTERED",
    }

    if req.auto_onboard:
        onboard_result = _orchestrator.onboard(entry)
        result["onboarding"] = onboard_result.to_dict()

    return result


@router.put("/{system_id}")
def update_system(system_id: str, req: UpdateSystemRequest) -> dict[str, Any]:
    s = _registry.get_system(system_id)
    if not s:
        raise HTTPException(404, f"System {system_id} not found")

    updates: dict[str, Any] = {}
    if req.name is not None:
        updates["name"] = req.name
    if req.base_url is not None:
        updates["connection"] = {"base_url": req.base_url}
    if req.auth_type is not None or req.credentials is not None:
        auth_update: dict[str, Any] = {}
        if req.auth_type is not None:
            auth_update["auth_type"] = req.auth_type
        if req.credentials is not None:
            auth_update["credentials"] = req.credentials
        updates["auth"] = auth_update
    ing_updates: dict[str, Any] = {}
    if req.entity_types is not None:
        ing_updates["entity_types"] = req.entity_types
    if req.ingestion_mode is not None:
        ing_updates["mode"] = req.ingestion_mode
    if req.poll_interval_minutes is not None:
        ing_updates["poll_interval_minutes"] = req.poll_interval_minutes
    if req.batch_size is not None:
        ing_updates["batch_size"] = req.batch_size
    if ing_updates:
        updates["ingestion"] = ing_updates
    if req.tags is not None:
        updates["tags"] = req.tags

    _registry.update_system(system_id, updates)
    return {"system_id": system_id, "updated": list(updates.keys())}


@router.delete("/{system_id}")
def remove_system(system_id: str) -> dict[str, Any]:
    s = _registry.get_system(system_id)
    if not s:
        raise HTTPException(404, f"System {system_id} not found")
    _registry.remove_system(system_id)
    return {"system_id": system_id, "removed": True}


@router.post("/{system_id}/test-connection")
def test_connection(system_id: str) -> dict[str, Any]:
    s = _registry.get_system(system_id)
    if not s:
        raise HTTPException(404, f"System {system_id} not found")
    result = _registry.test_connection(system_id)
    return result


@router.post("/{system_id}/set-status")
def set_status(system_id: str, status: str) -> dict[str, Any]:
    s = _registry.get_system(system_id)
    if not s:
        raise HTTPException(404, f"System {system_id} not found")
    try:
        new_status = SystemStatus(status)
    except ValueError:
        raise HTTPException(400, f"Invalid status: {status}")
    _registry.set_status(system_id, new_status)
    return {"system_id": system_id, "status": new_status.value}


@router.post("/{system_id}/onboard")
def onboard_system(system_id: str, req: OnboardRequest) -> dict[str, Any]:
    s = _registry.get_system(system_id)
    if not s:
        raise HTTPException(404, f"System {system_id} not found")
    result = _orchestrator.onboard(s, sample_data=req.sample_data, skip_ingestion=req.skip_ingestion)
    return result.to_dict()


@router.get("/{system_id}/onboarding-status")
def get_onboarding_status(system_id: str) -> dict[str, Any]:
    status = _orchestrator.get_onboarding_status(system_id)
    if not status:
        raise HTTPException(404, f"No onboarding record for {system_id}")
    return status


@router.post("/{system_id}/generate-schema")
def generate_schema_for_system(system_id: str, req: OnboardRequest) -> dict[str, Any]:
    s = _registry.get_system(system_id)
    if not s:
        raise HTTPException(404, f"System {system_id} not found")
    if not req.sample_data:
        raise HTTPException(400, "sample_data is required for schema generation")
    schema = _schema_gen.generate_from_json(s.system_id, s.system_type, req.sample_data)
    return {
        "system_id": system_id,
        "entities": len(schema.entities),
        "relationships": len(schema.relationships),
        "graphql_sdl": schema.graphql_sdl,
        "json_schema": schema.json_schema,
        "field_mappings": schema.field_mappings,
        "golden_queries": schema.golden_queries,
        "validation_rules": schema.validation_rules,
    }


@router.post("/{system_id}/create-pipeline")
def create_pipeline(system_id: str) -> dict[str, Any]:
    s = _registry.get_system(system_id)
    if not s:
        raise HTTPException(404, f"System {system_id} not found")
    pipeline = _pipeline_factory.create_pipeline(s)
    return pipeline.to_dict()


@router.post("/schema/from-data")
def generate_schema_from_data(req: SchemaFromDataRequest) -> dict[str, Any]:
    schema = _schema_gen.generate_from_json(
        req.system_id, req.system_type, req.data, req.dataset_name,
    )
    return {
        "system_id": req.system_id,
        "entities": [{"label": e.label, "fields": len(e.fields), "records": e.record_count} for e in schema.entities],
        "relationships": [{"edge": r.edge_label, "from": r.from_entity, "to": r.to_entity} for r in schema.relationships],
        "graphql_sdl": schema.graphql_sdl,
        "json_schema": schema.json_schema,
        "field_mappings": schema.field_mappings,
        "golden_queries": schema.golden_queries,
        "validation_rules": schema.validation_rules,
        "data_fingerprint": schema.data_fingerprint,
    }


@router.get("/export/config")
def export_config() -> dict[str, Any]:
    return _registry.export_config()


@router.post("/import/config")
def import_config(config: dict[str, Any]) -> dict[str, Any]:
    count = _registry.import_config(config)
    return {"imported": True, "system_count": count}


# ── Helpers ──────────────────────────────────────────────────────────

def build_systems_router() -> APIRouter:
    return router


def _system_summary(s: SystemEntry) -> dict[str, Any]:
    return {
        "system_id": s.system_id,
        "system_type": s.system_type,
        "name": s.name,
        "category": s.category.value,
        "status": s.status.value,
        "tags": s.tags,
    }


def _system_detail(s: SystemEntry) -> dict[str, Any]:
    return {
        "system_id": s.system_id,
        "system_type": s.system_type,
        "name": s.name,
        "category": s.category.value,
        "status": s.status.value,
        "connection": {
            "base_url": s.connection.base_url,
            "port": s.connection.port,
            "database_name": s.connection.database_name,
        },
        "auth_type": s.auth.auth_type.value,
        "ingestion": {
            "mode": s.ingestion.mode,
            "entity_types": s.ingestion.entity_types,
            "batch_size": s.ingestion.batch_size,
            "poll_interval_minutes": s.ingestion.poll_interval_minutes,
            "cron_expression": s.ingestion.cron_expression,
            "incremental_sync": s.ingestion.incremental_sync,
            "auto_schema_induction": s.ingestion.auto_schema_induction,
            "schema_drift_detection": s.ingestion.schema_drift_detection,
        },
        "schema": {
            "graphql_sdl": s.schema.graphql_sdl,
            "json_schema": s.schema.json_schema,
            "entity_labels": s.schema.entity_labels,
            "edge_labels": s.schema.edge_labels,
        },
        "tags": s.tags,
        "created_at": s.created_at,
        "last_sync_at": s.last_sync_at,
        "last_health_check": s.last_health_check,
        "metadata": s.metadata,
    }
