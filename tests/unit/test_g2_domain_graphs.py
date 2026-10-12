"""Tests for G2 domain graphs (WP 4.4, 16 tasks): API, BIZ, DEC, OBS, PROC, RUNTIME, SEC, TEST."""

import pytest
from eoip.gaps.g2_observability import link_runtime_evidence
from eoip.graph.api_contracts import link_api_contract, track_contract_changes
from eoip.graph.business_intent import (
    ingest_capability,
    ingest_objective,
    intent_to_runtime_chain,
    link_to_capability,
    reverse_impact,
)
from eoip.graph.decisions import find_decisions_for_entity, ingest_decision
from eoip.graph.memory import MemoryGraphStore
from eoip.graph.process_mining import ProcessCase, compare_to_designed_flow, discover_process_paths
from eoip.graph.runtime_topology import (
    compare_runtime_vs_static_dependencies,
    record_temporal_service_call,
)
from eoip.graph.security_graph import compute_vulnerability_blast_radius
from eoip.graph.test_intelligence import map_tests_to_code, select_tests_for_changes


# --- 1. API Domain Graph (G2-GRAPH-API-002..003) ---

@pytest.mark.req("G2-GRAPH-API-002")
def test_g2_graph_api_002_contract_linking():
    store = MemoryGraphStore()
    ep = store.upsert_vertex("APIEndpoint", {
        "canonical_id": "urn:api:get_orders", "api_name": "getOrders", "api_path": "/orders", "api_method": "GET",
    })
    svc = store.upsert_vertex("APIService", {"canonical_id": "urn:apisvc:order", "name": "OrderService"})
    doc = store.upsert_vertex("Document", {"canonical_id": "urn:doc:api_spec", "name": "Order API Spec"})
    tc = store.upsert_vertex("TestCase", {"canonical_id": "urn:tc:order_api", "name": "test_get_orders"})
    dec = store.upsert_vertex("Decision", {"canonical_id": "urn:dec:rest_design", "name": "REST conventions"})
    consumer = store.upsert_vertex("APIService", {"canonical_id": "urn:apisvc:gateway", "name": "APIGateway"})

    result = link_api_contract(
        store,
        ep["canonical_id"],
        service_cid=svc["canonical_id"],
        doc_cid=doc["canonical_id"],
        test_cid=tc["canonical_id"],
        decision_cid=dec["canonical_id"],
        consumer_service_cids=[consumer["canonical_id"]],
    )
    assert result["links_count"] == 5
    assert any(l["edge"] == "EXPOSES" for l in result["links"])
    assert any(l["edge"] == "DOCUMENTS_API" for l in result["links"])
    assert any(l["edge"] == "TESTS" for l in result["links"])
    assert any(l["edge"] == "DECIDES" for l in result["links"])
    assert any(l["edge"] == "CONNECTS_TO" for l in result["links"])


@pytest.mark.req("G2-GRAPH-API-003")
def test_g2_graph_api_003_breaking_changes():
    old_spec = {
        "paths": {
            "/users": {"get": {"parameters": []}, "delete": {"parameters": []}},
            "/orders": {"post": {"parameters": [{"name": "item", "required": True}]}},
        }
    }
    new_spec = {
        "paths": {
            "/users": {"get": {"parameters": []}},  # removed delete -> breaking
            "/orders": {
                "post": {
                    "parameters": [
                        {"name": "item", "required": True},
                        {"name": "token", "required": True},  # added required param -> breaking
                        {"name": "promo", "required": False}, # added optional param -> non-breaking
                    ]
                }
            },
            "/products": {"get": {"parameters": []}}, # added endpoint -> non-breaking
        }
    }

    report = track_contract_changes(old_spec, new_spec)
    assert report["is_breaking"] is True
    assert report["breaking_count"] == 2
    assert report["non_breaking_count"] == 2
    types = {c["type"] for c in report["breaking_changes"]}
    assert "method_removed" in types
    assert "required_parameter_added" in types


# --- 2. Business Intent Graph (G2-GRAPH-BIZ-002..003) ---

