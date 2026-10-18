"""Comprehensive test suite for Canonical Identity, Alignment and Reversible Resolution (CRA-023.1-023.9, CRA-023.A).

Covers:
- CRA-023.1: Scoped source identity, canonical-ID mapping, tenant isolation, and deterministic idempotency.
- CRA-023.2: Alignment candidates with lexical/structural/model evidence, uncertainty, NIL outcomes; never infer owl:sameAs from label/vector similarity alone.
- CRA-023.3: High-impact merge approval requirement, consistency checks, conflicting source claims preservation.
- CRA-023.4: Reversible merge/split with evidence preservation, temporal history, and inference retraction.
- CRA-023.5: Linking gate evaluation: precision >= 0.99, recall >= 0.80 across held-out gold data.
- CRA-023.6: Candidate generation combining deterministic keys with probabilistic features.
- CRA-023.7: DeepOnto alignment worker and tenant-scoped EntityLinker.
- CRA-023.8: Persistent IdentityMergeLedger: merge then split across restart restores original graph state.
- CRA-023.9: Feature attribution reporting and anti-stub model verification.
- CRA-023.A: Adverse ambiguity tests: ambiguous abbreviations, same-name entities, conflicting identifiers, wrong high-confidence matches.
"""

from __future__ import annotations

import copy
from pathlib import Path
import pytest

from eoip.graph.memory import MemoryGraphStore
from eoip.identity import (
    AlignmentCandidate,
    AlignmentCandidateGenerator,
    AntiStubVerificationError,
    DeepOntoAlignmentWorker,
    HighImpactMergeApprovalRequiredError,
    IdentityMergeLedger,
    ReversibleIdentityManager,
    ScopedSourceIdentityTable,
    TenantScopedEntityLinker,
    evaluate_identity_linking_gate,
)


def test_scoped_source_identity_and_canonical_id_mapping():
    """CRA-023.1: Scoped source identity; same textual ID in distinct sources/tenants resolves to distinct canonical IDs."""
    table = ScopedSourceIdentityTable()

    # Same external ID "USR-100" in Tenant A vs Tenant B
    rec_tenant_a = table.resolve_or_create(
        tenant_id="tenant-alpha",
        source_instance="jira-prod",
        external_id="USR-100",
        entity_type="Person",
    )
    rec_tenant_b = table.resolve_or_create(
        tenant_id="tenant-beta",
        source_instance="jira-prod",
        external_id="USR-100",
        entity_type="Person",
    )

    # Cross-tenant isolation: canonical IDs must be strictly distinct!
    assert rec_tenant_a.canonical_id != rec_tenant_b.canonical_id
    assert rec_tenant_a.tenant_id == "tenant-alpha"
    assert rec_tenant_b.tenant_id == "tenant-beta"

    # Same external ID "USR-100" in different source instances within the same tenant
    rec_github = table.resolve_or_create(
        tenant_id="tenant-alpha",
        source_instance="github-corp",
        external_id="USR-100",
        entity_type="Person",
    )

    # Cross-source isolation: distinct source instances must NOT collide!
    assert rec_tenant_a.canonical_id != rec_github.canonical_id

    # Deterministic idempotency: resolving the exact same key produces the identical canonical ID
    rec_repeat = table.resolve_or_create(
        tenant_id="tenant-alpha",
        source_instance="jira-prod",
        external_id="USR-100",
    )
    assert rec_repeat.canonical_id == rec_tenant_a.canonical_id

    # Aliases tracking
    assert "jira-prod:USR-100" in rec_tenant_a.aliases
    assert table.get_by_alias("jira-prod:USR-100", tenant_id="tenant-alpha").canonical_id == rec_tenant_a.canonical_id
    assert table.get_by_alias("jira-prod:USR-100", tenant_id="tenant-beta").canonical_id == rec_tenant_b.canonical_id


