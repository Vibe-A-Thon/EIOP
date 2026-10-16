from eoip.future_scope import (
    ArtifactTemplate,
    CacheDependency,
    CatalogAsset,
    CatalogAssetType,
    ChangeDataCaptureLog,
    DeterministicRuleEngine,
    DualSemanticRecord,
    Fact,
    FUTURE_SCOPE_GAP_IDS,
    FederationMode,
    FederationSourceSpec,
    GraphViewDefinition,
    KnowledgeAppDefinition,
    KnowledgeAppPanel,
    LifecyclePolicy,
    LifecycleTier,
    LineageStandardsMapper,
    OntologyBranch,
    ObservabilityTracePlan,
    RuleDefinition,
    StewardshipItem,
    StewardshipState,
    TransformationLineageEvent,
    UnifiedCatalog,
    detect_semantic_merge_conflicts,
    evaluate_cache_freshness,
    estimate_deployment_size,
    roundtrip_dual_record,
    GraphChangeEvent,
)
from eoip.graph.memory import MemoryGraphStore
from eoip.federation.planner import SourceMode


def test_federation_source_spec_maps_policy_to_capability() -> None:
    assert "GAP-FED-004" in FUTURE_SCOPE_GAP_IDS
    assert "GAP-CATALOG-005" in FUTURE_SCOPE_GAP_IDS
    spec = FederationSourceSpec(
        source_id="jira-live",
        adapter_kind="rest",
        entity_types=("WorkItem",),
        mode=FederationMode.HYBRID,
        pushdown_filters=True,
        policy_tags=("internal",),
    )
    capability = spec.to_capability()
    assert capability.mode == SourceMode.HYBRID
    assert capability.pushdown_filters is True
    assert spec.explain()["hugegraph_required"] is False


def test_dual_semantic_record_round_trips_losslessly() -> None:
    record = DualSemanticRecord(
        canonical_id="urn:eoip:project:demo",
        label="Project",
        properties={"name": "Demo"},
        semantic_type="eoip:entity/Project",
    )
    result = roundtrip_dual_record(record)
    assert result["lossless"] is True
    assert result["restored"]["canonical_id"] == record.canonical_id


def test_rule_engine_infers_and_recomputes_after_retraction() -> None:
    engine = DeterministicRuleEngine(
        [
            RuleDefinition(
                rule_id="owner-is-expert",
                version="1",
                when={"predicate": "OWNS"},
                infer={"predicate": "IS_EXPERT_IN", "object": "owned-component"},
            )
        ]
    )
    facts = [
        Fact(
            subject="urn:person:ada",
            predicate="OWNS",
            object="urn:service:billing",
            source_id="src-1",
        )
    ]
    inferred = engine.infer(facts)
    assert inferred[0].status == "INFERRED"
    assert inferred[0].rule_id == "owner-is-expert@1"

    recomputed = engine.recompute_after_retraction(facts, retracted_source_ids={"src-1"})
    assert recomputed["asserted"] == []
    assert recomputed["inferred"] == []


def test_stewardship_workflow_and_semantic_merge_conflicts() -> None:
    item = StewardshipItem("ontology:demo")
    item.transition(StewardshipState.REVIEW, actor="alice")
    item.transition(StewardshipState.APPROVED, actor="bob")
    assert item.state == StewardshipState.APPROVED
    assert len(item.history) == 2

    base = {
        "vertex_labels": {"Project": {"domain": "WORK", "required": ["canonical_id"], "optional": []}},
        "edge_labels": {},
        "property_keys": {"canonical_id": "TEXT"},
    }
    left = {
        "vertex_labels": {"Project": {"domain": "WORK", "required": ["canonical_id", "name"], "optional": []}},
        "edge_labels": {},
        "property_keys": {"canonical_id": "TEXT"},
    }
    right = {
        "vertex_labels": {"Project": {"domain": "WORK", "required": ["canonical_id", "name"], "optional": []}},
        "edge_labels": {},
        "property_keys": {"canonical_id": "TEXT"},
    }
    conflicts = detect_semantic_merge_conflicts(
        OntologyBranch("left", base, left),
        OntologyBranch("right", base, right),
    )
    assert conflicts["mergeable"] is False
    assert conflicts["conflicts"][0]["subject"] == "Project.name"


def test_graph_view_materializes_reproducible_subset() -> None:
    store = MemoryGraphStore()
    store.upsert_vertex("Project", {"canonical_id": "urn:project:a", "name": "A", "owner": "team-a"})
    store.upsert_vertex("Project", {"canonical_id": "urn:project:b", "name": "B", "owner": "team-b"})
    view = GraphViewDefinition(
        view_id="team-a-projects",
        version="1.0.0",
        labels=("Project",),
        filters={"owner": "team-a"},
        projection=("name", "owner"),
    )
    materialized = view.materialize(store)
    assert materialized["row_count"] == 1
    assert materialized["rows"][0]["name"] == "A"
    assert materialized["fingerprint"].startswith("urn:eoip:view-materialization:")