@pytest.mark.req("G2-GRAPH-BIZ-002")
def test_g2_graph_biz_002_intent_to_technical():
    store = MemoryGraphStore()
    obj = ingest_objective(store, "Market Expansion")
    cap = ingest_capability(store, "MultiCurrency Billing", objective_cid=obj["canonical_id"])
    store.upsert_vertex("Service", {"canonical_id": "urn:svc:fx_service", "name": "FX Converter"})
    link_to_capability(store, "urn:svc:fx_service", cap["canonical_id"])

    chain = intent_to_runtime_chain(store, obj["canonical_id"])
    labels = chain["labels_present"]
    assert "BusinessObjective" in labels
    assert len(chain["chain"]) >= 2


@pytest.mark.req("G2-GRAPH-BIZ-003")
def test_g2_graph_biz_003_reverse_query():
    store = MemoryGraphStore()
    obj = ingest_objective(store, "Reliable Deliveries")
    cap = ingest_capability(store, "Shipment Dispatch", objective_cid=obj["canonical_id"])
    store.upsert_vertex("Service", {"canonical_id": "urn:svc:logistics", "name": "Logistics Dispatch"})
    link_to_capability(store, "urn:svc:logistics", cap["canonical_id"])

    result = reverse_impact(store, "urn:svc:logistics")
    assert len(result["capabilities"]) == 1
    assert result["capabilities"][0]["name"] == "Shipment Dispatch"
    assert len(result["objectives"]) == 1
    assert result["objectives"][0]["name"] == "Reliable Deliveries"


# --- 3. Decision Graph (G2-GRAPH-DEC-002..003) ---

@pytest.mark.req("G2-GRAPH-DEC-002")
def test_g2_graph_dec_002_adr_links():
    store = MemoryGraphStore()
    store.upsert_vertex("Service", {"canonical_id": "urn:svc:auth", "name": "AuthService"})
    res = ingest_decision(
        store,
        "Use JWT for Auth",
        rationale="Stateless authentication scales horizontally across nodes",
        status="Accepted",
        alternatives=[{"name": "Session Cookies", "rationale": "High memory overhead"}],
        linked_entities=["urn:svc:auth"],
    )
    assert res["decision"]["canonical_id"] == "urn:eoip:decision:use-jwt-for-auth"
    assert len(res["alternatives"]) == 1
    assert len(res["linked_entities"]) == 1
    assert res["linked_entities"][0]["edge"] == "DECIDES"


@pytest.mark.req("G2-GRAPH-DEC-003")
def test_g2_graph_dec_003_why_architecture():
    store = MemoryGraphStore()
    store.upsert_vertex("Service", {"canonical_id": "urn:svc:storage", "name": "BlobStorageService"})
    ingest_decision(
        store,
        "Adopt Object Storage",
        rationale="S3-compatible tier reduces disk I/O bottlenecks",
        status="Accepted",
        alternatives=[{"name": "NFS Mounts", "rationale": "POSIX locking contention"}],
        linked_entities=["urn:svc:storage"],
    )

    decisions = find_decisions_for_entity(store, "urn:svc:storage")
    assert len(decisions) == 1
    assert decisions[0]["name"] == "Adopt Object Storage"
    assert "S3-compatible" in decisions[0]["rationale"]
    assert len(decisions[0]["alternatives"]) == 1


# --- 4. Observability Graph (G2-GRAPH-OBS-002..003) ---

@pytest.mark.req("G2-GRAPH-OBS-002")
def test_g2_graph_obs_002_link_runtime_evidence():
    store = MemoryGraphStore()
    dep = store.upsert_vertex("Deployment", {"canonical_id": "urn:dep:prod_v2", "name": "Prod V2", "environment": "production"})
    ev = store.upsert_vertex("Evidence", {
        "canonical_id": "urn:ev:trace_001", "source_system": "datadog", "source_ref": "trace:12345", "method": "telemetry",
    })

    result = link_runtime_evidence(
        store,
        dep["canonical_id"],
        ev["canonical_id"],
        window_start="2026-10-12T00:00:00Z",
        window_end="2026-10-12T01:00:00Z",
    )
    assert result["target"] == dep["canonical_id"]
    assert result["evidence"] == ev["canonical_id"]