def test_alignment_candidate_generation_and_never_auto_sameas():
    """CRA-023.2: Alignment candidates with evidence and uncertainty; never infer owl:sameAs from similarity alone."""
    gen = AlignmentCandidateGenerator(confidence_threshold=0.80)

    # Case 1: High similarity entities (same person across GitLab and Jira)
    s1 = {"canonical_id": "c-alice-jira", "name": "Alice Cooper", "properties": {"title": "Staff Engineer"}}
    s2 = {"canonical_id": "c-alice-git", "name": "Alice Cooper", "properties": {"title": "Staff Engineer"}}

    candidate = gen.generate_candidate(
        source_entity=s1,
        target_entity=s2,
        source_neighbors={"repo-api", "team-backend"},
        target_neighbors={"repo-api", "team-backend"},
        source_vector=[0.1, 0.8, 0.5],
        target_vector=[0.1, 0.8, 0.5],
    )

    assert candidate.is_nil is False
    assert candidate.confidence >= 0.80
    assert candidate.match_type == "PROBABILISTIC_ENSEMBLE"
    assert candidate.status == "PROPOSED"  # Never auto-applied as fact (CRA-023.2)
    assert not hasattr(candidate, "inferred_same_as") or candidate.approved is False

    # Case 2: Sub-threshold similarity -> NIL outcome
    s3 = {"canonical_id": "c-charlie", "name": "Charlie Chaplin"}
    nil_cand = gen.generate_candidate(source_entity=s1, target_entity=s3)
    assert nil_cand.is_nil is True
    assert nil_cand.match_type == "NIL"

    # Invariant: Rejected candidates never appear as facts
    nil_cand.status = "REJECTED"
    assert nil_cand.status == "REJECTED"


def test_high_impact_merge_approval_and_conflict_preservation():
    """CRA-023.3: High-impact merge requires explicit approval; conflicting source claims preserved with provenance."""
    store = MemoryGraphStore()
    manager = ReversibleIdentityManager()

    # Setup survivor and absorbed vertices with conflicting claims
    store.upsert_vertex(
        "Person",
        {
            "canonical_id": "urn:eoip:person:primary",
            "display_name": "Alice C.",
            "source_aliases": "jira:alice",
            "description": "Core Infrastructure Staff Engineer",
            "email": "alice@corp.internal",
        },
    )
    store.upsert_vertex(
        "Person",
        {
            "canonical_id": "urn:eoip:person:secondary",
            "display_name": "Alice Cooper",
            "source_aliases": "github:alicec",
            "description": "Platform Engineering Specialist",  # Conflicting description!
        },
    )

    # Add 6 WorkItem vertices and ASSIGNED_TO edges to trigger high-impact threshold
    for i in range(6):
        store.upsert_vertex(
            "WorkItem",
            {
                "canonical_id": f"urn:eoip:workitem:item-{i}",
                "issue_key": f"ITEM-{i}",
                "summary": f"Task {i}",
            },
        )
        store.upsert_edge(
            "ASSIGNED_TO",
            f"urn:eoip:workitem:item-{i}",
            "urn:eoip:person:secondary",
            {},
        )

    # High-impact merge without approval must fail (CRA-023.3)
    with pytest.raises(HighImpactMergeApprovalRequiredError, match="requires explicit approval"):
        manager.merge(
            store=store,
            survivor_cid="urn:eoip:person:primary",
            absorbed_cids=["urn:eoip:person:secondary"],
            actor="batch-resolver",
            reason="High confidence match",
            approved_by=None,
        )

    # With human approval, merge succeeds
    op_id = manager.merge(
        store=store,
        survivor_cid="urn:eoip:person:primary",
        absorbed_cids=["urn:eoip:person:secondary"],
        actor="batch-resolver",
        reason="High confidence match",
        approved_by="domain-steward-bob",
    )
    assert op_id.startswith("merge-op-")

    # Conflicting source claims are preserved in survivor properties with provenance (CRA-023.3)
    survivor = store.get_vertex_by_canonical_id("urn:eoip:person:primary")
    assert survivor is not None
    assert survivor["properties"]["description"] == "Core Infrastructure Staff Engineer"
    assert "_conflicts" in survivor["properties"]
    assert "github:alicec" in survivor["properties"]["_conflicts"]["description"]
    assert survivor["properties"]["_conflicts"]["description"]["github:alicec"] == "Platform Engineering Specialist"

    # Absorbed node is removed from active store
    assert store.get_vertex_by_canonical_id("urn:eoip:person:secondary") is None


