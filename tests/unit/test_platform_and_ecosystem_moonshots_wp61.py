"""Unit tests for Phase 6 WP 6.1: Platform and Ecosystem Moonshots (14 tasks).

Requirements:
- MS-6: WebGPU Spatial 3D / Level-of-Detail Canvas for >50K vertices
- MS-7: Zero-Knowledge Privacy-Preserving Federated Mesh & Evidence Verifier
- MS-11: Universal Plugin & Extension Marketplace with Sandboxed Execution
- MS-12: Live Collaborative Graph Studio via CRDT
- MS-13: Graph-as-Code & GitOps for Ontology, Data, and Policy
- MS-16: Agentic Process Intelligence & Digital Process Twin
- MS-17: Multi-Agent A2A + MCP Orchestration Fabric
- MS-25: Industry Intelligence Domain Packs (BFSI, Healthcare, Software Eng)
- MS-26: White-Label Partner Ecosystem & OEM Multi-Tenant Theme Framework
- MS-27: Usage Intelligence & Embedded Billing Metering Engine
- G2-PM-002: Ingestion of enterprise event logs (Jira, ServiceNow, CI/CD)
- G2-PM-003: Discovery of observed process paths and transition frequencies
- G2-PM-004: Conformance checking against reference process models
- G2-PM-005: Bottleneck detection and process deviation reporting
"""

from __future__ import annotations

import pytest

from eoip.agents.mesh_supervisor import ResilientAgentMeshSupervisor
from eoip.billing.metering import UsageIntelligenceMeter
from eoip.branding.theme import (
    ColorPalette,
    LogoRef,
    ThemeMode,
    ThemePackage,
    ThemeRegistry,
    ThemeVariant,
)
from eoip.graph.memory import MemoryGraphStore
from eoip.graph.process_mining import (
    ProcessCase,
    check_process_conformance,
    compare_to_designed_flow,
    detect_process_bottlenecks,
    deviation_report,
    discover_directly_follows_graph,
    discover_process_paths,
    extract_cases_from_graph,
    ingest_event_log,
)
from eoip.marketplace.manifest import CapabilityKind, PackageManifest
from eoip.marketplace.packager import PackageReader, build_package, package_query_template
from eoip.moonshot.collaborative_crdt import CollaborativeGraphCRDT
from eoip.moonshot.confidential_graph import ZeroKnowledgeEvidenceVerifier
from eoip.moonshot.spatial_lod_canvas import BoundingBox, SpatialLODCanvasEngine
from eoip.ontology.domain_pack_manager import DomainPackLifecycleManager
from eoip.ontology.gitops import (
    OntologyGitOpsWorkflow,
    PullRequestStatus,
    current_manifest_snapshot,
    diff_manifests,
)


# --- 1. MS-6: Spatial LOD Canvas ---