@pytest.mark.req("G2-GRAPH-OBS-003")
def test_g2_graph_obs_003_bounded_observation_window():
    store = MemoryGraphStore()
    svc = store.upsert_vertex("Service", {"canonical_id": "urn:svc:worker", "name": "QueueWorker"})
    ev = store.upsert_vertex("Evidence", {
        "canonical_id": "urn:ev:metric_99", "source_system": "prometheus", "source_ref": "metric:queue_latency", "method": "telemetry",
    })

    result = link_runtime_evidence(
        store,
        svc["canonical_id"],
        ev["canonical_id"],
        window_start="2026-10-11T12:00:00Z",
        window_end="2026-10-11T12:15:00Z",
    )
    assert result["bounded_window"] is True
    assert result["window_start"] == "2026-10-11T12:00:00Z"
    assert result["window_end"] == "2026-10-11T12:15:00Z"


# --- 5. Process Graph (G2-GRAPH-PROC-002..003) ---

@pytest.mark.req("G2-GRAPH-PROC-002")
def test_g2_graph_proc_002_designed_vs_observed():
    cases = [
        ProcessCase(
            case_id="case-1",
            events=[
                {"field": "status", "to_value": "Created"},
                {"field": "status", "to_value": "Reviewed"},
                {"field": "status", "to_value": "Approved"},
                {"field": "status", "to_value": "Deployed"},
            ],
        ),
    ]
    observed = discover_process_paths(cases)
    assert observed["total_cases"] == 1
    assert len(observed["paths"]) == 1

    designed_steps = ["Created", "Reviewed", "Approved", "Deployed"]
    comparison = compare_to_designed_flow(observed, designed_steps)
    assert comparison["conformance_rate"] == 1.0
    assert len(comparison["deviations"]) == 0


@pytest.mark.req("G2-GRAPH-PROC-003")
def test_g2_graph_proc_003_deviations_and_bottlenecks():
    # Case with skipped step ("Reviewed" skipped) and rework loop ("Created" -> "Rejected" -> "Created")
    cases = [
        ProcessCase(
            case_id="case-2",
            events=[
                {"field": "status", "to_value": "Created"},
                {"field": "status", "to_value": "Rejected"},
                {"field": "status", "to_value": "Created"},
                {"field": "status", "to_value": "Approved"},
            ],
        )
    ]
    observed = discover_process_paths(cases)
    designed_steps = ["Created", "Reviewed", "Approved", "Deployed"]
    comparison = compare_to_designed_flow(observed, designed_steps)

    dev_types = {d["type"] for d in comparison["deviations"]}
    assert "skipped_steps" in dev_types
    assert "rework_loop" in dev_types


# --- 6. Runtime Graph (G2-GRAPH-RUNTIME-002..003) ---

@pytest.mark.req("G2-GRAPH-RUNTIME-002")
def test_g2_graph_runtime_002_temporal_service_calls():
    store = MemoryGraphStore()
    s1 = store.upsert_vertex("Service", {"canonical_id": "urn:svc:frontend", "name": "Frontend"})
    s2 = store.upsert_vertex("Service", {"canonical_id": "urn:svc:backend", "name": "Backend"})

    call = record_temporal_service_call(
        store,
        s1["canonical_id"],
        s2["canonical_id"],
        observed_at="2026-10-12T04:00:00Z",
        call_count=150,
        latency_ms=12.5,
    )
    assert call["caller"] == s1["canonical_id"]
    assert call["callee"] == s2["canonical_id"]
    assert call["observed_at"] == "2026-10-12T04:00:00Z"


@pytest.mark.req("G2-GRAPH-RUNTIME-003")
def test_g2_graph_runtime_003_compare_runtime_vs_static():
    store = MemoryGraphStore()
    s1 = store.upsert_vertex("Service", {"canonical_id": "urn:svc:s1", "name": "S1"})
    s2 = store.upsert_vertex("Service", {"canonical_id": "urn:svc:s2", "name": "S2"})
    s3 = store.upsert_vertex("Service", {"canonical_id": "urn:svc:s3", "name": "S3"})

    # Static edge: s1 -> s2
    store.upsert_edge("DEPENDS_ON", s1["vid"], s2["vid"], {"fact_key": "static:s1:s2"})
    # Runtime edge: s1 -> s3 (shadow dependency)
    record_temporal_service_call(store, s1["canonical_id"], s3["canonical_id"], "2026-10-12T00:00:00Z")

    diff = compare_runtime_vs_static_dependencies(store)
    shadow = [d["callee"] for d in diff["shadow_runtime_dependencies"]]
    dormant = [d["callee"] for d in diff["dormant_static_dependencies"]]
    assert "urn:svc:s3" in shadow
    assert "urn:svc:s2" in dormant


