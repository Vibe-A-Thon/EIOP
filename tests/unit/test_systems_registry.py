"""Tests for the Systems Registry, AutoSchemaGenerator, PipelineFactory, and AutoOnboardOrchestrator."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from eoip.systems.registry import (
    SystemCategory, SystemEntry, SystemsRegistry, SystemStatus,
    KNOWN_SYSTEM_TYPES,
)
from eoip.systems.schema_generator import AutoSchemaGenerator, GeneratedSchema
from eoip.systems.pipeline_factory import (
    PipelineFactory, PipelineSpec, PipelineStageType,
)
from eoip.systems.auto_onboard import (
    AutoOnboardOrchestrator, OnboardingPhase, OnboardingResult,
)


# ── Fixtures ─────────────────────────────────────────────────────────

@pytest.fixture
def tmp_config(tmp_path):
    config = {
        "$schema": "urn:eoip:systems-registry:v1",
        "version": "1.0.0",
        "global_defaults": {},
        "systems": [],
    }
    p = tmp_path / "systems-registry.json"
    p.write_text(json.dumps(config), encoding="utf-8")
    return str(p)


@pytest.fixture
def registry(tmp_config):
    return SystemsRegistry(tmp_config)


def _register_jira(registry: SystemsRegistry) -> SystemEntry:
    return registry.register_system(
        name="Test Jira",
        system_type="jira",
        connection={"base_url": "https://jira.example.com"},
        auth={"auth_type": "token", "credentials": {"token": "test123"}},
        ingestion={"entity_types": ["issue", "project", "user"]},
    )


@pytest.fixture
def sample_entry(registry):
    return _register_jira(registry)


@pytest.fixture
def sample_json_data():
    return [
        {"id": 1, "title": "Bug fix", "status": "open", "assignee_id": 42, "created_at": "2024-01-15T10:00:00Z"},
        {"id": 2, "title": "Feature", "status": "closed", "assignee_id": 43, "created_at": "2024-02-20T14:30:00Z"},
        {"id": 3, "title": "Refactor", "status": "open", "assignee_id": 42, "created_at": "2024-03-10T08:00:00Z"},
    ]


# ══════════════════════════════════════════════════════════════════════
#  SystemsRegistry
# ══════════════════════════════════════════════════════════════════════

class TestSystemsRegistry:
    def test_register_and_get(self, registry, sample_entry):
        got = registry.get_system(sample_entry.system_id)
        assert got is not None
        assert got.name == "Test Jira"
        assert got.system_type == "jira"

    def test_list_systems(self, registry):
        assert registry.list_systems() == []
        _register_jira(registry)
        # Note: _register_jira also called in fixture; calling on fresh registry
        # Let's just check the one registered by the fixture indirectly

    def test_list_systems_populated(self, registry, sample_entry):
        assert len(registry.list_systems()) == 1

    def test_update_system(self, registry, sample_entry):
        registry.update_system(sample_entry.system_id, {"name": "Updated Jira"})
        got = registry.get_system(sample_entry.system_id)
        assert got.name == "Updated Jira"

    def test_remove_system(self, registry, sample_entry):
        registry.remove_system(sample_entry.system_id)
        assert registry.get_system(sample_entry.system_id) is None
        assert len(registry.list_systems()) == 0

    def test_set_status(self, registry, sample_entry):
        registry.set_status(sample_entry.system_id, SystemStatus.ACTIVE)
        got = registry.get_system(sample_entry.system_id)
        assert got.status == SystemStatus.ACTIVE

    def test_record_sync(self, registry, sample_entry):
        registry.record_sync(sample_entry.system_id, {"success": True, "records": 100})
        got = registry.get_system(sample_entry.system_id)
        assert got.last_sync_at is not None

    def test_record_health(self, registry, sample_entry):
        registry.record_health(sample_entry.system_id, {"healthy": True})
        got = registry.get_system(sample_entry.system_id)
        assert got.last_health_check is not None

    def test_test_connection(self, registry, sample_entry):
        result = registry.test_connection(sample_entry.system_id)
        assert isinstance(result, dict)
        assert result["success"]

    def test_export_config(self, registry, sample_entry):
        exported = registry.export_config()
        assert exported["version"] == "1.0.0"
        assert len(exported["systems"]) == 1

    def test_known_system_types(self):
        assert len(KNOWN_SYSTEM_TYPES) >= 34
        assert "jira" in KNOWN_SYSTEM_TYPES
        assert "postgresql" in KNOWN_SYSTEM_TYPES
        assert "kubernetes" in KNOWN_SYSTEM_TYPES

    def test_known_types_have_category(self):
        for name, info in KNOWN_SYSTEM_TYPES.items():
            assert "category" in info, f"{name} missing category"
            assert "entity_types" in info, f"{name} missing entity_types"


# ══════════════════════════════════════════════════════════════════════
#  AutoSchemaGenerator
# ══════════════════════════════════════════════════════════════════════

class TestAutoSchemaGenerator:
    def test_generate_from_flat_array(self, sample_json_data):
        gen = AutoSchemaGenerator()
        schema = gen.generate_from_json("sys1", "jira", sample_json_data)
        assert isinstance(schema, GeneratedSchema)
        assert len(schema.entities) >= 1
        assert schema.graphql_sdl
        assert schema.json_schema
        assert schema.data_fingerprint

    def test_entity_fields_detected(self, sample_json_data):
        gen = AutoSchemaGenerator()
        schema = gen.generate_from_json("sys1", "jira", sample_json_data)
        entity = schema.entities[0]
        field_names = {f.name for f in entity.fields}
        assert "id" in field_names
        assert "title" in field_names
        assert "status" in field_names

    def test_key_field_detected(self, sample_json_data):
        gen = AutoSchemaGenerator()
        schema = gen.generate_from_json("sys1", "jira", sample_json_data)
        entity = schema.entities[0]
        assert entity.key_field == "id"

    def test_foreign_key_detected(self, sample_json_data):
        gen = AutoSchemaGenerator()
        schema = gen.generate_from_json("sys1", "jira", sample_json_data)
        entity = schema.entities[0]
        fk_fields = [f for f in entity.fields if f.is_foreign_key]
        assert len(fk_fields) >= 1
        assert fk_fields[0].name == "assignee_id"
        assert fk_fields[0].foreign_key_target == "assignee"

    def test_relationship_from_fk(self, sample_json_data):
        gen = AutoSchemaGenerator()
        schema = gen.generate_from_json("sys1", "jira", sample_json_data)
        assert len(schema.relationships) >= 1
        edge_labels = [r.edge_label for r in schema.relationships]
        assert "REL_ASSIGNEE" in edge_labels

    def test_datetime_detection(self, sample_json_data):
        gen = AutoSchemaGenerator()
        schema = gen.generate_from_json("sys1", "jira", sample_json_data)
        entity = schema.entities[0]
        dt_fields = [f for f in entity.fields if f.inferred_type == "datetime"]
        assert len(dt_fields) >= 1

    def test_nested_object_data(self):
        gen = AutoSchemaGenerator()
        data = {"issues": [{"id": 1, "name": "a"}], "users": [{"id": 10, "email": "a@b.com"}]}
        schema = gen.generate_from_json("sys1", "jira", data)
        assert len(schema.entities) == 2
        labels = {e.label for e in schema.entities}
        assert "Issues" in labels
        assert "Users" in labels

    def test_graphql_sdl_has_types(self, sample_json_data):
        gen = AutoSchemaGenerator()
        schema = gen.generate_from_json("sys1", "jira", sample_json_data)
        assert "type " in schema.graphql_sdl
        assert "@key" in schema.graphql_sdl

    def test_golden_queries_generated(self, sample_json_data):
        gen = AutoSchemaGenerator()
        schema = gen.generate_from_json("sys1", "jira", sample_json_data)
        assert len(schema.golden_queries) >= 2
        assert any("MATCH" in q for q in schema.golden_queries)

    def test_validation_rules_generated(self, sample_json_data):
        gen = AutoSchemaGenerator()
        schema = gen.generate_from_json("sys1", "jira", sample_json_data)
        assert len(schema.validation_rules) >= 1
        assert any(r["rule"] == "NOT_NULL" for r in schema.validation_rules)

    def test_generate_from_file(self, sample_json_data, tmp_path):
        gen = AutoSchemaGenerator()
        p = tmp_path / "sample.json"
        p.write_text(json.dumps(sample_json_data), encoding="utf-8")
        schema = gen.generate_from_file("sys1", "jira", str(p))
        assert len(schema.entities) >= 1

    def test_field_mappings(self, sample_json_data):
        gen = AutoSchemaGenerator()
        schema = gen.generate_from_json("sys1", "jira", sample_json_data)
        assert len(schema.field_mappings) >= 1
        for label, mapping in schema.field_mappings.items():
            assert "canonical_id" in mapping.values()

    def test_ontology_labels(self, sample_json_data):
        gen = AutoSchemaGenerator()
        schema = gen.generate_from_json("sys1", "jira", sample_json_data)
        assert "vertex_labels" in schema.ontology_labels
        assert "edge_labels" in schema.ontology_labels
        assert len(schema.ontology_labels["vertex_labels"]) >= 1


# ══════════════════════════════════════════════════════════════════════
#  PipelineFactory
# ══════════════════════════════════════════════════════════════════════

class TestPipelineFactory:
    def test_create_pipeline(self, sample_entry):
        factory = PipelineFactory()
        spec = factory.create_pipeline(sample_entry)
        assert isinstance(spec, PipelineSpec)
        assert spec.system_id == sample_entry.system_id
        assert len(spec.stages) >= 10

    def test_pipeline_stages_have_dependencies(self, sample_entry):
        factory = PipelineFactory()
        spec = factory.create_pipeline(sample_entry)
        for stage in spec.stages:
            if stage.stage_id != "connect":
                assert len(stage.depends_on) >= 1

    def test_execution_order(self, sample_entry):
        factory = PipelineFactory()
        spec = factory.create_pipeline(sample_entry)
        order = spec.get_execution_order()
        assert order[0] == "connect"
        assert "load" in order
        assert order.index("connect") < order.index("load")

    def test_discover_stage_for_api_systems(self, sample_entry):
        factory = PipelineFactory()
        spec = factory.create_pipeline(sample_entry)
        stage_ids = [s.stage_id for s in spec.stages]
        assert "discover" in stage_ids

    def test_no_discover_for_database_systems(self, registry):
        entry = registry.register_system(
            name="Test PG",
            system_type="postgresql",
            connection={"base_url": "postgresql://localhost:5432/db"},
            auth={"auth_type": "basic", "credentials": {"user": "test"}},
            ingestion={"entity_types": ["table"]},
        )
        factory = PipelineFactory()
        spec = factory.create_pipeline(entry)
        stage_ids = [s.stage_id for s in spec.stages]
        assert "discover" not in stage_ids

    def test_profile_stage_when_auto_schema(self, sample_entry):
        sample_entry.ingestion.auto_schema_induction = True
        factory = PipelineFactory()
        spec = factory.create_pipeline(sample_entry)
        stage_ids = [s.stage_id for s in spec.stages]
        assert "profile" in stage_ids

    def test_schedule_interval(self, sample_entry):
        factory = PipelineFactory()
        spec = factory.create_pipeline(sample_entry)
        assert spec.schedule.mode in ("interval", "cron", "immediate")

    def test_schedule_event_driven(self, sample_entry):
        sample_entry.ingestion.mode = "event_driven"
        factory = PipelineFactory()
        spec = factory.create_pipeline(sample_entry)
        assert spec.schedule.mode == "event_driven"

    def test_schedule_cron(self, sample_entry):
        sample_entry.ingestion.mode = "scheduled"
        sample_entry.ingestion.cron_expression = "0 */6 * * *"
        factory = PipelineFactory()
        spec = factory.create_pipeline(sample_entry)
        assert spec.schedule.mode == "cron"
        assert spec.schedule.cron_expression == "0 */6 * * *"

    def test_manual_pipeline(self, sample_entry):
        factory = PipelineFactory()
        spec = factory.create_manual_pipeline(sample_entry)
        assert spec.schedule.mode == "manual"
        assert "Manual" in spec.name

    def test_monitoring_config(self, sample_entry):
        factory = PipelineFactory()
        spec = factory.create_pipeline(sample_entry)
        assert spec.monitoring.metrics_enabled
        assert spec.monitoring.alerting_enabled

    def test_pipeline_with_schema(self, sample_entry, sample_json_data):
        gen = AutoSchemaGenerator()
        schema = gen.generate_from_json(sample_entry.system_id, "jira", sample_json_data)
        factory = PipelineFactory()
        spec = factory.create_pipeline(sample_entry, schema)
        transform = next(s for s in spec.stages if s.stage_id == "transform")
        assert transform.config["mappings"]

    def test_to_dict(self, sample_entry):
        factory = PipelineFactory()
        spec = factory.create_pipeline(sample_entry)
        d = spec.to_dict()
        assert isinstance(d, dict)
        assert "stages" in d
        assert "schedule" in d


# ══════════════════════════════════════════════════════════════════════
#  AutoOnboardOrchestrator
# ══════════════════════════════════════════════════════════════════════

class TestAutoOnboardOrchestrator:
    def test_full_onboard_with_sample_data(self, registry, sample_entry, sample_json_data):
        orch = AutoOnboardOrchestrator(registry)
        result = orch.onboard(sample_entry, sample_data=sample_json_data, skip_ingestion=True)
        assert isinstance(result, OnboardingResult)
        assert result.success
        assert result.schema is not None
        assert len(result.schema.entities) >= 1
        assert result.auto_pipeline is not None
        assert result.manual_pipeline is not None

    def test_onboard_without_sample_data(self, registry, sample_entry):
        orch = AutoOnboardOrchestrator(registry)
        result = orch.onboard(sample_entry, skip_ingestion=True)
        assert result.success
        assert result.schema is None

    def test_onboard_phases_recorded(self, registry, sample_entry, sample_json_data):
        orch = AutoOnboardOrchestrator(registry)
        result = orch.onboard(sample_entry, sample_data=sample_json_data, skip_ingestion=True)
        phase_names = [p.phase for p in result.phases]
        assert OnboardingPhase.VALIDATE in phase_names
        assert OnboardingPhase.CONNECT in phase_names
        assert OnboardingPhase.SCHEMA in phase_names
        assert OnboardingPhase.PIPELINE in phase_names
        assert OnboardingPhase.VERIFY in phase_names

    def test_onboard_sets_active_status(self, registry, sample_entry):
        orch = AutoOnboardOrchestrator(registry)
        orch.onboard(sample_entry, skip_ingestion=True)
        got = registry.get_system(sample_entry.system_id)
        assert got.status == SystemStatus.ACTIVE

    def test_onboard_validation_failure(self, registry):
        bad_entry = registry.register_system(
            name="Bad System",
            system_type="custom_json",
        )
        # Validation expects base_url, but custom_json with no connection will have empty URL
        orch = AutoOnboardOrchestrator(registry)
        result = orch.onboard(bad_entry)
        assert not result.success
        assert result.error

    def test_onboard_from_config(self, registry):
        orch = AutoOnboardOrchestrator(registry)
        result = orch.onboard_from_config({
            "system_type": "gitlab",
            "name": "Test GitLab",
            "base_url": "https://gitlab.example.com",
            "auth_type": "token",
            "credentials": {"token": "test"},
        })
        assert isinstance(result, OnboardingResult)
        assert registry.get_system(result.system_id) is not None

    def test_re_onboard(self, registry, sample_entry, sample_json_data):
        orch = AutoOnboardOrchestrator(registry)
        orch.onboard(sample_entry, skip_ingestion=True)
        result2 = orch.re_onboard(sample_entry.system_id, sample_data=sample_json_data)
        assert result2.success

    def test_onboarding_status_persisted(self, registry, sample_entry):
        orch = AutoOnboardOrchestrator(registry)
        orch.onboard(sample_entry, skip_ingestion=True)
        status = orch.get_onboarding_status(sample_entry.system_id)
        assert status is not None
        assert "onboarding_id" in status

    def test_to_dict(self, registry, sample_entry):
        orch = AutoOnboardOrchestrator(registry)
        result = orch.onboard(sample_entry, skip_ingestion=True)
        d = result.to_dict()
        assert isinstance(d, dict)
        assert d["system_id"] == sample_entry.system_id
        assert "phases" in d

    def test_batch_onboard(self, registry):
        entries = []
        for stype in ["jira", "gitlab", "postgresql"]:
            e = registry.register_system(
                name=f"Batch {stype}",
                system_type=stype,
                connection={"base_url": f"https://{stype}.example.com"},
                auth={"auth_type": "token", "credentials": {"token": "x"}},
            )
            entries.append(e)
        orch = AutoOnboardOrchestrator(registry)
        results = orch.onboard_batch(entries)
        assert len(results) == 3
        assert all(r.success for r in results)


# ══════════════════════════════════════════════════════════════════════
#  Integration: end-to-end flow
# ══════════════════════════════════════════════════════════════════════

class TestEndToEnd:
    def test_register_onboard_pipeline_flow(self, tmp_config):
        registry = SystemsRegistry(tmp_config)
        entry = registry.register_system(
            name="E2E Jira",
            system_type="jira",
            connection={"base_url": "https://jira.example.com"},
            auth={"auth_type": "token", "credentials": {"token": "abc"}},
            ingestion={"entity_types": ["issue", "project"]},
        )

        sample = [
            {"id": "ISS-1", "summary": "Login bug", "priority": "high", "project_id": "PROJ-1"},
            {"id": "ISS-2", "summary": "UI tweak", "priority": "low", "project_id": "PROJ-2"},
        ]

        orch = AutoOnboardOrchestrator(registry)
        result = orch.onboard(entry, sample_data=sample, skip_ingestion=True)

        assert result.success
        assert result.schema is not None
        assert len(result.schema.entities) >= 1
        assert result.auto_pipeline is not None
        assert len(result.auto_pipeline.stages) >= 10

        got = registry.get_system(entry.system_id)
        assert got.status == SystemStatus.ACTIVE

        exported = registry.export_config()
        assert len(exported["systems"]) == 1
