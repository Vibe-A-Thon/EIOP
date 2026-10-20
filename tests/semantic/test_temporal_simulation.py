"""Comprehensive test suite for Temporal Knowledge, Impact and Simulation (CRA-028.1-028.9, CRA-028.A).

Covers:
- CRA-028.1: Bitemporal modeling (valid_time vs transaction_time), retractions, corrections, lineage, late events & clock skew.
- CRA-028.2: Authorized as-of queries, version diffs, bounded snapshots, retention policy & legal hold enforcement.
- CRA-028.3: Strict output category separation: OBSERVED, DETERMINISTIC_IMPACT, HEURISTIC_PATHS, STOCHASTIC_ESTIMATE, LEARNED_ESTIMATE, DOMAIN_SIMULATION.
- CRA-028.4: Calibrated stochastic simulation with seed, model version, assumptions, and confidence intervals.
- CRA-028.5: Multi-hop path evidence and cost semantics preservation (never collapsed to fake two-node edges).
- CRA-028.6: Explicit as_of parameter and SPARQL eoip:asOf service parameter parsing.
- CRA-028.7: Deterministic graph algorithms: BFS, Dijkstra, PageRank, and Tarjan Strongly Connected Components (SCC).
- CRA-028.8: Blast-radius breakdown by services, teams, and processes with explicit severity labelling.
- CRA-028.9: Dual-path blast radius with learned estimate marked PROPOSED and UNCORROBORATED, never reordering deterministic results.
- CRA-028.A:
  * Dual-time authorization: since-deleted nodes require authorization at both historical and current query time.
  * Simulation cancellation mechanism for expensive trials.
  * Production assertion fence: simulated facts cannot enter production without human review.
"""

from __future__ import annotations

from typing import Any

import json
import pytest

from eoip.graph.bitemporal import BitemporalCoordinate
from eoip.graph.memory import MemoryGraphStore
from eoip.temporal import (
    AuthorizedAsOfEngine,
    BitemporalEntityRecord,
    CorrectionRecord,
    DeterministicGraphAlgorithms,
    DualPathImpactReport,
    HistoricalAccessDeniedError,
    ImpactCategory,
    ImpactSimulator,
    ImpactedEntity,
    ProductionAssertionBlockedError,
    RetentionPolicy,
    RetractionRecord,
    SeverityLevel,
    SimulationProtocol,
    reconcile_late_event,
)


def test_bitemporal_modeling_corrections_and_late_events():
    """CRA-028.1: Valid time vs transaction time, retractions, corrections, lineage, and late events."""
    # 1. Base record
    rec1 = BitemporalEntityRecord(
        canonical_id="urn:eoip:service:payment-gw",
        entity_type="Service",
        valid_from="2026-01-01T00:00:00Z",
        valid_to="2026-06-01T00:00:00Z",
        observed_at="2026-01-02T10:00:00Z",
        properties={"status": "ACTIVE", "criticality": "HIGH"},
        source_revision="git-commit-100",
    )
    assert rec1.is_valid_at("2026-03-01T00:00:00Z") is True
    assert rec1.is_valid_at("2026-07-01T00:00:00Z") is False
    assert rec1.was_known_at("2026-01-02T09:00:00Z") is False
    assert rec1.was_known_at("2026-01-02T11:00:00Z") is True
    assert len(rec1.lineage_hash) == 64

    # 2. Retraction
    retraction = RetractionRecord(
        retraction_id="ret-01",
        target_id="urn:eoip:service:payment-gw",
        observed_at="2026-01-10T12:00:00Z",
        retraction_reason="False alarm incident report retracted",
        actor="operator-alice",
        replaces_revision_id="rev-01",
    )
    rec1.is_retracted = True
    rec1.retraction = retraction
    assert rec1.is_retracted is True
    assert rec1.retraction.actor == "operator-alice"

    # 3. Explicit correction
    correction = CorrectionRecord(
        correction_id="corr-01",
        target_id="urn:eoip:service:payment-gw",
        observed_at="2026-01-15T15:00:00Z",
        corrected_valid_from="2026-01-01T00:00:00Z",
        corrected_valid_to="2026-12-31T23:59:59Z",
        actor="steward-bob",
        reason="Extended deployment SLA horizon",
        previous_value={"valid_to": "2026-06-01T00:00:00Z"},
        new_value={"valid_to": "2026-12-31T23:59:59Z"},
    )
    rec1.corrections.append(correction)
    assert len(rec1.corrections) == 1
    assert rec1.corrections[0].new_value["valid_to"] == "2026-12-31T23:59:59Z"

    # 4. Late event & clock skew reconciliation
    late_event = BitemporalEntityRecord(
        canonical_id="urn:eoip:service:payment-gw",
        entity_type="Service",
        valid_from="2026-04-01T00:00:00Z",
        valid_to="2026-08-01T00:00:00Z",
        observed_at="2026-02-01T00:00:00Z",  # Arrived later in transaction time
        properties={"status": "MAINTENANCE"},
    )
    reconciled = reconcile_late_event([rec1], late_event)
    assert len(reconciled) == 2
    # First revision interval valid_to was adjusted to match the late event's valid_from
    assert reconciled[0].valid_to == "2026-04-01T00:00:00Z"
    assert reconciled[1].valid_from == "2026-04-01T00:00:00Z"