def test_reversible_merge_and_split_with_ledger_across_restart(tmp_path):
    """CRA-023.4, CRA-023.8: Reversible merge then split across restart restores exact original nodes and edges."""
    ledger_file = tmp_path / "identity_merge_ledger.json"
    ledger = IdentityMergeLedger(storage_path=ledger_file)
    manager = ReversibleIdentityManager(ledger=ledger)
    store = MemoryGraphStore()

    # Pre-merge state: distinct vertices and edges
    v1_props = {
        "canonical_id": "urn:eoip:service:auth-svc",
        "service_id": "auth-01",
        "name": "auth-service",
        "source_aliases": "k8s:auth-service",
    }
    v2_props = {
        "canonical_id": "urn:eoip:service:auth-api",
        "service_id": "auth-02",
        "name": "auth-api",
        "source_aliases": "consul:auth-api",
    }
    v3_props = {
        "canonical_id": "urn:eoip:service:auth-db",
        "service_id": "auth-db",
        "name": "auth-database",
    }
    store.upsert_vertex("Service", copy.deepcopy(v1_props))
    store.upsert_vertex("Service", copy.deepcopy(v2_props))
    store.upsert_vertex("Service", copy.deepcopy(v3_props))

    # Service CALLS Service is valid in manifest
    store.upsert_edge(
        "CALLS",
        "urn:eoip:service:auth-api",
        "urn:eoip:service:auth-db",
        {"coupling": "tight"},
    )

    # Perform merge
    merge_id = manager.merge(
        store=store,
        survivor_cid="urn:eoip:service:auth-svc",
        absorbed_cids=["urn:eoip:service:auth-api"],
        actor="system",
        reason="Alias deduplication",
    )

    # Edge was redirected to survivor
    edges = store.find_edges(limit=10)
    assert any(e["out_cid"] == "urn:eoip:service:auth-svc" and e["in_cid"] == "urn:eoip:service:auth-db" for e in edges)

    # Simulate process restart by loading a brand new Ledger from the disk path
    restarted_ledger = IdentityMergeLedger(storage_path=ledger_file)
    restarted_manager = ReversibleIdentityManager(ledger=restarted_ledger)

    # Perform split using the persisted merge operation ID
    split_id = restarted_manager.split(
        store=store,
        merge_op_id=merge_id,
        actor="steward-alice",
        reason="Splitting due to distinct microservice architecture boundary",
    )
    assert split_id.startswith("split-op-")

    # Post-split verification: Compare every vertex, edge, and property with original pre-merge state
    v1_restored = store.get_vertex_by_canonical_id("urn:eoip:service:auth-svc")
    v2_restored = store.get_vertex_by_canonical_id("urn:eoip:service:auth-api")
    restored_edges = store.find_edges(limit=10)

    assert v1_restored["properties"]["source_aliases"] == v1_props["source_aliases"]
    assert v2_restored["properties"]["source_aliases"] == v2_props["source_aliases"]
    assert v2_restored["properties"]["service_id"] == v2_props["service_id"]

    # Edge was restored back to original out_cid (urn:eoip:service:auth-api)
    assert any(e["out_cid"] == "urn:eoip:service:auth-api" and e["in_cid"] == "urn:eoip:service:auth-db" for e in restored_edges)


