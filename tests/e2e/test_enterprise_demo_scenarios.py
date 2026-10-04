import json
from pathlib import Path

from eoip.demo import load_demo
from eoip.demo_scenarios import load_demo_scenario_pack, validate_demo_scenario_pack
from eoip.graph.memory import MemoryGraphStore
from eoip.graph.metrics import GraphMetricsEngine
from eoip.graph.paths import GraphPathFinder
from eoip.graph.traversal import GraphTraversal
from eoip.validation.engine import ValidationEngine
from fastapi.testclient import TestClient
from jsonschema import Draft202012Validator

from apps.api.app import create_app

ROOT = Path(__file__).resolve().parents[2]
PACK_PATH = ROOT / "demo/demodata/enterprise/scenario-pack.json"
SCHEMA_PATH = ROOT / "schemas/demo_scenario_pack.schema.json"


def _environment(tmp_path):
    for directory in ("raw", "dlq", "state"):
        (tmp_path / directory).mkdir()
    store = MemoryGraphStore()
    result = load_demo(store, tmp_path)
    return store, result


def test_enterprise_pack_is_schema_and_ontology_valid():
    pack = json.loads(PACK_PATH.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validate_demo_scenario_pack(pack, schema)
    assert len(pack["scenarios"]) == 8
    assert len(pack["vertices"]) >= 50
    assert len(pack["edges"]) >= 90


def test_all_source_fixtures_are_parseable_json():
    fixture_paths = sorted((ROOT / "demo/demodata/enterprise/source-fixtures").glob("*.json"))
    assert {item.name for item in fixture_paths} == {
        "api-portal.json",
        "confluence.json",
        "figma.json",
        "gitlab.json",
        "jira.json",
        "observability.json",
        "qtest.json",
        "servicenow.json",
    }
    for path in fixture_paths:
        assert json.loads(path.read_text(encoding="utf-8"))
    assert json.loads(
        (ROOT / "demo/demodata/enterprise/api/checkout-openapi.json").read_text(encoding="utf-8")
    )["openapi"] == "3.1.0"


def test_demo_loads_every_sales_scenario_with_clean_validation(tmp_path):
    store, result = _environment(tmp_path)
    enterprise = result["enterprise"]
    assert enterprise["run_status"] == "SUCCEEDED"
    assert enterprise["vertices"] == 56
    assert enterprise["edges"] == 92
    assert len(enterprise["scenarios"]) == 8

    validation = ValidationEngine(store).run()
    assert validation["valid"] is True
    assert validation["quality"]["error_count"] == 0
    assert validation["quality"]["warning_count"] == 0
    assert validation["quality"]["evidence_coverage"] == 1.0
    assert validation["quality"]["provenance_coverage"] == 1.0


def test_intent_to_runtime_and_cross_domain_paths_exist(tmp_path):
    store, _ = _environment(tmp_path)
    traversal = GraphTraversal(store, max_depth=8)
    path = traversal.find_path(
        "urn:eoip:work:item:jira:PAY-142",
        "urn:eoip:code:symbol:northstar:risk:authorize_order",
    )
    assert path is not None
    labels = {edge["label"] for edge in path["edges"]}
    assert labels == {"IMPLEMENTS", "MODIFIES", "DECLARES"}

    finder = GraphPathFinder(store)
    assert finder.all_shortest_paths(
        "urn:eoip:ops:incident:INC0012042",
        "urn:eoip:cicd:pipeline:northstar:4815",
    )
    assert finder.all_shortest_paths(
        "urn:eoip:design:file:northstar:checkout",
        "urn:eoip:work:feature:northstar:FTR-42",
    )
    assert finder.all_shortest_paths(
        "urn:eoip:test:suite:northstar:checkout-regression",
        "urn:eoip:code:api-endpoint:northstar:checkout:post-orders",
    )


def test_demo_is_idempotent_and_analytics_have_useful_structure(tmp_path):
    store, _ = _environment(tmp_path)
    vertices_before = store.count_vertices()
    edges_before = store.count_edges()
    load_demo_scenario_pack(store, tmp_path)
    assert store.count_vertices() == vertices_before
    assert store.count_edges() == edges_before

    metrics = GraphMetricsEngine(store)
    stats = metrics.graph_statistics()
    # Keep the gate bound to the deterministic one-commit Docker fixture.
    # A developer checkout can contain additional Git history and therefore
    # legitimately produce higher counts, but must not define the demo floor.
    assert stats["vertex_count"] >= 110
    assert stats["edge_count"] >= 300
    assert len(metrics.connected_components()) >= 1
    assert metrics.blast_radius("urn:eoip:code:api-service:northstar:checkout", 4).total_affected >= 8


def test_demo_catalog_endpoint_reports_live_readiness(tmp_path):
    store, _ = _environment(tmp_path)
    response = TestClient(create_app(store)).get("/api/v1/demo/scenarios")
    assert response.status_code == 200
    body = response.json()
    assert body["dataset_id"] == "northstar-commerce"
    assert body["ready"] is True
    assert len(body["scenarios"]) == 8
    assert all(item["ready"] and item["available"] for item in body["scenarios"])