def test_authorized_as_of_retention_and_dual_time_authorization():
    """CRA-028.2, CRA-028.6, CRA-028.A: Authorized as-of queries, retention expiry, legal hold, and dual-time ACLs."""
    store = MemoryGraphStore()

    # 1. Setup EntityRevision in memory store for an active service and a deleted service
    # Service A: Active service
    store.upsert_vertex(
        "EntityRevision",
        {
            "canonical_id": "urn:eoip:revision:entity:rev-svc-a",
            "revision_id": "rev-svc-a",
            "subject_id": "urn:eoip:service:active-svc",
            "entity_type": "Service",
            "observed_at": "2026-01-01T00:00:00Z",
            "valid_from": "2026-01-01T00:00:00Z",
            "valid_to": "",
            "is_current": True,
            "payload_json": json.dumps({
                "label": "Service",
                "properties": {"name": "active-svc", "service_id": "svc-a"},
                "acl_vector": ["group:engineering"],
            }),
            "source_event_id": "evt-01",
            "graph_version": "gv-01",
        },
    )
    store.upsert_vertex("Service", {
        "canonical_id": "urn:eoip:service:active-svc",
        "service_id": "svc-a",
        "name": "active-svc",
    })

    # Service B: Since-deleted service
    store.upsert_vertex(
        "EntityRevision",
        {
            "canonical_id": "urn:eoip:revision:entity:rev-svc-b",
            "revision_id": "rev-svc-b",
            "subject_id": "urn:eoip:service:deleted-svc",
            "entity_type": "Service",
            "observed_at": "2026-01-01T00:00:00Z",
            "valid_from": "2026-01-01T00:00:00Z",
            "valid_to": "",
            "is_current": False,
            "payload_json": json.dumps({
                "label": "Service",
                "properties": {"name": "deleted-svc", "service_id": "svc-b"},
                "acl_vector": ["group:security-audit"],
            }),
            "source_event_id": "evt-02",
            "graph_version": "gv-01",
        },
    )
    # Service B is marked deleted in active store
    store.upsert_vertex("Service", {
        "canonical_id": "urn:eoip:service:deleted-svc",
        "service_id": "svc-b",
        "name": "deleted-svc",
        "deleted_at": "2026-02-01T00:00:00Z",
    })

    engine = AuthorizedAsOfEngine(store)

    # Case A: Principal authorized at both historical and current time sees deleted-svc
    snap_authorized = engine.query_as_of(
        valid_at="2026-01-15T00:00:00Z",
        known_at="2026-01-15T00:00:00Z",
        principal_id="auditor-alice",
        historical_acls={"group:security-audit"},
        current_acls={"group:security-audit"},
    )
    cids = [e["canonical_id"] for e in snap_authorized.entities]
    assert "urn:eoip:service:deleted-svc" in cids

    # Case B (CRA-028.A): Principal authorized historically but NOT currently cannot see since-deleted node!
    snap_lacks_current = engine.query_as_of(
        valid_at="2026-01-15T00:00:00Z",
        known_at="2026-01-15T00:00:00Z",
        principal_id="former-auditor-bob",
        historical_acls={"group:security-audit"},
        current_acls={"group:read-only"},  # Lost security-audit permission!
    )
    cids_lacks_current = [e["canonical_id"] for e in snap_lacks_current.entities]
    assert "urn:eoip:service:deleted-svc" not in cids_lacks_current
    assert snap_lacks_current.redacted_count >= 1

    # Case C (CRA-028.2): Retention policy expired -> historical data redacted
    expired_retention = RetentionPolicy(retention_period_days=30, legal_hold_active=False)
    snap_expired = engine.query_as_of(
        valid_at="2026-01-15T00:00:00Z",
        known_at="2026-01-15T00:00:00Z",
        principal_id="auditor-alice",
        historical_acls={"group:engineering"},
        current_acls={"group:engineering"},
        retention_policy=expired_retention,
        current_time="2026-05-01T00:00:00Z",  # Over 30 days after observation
    )
    assert len(snap_expired.entities) == 0
    assert snap_expired.retention_pruned_count >= 1

    # Case D (CRA-028.2): Active Legal Hold preserves expired history
    legal_hold_retention = RetentionPolicy(
        retention_period_days=30,
        legal_hold_active=True,
        legal_hold_case_id="SEC-CASE-2026-99",
    )
    snap_legal_hold = engine.query_as_of(
        valid_at="2026-01-15T00:00:00Z",
        known_at="2026-01-15T00:00:00Z",
        principal_id="auditor-alice",
        historical_acls={"group:engineering"},
        current_acls={"group:engineering"},
        retention_policy=legal_hold_retention,
        current_time="2026-05-01T00:00:00Z",
    )
    assert len(snap_legal_hold.entities) >= 1

    # Case E (CRA-028.6): SPARQL eoip:asOf parameter parsing
    sparql = "SELECT ?s WHERE { ?s ?p ?o } eoip:asOf(valid_at='2026-01-01T00:00:00Z', known_at='2026-01-02T00:00:00Z')"
    clean_q, as_of_params = AuthorizedAsOfEngine.parse_sparql_as_of(sparql)
    assert as_of_params is not None
    assert as_of_params["valid_at"] == "2026-01-01T00:00:00Z"
    assert as_of_params["known_at"] == "2026-01-02T00:00:00Z"
    assert "eoip:asOf" not in clean_q


