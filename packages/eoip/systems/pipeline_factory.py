"""Pipeline Factory — automatically creates ingestion pipelines for newly connected systems.

When a new system is registered, this module:
1. Determines the optimal pipeline topology (stages, parallelism, error handling)
2. Creates connector, mapping, and ingestion configurations
3. Sets up scheduled/event-driven/manual sync modes
4. Configures monitoring, alerting, and dead-letter queue handling
5. Produces a complete PipelineSpec that can be executed immediately
"""

from __future__ import annotations

import time
import uuid
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any

from eoip.systems.registry import (
    SystemCategory, SystemEntry, KNOWN_SYSTEM_TYPES,
)
from eoip.systems.schema_generator import GeneratedSchema


class PipelineStageType(str, Enum):
    CONNECT = "CONNECT"
    DISCOVER = "DISCOVER"
    EXTRACT = "EXTRACT"
    PROFILE = "PROFILE"
    TRANSFORM = "TRANSFORM"
    MAP = "MAP"
    VALIDATE = "VALIDATE"
    DEDUPLICATE = "DEDUPLICATE"
    RESOLVE_IDENTITY = "RESOLVE_IDENTITY"
    ENRICH = "ENRICH"
    LOAD = "LOAD"
    INDEX = "INDEX"
    VERIFY = "VERIFY"
    NOTIFY = "NOTIFY"


@dataclass
class PipelineStage:
    stage_id: str
    stage_type: PipelineStageType
    name: str
    config: dict[str, Any] = field(default_factory=dict)
    depends_on: list[str] = field(default_factory=list)
    retry_on_failure: bool = True
    timeout_seconds: int = 300
    parallel: bool = False


@dataclass
class PipelineSchedule:
    mode: str  # immediate, cron, interval, event_driven, manual
    cron_expression: str | None = None
    interval_minutes: int = 60
    event_triggers: list[str] = field(default_factory=list)


@dataclass
class PipelineMonitoring:
    metrics_enabled: bool = True
    alerting_enabled: bool = True
    dlq_enabled: bool = True
    log_level: str = "INFO"
    alert_on_failure: bool = True
    alert_on_drift: bool = True
    max_consecutive_failures: int = 3


@dataclass
class PipelineSpec:
    pipeline_id: str
    system_id: str
    system_type: str
    name: str
    stages: list[PipelineStage]
    schedule: PipelineSchedule
    monitoring: PipelineMonitoring
    schema_version: str = "1.0.0"
    created_at: str = ""
    status: str = "CREATED"
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        for stage in d["stages"]:
            stage["stage_type"] = stage["stage_type"]
        return d

    def get_execution_order(self) -> list[str]:
        visited: set[str] = set()
        order: list[str] = []
        stage_map = {s.stage_id: s for s in self.stages}

        def visit(sid: str) -> None:
            if sid in visited:
                return
            visited.add(sid)
            stage = stage_map.get(sid)
            if stage:
                for dep in stage.depends_on:
                    visit(dep)
                order.append(sid)

        for s in self.stages:
            visit(s.stage_id)
        return order