@pytest.mark.req("MS-6")
def test_ms_06_spatial_lod_canvas():
    engine = SpatialLODCanvasEngine()
    # Insert 1000 nodes distributed across space centered at origin
    for i in range(1000):
        x = (i % 50) * 40.0 - 1000.0
        y = (i // 50) * 40.0 - 400.0
        engine.insert_node(f"node-{i}", x, y, label="Service")

    assert len(engine.nodes) == 1000

    # Query with high zoom (LOD_0)
    vp_tight = BoundingBox(-200.0, -200.0, 200.0, 200.0)
    res_tight = engine.query_viewport(vp_tight, zoom_level=1.0)
    assert res_tight["lod_tier"] == "LOD_0"
    assert res_tight["rendered_node_count"] > 0
    assert res_tight["culled_node_count"] > 0

    # Query with low zoom (LOD_2)
    vp_wide = BoundingBox(-2000.0, -2000.0, 2000.0, 2000.0)
    res_wide = engine.query_viewport(vp_wide, zoom_level=0.1)
    assert res_wide["lod_tier"] == "LOD_2"
    assert res_wide["rendered_node_count"] <= 1000


# --- 2. MS-7: Zero-Knowledge Privacy-Preserving Mesh ---

@pytest.mark.req("MS-7")
def test_ms_07_zk_privacy_mesh():
    verifier = ZeroKnowledgeEvidenceVerifier()
    # Generate proof for path connectivity across privacy boundaries
    proof = verifier.generate_path_proof(
        path_nodes=["srv-auth", "db-users", "sec-gateway"],
        secret_salt="boundary-enclave-salt",
    )
    assert proof.root_hash
    assert len(proof.commitments) == 3

    # Verification succeeds with valid proof
    assert verifier.verify_path_proof(proof, "srv-auth", "sec-gateway") is True
    assert verifier.verify_path_proof(proof, "srv-auth", "wrong-gateway") is False


# --- 3. MS-11: Plugin & Extension Marketplace ---

@pytest.mark.req("MS-11")
def test_ms_11_plugin_marketplace():
    archive_bytes = package_query_template(
        name="sec-scanner-query",
        version="1.0.0",
        template_id="vuln-scanner",
        query_text="SELECT * FROM Vulnerability WHERE severity = 'CRITICAL'",
        description="Automated SAST & dependency vulnerability scanner",
    )
    assert len(archive_bytes) > 0
    reader = PackageReader(archive_bytes)
    manifest = reader.manifest()
    assert manifest.name == "sec-scanner-query"
    assert manifest.version == "1.0.0"
    assert CapabilityKind.QUERY_TEMPLATES in manifest.provides
    assert reader.verify_checksums() == []


# --- 4. MS-12: Live Collaborative Graph Studio (CRDT) ---

@pytest.mark.req("MS-12")
def test_ms_12_collaborative_crdt_graph_studio():
    # Peer Alice and Peer Bob start separate replicas
    alice = CollaborativeGraphCRDT(peer_id="alice")
    bob = CollaborativeGraphCRDT(peer_id="bob")

    # Alice adds a vertex and an edge
    op_v1 = alice.add_vertex("srv-order", "Service", {"tier": "gold", "owner": "alice"})
    bob.add_vertex("srv-pay", "Service", {"tier": "silver", "owner": "bob"})

    # Concurrent edits: Alice updates srv-order, Bob deletes srv-pay
    alice.update_vertex("srv-order", {"status": "ACTIVE"})
    bob.remove_vertex("srv-pay")

    # Connect replicas by merging
    alice.merge(bob)
    bob.merge(alice)

    # Deterministic convergence: both replicas have identical state
    snap_a = alice.get_snapshot()
    snap_b = bob.get_snapshot()
    assert snap_a["vertex_count"] == snap_b["vertex_count"]
    assert "srv-order" in snap_a["vertices"]
    assert "srv-pay" not in snap_a["vertices"]
    assert snap_a["vertices"]["srv-order"]["status"] == "ACTIVE"


# --- 5. MS-13: Graph-as-Code & GitOps for Ontology ---

@pytest.mark.req("MS-13")
def test_ms_13_gitops_graph_as_code():
    workflow = OntologyGitOpsWorkflow()
    workflow.create_branch("feature/billing-models")
    manifest = workflow.get_branch_manifest("feature/billing-models")
    manifest["vertex_labels"]["LedgerTransaction"] = {
        "domain": "FINANCE",
        "required": ["canonical_id"],
        "optional": ["amount", "currency"],
    }
    workflow.commit_manifest("feature/billing-models", manifest, "Add LedgerTransaction", author="architect@corp.internal")

    # Generate PR proposal
    pr = workflow.create_pull_request(
        title="Introduce LedgerTransaction entity",
        source_branch="feature/billing-models",
        target_branch="main",
        author="architect@corp.internal",
    )
    assert pr.pr_id
    assert pr.status == PullRequestStatus.OPEN.value

    # Review and approve
    workflow.review_pull_request(pr.pr_id, reviewer="lead-architect", decision="approve")
    assert pr.status == PullRequestStatus.APPROVED.value

    # Merge proposal
    merge_res = workflow.merge_pull_request(pr.pr_id, merger="lead-architect")
    assert merge_res["status"] == "MERGED"


# --- 6. MS-16: Agentic Process Intelligence & Process Twin ---

@pytest.mark.req("MS-16")
def test_ms_16_agentic_process_intelligence():
    raw_logs = [
        {"case_id": "C-1", "activity": "Create", "timestamp": "2026-10-01T10:00:00Z"},
        {"case_id": "C-1", "activity": "Review", "timestamp": "2026-10-01T10:30:00Z"},
        {"case_id": "C-1", "activity": "Deploy", "timestamp": "2026-10-01T11:00:00Z"},
        {"case_id": "C-2", "activity": "Create", "timestamp": "2026-10-01T10:15:00Z"},
        {"case_id": "C-2", "activity": "Deploy", "timestamp": "2026-10-01T11:45:00Z"},  # skipped review
    ]
    cases = ingest_event_log(raw_logs)
    assert len(cases) == 2

    # Discover process graph
    dfg = discover_process_paths(cases)
    assert dfg["total_cases"] == 2
    assert len(dfg["transitions"]) >= 2

    # Digital Process Twin conformance checking
    designed = ["Create", "Review", "Deploy"]
    comp = compare_to_designed_flow(dfg, designed)
    assert comp["conformance_rate"] < 1.0  # C-2 has skipped step
    assert any(d["type"] == "skipped_steps" for d in comp["deviations"])


# --- 7. MS-17: Multi-Agent A2A + MCP Orchestration ---

@pytest.mark.req("MS-17")
def test_ms_17_multi_agent_a2a_orchestration(tmp_path):
    supervisor = ResilientAgentMeshSupervisor(storage_dir=tmp_path)
    bundle = supervisor.start_session(
        agent_id="SupervisorAgent",
        request_id="req-101",
        goal="Coordinate cross-domain code impact and security audit",
    )
    assert bundle.recovery_id
    assert bundle.status == "IN_PROGRESS"

    # Checkpoint step
    supervisor.checkpoint_step(
        bundle.recovery_id,
        step_name="Step1: Graph Blast Radius Computed",
        state_update={"impacted_nodes": ["srv-gateway", "auth-service"]},
    )
    assert bundle.step_count == 1

    # Succeeded run
    res = supervisor.mark_succeeded(bundle.recovery_id, final_result={"summary": "Audit clean. Deployment approved."})
    assert res.status == "SUCCEEDED"


# --- 8. MS-25: Industry Intelligence Domain Packs ---

@pytest.mark.req("MS-25")
def test_ms_25_industry_domain_packs():
    store = MemoryGraphStore()
    manager = DomainPackLifecycleManager(store)
    packs = manager.list_packs()
    pack_names = {p["name"] for p in packs}
    for required in ("bfsi", "cybersecurity", "healthcare", "software-engineering"):
        assert required in pack_names

    # Activate healthcare vertical
    res = manager.activate_pack("healthcare", seed_sample_topology=True)
    assert res["status"] == "ACTIVATED"
    assert res["entities_seeded"] >= 1


# --- 9. MS-26: White-Label Partner & OEM Framework ---

@pytest.mark.req("MS-26")
def test_ms_26_white_label_oem_framework():
    registry = ThemeRegistry()
    tenant_theme = ThemePackage(
        id="urn:eoip:branding:theme:acme-oem",
        name="Acme Financial Knowledge Portal",
        app_name="Acme Graph Studio",
        variants={
            ThemeMode.LIGHT: ThemeVariant(
                mode=ThemeMode.LIGHT,
                colors=ColorPalette(primary="#1a365d", secondary="#2b6cb0", background="#0f172a"),
            )
        },
        logos={ThemeMode.LIGHT: LogoRef(key="logos/acme-logo.svg", alt="Acme Corp")},
    )
    registry.register(tenant_theme)
    registry.assign("tenant-acme", tenant_theme.id)

    resolved = registry.resolve("tenant-acme")
    assert resolved.name == "Acme Financial Knowledge Portal"
    assert resolved.app_name == "Acme Graph Studio"
    assert resolved.variants[ThemeMode.LIGHT].colors.primary == "#1a365d"


# --- 10. MS-27: Usage Intelligence & Embedded Billing ---

@pytest.mark.req("MS-27")
def test_ms_27_usage_intelligence_metering():
    meter = UsageIntelligenceMeter(
        tenant_quotas={"tenant-alpha": {"QUERY_TOKENS": 10000.0, "API_CALLS": 500.0}}
    )
    rec1 = meter.record_usage("tenant-alpha", "QUERY_TOKENS", 1200.0, {"query_id": "q-1"})
    rec2 = meter.record_usage("tenant-alpha", "API_CALLS", 10.0, {"route": "/api/v1/search"})

    assert rec1.receipt_hash
    assert meter.verify_receipt(rec1) is True

    summary = meter.get_tenant_summary("tenant-alpha")
    assert summary["consumption"]["QUERY_TOKENS"] == 1200.0
    assert summary["consumption"]["API_CALLS"] == 10.0
    assert summary["record_count"] == 2


# --- 11. G2-PM-002: Ingestion of Enterprise Event Logs ---

@pytest.mark.req("G2-PM-002")
def test_g2_pm_002_event_log_ingestion():
    events = [
        {"case_id": "INC-101", "activity": "Reported", "timestamp": "2026-10-05T01:00:00Z"},
        {"case_id": "INC-101", "activity": "Triage", "timestamp": "2026-10-05T01:15:00Z"},
        {"case_id": "INC-101", "activity": "Resolved", "timestamp": "2026-10-05T02:00:00Z"},
    ]
    cases = ingest_event_log(events)
    assert len(cases) == 1
    assert cases[0].case_id == "INC-101"
    assert len(cases[0].events) == 3


# --- 12. G2-PM-003: Discovery of Observed Process Paths ---

@pytest.mark.req("G2-PM-003")
def test_g2_pm_003_process_path_discovery():
    cases = [
        ProcessCase(case_id="1", events=[{"field": "status", "to_value": "A"}, {"field": "status", "to_value": "B"}]),
        ProcessCase(case_id="2", events=[{"field": "status", "to_value": "A"}, {"field": "status", "to_value": "B"}]),
        ProcessCase(case_id="3", events=[{"field": "status", "to_value": "A"}, {"field": "status", "to_value": "C"}]),
    ]
    dfg = discover_directly_follows_graph(cases)
    assert dfg["total_cases"] == 3
    assert len(dfg["paths"]) == 2
    transitions = {f"{t['from']}->{t['to']}": t["count"] for t in dfg["transitions"]}
    assert transitions.get("A->B") == 2
    assert transitions.get("A->C") == 1


# --- 13. G2-PM-004: Conformance Checking Against Reference Flow ---

@pytest.mark.req("G2-PM-004")
def test_g2_pm_004_conformance_checking():
    cases = [
        ProcessCase(case_id="1", events=[{"field": "status", "to_value": "Open"}, {"field": "status", "to_value": "Closed"}]),
    ]
    res = check_process_conformance(cases, reference_model=["Open", "In_Progress", "Closed"])
    assert res["deviation_count"] > 0
    assert any(d["type"] == "skipped_steps" and "In_Progress" in d["skipped"] for d in res["deviations"])


# --- 14. G2-PM-005: Bottleneck Detection & Deviation Reporting ---

@pytest.mark.req("G2-PM-005")
def test_g2_pm_005_bottleneck_detection():
    cases = [
        ProcessCase(case_id=str(i), events=[{"field": "status", "to_value": "Triage"}, {"field": "status", "to_value": "Investigation"}])
        for i in range(10)
    ]
    bottlenecks = detect_process_bottlenecks(cases)
    assert len(bottlenecks) >= 1
    assert bottlenecks[0]["from"] == "Triage"
    assert bottlenecks[0]["to"] == "Investigation"
    assert bottlenecks[0]["is_bottleneck"] is True