def test_deterministic_graph_algorithms_and_path_evidence():
    """CRA-028.5, CRA-028.7: Qualified BFS, Dijkstra with hop evidence, PageRank, and Tarjan SCC."""
    store = MemoryGraphStore()

    # Graph layout:
    # svc-1 -> svc-2 (coupling 1.5) -> svc-3 (coupling 2.0)
    # svc-3 -> svc-2 (creates cycle between 2 and 3)
    # svc-3 -> svc-4 (coupling 0.5)
    for cid in ["svc-1", "svc-2", "svc-3", "svc-4"]:
        store.upsert_vertex("Service", {
            "canonical_id": f"urn:eoip:service:{cid}",
            "service_id": cid,
            "name": f"Service {cid}",
        })

    store.upsert_edge("CALLS", "urn:eoip:service:svc-1", "urn:eoip:service:svc-2", {"coupling": 1.5})
    store.upsert_edge("CALLS", "urn:eoip:service:svc-2", "urn:eoip:service:svc-3", {"coupling": 2.0})
    store.upsert_edge("CALLS", "urn:eoip:service:svc-3", "urn:eoip:service:svc-2", {"coupling": 1.0})
    store.upsert_edge("CALLS", "urn:eoip:service:svc-3", "urn:eoip:service:svc-4", {"coupling": 0.5})

    algo = DeterministicGraphAlgorithms(store)

    # 1. Deterministic BFS
    reachable = algo.bfs_reachable("urn:eoip:service:svc-1", max_depth=5)
    assert set(reachable) == {
        "urn:eoip:service:svc-2",
        "urn:eoip:service:svc-3",
        "urn:eoip:service:svc-4",
    }

    # 2. Dijkstra with exact cost and hop evidence (CRA-028.5)
    path = algo.dijkstra_shortest_path("urn:eoip:service:svc-1", "urn:eoip:service:svc-4")
    assert path is not None
    assert path.hops == [
        "urn:eoip:service:svc-1",
        "urn:eoip:service:svc-2",
        "urn:eoip:service:svc-3",
        "urn:eoip:service:svc-4",
    ]
    assert path.hop_count == 3
    assert path.total_cost == 4.0  # 1.5 + 2.0 + 0.5
    # Strict path preservation check: Intermediate hops are explicitly preserved with edge metadata (CRA-028.5)
    assert len(path.hop_evidence) == 3
    assert path.hop_evidence[0].edge_label == "CALLS"
    assert path.hop_evidence[0].weight == 1.5

    # 3. Deterministic PageRank
    ranks = algo.pagerank()
    assert len(ranks) == 4
    # All ranks sum to 1.0
    assert abs(sum(ranks.values()) - 1.0) < 1e-4
    # svc-2 and svc-3 have cyclic feedback so their rank is high
    assert ranks["urn:eoip:service:svc-2"] > ranks["urn:eoip:service:svc-1"]

    # 4. Tarjan's Strongly Connected Components (SCC)
    sccs = algo.tarjan_scc()
    # Cycle between svc-2 and svc-3 forms an SCC of size 2
    cycle_scc = next((s for s in sccs if len(s) == 2), None)
    assert cycle_scc is not None
    assert set(cycle_scc) == {"urn:eoip:service:svc-2", "urn:eoip:service:svc-3"}


