"""Tests for GAPS/GAPS2 gap-closing implementations."""

import math
from eoip.graph.memory import MemoryGraphStore
from eoip.graph.benchmark import BenchmarkHarness, BenchmarkResult
from eoip.ontology.schema_gen import generate_json_schema, generate_openapi_schemas, generate_form_spec
from eoip.ontology.embedding_drift import (
    EmbeddingDriftReport,
    cosine_similarity,
    detect_embedding_drift,
)
from eoip.codegraph.diff_hunk import parse_unified_diff, link_commit_to_symbols


def test_benchmark_harness_vertex_insert():
    store = MemoryGraphStore()
    harness = BenchmarkHarness()
    result = harness.run_vertex_insert_benchmark(store, count=50)
    assert isinstance(result, BenchmarkResult)
    assert result.operation == "vertex_insert"
    assert result.count == 50
    assert result.throughput_ops_sec > 0
    assert result.p50_ms >= 0
    assert result.p95_ms >= result.p50_ms
    assert result.p99_ms >= result.p95_ms


def test_benchmark_harness_edge_insert():
    store = MemoryGraphStore()
    harness = BenchmarkHarness()
    harness.run_vertex_insert_benchmark(store, count=20)
    result = harness.run_edge_insert_benchmark(store, count=10)
    assert isinstance(result, BenchmarkResult)
    assert result.operation == "edge_insert"


def test_benchmark_harness_vertex_lookup():
    store = MemoryGraphStore()
    harness = BenchmarkHarness()
    harness.run_vertex_insert_benchmark(store, count=20)
    result = harness.run_vertex_lookup_benchmark(store, count=20)
    assert isinstance(result, BenchmarkResult)
    assert result.operation == "vertex_lookup"


def test_benchmark_harness_run_all():
    store = MemoryGraphStore()
    harness = BenchmarkHarness()
    results = harness.run_all(store)
    assert len(results) >= 3
    ops = [r.operation for r in results]
    assert "vertex_insert" in ops
    assert "edge_insert" in ops
    assert "vertex_lookup" in ops


def test_generate_json_schema_workitem():
    schema = generate_json_schema("WorkItem")
    assert schema["type"] == "object"
    assert "properties" in schema
    assert "canonical_id" in schema["properties"]
    assert len(schema.get("required", [])) > 0


def test_generate_json_schema_unknown_label():
    import pytest
    with pytest.raises(KeyError, match="Unknown vertex label"):
        generate_json_schema("NonExistentLabel")


def test_generate_openapi_schemas():
    result = generate_openapi_schemas()
    assert isinstance(result, dict)
    schemas = result.get("schemas", result)
    assert len(schemas) > 10
    assert "WorkItem" in schemas
    assert "File" in schemas


def test_generate_form_spec():
    spec = generate_form_spec("WorkItem")
    assert isinstance(spec, dict)
    assert "label" in spec
    assert spec["label"] == "WorkItem"
    assert "fields" in spec
    assert len(spec["fields"]) > 0
    for field in spec["fields"]:
        assert "name" in field
        assert "type" in field
        assert "required" in field


def test_cosine_similarity_identical():
    a = [1.0, 0.0, 0.0]
    b = [1.0, 0.0, 0.0]
    assert abs(cosine_similarity(a, b) - 1.0) < 1e-6


def test_cosine_similarity_orthogonal():
    a = [1.0, 0.0]
    b = [0.0, 1.0]
    assert abs(cosine_similarity(a, b)) < 1e-6


def test_cosine_similarity_opposite():
    a = [1.0, 0.0]
    b = [-1.0, 0.0]
    assert abs(cosine_similarity(a, b) + 1.0) < 1e-6


def test_detect_embedding_drift_no_drift():
    baseline = {
        "WorkItem::1": [1.0, 0.0, 0.0],
        "WorkItem::2": [0.9, 0.1, 0.0],
    }
    current = {
        "WorkItem::1": [1.0, 0.0, 0.0],
        "WorkItem::2": [0.9, 0.1, 0.0],
    }
    report = detect_embedding_drift(baseline, current)
    assert isinstance(report, EmbeddingDriftReport)
    assert len(report.drifted_labels) == 0


def test_detect_embedding_drift_with_drift():
    baseline = {
        "WorkItem::1": [1.0, 0.0, 0.0],
        "WorkItem::2": [1.0, 0.0, 0.0],
    }
    current = {
        "WorkItem::1": [0.0, 1.0, 0.0],
        "WorkItem::2": [0.0, 1.0, 0.0],
    }
    report = detect_embedding_drift(baseline, current, threshold=0.1)
    assert len(report.drifted_labels) > 0
    assert report.drift_score > 0.1


def test_detect_embedding_drift_empty():
    report = detect_embedding_drift({}, {})
    assert report.baseline_count == 0
    assert report.current_count == 0
    assert len(report.drifted_labels) == 0


def test_connector_imports():
    from eoip.connectors.otel import OpenTelemetryConnector
    from eoip.connectors.runtime_infra import RuntimeInfraConnector
    from eoip.connectors.sbom import SBOMConnector
    from eoip.connectors.cicd import CICDConnector
    assert OpenTelemetryConnector is not None
    assert RuntimeInfraConnector is not None
    assert SBOMConnector is not None
    assert CICDConnector is not None


def test_otel_connector_health():
    from eoip.connectors.otel import OpenTelemetryConnector
    connector = OpenTelemetryConnector()
    health = connector.health()
    assert health is not None


def test_sbom_connector_discover():
    from eoip.connectors.sbom import SBOMConnector
    from eoip.connectors.base import DiscoveryResult
    connector = SBOMConnector()
    result = connector.discover()
    assert isinstance(result, DiscoveryResult)
    assert len(result.resources) >= 2


def test_cicd_connector_discover():
    from eoip.connectors.cicd import CICDConnector
    from eoip.connectors.base import DiscoveryResult
    connector = CICDConnector(provider="test-ci")
    result = connector.discover()
    assert isinstance(result, DiscoveryResult)
    assert len(result.resources) >= 2
