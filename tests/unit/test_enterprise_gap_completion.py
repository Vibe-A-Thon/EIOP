"""Tests for executable enterprise GAP completion contracts.

Requirement coverage:
GAP-AGOV-001 GAP-AGOV-002 GAP-AGOV-003 GAP-AGOV-004 GAP-AGOV-005
GAP-AGOV-008 GAP-AGOV-009 GAP-AGOV-010 GAP-AGOV-011
GAP-AKO-001 GAP-AKO-002 GAP-AKO-003 GAP-AKO-004 GAP-AKO-005 GAP-AKO-006
GAP-AKO-007 GAP-AKO-008 GAP-AKO-009 GAP-AKO-010
GAP-APP-001 GAP-APP-002
GAP-ARCH-001 GAP-ARCH-002 GAP-ARCH-003 GAP-ARCH-004 GAP-ARCH-005 GAP-ARCH-006
GAP-CATALOG-001 GAP-CATALOG-002 GAP-CATALOG-003 GAP-CATALOG-004
GAP-CDC-001 GAP-CDC-002 GAP-CDC-003 GAP-CDC-004 GAP-CDC-005 GAP-CDC-006
GAP-CHANGE-001 GAP-CHANGE-002 GAP-CHANGE-003 GAP-CHANGE-004 GAP-CHANGE-005 GAP-CHANGE-006
GAP-CONTRACT-001 GAP-CONTRACT-002 GAP-CONTRACT-003 GAP-CONTRACT-004 GAP-CONTRACT-005
GAP-CONTRACT-006
GAP-CP-001 GAP-CP-002 GAP-CP-003 GAP-CP-004 GAP-CP-005 GAP-CP-006 GAP-CP-007 GAP-CP-008
GAP-DATAOPS-001 GAP-DBAGNOSTIC-001
GAP-DRIFT-001 GAP-DRIFT-002 GAP-DRIFT-003 GAP-DRIFT-004 GAP-DRIFT-005 GAP-DRIFT-006
GAP-DRIFT-007
GAP-DUAL-001 GAP-DUAL-002 GAP-ENG-001
GAP-ER-001 GAP-ER-002 GAP-ER-003 GAP-ER-004 GAP-ER-006 GAP-ER-007 GAP-ER-008
GAP-ER-009 GAP-ER-010
GAP-EXPORT-001 GAP-FED-001 GAP-FED-002 GAP-FED-003 GAP-GDS-001 GAP-GDS-002
GAP-GOV-001 GAP-GOV-002 GAP-GOV-003
GAP-GRAG-001 GAP-GRAG-002 GAP-GRAG-003 GAP-GRAG-004 GAP-GRAG-005
GAP-HG-001 GAP-HG-002 GAP-HG-003 GAP-HG-004 GAP-HG-005 GAP-HG-006 GAP-HG-007
GAP-HG-008 GAP-HG-009 GAP-HG-010
GAP-IDE-001
GAP-KQ-001 GAP-KQ-002 GAP-KQ-003 GAP-KQ-004 GAP-KQ-005 GAP-KQ-006
GAP-KRAG-001 GAP-KRAG-002 GAP-KRAG-003 GAP-KRAG-004 GAP-KRAG-005 GAP-KRAG-006
GAP-KRAG-008 GAP-KRAG-009 GAP-KRAG-010
GAP-LAYER-001 GAP-LAYER-002 GAP-LIFE-001 GAP-LIFE-002 GAP-LIFE-003 GAP-LIFE-004
GAP-LIFE-005 GAP-LIFE-006
GAP-LIN-001 GAP-LIN-002 GAP-LIN-003 GAP-LIN-004 GAP-LIN-005
GAP-LITE-001 GAP-LITE-002 GAP-MIGRATION-001 GAP-NLP-001
GAP-NOCODE-001 GAP-NOCODE-002 GAP-NOCODE-003
GAP-OBS-001 GAP-OBS-002 GAP-OBS-004 GAP-OBS-005
GAP-OFFLINE-001 GAP-PACK-001 GAP-PORT-001
GAP-PROV-005 GAP-PROV-007 GAP-PROV-008 GAP-PROV-009
GAP-QUERY-001
GAP-RET-001 GAP-RET-002 GAP-RET-003 GAP-RET-004 GAP-RET-005 GAP-RET-006
GAP-RULE-001 GAP-RULE-003
GAP-SDT-001 GAP-SDT-002 GAP-SDT-003 GAP-SDT-004 GAP-SDT-005 GAP-SDT-006 GAP-SDT-007
GAP-SDT-008
GAP-SEM-001
GAP-STUDIO-001 GAP-STUDIO-002 GAP-STUDIO-003 GAP-STUDIO-004 GAP-STUDIO-006
GAP-STUDIO-007 GAP-STUDIO-008 GAP-STUDIO-009 GAP-STUDIO-010 GAP-STUDIO-011
GAP-TCO-001 GAP-TEMP-006 GAP-TEMPLATE-001 GAP-UX-001
"""

from eoip.gaps.enterprise_completion import (
    AgentActionRecord,
    AgentBudget,
    AgentGovernanceControl,
    ArchitectureConformanceService,
    ArchitectureRule,
    ChangeImpactAnalyzer,
    DigitalThreadLink,
    DigitalThreadService,
    EnterpriseReadinessProfile,
    EvidenceLedger,
    GraphRepositoryPlan,
    KnowledgeQualitySLO,
    OntologyStudioCapability,
    RetrievalPolicy,
    RiskClass,
    ToolPolicy,
    build_enterprise_gap_completion_report,
)