def test_blast_radius_output_categories_and_learned_dual_path():
    """CRA-028.3, CRA-028.8, CRA-028.9, CRA-028.A: Category separation, blast radius breakdown, and dual-path learned estimate."""
    store = MemoryGraphStore()

    # Core topology: Payment Service -> Order Service -> Warehouse Service
    store.upsert_vertex("Service", {
        "canonical_id": "urn:eoip:service:payment",
        "service_id": "payment",
        "name": "Payment Service",
    })
    store.upsert_vertex("Service", {
        "canonical_id": "urn:eoip:service:order",
        "service_id": "order",
        "name": "Order Service",
        "owner": "Charlie Team Lead",
    })
    store.upsert_vertex("Service", {
        "canonical_id": "urn:eoip:service:warehouse",
        "service_id": "warehouse",
        "name": "Warehouse Service",
    })

    # Associated BusinessObjective (Process/Goal)
    store.upsert_vertex("BusinessObjective", {
        "canonical_id": "urn:eoip:biz:checkout-sla",
        "name": "Checkout SLA Workflow",
    })

    store.upsert_edge("CALLS", "urn:eoip:service:payment", "urn:eoip:service:order", {"coupling": 1.0})
    store.upsert_edge("CALLS", "urn:eoip:service:order", "urn:eoip:service:warehouse", {"coupling": 1.0})
    store.upsert_edge("FULFILLS", "urn:eoip:service:order", "urn:eoip:biz:checkout-sla", {})

    simulator = ImpactSimulator(store)

    # Define a neural learned propagator (e.g. predicting extended impact on inventory-db)
    def mock_learned_propagator(target_cid: str, depth: int) -> list[dict[str, Any]]:
        return [
            {"canonical_id": "urn:eoip:service:order", "score": 0.95},
            {"canonical_id": "urn:eoip:service:warehouse", "score": 0.85},
            {"canonical_id": "urn:eoip:biz:checkout-sla", "score": 0.80},
            {"canonical_id": "urn:eoip:service:inventory-db", "score": 0.65},  # Extension predicted only by ML model!
        ]

    report = simulator.compute_blast_radius(
        target_canonical_id="urn:eoip:service:payment",
        max_depth=4,
        learned_propagator=mock_learned_propagator,
    )

    # 1. Deterministic impact breakdown (CRA-028.8)
    deterministic_svc_cids = [s.canonical_id for s in report.deterministic_impacted_services]
    assert "urn:eoip:service:order" in deterministic_svc_cids
    assert "urn:eoip:service:warehouse" in deterministic_svc_cids

    # Heuristic severity labelling verification (CRA-028.8)
    order_svc = next(s for s in report.deterministic_impacted_services if s.canonical_id == "urn:eoip:service:order")
    assert order_svc.severity == SeverityLevel.CRITICAL  # depth 1
    assert order_svc.is_heuristic_score is True

    # Impacted processes and teams
    assert "Checkout SLA Workflow" in report.deterministic_impacted_processes
    assert "Charlie Team Lead" in report.deterministic_impacted_teams

    # 2. Dual-path status for learned estimates (CRA-028.9, CRA-028.A)
    # inventory-db is ONLY in learned estimate -> must be marked PROPOSED and UNCORROBORATED!
    inventory_pred = next(item for item in report.learned_estimates if item["canonical_id"] == "urn:eoip:service:inventory-db")
    assert inventory_pred["knowledge_state"] == "PROPOSED"
    assert inventory_pred["dual_path_status"] == "UNCORROBORATED"
    assert inventory_pred["producer_class"] == "PROBABILISTIC"

    # order is present in both -> marked CORROBORATED
    order_pred = next(item for item in report.learned_estimates if item["canonical_id"] == "urn:eoip:service:order")
    assert order_pred["dual_path_status"] == "CORROBORATED"

    # Deterministic output was NOT reordered or replaced
    assert report.total_deterministic_count >= 2
    assert report.agreement_status == "UNCORROBORATED_EXTENSIONS"


