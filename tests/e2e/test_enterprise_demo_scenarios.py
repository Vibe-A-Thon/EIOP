import json
from pathlib import Path
import pytest

from eoip.demo import load_demo
from eoip.demo_scenarios import load_demo_scenario_pack, validate_demo_scenario_pack
from eoip.graph.memory import MemoryGraphStore
from eoip.graph.metrics import GraphMetricsEngine
from eoip.graph.paths import GraphPathFinder
from eoip.graph.traversal import GraphTraversal
from eoip.ontology.manifest import PROPERTY_KEYS
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
    assert len(pack["scenarios"]) == 13
    assert len(pack["vertices"]) >= 50
    assert len(pack["edges"]) >= 90
    for item in pack["vertices"]:
        for key, value in item["properties"].items():
            if PROPERTY_KEYS[key] == "TEXT":
                assert isinstance(value, str), f"{item['label']}.{key} must match RocksDB TEXT schema"


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


def test_corrected_pack_preserves_immutable_capture_and_business_identities(tmp_path):
    pack = json.loads(PACK_PATH.read_text(encoding="utf-8"))
    source = tmp_path / "pack.json"
    source.write_text(json.dumps(pack), encoding="utf-8")
    store = MemoryGraphStore()
    load_demo_scenario_pack(store, tmp_path, pack_path=source)
    captures = list((tmp_path / "raw" / "demo_enterprise").glob("*.json"))
    assert len(captures) == 1
    original_bytes = captures[0].read_bytes()
    pack["vertices"][0]["properties"]["description"] = "Corrected synthetic description."
    source.write_text(json.dumps(pack), encoding="utf-8")
    load_demo_scenario_pack(store, tmp_path, pack_path=source)
    load_demo_scenario_pack(store, tmp_path, pack_path=source)
    assert captures[0].read_bytes() == original_bytes
    assert len(list((tmp_path / "raw" / "demo_enterprise").glob("*.json"))) == 2
    assert len([e for e in store.find_edges(limit=10000)
                if e["properties"].get("fact_key", "").startswith("demo:1.0.0:")]) == 92
    vertex = store.get_vertex_by_canonical_id(pack["vertices"][0]["properties"]["canonical_id"])
    assert vertex["properties"]["description"].endswith("Corrected synthetic description.")


def test_enrichment_preserves_legacy_edge_keys_and_names(tmp_path):
    pack = json.loads(PACK_PATH.read_text(encoding="utf-8"))
    original = dict(pack, version="1.0.0",
                    vertices=pack["vertices"][24:], edges=pack["edges"][42:],
                    scenarios=pack["scenarios"][5:])
    store = MemoryGraphStore()
    legacy_path = tmp_path / "legacy.json"
    legacy_path.write_text(json.dumps(original), encoding="utf-8")
    load_demo_scenario_pack(store, tmp_path, pack_path=legacy_path)
    keys = {e["properties"]["edge_key"] for e in store.find_edges(limit=10000)
            if e["properties"].get("fact_key", "").startswith("demo:")}
    assert len(keys) == 92
    load_demo_scenario_pack(store, tmp_path)
    after = {e["properties"]["edge_key"] for e in store.find_edges(limit=10000)
             if e["properties"].get("fact_key", "").startswith("demo:")}
    assert after == keys
    for v in store.find_vertices(limit=10000):
        if v["canonical_id"] in {item["properties"]["canonical_id"] for item in pack["vertices"]}:
            assert v["properties"]["display_name"]


def test_business_decisions_and_ordered_process_paths(tmp_path):
    store, _ = _environment(tmp_path)
    vertices = {v["canonical_id"]: v for v in store.find_vertices(limit=10000)}
    assert {"BUSINESS", "DECISION", "PROCESS"} <= {
        v["properties"].get("graph_domain") for v in vertices.values()
    }
    pack = json.loads(PACK_PATH.read_text(encoding="utf-8"))
    finder = GraphPathFinder(store)
    for scenario in pack["scenarios"]:
        assert finder.all_shortest_paths(scenario["expected_path"][0], scenario["expected_path"][-1]), scenario["id"]
    pairs = {frozenset((e["out_cid"], e["in_cid"])) for e in store.find_edges(limit=10000)
             if e["label"] not in {"EVIDENCED_BY", "INGESTED_IN", "BELONGS_TO_DOMAIN"}}
    for scenario in pack["scenarios"]:
        assert all(frozenset(pair) in pairs for pair in
                   zip(scenario["expected_path"], scenario["expected_path"][1:])), scenario["id"]
    steps = {(e["out_cid"], e["in_cid"]) for e in store.find_edges(limit=10000)
             if e["label"] == "PRECEDES"}
    assert ("urn:eoip:process:step:northstar:triage", "urn:eoip:process:step:northstar:approve") in steps
    assert ("urn:eoip:process:step:northstar:approve", "urn:eoip:process:step:northstar:deploy") in steps