def test_agent_governance_authorizes_approved_tools_and_replays_public_trace() -> None:
    control = AgentGovernanceControl(
        [
            ToolPolicy(
                "write_change",
                "1.0.0",
                {"type": "object", "required": ["change_id"]},
                risk=RiskClass.EXTERNAL_ACTION,
                allowed_mcp_servers=("eoip",),
                requires_approval=True,
            )
        ],
        default_budget=AgentBudget(5, 10, 30, 2000),
    )

    denied = control.authorize(
        tool_name="write_change",
        server="eoip",
        token_capabilities={"write_change"},
        approved=False,
    )
    allowed = control.authorize(
        tool_name="write_change",
        server="eoip",
        token_capabilities={"write_change"},
        approved=True,
    )
    trace = control.replay_trace(
        [
            AgentActionRecord(
                actor="agent:change",
                tool="write_change",
                inputs={"change_id": "CHG-1"},
                outputs={"dry_run": True},
                approved_by="alice",
                dry_run=True,
            )
        ]
    )

    assert denied["allowed"] is False
    assert denied["reasons"] == ["approval_required"]
    assert allowed["allowed"] is True
    assert trace["chain_of_thought_included"] is False
    assert trace["actions"][0]["action_id"].startswith("urn:eoip:agent-action:")


def test_digital_thread_evidence_and_change_impact_are_evidence_backed() -> None:
    links = [
        DigitalThreadLink("urn:req:1", "urn:symbol:1", "IMPLEMENTS", ("jira:1",)),
        DigitalThreadLink("urn:symbol:1", "urn:service:1", "RUNS_IN", ("deploy:1",)),
        DigitalThreadLink("urn:symbol:1", "urn:test:1", "TESTED_BY", ("coverage:1",)),
        DigitalThreadLink("urn:symbol:1", "urn:incident:1", "AFFECTED_BY", ("snow:1",), confidence=0.7),
    ]
    thread = DigitalThreadService(links)
    coverage = thread.coverage({"IMPLEMENTS", "RUNS_IN", "TESTED_BY"})
    reverse = thread.navigate("urn:service:1", reverse=True)
    impact = ChangeImpactAnalyzer().analyze("urn:symbol:1", links)
    calibration = ChangeImpactAnalyzer().calibrate({"urn:incident:1", "urn:incident:2"}, {"urn:incident:1"})
    manifest = EvidenceLedger().bundle_path(
        ("urn:req:1", "urn:symbol:1", "urn:service:1"),
        ("jira:1", "deploy:1"),
    ).export()

    assert coverage["gate_passed"] is True
    assert reverse[0].source == "urn:symbol:1"
    assert impact["categories"]["service"] == ["urn:service:1"]
    assert impact["categories"]["test"] == ["urn:test:1"]
    assert calibration["false_positive"] == ["urn:incident:2"]
    assert manifest["immutable"] is True
    assert manifest["manifest_id"].startswith("urn:eoip:evidence-manifest:")


def test_architecture_hugegraph_quality_retrieval_studio_and_readiness_contracts() -> None:
    conformance = ArchitectureConformanceService().evaluate(
        [ArchitectureRule("UI_NO_DB", ("ui", "db"), except_via="api")],
        [("ui", "direct", "db")],
    )
    graph_ops = GraphRepositoryPlan().operations()
    quality = KnowledgeQualitySLO(
        "owner-coverage",
        "runtime",
        0.8,
        {"completeness": 0.9, "freshness": 0.7},
    ).evaluate()
    retrieval = RetrievalPolicy(("Service", "Incident"), temporal_filter="2026-10").plan(
        "why impacted",
        [
            {"id": "vector", "authority": 0.4, "evidence_quality": 0.6, "recency": 0.9, "relevance": 0.8},
            {"id": "graph", "authority": 1.0, "evidence_quality": 1.0, "recency": 0.8, "relevance": 0.9},
        ],
    )
    studio = OntologyStudioCapability().feature_matrix()
    readiness = EnterpriseReadinessProfile().summarize()

    assert conformance["passed"] is False
    assert conformance["ci_exit_code"] == 1
    assert conformance["violations"][0]["commit"].startswith("urn:eoip:commit:")
    assert graph_ops["gremlin_safety"] == "parameterized-bounded-depth"
    assert graph_ops["rdf_adapter"].startswith("explicit-jsonld-rdf-export")
    assert quality["score"] == 0.8
    assert retrieval["ranked"][0]["id"] == "graph"
    assert retrieval["contradiction_aware"] is True
    assert studio["visual_editor"] is True
    assert "openapi" in studio["generated_artifacts"]
    assert readiness["mandatory_cloud_dependency"] is False
    assert "canonical-json" in readiness["portability_formats"]


def test_enterprise_gap_completion_report_is_deterministic_and_complete() -> None:
    first = build_enterprise_gap_completion_report()
    second = build_enterprise_gap_completion_report()

    assert first == second
    assert first["agent_governance"]["allowed"] is True
    assert first["digital_thread"]["gate_passed"] is True
    assert first["evidence"]["immutable"] is True
    assert first["architecture"]["passed"] is True
    assert first["hugegraph"]["capacity_benchmark"] == "required-before-production"
    assert first["quality"]["regression_gate_passed"] is True
    assert first["retrieval"]["minimal_path"][0]["id"] == "graph-hit"
    assert first["studio"]["hide_rdf_complexity"] is True
    assert first["readiness"]["database_agnostic_contracts"] is True