class PipelineFactory:
    """Creates optimized ingestion pipelines from system configuration and schema."""

    def create_pipeline(
        self,
        system: SystemEntry,
        schema: GeneratedSchema | None = None,
    ) -> PipelineSpec:
        pipeline_id = f"pipeline-{system.system_id}-{uuid.uuid4().hex[:6]}"
        stages = self._build_stages(system, schema)
        schedule = self._build_schedule(system)
        monitoring = self._build_monitoring(system)

        return PipelineSpec(
            pipeline_id=pipeline_id,
            system_id=system.system_id,
            system_type=system.system_type,
            name=f"{system.name} Ingestion Pipeline",
            stages=stages,
            schedule=schedule,
            monitoring=monitoring,
            created_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            metadata={
                "system_category": system.category.value,
                "entity_types": system.ingestion.entity_types,
                "schema_available": schema is not None,
            },
        )

    def create_manual_pipeline(self, system: SystemEntry) -> PipelineSpec:
        spec = self.create_pipeline(system)
        spec.schedule = PipelineSchedule(mode="manual")
        spec.name = f"{system.name} Manual Import Pipeline"
        return spec

    def _build_stages(self, system: SystemEntry,
                      schema: GeneratedSchema | None) -> list[PipelineStage]:
        stages: list[PipelineStage] = []

        # Stage 1: Connect
        stages.append(PipelineStage(
            stage_id="connect",
            stage_type=PipelineStageType.CONNECT,
            name="Establish Connection",
            config={
                "base_url": system.connection.base_url,
                "timeout_seconds": 30,
            },
            timeout_seconds=60,
        ))

        # Stage 2: Discover (for API-based systems)
        if system.category in (
            SystemCategory.PROJECT_MANAGEMENT, SystemCategory.SOURCE_CONTROL,
            SystemCategory.DOCUMENTATION, SystemCategory.ITSM,
            SystemCategory.MONITORING, SystemCategory.CI_CD,
        ):
            stages.append(PipelineStage(
                stage_id="discover",
                stage_type=PipelineStageType.DISCOVER,
                name="Discover Resources",
                config={"entity_types": system.ingestion.entity_types},
                depends_on=["connect"],
            ))

        # Stage 3: Extract
        stages.append(PipelineStage(
            stage_id="extract",
            stage_type=PipelineStageType.EXTRACT,
            name="Extract Data",
            config={
                "batch_size": system.ingestion.batch_size,
                "incremental": system.ingestion.incremental_sync,
                "entity_types": system.ingestion.entity_types,
            },
            depends_on=["discover"] if any(
                s.stage_id == "discover" for s in stages
            ) else ["connect"],
            timeout_seconds=600,
        ))

        # Stage 4: Profile (for auto-schema)
        if system.ingestion.auto_schema_induction:
            stages.append(PipelineStage(
                stage_id="profile",
                stage_type=PipelineStageType.PROFILE,
                name="Profile & Induce Schema",
                config={
                    "auto_schema": True,
                    "detect_keys": True,
                    "detect_relationships": True,
                    "drift_detection": system.ingestion.schema_drift_detection,
                },
                depends_on=["extract"],
            ))

        # Stage 5: Transform
        stages.append(PipelineStage(
            stage_id="transform",
            stage_type=PipelineStageType.TRANSFORM,
            name="Transform & Normalize",
            config={
                "mappings": schema.field_mappings if schema else {},
                "custom_mappings": system.ingestion.custom_mappings,
            },
            depends_on=["profile"] if any(
                s.stage_id == "profile" for s in stages
            ) else ["extract"],
        ))

        # Stage 6: Map to ontology
        stages.append(PipelineStage(
            stage_id="map",
            stage_type=PipelineStageType.MAP,
            name="Map to Ontology",
            config={
                "entity_labels": schema.ontology_labels["vertex_labels"] if schema else [],
                "edge_labels": schema.ontology_labels["edge_labels"] if schema else [],
            },
            depends_on=["transform"],
        ))

        # Stage 7: Validate
        stages.append(PipelineStage(
            stage_id="validate",
            stage_type=PipelineStageType.VALIDATE,
            name="Validate Entities",
            config={
                "validation_rules": schema.validation_rules if schema else [],
                "reject_invalid": False,
                "dlq_enabled": system.ingestion.dead_letter_queue_enabled,
            },
            depends_on=["map"],
        ))

        # Stage 8: Deduplicate
        stages.append(PipelineStage(
            stage_id="deduplicate",
            stage_type=PipelineStageType.DEDUPLICATE,
            name="Deduplicate Records",
            config={"strategy": "canonical_id_merge"},
            depends_on=["validate"],
        ))

        # Stage 9: Identity Resolution
        stages.append(PipelineStage(
            stage_id="resolve_identity",
            stage_type=PipelineStageType.RESOLVE_IDENTITY,
            name="Resolve Identities",
            config={"cross_source": True},
            depends_on=["deduplicate"],
        ))

        # Stage 10: Enrich
        stages.append(PipelineStage(
            stage_id="enrich",
            stage_type=PipelineStageType.ENRICH,
            name="Semantic Enrichment",
            config={"bridge_edges": True, "metadata_enrichment": True},
            depends_on=["resolve_identity"],
        ))

        # Stage 11: Load into graph
        stages.append(PipelineStage(
            stage_id="load",
            stage_type=PipelineStageType.LOAD,
            name="Load into Knowledge Graph",
            config={"upsert_mode": True, "provenance_tracking": True},
            depends_on=["enrich"],
            timeout_seconds=600,
        ))

        # Stage 12: Index
        stages.append(PipelineStage(
            stage_id="index",
            stage_type=PipelineStageType.INDEX,
            name="Update Search Index",
            config={"vector_index": True, "full_text_index": True},
            depends_on=["load"],
            parallel=True,
        ))

        # Stage 13: Verify
        stages.append(PipelineStage(
            stage_id="verify",
            stage_type=PipelineStageType.VERIFY,
            name="Verify Ingestion",
            config={"reconciliation": True, "count_check": True},
            depends_on=["load"],
        ))

        # Stage 14: Notify
        stages.append(PipelineStage(
            stage_id="notify",
            stage_type=PipelineStageType.NOTIFY,
            name="Send Notifications",
            config={"channels": ["audit_log", "webhook"]},
            depends_on=["verify"],
            retry_on_failure=False,
        ))

        return stages

    def _build_schedule(self, system: SystemEntry) -> PipelineSchedule:
        mode = system.ingestion.mode
        if mode == "event_driven":
            return PipelineSchedule(
                mode="event_driven",
                event_triggers=["webhook", "file_watch", "cdc_event"],
            )
        if mode == "scheduled" and system.ingestion.cron_expression:
            return PipelineSchedule(
                mode="cron",
                cron_expression=system.ingestion.cron_expression,
            )
        if mode == "manual":
            return PipelineSchedule(mode="manual")
        return PipelineSchedule(
            mode="interval",
            interval_minutes=system.ingestion.poll_interval_minutes,
        )

    def _build_monitoring(self, system: SystemEntry) -> PipelineMonitoring:
        return PipelineMonitoring(
            metrics_enabled=True,
            alerting_enabled=True,
            dlq_enabled=system.ingestion.dead_letter_queue_enabled,
            alert_on_failure=True,
            alert_on_drift=system.ingestion.schema_drift_detection,
        )