def test_sizing_lineage_app_template_and_catalog_primitives() -> None:
    size = estimate_deployment_size(vertices=10_000, edges=20_000, users=3)
    assert size["profile"] == "laptop-dev"
    assert size["offline_capable"] is True

    lineage = TransformationLineageEvent(
        transformation_id="normalize-jira",
        inputs=("raw:jira:1",),
        outputs=("entity:workitem:1",),
        actor="worker",
        code_version="abc123",
        parameters={"mapper": "v1"},
    ).to_provenance()
    assert lineage["event_id"].startswith("urn:eoip:dataops:")

    app = KnowledgeAppDefinition(
        app_id="risk-app",
        version="1",
        panels=(
            KnowledgeAppPanel("graph", "graph", "q1"),
            KnowledgeAppPanel("evidence", "evidence", "q2"),
        ),
    )
    assert app.validate()["valid"] is True

    template = ArtifactTemplate(
        template_id="dashboard",
        artifact_type="knowledge-app",
        version="1",
        parameters={"owner": "string"},
    )
    assert template.instantiate({"owner": "team-a"})["valid"] is True

    catalog = UnifiedCatalog()
    catalog.upsert(CatalogAsset("source:jira", CatalogAssetType.DATA_SOURCE, "Jira", "team-a"))
    catalog.upsert(
        CatalogAsset(
            "product:risk",
            CatalogAssetType.KNOWLEDGE_PRODUCT,
            "Risk Product",
            "team-a",
            dependencies=("source:jira",),
        )
    )
    assert [asset.asset_id for asset in catalog.list()] == ["product:risk", "source:jira"]
    assert catalog.dependency_plan("product:risk")["dependencies_first"] == [
        "source:jira",
        "product:risk",
    ]


def test_lineage_standards_mapper_emits_openlineage_and_prov_o() -> None:
    event = TransformationLineageEvent(
        transformation_id="sync-docs",
        inputs=("doc:1",),
        outputs=("section:1",),
        actor="worker",
        code_version="def456",
    )
    mapped = LineageStandardsMapper().platform_emit_event(event)
    assert mapped["openlineage"]["job"]["name"] == "sync-docs"
    assert mapped["prov_o"]["prov:used"] == ["doc:1"]
    assert mapped["internal"]["outputs"] == ["section:1"]


def test_cdc_log_subscribe_replay_and_sync_plan() -> None:
    log = ChangeDataCaptureLog()
    log.append(
        GraphChangeEvent(
            sequence=1,
            entity_id="urn:project:a",
            domain="WORK",
            change_type="UPSERT",
            before=None,
            after={"name": "A"},
        )
    )
    log.append(
        GraphChangeEvent(
            sequence=2,
            entity_id="urn:service:b",
            domain="RUNTIME",
            change_type="UPSERT",
            before=None,
            after={"name": "B"},
        )
    )
    assert [event.entity_id for event in log.subscribe(domain="WORK")] == ["urn:project:a"]
    replay = log.replay(checkpoint=1)
    assert replay["next_checkpoint"] == 2
    plan = log.synchronization_plan(checkpoint=0)
    assert plan["search_index_entities"] == ["urn:project:a", "urn:service:b"]
    assert plan["graphrag_summary_domains"] == ["RUNTIME", "WORK"]


def test_cache_freshness_uses_version_freshness_ttl_and_cdc_dependencies() -> None:
    dependency = CacheDependency(
        graph_version="v1",
        source_freshness={"jira": 10},
        max_staleness_seconds=60,
    )
    ok = evaluate_cache_freshness(
        dependency,
        current_graph_version="v1",
        current_source_freshness={"jira": 10},
        age_seconds=30,
    )
    assert ok["serve_from_cache"] is True

    stale = evaluate_cache_freshness(
        dependency,
        current_graph_version="v2",
        current_source_freshness={"jira": 12},
        age_seconds=90,
        changed_entities={"urn:issue:1"},
        cached_entities={"urn:issue:1"},
    )
    assert stale["invalidate"] is True
    assert "graph_version_changed" in stale["reasons"]
    assert "cdc_entity_dependency_changed" in stale["reasons"]


def test_lifecycle_policy_tiers_purge_and_rebuild_plan() -> None:
    policy = LifecyclePolicy(hot_days=10, warm_days=20, retention_days=30, agent_memory_days=5)
    assert policy.tier_for_age(2) == LifecycleTier.HOT
    assert policy.tier_for_age(15) == LifecycleTier.WARM
    assert policy.tier_for_age(25) == LifecycleTier.ARCHIVE
    assert policy.tier_for_age(6, is_agent_memory=True) == LifecycleTier.PURGED
    assert policy.purge_plan("fact:1")["purge_allowed"] is True
    assert policy.purge_plan("fact:1", legal_hold=True)["purge_allowed"] is False
    assert policy.rebuild_plan("summary:1", ("fact:1",))["rebuildable"] is True


def test_observability_trace_plan_correlates_logs_metrics_and_graph_metrics() -> None:
    request = ObservabilityTracePlan.request_path("corr-1").correlation_envelope()
    assert [step["component"] for step in request["traces"]][:3] == ["ui", "api", "planner"]
    assert request["metrics"]["labels"]["correlation_id"] == "corr-1"
    assert "query_latency_ms" in request["graph_metrics"]

    ingestion = ObservabilityTracePlan.ingestion_path("corr-2").correlation_envelope()
    assert [step["component"] for step in ingestion["traces"]] == [
        "source_record",
        "canonical_entity",
        "graph_edge",
        "search_index",
        "vector_index",
    ]