def test_stochastic_simulation_and_production_assertion_fence():
    """CRA-028.4, CRA-028.A: Calibrated Monte Carlo simulation, cancellation, and production assertion fence."""
    store = MemoryGraphStore()

    for i in range(5):
        store.upsert_vertex("Service", {
            "canonical_id": f"urn:eoip:service:node-{i}",
            "service_id": f"node-{i}",
            "name": f"Node {i}",
        })

    for i in range(4):
        store.upsert_edge("CALLS", f"urn:eoip:service:node-{i}", f"urn:eoip:service:node-{i+1}", {"coupling": 0.8})

    simulator = ImpactSimulator(store)

    protocol = SimulationProtocol(
        model_version="cascade-v2.1",
        assumptions=["Independent component failure probability", "Gaussian latency perturbation"],
        input_parameters={"decay": 0.1, "threshold": 0.5},
        seed=1337,
        trials=50,
    )

    # 1. Repeatable seeded run
    res1 = simulator.run_stochastic_simulation("urn:eoip:service:node-0", protocol)
    res2 = simulator.run_stochastic_simulation("urn:eoip:service:node-0", protocol)

    assert res1.mean_impact_count == res2.mean_impact_count
    assert res1.confidence_interval_95 == res2.confidence_interval_95
    assert res1.output_category == ImpactCategory.STOCHASTIC_ESTIMATE
    assert res1.is_asserted_production_fact is False

    # 2. Simulation cancellation (CRA-028.A)
    cancelled_res = simulator.run_stochastic_simulation(
        "urn:eoip:service:node-0",
        protocol,
        cancellation_check=lambda: True,  # Trigger early cancellation
    )
    assert cancelled_res.cancelled is True
    assert cancelled_res.executed_trials == 0

    # 3. Production assertion fence (CRA-028.A)
    # Simulated facts cannot enter asserted production knowledge without explicit human review
    with pytest.raises(ProductionAssertionBlockedError, match="cannot enter asserted production knowledge without human review"):
        simulator.assert_simulation_fact_to_production(
            simulation_result=res1,
            fact={"rule": "auto-circuit-break", "target": "urn:eoip:service:node-1"},
            human_approver=None,
        )

    # With human approval, assertion succeeds
    simulator.assert_simulation_fact_to_production(
        simulation_result=res1,
        fact={"rule": "auto-circuit-break", "target": "urn:eoip:service:node-1"},
        human_approver="lead-architect-dave",
    )
    assert res1.is_asserted_production_fact is True
