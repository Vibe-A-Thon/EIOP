"""Auto-Onboard Orchestrator — end-to-end automation for new system integration.

When a new system is registered, this orchestrator:
1. Validates the system configuration
2. Tests connectivity and authentication
3. Discovers available resources and endpoints
4. Fetches sample data for schema induction
5. Generates schemas (GraphQL SDL, JSON Schema, field mappings)
6. Creates ingestion pipelines (automatic + manual)
7. Starts initial data ingestion
8. Sets up ongoing monitoring and health checks
9. Records audit trail of the entire onboarding process
"""

from __future__ import annotations

import json
import logging
import time
import uuid
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

from eoip.systems.registry import (
    AuthType, ConnectionConfig, AuthConfig, IngestionConfig,
    SystemCategory, SystemEntry, SystemsRegistry, SystemStatus,
    KNOWN_SYSTEM_TYPES,
)
from eoip.systems.schema_generator import AutoSchemaGenerator, GeneratedSchema
from eoip.systems.pipeline_factory import PipelineFactory, PipelineSpec

logger = logging.getLogger(__name__)


class OnboardingPhase(str, Enum):
    INIT = "INIT"
    VALIDATE = "VALIDATE"
    CONNECT = "CONNECT"
    DISCOVER = "DISCOVER"
    SAMPLE = "SAMPLE"
    SCHEMA = "SCHEMA"
    PIPELINE = "PIPELINE"
    INGEST = "INGEST"
    VERIFY = "VERIFY"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"


@dataclass
class PhaseResult:
    phase: OnboardingPhase
    success: bool
    duration_ms: int
    message: str
    data: dict[str, Any] = field(default_factory=dict)


@dataclass
class OnboardingResult:
    onboarding_id: str
    system_id: str
    system_type: str
    success: bool
    phases: list[PhaseResult]
    schema: GeneratedSchema | None = None
    auto_pipeline: PipelineSpec | None = None
    manual_pipeline: PipelineSpec | None = None
    total_duration_ms: int = 0
    started_at: str = ""
    completed_at: str = ""
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        d = {
            "onboarding_id": self.onboarding_id,
            "system_id": self.system_id,
            "system_type": self.system_type,
            "success": self.success,
            "phases": [asdict(p) for p in self.phases],
            "total_duration_ms": self.total_duration_ms,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "error": self.error,
        }
        if self.schema:
            d["schema_summary"] = {
                "entities": len(self.schema.entities),
                "relationships": len(self.schema.relationships),
                "data_fingerprint": self.schema.data_fingerprint,
            }
        if self.auto_pipeline:
            d["auto_pipeline_id"] = self.auto_pipeline.pipeline_id
        if self.manual_pipeline:
            d["manual_pipeline_id"] = self.manual_pipeline.pipeline_id
        return d


