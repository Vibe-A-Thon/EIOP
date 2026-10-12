"""Tests for Intent-to-Retrieval and Intent-to-Runtime Traceability (G2-I2R-002..005)."""

import pytest
from eoip.graph.business_intent import (
    flag_unowned_production_assets,
    flag_untraced_critical_requirements,
    ingest_capability,
    ingest_objective,
    link_to_capability,
    reverse_impact,
    reverse_traversal,
)
from eoip.graph.memory import MemoryGraphStore
from eoip.graph.twin import detect_missing_links, digital_thread_coverage


@pytest.mark.req("G2-I2R-002")
def test_reverse_traversal_g2_i2r_002():
    store = MemoryGraphStore()
    obj = ingest_objective(store, "Revenue Growth", priority="high")
    cap = ingest_capability(store, "Billing Engine", objective_cid=obj["canonical_id"])
    store.upsert_vertex("Service", {"canonical_id": "urn:svc:billing", "service_id": "billing", "name": "Billing Service"})
    link_to_capability(store, "urn:svc:billing", cap["canonical_id"])

    result = reverse_traversal(store, "urn:svc:billing")
    assert len(result["capabilities"]) == 1
    assert result["capabilities"][0]["canonical_id"] == cap["canonical_id"]
    assert len(result["objectives"]) == 1
    assert result["objectives"][0]["name"] == "Revenue Growth"
    assert result["total_affected"] == 2


@pytest.mark.req("G2-I2R-003")
def test_compute_coverage_for_missing_links_g2_i2r_003():
    store = MemoryGraphStore()
    store.upsert_vertex("BusinessObjective", {"canonical_id": "urn:obj:1", "name": "Objective 1"})
    store.upsert_vertex("Requirement", {"canonical_id": "urn:req:1", "name": "Requirement 1"})
    store.upsert_vertex("Service", {"canonical_id": "urn:svc:1", "name": "Service 1"})

    cov = digital_thread_coverage(store)
    assert "per_stage" in cov
    assert "BusinessObjective" in cov["per_stage"]
    assert "stages_missing" in cov
    assert len(cov["stages_missing"]) > 0

    gaps = detect_missing_links(store)
    assert gaps["total_gaps"] > 0
    missing_labels = {f["label"] for f in gaps["findings"]}
    assert "BusinessObjective" in missing_labels or "Requirement" in missing_labels


@pytest.mark.req("G2-I2R-004")
def test_flag_unowned_production_assets_g2_i2r_004():
    store = MemoryGraphStore()
    # Unowned production deployment
    store.upsert_vertex("Deployment", {
        "canonical_id": "urn:dep:unowned_prod",
        "name": "ProdCluster",
        "environment": "production",
    })
    # Owned service
    obj = ingest_objective(store, "Core Platform")
    cap = ingest_capability(store, "Core Platform Cap", objective_cid=obj["canonical_id"])
    store.upsert_vertex("Service", {
        "canonical_id": "urn:svc:owned_prod",
        "name": "CoreSvc",
        "environment": "production",
    })
    link_to_capability(store, "urn:svc:owned_prod", cap["canonical_id"])

    findings = flag_unowned_production_assets(store)
    unowned_ids = {f["canonical_id"] for f in findings}
    assert "urn:dep:unowned_prod" in unowned_ids
    assert "urn:svc:owned_prod" not in unowned_ids


@pytest.mark.req("G2-I2R-005")
def test_flag_untraced_critical_requirements_g2_i2r_005():
    store = MemoryGraphStore()
    # Critical requirement with no runtime link
    store.upsert_vertex("Requirement", {
        "canonical_id": "urn:req:critical_orphan",
        "name": "Zero-trust auth",
        "severity": "CRITICAL",
    })
    # Critical requirement linked to Service
    req_linked = store.upsert_vertex("Requirement", {
        "canonical_id": "urn:req:critical_linked",
        "name": "Payment validation",
        "severity": "CRITICAL",
    })
    svc = store.upsert_vertex("Service", {
        "canonical_id": "urn:svc:payment",
        "name": "PaymentService",
    })
    store.upsert_edge("TRACES_TO", req_linked["vid"], svc["vid"], {"fact_key": "traces:payment"})

    findings = flag_untraced_critical_requirements(store)
    finding_cids = {f["canonical_id"] for f in findings}
    assert "urn:req:critical_orphan" in finding_cids
    assert "urn:req:critical_linked" not in finding_cids