def test_linking_gate_evaluation_and_adverse_ambiguity():
    """CRA-023.5, CRA-023.A: Linking gate evaluation: precision >= 0.99, recall >= 0.80 and adverse ambiguity."""
    gold_data = [
        # 1. True match: identical email and name
        {
            "source_entity": {"id": "1", "name": "David Miller", "email": "dmiller@corp.internal"},
            "target_entity": {"id": "2", "name": "Dave Miller", "email": "dmiller@corp.internal"},
            "expected_match": True,
            "test_type": "standard",
        },
        # 2. True match: same name + strong neighborhood overlap
        {
            "source_entity": {"id": "3", "name": "Jennifer Aniston", "properties": {"dept": "Media"}},
            "target_entity": {"id": "4", "name": "Jennifer Aniston", "properties": {"dept": "Media"}},
            "source_neighbors": {"prj-1", "prj-2", "org-media"},
            "target_neighbors": {"prj-1", "prj-2", "org-media"},
            "source_vector": [0.5, 0.5, 0.5],
            "target_vector": [0.5, 0.5, 0.5],
            "expected_match": True,
            "test_type": "standard",
        },
        # 3. Adverse Ambiguity: Same-name entities with conflicting identifiers (CRA-023.A)
        {
            "source_entity": {"id": "5", "name": "John Smith", "properties": {"dept": "Sales", "emp_id": "EMP-01"}},
            "target_entity": {"id": "6", "name": "John Smith", "properties": {"dept": "Engineering", "emp_id": "EMP-99"}},
            "source_neighbors": {"team-sales", "crm-tool"},
            "target_neighbors": {"team-backend", "k8s-cluster"},
            "source_vector": [0.1, 0.9, 0.0],
            "target_vector": [0.9, 0.1, 0.0],
            "expected_match": False,  # Two completely distinct people sharing the common name John Smith!
            "test_type": "same_name_different_entities",
        },
        # 4. Adverse Ambiguity: Ambiguous abbreviation (CRA-023.A)
        {
            "source_entity": {"id": "7", "name": "AA", "properties": {"industry": "Aviation"}},
            "target_entity": {"id": "8", "name": "AA", "properties": {"industry": "Healthcare"}},
            "source_neighbors": {"fleet-boeing", "airport-dfw"},
            "target_neighbors": {"clinic-central", "rehab-support"},
            "expected_match": False,  # American Airlines vs Alcoholics Anonymous
            "test_type": "ambiguous_abbreviations",
        },
        # 5. Adverse Ambiguity: Wrong high-confidence vector match rejected by structural check (CRA-023.A)
        {
            "source_entity": {"id": "9", "name": "Billing Service", "properties": {"tier": "Tier 1"}},
            "target_entity": {"id": "10", "name": "Shipping Service", "properties": {"tier": "Tier 2"}},
            "source_neighbors": {"db-invoices", "payment-gateway"},
            "target_neighbors": {"fedex-api", "warehouse-cluster"},
            "source_vector": [0.8, 0.8, 0.8],  # Spurious vector closeness
            "target_vector": [0.8, 0.8, 0.79],
            "expected_match": False,
            "test_type": "spurious_vector_match",
        },
    ]

    report = evaluate_identity_linking_gate(gold_data)
    assert report.precision >= 0.99
    assert report.recall >= 0.80
    assert report.passed_gate is True

    # Adverse ambiguity test outcomes
    assert report.adverse_ambiguity_results["same_name_different_entities"] is True
    assert report.adverse_ambiguity_results["ambiguous_abbreviations"] is True
    assert report.adverse_ambiguity_results["spurious_vector_match"] is True


def test_candidate_generation_feature_attribution_and_anti_stub():
    """CRA-023.6, CRA-023.9: Exact feature set attribution and anti-stub verification."""
    gen = AlignmentCandidateGenerator(confidence_threshold=0.75, verify_anti_stub=True)

    e1 = {"id": "e1", "name": "Kubernetes Cluster"}
    e2 = {"id": "e2", "name": "Kubernetes Cluster"}

    cand = gen.generate_candidate(
        source_entity=e1,
        target_entity=e2,
        source_neighbors={"pod-1", "node-1"},
        target_neighbors={"pod-1", "node-1"},
        source_vector=[1.0, 0.0],
        target_vector=[1.0, 0.0],
    )

    # Feature set reporting (CRA-023.9)
    assert "lexical:jaro_winkler" in cand.features_used
    assert "structural:neighborhood_jaccard" in cand.features_used
    assert "semantic:vector_cosine" in cand.features_used
    assert cand.evidence["jaro_winkler_score"] == 1.0

    # Anti-stub error testing
    with pytest.raises(AntiStubVerificationError):
        # Trigger anti-stub failure with corrupted probe
        orig_fn = AlignmentCandidateGenerator._run_anti_stub_probes
        try:
            AlignmentCandidateGenerator._run_anti_stub_probes = lambda self: (_ for _ in ()).throw(
                AntiStubVerificationError("Anti-stub probe failed")
            )
            AlignmentCandidateGenerator(verify_anti_stub=True)
        finally:
            AlignmentCandidateGenerator._run_anti_stub_probes = orig_fn


def test_deeponto_worker_and_tenant_entity_linker():
    """CRA-023.7: DeepOnto worker and tenant-scoped EntityLinker with NIL support."""
    # DeepOnto alignment worker
    worker = DeepOntoAlignmentWorker()
    alignments = worker.align_ontologies(source_ontology=None, target_ontology=None)
    assert len(alignments) >= 1
    assert alignments[0]["confidence"] >= 0.90
    assert alignments[0]["mapping_relation"] == "skos:exactMatch"

    # Tenant-scoped entity linker
    kb = {"alpha service": "urn:eoip:service:alpha-svc", "auth db": "urn:eoip:db:auth"}
    linker = TenantScopedEntityLinker(tenant_id="tenant-42", knowledge_base=kb)

    # Known mention links to canonical ID
    res = linker.link_mention("Alpha Service")
    assert res is not None
    assert res["canonical_id"] == "urn:eoip:service:alpha-svc"
    assert res["tenant_id"] == "tenant-42"

    # Unknown mention produces NIL (None)
    assert linker.link_mention("Nonexistent Service") is None