# --- 7. Security & Supply-Chain Graph (G2-GRAPH-SEC-002..003) ---

@pytest.mark.req("G2-GRAPH-SEC-002")
def test_g2_graph_sec_002_vulnerability_blast_radius():
    store = MemoryGraphStore()
    pkg = store.upsert_vertex("Dependency", {"canonical_id": "urn:dep:log4j", "name": "log4j-core"})
    svc = store.upsert_vertex("Service", {"canonical_id": "urn:svc:analytics", "name": "AnalyticsService"})
    dep = store.upsert_vertex("Deployment", {"canonical_id": "urn:dep:prod_analytics", "name": "ProdAnalytics", "environment": "production"})

    dec = store.upsert_vertex("Decision", {"canonical_id": "urn:dec:deploy", "name": "DeployConfig"})
    store.upsert_edge("DEPENDS_ON", svc["vid"], pkg["vid"], {"fact_key": "svc:pkg"})
    store.upsert_edge("DECIDES", dec["vid"], svc["vid"], {"fact_key": "dec:svc"})
    store.upsert_edge("DECIDES", dec["vid"], dep["vid"], {"fact_key": "dec:dep"})

    report = compute_vulnerability_blast_radius(store, pkg["canonical_id"])
    assert report["blast_radius_count"] >= 2
    svcs = [s["canonical_id"] for s in report["impacted_services"]]
    assert "urn:svc:analytics" in svcs


@pytest.mark.req("G2-GRAPH-SEC-003")
def test_g2_graph_sec_003_preserve_scanner_provenance():
    store = MemoryGraphStore()
    pkg = store.upsert_vertex("Dependency", {"canonical_id": "urn:dep:openssl", "name": "openssl"})
    ev = store.upsert_vertex("Evidence", {
        "canonical_id": "urn:ev:trivy_cve",
        "source_system": "trivy-scanner",
        "source_ref": "CVE-2026-0042",
        "method": "sbom_scan",
    })
    store.upsert_edge("EVIDENCED_BY", pkg["vid"], ev["vid"], {"fact_key": "pkg:ev"})

    report = compute_vulnerability_blast_radius(store, pkg["canonical_id"])
    assert report["has_provenance"] is True
    assert report["provenance"][0]["source_system"] == "trivy-scanner"
    assert report["provenance"][0]["source_ref"] == "CVE-2026-0042"


# --- 8. Test Intelligence Graph (G2-GRAPH-TEST-002..003) ---

@pytest.mark.req("G2-GRAPH-TEST-002")
def test_g2_graph_test_002_change_impact_analysis():
    store = MemoryGraphStore()
    f = store.upsert_vertex("File", {"canonical_id": "urn:file:user_py", "repo_id": "r1", "path": "user.py"})
    sym = store.upsert_vertex("CodeSymbol", {"canonical_id": "urn:sym:login", "qualified_name": "user.login"})
    tc = store.upsert_vertex("TestCase", {"canonical_id": "urn:tc:test_login", "name": "test_login_flow"})

    store.upsert_edge("DECLARES", f["vid"], sym["vid"], {"fact_key": "decl:f:sym"})
    store.upsert_edge("TESTS", tc["vid"], sym["vid"], {"fact_key": "tests:tc:sym"})

    impact = select_tests_for_changes(store, [f["canonical_id"]])
    assert impact["total_tests"] == 1
    assert impact["selected_tests"][0]["test_id"] == tc["canonical_id"]


@pytest.mark.req("G2-GRAPH-TEST-003")
def test_g2_graph_test_003_test_coverage_confidence_provenance():
    store = MemoryGraphStore()
    sym = store.upsert_vertex("CodeSymbol", {"canonical_id": "urn:sym:calc", "qualified_name": "calc.add"})
    tc = store.upsert_vertex("TestCase", {"canonical_id": "urn:tc:calc_add", "name": "test_add"})

    store.upsert_edge(
        "TESTS",
        tc["vid"],
        sym["vid"],
        {
            "fact_key": "tests:calc",
            "confidence": 0.95,
            "source_ref": "coverage.py:L42",
            "creation_status": "DETERMINISTIC",
        },
    )

    mappings = map_tests_to_code(store)
    assert len(mappings) == 1
    target = mappings[0]["code_targets"][0]
    assert target["confidence"] == 0.95
    assert target["source_ref"] == "coverage.py:L42"