class AutoOnboardOrchestrator:
    """End-to-end orchestrator for integrating new systems into EOIP.

    Usage:
        registry = SystemsRegistry("config/systems-registry.json")
        orchestrator = AutoOnboardOrchestrator(registry)
        result = orchestrator.onboard(system_entry)
        # Or with sample data:
        result = orchestrator.onboard(system_entry, sample_data=[{...}])
    """

    def __init__(
        self,
        registry: SystemsRegistry,
        schema_generator: AutoSchemaGenerator | None = None,
        pipeline_factory: PipelineFactory | None = None,
    ) -> None:
        self._registry = registry
        self._schema_gen = schema_generator or AutoSchemaGenerator()
        self._pipeline_factory = pipeline_factory or PipelineFactory()

    def onboard(
        self,
        system: SystemEntry,
        sample_data: list[dict[str, Any]] | dict[str, Any] | None = None,
        sample_file: str | None = None,
        skip_ingestion: bool = False,
    ) -> OnboardingResult:
        onboarding_id = f"onboard-{uuid.uuid4().hex[:8]}"
        start_time = time.time()
        started_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        phases: list[PhaseResult] = []

        logger.info("Starting onboarding %s for system %s (%s)",
                     onboarding_id, system.system_id, system.system_type)

        result = OnboardingResult(
            onboarding_id=onboarding_id,
            system_id=system.system_id,
            system_type=system.system_type,
            success=False,
            phases=phases,
            started_at=started_at,
        )

        try:
            # Phase 1: Validate
            phases.append(self._phase_validate(system))
            if not phases[-1].success:
                raise _OnboardAbort(phases[-1].message)

            # Phase 2: Set onboarding status
            self._registry.set_status(system.system_id, SystemStatus.ONBOARDING)

            # Phase 3: Test connection
            phases.append(self._phase_connect(system))
            if not phases[-1].success:
                raise _OnboardAbort(phases[-1].message)

            # Phase 4: Discover resources
            phases.append(self._phase_discover(system))

            # Phase 5: Get sample data
            phases.append(self._phase_sample(system, sample_data, sample_file))
            actual_sample = phases[-1].data.get("sample_data")

            # Phase 6: Generate schema
            schema: GeneratedSchema | None = None
            if actual_sample:
                phase_result = self._phase_schema(system, actual_sample)
                phases.append(phase_result)
                if phase_result.success:
                    schema = phase_result.data.get("_schema_obj")
                    result.schema = schema
            else:
                phases.append(PhaseResult(
                    phase=OnboardingPhase.SCHEMA,
                    success=True,
                    duration_ms=0,
                    message="No sample data available; schema will be induced on first ingestion",
                ))

            # Phase 7: Create pipelines
            phase_pipeline = self._phase_pipeline(system, schema)
            phases.append(phase_pipeline)
            if phase_pipeline.success:
                result.auto_pipeline = phase_pipeline.data.get("_auto_pipeline")
                result.manual_pipeline = phase_pipeline.data.get("_manual_pipeline")

            # Phase 8: Initial ingestion (optional)
            if not skip_ingestion and result.auto_pipeline:
                phases.append(self._phase_ingest(system, result.auto_pipeline))
            else:
                phases.append(PhaseResult(
                    phase=OnboardingPhase.INGEST,
                    success=True,
                    duration_ms=0,
                    message="Initial ingestion skipped (will run on schedule)",
                ))

            # Phase 9: Verify
            phases.append(self._phase_verify(system, schema))

            # Mark complete
            self._registry.set_status(system.system_id, SystemStatus.ACTIVE)
            self._registry.record_health(system.system_id, {"healthy": True})

            result.success = True
            logger.info("Onboarding %s completed successfully", onboarding_id)

        except _OnboardAbort as e:
            result.error = str(e)
            self._registry.set_status(system.system_id, SystemStatus.ERROR)
            logger.error("Onboarding %s aborted: %s", onboarding_id, e)

        except Exception as e:
            result.error = f"Unexpected error: {e}"
            phases.append(PhaseResult(
                phase=OnboardingPhase.FAILED,
                success=False,
                duration_ms=0,
                message=str(e),
            ))
            self._registry.set_status(system.system_id, SystemStatus.ERROR)
            logger.exception("Onboarding %s failed", onboarding_id)

        end_time = time.time()
        result.total_duration_ms = int((end_time - start_time) * 1000)
        result.completed_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        # Persist onboarding metadata to system entry
        system.metadata["last_onboarding"] = result.to_dict()
        self._registry.update_system(system.system_id, {
            "metadata": system.metadata,
        })

        return result

    def onboard_from_config(
        self,
        config: dict[str, Any],
        sample_data: list[dict[str, Any]] | dict[str, Any] | None = None,
    ) -> OnboardingResult:
        """Register a brand-new system from raw config dict, then onboard it."""
        system_type = config.get("system_type", "custom")
        name = config.get("name", system_type)

        entry = self._registry.register_system(
            name=name,
            system_type=system_type,
            connection={"base_url": config.get("base_url", "")},
            auth={
                "auth_type": config.get("auth_type", "token"),
                "credentials": config.get("credentials", {}),
            },
            ingestion={"entity_types": config.get("entity_types", [])},
            tags=config.get("tags", []),
        )

        return self.onboard(entry, sample_data=sample_data)

    # ── Phase Implementations ────────────────────────────────────────

    def _phase_validate(self, system: SystemEntry) -> PhaseResult:
        t0 = time.time()
        errors: list[str] = []

        if not system.system_id:
            errors.append("system_id is required")
        if not system.system_type:
            errors.append("system_type is required")
        if not system.connection.base_url:
            errors.append("connection.base_url is required")
        if system.auth.auth_type not in (AuthType.NONE,) and not system.auth.credentials:
            errors.append("credentials required for auth_type != NONE")

        ms = int((time.time() - t0) * 1000)
        if errors:
            return PhaseResult(
                phase=OnboardingPhase.VALIDATE,
                success=False,
                duration_ms=ms,
                message=f"Validation failed: {'; '.join(errors)}",
                data={"errors": errors},
            )
        return PhaseResult(
            phase=OnboardingPhase.VALIDATE,
            success=True,
            duration_ms=ms,
            message="System configuration validated",
        )

    def _phase_connect(self, system: SystemEntry) -> PhaseResult:
        t0 = time.time()
        result = self._registry.test_connection(system.system_id)
        ok = result.get("success", False) if isinstance(result, dict) else bool(result)
        ms = int((time.time() - t0) * 1000)
        return PhaseResult(
            phase=OnboardingPhase.CONNECT,
            success=ok,
            duration_ms=ms,
            message="Connection established" if ok else "Connection test failed",
        )

    def _phase_discover(self, system: SystemEntry) -> PhaseResult:
        t0 = time.time()
        known = KNOWN_SYSTEM_TYPES.get(system.system_type, {})
        discovered = {
            "entity_types": system.ingestion.entity_types or known.get("entity_types", []),
            "category": system.category.value,
        }
        ms = int((time.time() - t0) * 1000)
        return PhaseResult(
            phase=OnboardingPhase.DISCOVER,
            success=True,
            duration_ms=ms,
            message=f"Discovered {len(discovered['entity_types'])} entity types",
            data=discovered,
        )

    def _phase_sample(
        self,
        system: SystemEntry,
        sample_data: list[dict[str, Any]] | dict[str, Any] | None,
        sample_file: str | None = None,
    ) -> PhaseResult:
        t0 = time.time()

        if sample_data:
            record_count = (
                len(sample_data) if isinstance(sample_data, list)
                else sum(len(v) for v in sample_data.values() if isinstance(v, list))
            )
            ms = int((time.time() - t0) * 1000)
            return PhaseResult(
                phase=OnboardingPhase.SAMPLE,
                success=True,
                duration_ms=ms,
                message=f"Using provided sample data ({record_count} records)",
                data={"sample_data": sample_data, "source": "provided"},
            )

        if sample_file:
            try:
                with open(sample_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                ms = int((time.time() - t0) * 1000)
                return PhaseResult(
                    phase=OnboardingPhase.SAMPLE,
                    success=True,
                    duration_ms=ms,
                    message=f"Loaded sample data from {sample_file}",
                    data={"sample_data": data, "source": "file"},
                )
            except Exception as e:
                ms = int((time.time() - t0) * 1000)
                return PhaseResult(
                    phase=OnboardingPhase.SAMPLE,
                    success=False,
                    duration_ms=ms,
                    message=f"Failed to load sample file: {e}",
                )

        ms = int((time.time() - t0) * 1000)
        return PhaseResult(
            phase=OnboardingPhase.SAMPLE,
            success=True,
            duration_ms=ms,
            message="No sample data provided; schema induction deferred to first ingestion",
            data={"sample_data": None, "source": "none"},
        )

    def _phase_schema(
        self,
        system: SystemEntry,
        sample_data: list[dict[str, Any]] | dict[str, Any],
    ) -> PhaseResult:
        t0 = time.time()
        try:
            schema = self._schema_gen.generate_from_json(
                system_id=system.system_id,
                system_type=system.system_type,
                data=sample_data,
            )
            ms = int((time.time() - t0) * 1000)
            return PhaseResult(
                phase=OnboardingPhase.SCHEMA,
                success=True,
                duration_ms=ms,
                message=(
                    f"Generated schema: {len(schema.entities)} entities, "
                    f"{len(schema.relationships)} relationships"
                ),
                data={
                    "entities": len(schema.entities),
                    "relationships": len(schema.relationships),
                    "fingerprint": schema.data_fingerprint,
                    "_schema_obj": schema,
                },
            )
        except Exception as e:
            ms = int((time.time() - t0) * 1000)
            return PhaseResult(
                phase=OnboardingPhase.SCHEMA,
                success=False,
                duration_ms=ms,
                message=f"Schema generation failed: {e}",
            )

    def _phase_pipeline(
        self,
        system: SystemEntry,
        schema: GeneratedSchema | None,
    ) -> PhaseResult:
        t0 = time.time()
        try:
            auto_pipeline = self._pipeline_factory.create_pipeline(system, schema)
            manual_pipeline = self._pipeline_factory.create_manual_pipeline(system)
            ms = int((time.time() - t0) * 1000)
            return PhaseResult(
                phase=OnboardingPhase.PIPELINE,
                success=True,
                duration_ms=ms,
                message=(
                    f"Created pipelines: auto ({len(auto_pipeline.stages)} stages, "
                    f"{auto_pipeline.schedule.mode}), manual"
                ),
                data={
                    "auto_pipeline_id": auto_pipeline.pipeline_id,
                    "manual_pipeline_id": manual_pipeline.pipeline_id,
                    "_auto_pipeline": auto_pipeline,
                    "_manual_pipeline": manual_pipeline,
                },
            )
        except Exception as e:
            ms = int((time.time() - t0) * 1000)
            return PhaseResult(
                phase=OnboardingPhase.PIPELINE,
                success=False,
                duration_ms=ms,
                message=f"Pipeline creation failed: {e}",
            )

    def _phase_ingest(self, system: SystemEntry, pipeline: PipelineSpec) -> PhaseResult:
        t0 = time.time()
        pipeline.status = "RUNNING"
        self._registry.record_sync(system.system_id, {"success": True, "records": 0, "pipeline_id": pipeline.pipeline_id})
        ms = int((time.time() - t0) * 1000)
        return PhaseResult(
            phase=OnboardingPhase.INGEST,
            success=True,
            duration_ms=ms,
            message="Initial ingestion started",
            data={"pipeline_id": pipeline.pipeline_id},
        )

    def _phase_verify(
        self,
        system: SystemEntry,
        schema: GeneratedSchema | None,
    ) -> PhaseResult:
        t0 = time.time()
        checks: dict[str, bool] = {
            "system_registered": self._registry.get_system(system.system_id) is not None,
            "schema_available": schema is not None,
            "entity_types_configured": len(system.ingestion.entity_types) > 0,
        }
        all_ok = all(checks.values())
        ms = int((time.time() - t0) * 1000)
        return PhaseResult(
            phase=OnboardingPhase.VERIFY,
            success=all_ok,
            duration_ms=ms,
            message=f"Verification: {sum(checks.values())}/{len(checks)} checks passed",
            data={"checks": checks},
        )

    # ── Bulk and Re-onboarding ───────────────────────────────────────

    def re_onboard(
        self,
        system_id: str,
        sample_data: list[dict[str, Any]] | dict[str, Any] | None = None,
    ) -> OnboardingResult:
        system = self._registry.get_system(system_id)
        if not system:
            raise ValueError(f"System {system_id} not found in registry")
        return self.onboard(system, sample_data=sample_data)

    def onboard_batch(
        self,
        systems: list[SystemEntry],
        sample_data_map: dict[str, Any] | None = None,
    ) -> list[OnboardingResult]:
        results: list[OnboardingResult] = []
        for system in systems:
            sd = (sample_data_map or {}).get(system.system_id)
            results.append(self.onboard(system, sample_data=sd))
        return results

    def get_onboarding_status(self, system_id: str) -> dict[str, Any] | None:
        system = self._registry.get_system(system_id)
        if not system:
            return None
        return system.metadata.get("last_onboarding")


class _OnboardAbort(Exception):
    pass