def test_demo_loads_every_sales_scenario_with_clean_validation(tmp_path):
    store, result = _environment(tmp_path)
    enterprise = result["enterprise"]
    assert enterprise["run_status"] == "SUCCEEDED"
    assert enterprise["vertices"] == 80
    assert enterprise["edges"] == 134
    assert len(enterprise["scenarios"]) == 13

    validation = ValidationEngine(store).run()
    assert validation["valid"] is True
    assert validation["quality"]["error_count"] == 0
    assert validation["quality"]["warning_count"] == 0
    assert validation["quality"]["evidence_coverage"] == 1.0
    assert validation["quality"]["provenance_coverage"] == 1.0


def test_disconnected_declared_scenario_is_rejected_before_ingestion():
    pack = json.loads(PACK_PATH.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    pack["scenarios"][0]["expected_path"][1] = "urn:eoip:identity:person:maya.chen"
    with pytest.raises(ValueError, match="disconnected path"):
        validate_demo_scenario_pack(pack, schema)


def test_remediation_has_truthful_failed_and_passed_qualification_chronology(tmp_path):
    store, _ = _environment(tmp_path)
    def properties(cid):
        return store.get_vertex_by_canonical_id(cid)["properties"]
    failed = properties("urn:eoip:test:run:northstar:4820")
    passed = properties("urn:eoip:test:run:northstar:4822")
    commit = properties("urn:eoip:code:commit:northstar:c0ffee155")
    deployment = properties("urn:eoip:cicd:deployment:northstar:checkout:prod:2026.10.2")
    assert failed["failed_count"] == 1 and failed["execution_status"] == "Failed"
    assert passed["failed_count"] == 0 and passed["skipped_count"] == 0
    assert failed["finished_at"] < commit["created_at"] < passed["created_at"]
    assert passed["finished_at"] < deployment["created_at"]
    for run in (failed, passed):
        assert run["passed_count"] + run["failed_count"] + run["skipped_count"] == run["total_count"]


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
    assert len(body["scenarios"]) == 13
    assert all(item["ready"] and item["available"] for item in body["scenarios"])


def test_all_declared_demo_paths_execute_through_policy_bounded_api(tmp_path):
    store, _ = _environment(tmp_path)
    client = TestClient(create_app(store))
    scenarios = client.get("/api/v1/demo/scenarios").json()["scenarios"]
    for scenario in scenarios:
        response = client.post(
            "/api/v1/path",
            json={
                "source_id": scenario["expected_path"][0],
                "target_id": scenario["expected_path"][-1],
                "max_depth": 8,
                "relationship_allowlist": scenario["relationship_allowlist"],
            },
        )
        assert response.status_code == 200, response.text
        paths = response.json()["paths"]
        assert paths, scenario["id"]
        assert paths[0]["node_ids"][0] == scenario["expected_path"][0]
        assert paths[0]["node_ids"][-1] == scenario["expected_path"][-1]
    invalid = client.post(
        "/api/v1/path",
        json={
            "source_id": scenarios[0]["expected_path"][0],
            "target_id": scenarios[0]["expected_path"][-1],
            "relationship_allowlist": ["NOT_AN_ONTOLOGY_EDGE"],
        },
    )
    assert invalid.status_code == 422


def test_multihop_demo_retrieves_blast_radius_evidence(tmp_path):
    store, _ = _environment(tmp_path)
    response = TestClient(create_app(store)).post(
        "/api/v1/rag/query",
        json={
            "query": "checkout",
            "pattern": "multihop",
            "context": {"selected_id": "urn:eoip:work:item:jira:PAY-142"},
        },
    )
    assert response.status_code == 200, response.text
    result = response.json()
    assert result["rag_pattern"] == "multihop"
    assert result["sources"]
    assert result["abstained"] is False
    assert result["evidence_manifest"]["entity_count"] > 0
