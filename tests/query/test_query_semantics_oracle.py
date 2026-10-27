"""Acceptance test suite: Query semantics oracle, SPARQL endpoint, OBDA federation, and budgets (WP-024, CRA-024.1-11, CRA-024.A)."""
from __future__ import annotations

import json
import pytest
import time
from typing import Any

from eoip.capabilities.model import UnsupportedCapabilityError
from eoip.federation.obda import (
    FederatedDataSource,
    FederatedExecutionOutcome,
    OBDAFederationEngine,
    SemanticsMode,
    SourceAuthDelegation,
)
from eoip.graph.rdf_backend import (
    FusekiGraphStore,
    GraphDBGraphStore,
    create_rdf_store_from_config,
)
from eoip.qlang.manifest_registry import DialectManifest, ManifestRegistry
from eoip.query.adapters.cypher_adapter import OpenCypherAdapter
from eoip.query.adapters.graphql_adapter import GraphQLShapeAdapter
from eoip.query.adapters.sql_adapter import SQLOntologyAdapter
from eoip.query.benchmarks import SemanticEquivalenceComparator, WarmedEndpointBenchmark
from eoip.query.bi_connectivity import BISessionDriver, BISessionEmulator
from eoip.query.plan_engine import (
    ParameterizedQuery,
    PlanNodeType,
    ScopeViolationError,
    TrustedScope,
    TypedPlanEngine,
)
from eoip.query.sensitive_redactor import (
    ScopedQueryManager,
    redact_sensitive_literals,
)
from eoip.query.service import (
    QueryBudget,
    QueryService,
    ReasoningMode,
)
from eoip.query.sparql_protocol import SparqlProtocolHandler


# ===========================================================================
# CRA-024.1: Grammar / capability manifests per dialect & backend
# ===========================================================================

@pytest.mark.req("CRA-024")
def test_cra_024_1_grammar_capability_manifests():
    registry = ManifestRegistry.get_instance()
    # Check registered manifests
    manifests = registry.list_manifests()
    assert "EQL" in manifests
    assert "EOQL" in manifests
    assert "SPARQL" in manifests
    assert "SQL" in manifests
    assert "OPENCYPHER" in manifests
    assert "GREMLIN" in manifests
    assert "GRAPHQL" in manifests

    # Supported constructs pass
    registry.validate_dialect_construct("EQL", "FIND")
    registry.validate_dialect_construct("EOQL", "SELECT")
    registry.validate_dialect_construct("SPARQL", "WHERE")

    # Unsupported constructs fail with UNSUPPORTED_CAPABILITY naming construct
    with pytest.raises(UnsupportedCapabilityError) as exc_info:
        registry.validate_dialect_construct("EOQL", "DROP_TABLE")
    assert exc_info.value.code == "UNSUPPORTED_CAPABILITY"
    assert "DROP_TABLE" in str(exc_info.value)

    # In-query inspection fails unsupported constructs
    with pytest.raises(UnsupportedCapabilityError) as exc_info2:
        registry.check_query_constructs("SQL", "DROP TABLE users;")
    assert exc_info2.value.code == "UNSUPPORTED_CAPABILITY"


# ===========================================================================
# CRA-024.2: Typed parsed plans, parameterization & scope injection
# ===========================================================================

@pytest.mark.req("CRA-024")
def test_cra_024_2_typed_plan_and_scope_injection():
    engine = TypedPlanEngine()
    scope = TrustedScope(
        tenant_id="tenant_alpha",
        principal_id="user_123",
        allowed_graphs=["default", "analytics"],
        allowed_sources=["local", "snowflake_dw"],
    )

    # Parse and parameter binding
    param_query = ParameterizedQuery(
        query_template="SELECT name FROM WorkItem WHERE id = :item_id",
        parameters={"item_id": "WI-999"},
        dialect="EOQL",
    )
    bound_params = param_query.bind_parameters()
    assert bound_params["item_id"] == "WI-999"

    # Rejection of dangerous injection parameters
    bad_param = ParameterizedQuery(
        query_template="SELECT * FROM WorkItem WHERE id = :item_id",
        parameters={"item_id": "1; DROP TABLE WorkItem;--"},
    )
    with pytest.raises(ValueError, match="Dangerous parameter value"):
        bad_param.bind_parameters()

    # Rejection of unauthorized DDL operations in query
    with pytest.raises(PermissionError, match="Unauthorized operation 'DROP'"):
        engine.parse_to_plan("DROP TABLE WorkItem", dialect="EOQL")

    # Plan generation & scope injection
    plan = engine.parse_to_plan("SELECT name FROM WorkItem WHERE priority = 'HIGH'", dialect="EOQL", parameters=bound_params)
    assert plan.node_type == PlanNodeType.PROJECT

    scoped_plan = engine.inject_scope(plan, scope)
    injected = scoped_plan.find_all(lambda n: n.node_type == PlanNodeType.FILTER and n.properties.get("injected_scope"))
    assert len(injected) > 0

    # Unauthorized graph selection rejected with ScopeViolationError (403)
    plan_forbidden = engine.parse_to_plan("SELECT * FROM WorkItem", dialect="EOQL")
    plan_forbidden.properties["graph"] = "secret_finance_graph"
    with pytest.raises(ScopeViolationError) as exc_info:
        engine.inject_scope(plan_forbidden, scope)
    assert exc_info.value.status_code == 403


# ===========================================================================
# CRA-024.3: Operations validate, explain, cost, profile, execute, cancel
# ===========================================================================

@pytest.mark.req("CRA-024")
def test_cra_024_3_operations_and_cancellation():
    service = QueryService()
    scope = TrustedScope(tenant_id="tenant_alpha", principal_id="user_123")

    # 1. Validate
    val = service.validate("SELECT name FROM WorkItem", dialect="EOQL")
    assert val.valid is True
    assert len(val.errors) == 0

    val_bad = service.validate("DROP TABLE WorkItem", dialect="EOQL")
    assert val_bad.valid is False

    # 2. Cost
    cost = service.cost("SELECT * FROM WorkItem", dialect="EOQL", scope=scope)
    assert cost.within_budget is True
    assert cost.estimated_memory_bytes > 0

    # 3. Explain
    exp = service.explain("SELECT * FROM WorkItem", dialect="EOQL", scope=scope, reasoning_mode=ReasoningMode.RDFS_ENTAILMENT)
    assert exp.reasoning_mode == ReasoningMode.RDFS_ENTAILMENT
    assert exp.plan["node_type"] == "PROJECT"
    assert "local" in exp.source_allocations

    # 4. Profile & Execute
    exec_res = service.execute("SELECT * FROM WorkItem", dialect="EOQL", scope=scope)
    assert exec_res.status == "COMPLETED"
    assert len(exec_res.rows) > 0
    assert exec_res.profile.rows_returned == len(exec_res.rows)
    assert exec_res.profile.elapsed_ms >= 0

    # 5. Cancel operation frees resources
    def long_executor(plan, budget, cancel_flag):
        cancel_flag.set()  # simulate immediate cancel signal
        return []

    cancel_res = service.execute(
        "SELECT * FROM WorkItem",
        dialect="EOQL",
        scope=scope,
        store_executor=long_executor,
    )
    assert cancel_res.status == "CANCELLED"
    assert cancel_res.profile.cancelled is True


# ===========================================================================
# CRA-024.4: Qualified OBDA / Federation with pushdown, null & degradation
# ===========================================================================

@pytest.mark.req("CRA-024")
def test_cra_024_4_obda_federation():
    engine = OBDAFederationEngine()

    auth = SourceAuthDelegation(
        source_id="snowflake_source",
        tenant_id="tenant_alpha",
        auth_type="BEARER_TOKEN",
        credentials={"token": "sno_token_xyz"},
    )
    assert auth.get_auth_headers()["Authorization"] == "Bearer sno_token_xyz"

    source = FederatedDataSource(
        source_id="snowflake_source",
        source_type="SNOWFLAKE",
        schema_hash="abc123hash",
        watermark_timestamp=1700000000.0,
        supports_pushdown=True,
        is_available=True,
        auth_delegation=auth,
    )

    def snowflake_worker(fragment):
        # returns remote rows
        return [
            {"issue_id": "JIRA-101", "customer_name": "Acme Corp", "arr": 50000},
            {"issue_id": "JIRA-102", "customer_name": "Globex", "arr": 25000},
            {"issue_id": None, "customer_name": "Unassigned", "arr": 0},  # SQL NULL
        ]

    engine.register_source(source, executor=snowflake_worker)

    # Pushdown plan check
    frag = engine.plan_pushdown("snowflake_source", {"arr": 50000}, ["customer_name", "arr"])
    # values are bound parameters, never interpolated into SQL text
    assert frag.raw_query == "SELECT customer_name, arr FROM snowflake_source WHERE arr = %(p0)s"
    assert frag.parameters == {"p0": 50000}

    # Schema drift check
    drifted = engine.check_schema_drift("snowflake_source", "CREATE TABLE modified (id INT);")
    assert drifted is True

    # Federated join execution with Null and Set semantics
    local_jira_rows = [
        {"issue_id": "JIRA-101", "summary": "Fix login bug", "status": "OPEN"},
        {"issue_id": "JIRA-103", "summary": "New UI theme", "status": "IN_PROGRESS"},
    ]

    outcome = engine.execute_federated_join(
        local_rows=local_jira_rows,
        remote_source_id="snowflake_source",
        join_key_local="issue_id",
        join_key_remote="issue_id",
        semantics=SemanticsMode.SET,
    )

    assert outcome.status == "SUCCESS"
    assert outcome.total_rows == 2
    # JIRA-101 matched
    r101 = next(r for r in outcome.rows if r["issue_id"] == "JIRA-101")
    assert r101["remote_customer_name"] == "Acme Corp"
    # JIRA-103 had no remote match -> remote_issue_id is None (3-valued logic)
    r103 = next(r for r in outcome.rows if r["issue_id"] == "JIRA-103")
    assert r103["remote_issue_id"] is None

    # Partial source degradation test (source unavailable)
    source.is_available = False
    degraded_outcome = engine.execute_federated_join(
        local_rows=local_jira_rows,
        remote_source_id="snowflake_source",
        join_key_local="issue_id",
        join_key_remote="issue_id",
    )
    assert degraded_outcome.status == "PARTIAL"
    assert "snowflake_source" in degraded_outcome.degraded_sources
    assert len(degraded_outcome.rows) == 2


# ===========================================================================
# CRA-024.5: Scoped templates, history, cache & sensitive literal redaction
# ===========================================================================

@pytest.mark.req("CRA-024")
def test_cra_024_5_sensitive_redaction_and_scoped_cache():
    # Sensitive redaction
    raw_query = "SELECT * FROM Users WHERE token = 'super_secret_token_12345' AND password = 'my_password'"
    clean_query = redact_sensitive_literals(raw_query)
    assert "super_secret_token_12345" not in clean_query
    assert "my_password" not in clean_query
    assert "[REDACTED]" in clean_query

    # Scoped query manager
    manager = ScopedQueryManager()
    manager.save_template("tenant_A", "user_query", raw_query)
    # Redacted template
    tmpl = manager.get_template("tenant_A", "user_query")
    assert "[REDACTED]" in tmpl
    # Tenant B cannot see Tenant A template
    assert manager.get_template("tenant_B", "user_query") is None

    # Scoped history
    rec = manager.record_history("tenant_A", "user_1", raw_query, dialect="SQL", execution_time_ms=12.5)
    assert "[REDACTED]" in rec.query_text_redacted
    assert len(manager.get_history("tenant_A")) == 1
    assert len(manager.get_history("tenant_B")) == 0

    # Scoped cache with intermediate fact stripping
    manager.cache_result(
        "tenant_A",
        "SELECT 1",
        {"data": [1], "_intermediate_eval_facts": "hidden_private_state"},
    )
    cached = manager.get_cached_result("tenant_A", "SELECT 1")
    assert cached is not None
    assert "_intermediate_eval_facts" not in cached
    assert manager.get_cached_result("tenant_B", "SELECT 1") is None


# ===========================================================================
# CRA-024.6: Warmed endpoint benchmarks & semantic equivalence
# ===========================================================================

@pytest.mark.req("CRA-024")
def test_cra_024_6_warmed_benchmarks_and_equivalence():
    bench = WarmedEndpointBenchmark(warmup_runs=3, measured_runs=10)

    def cold_setup():
        time.sleep(0.01)

    def query_op():
        time.sleep(0.001)
        return {"result": 42}

    report = bench.run_benchmark("endpoint_test", query_op, cold_setup_fn=cold_setup)
    assert report.warmed is True
    assert report.metrics.cold_startup_ms >= 10.0
    assert report.metrics.p50_ms < report.metrics.cold_startup_ms
    assert report.metrics.p95_ms >= report.metrics.p50_ms

    # Semantic equivalence comparator
    comp = SemanticEquivalenceComparator()
    mat_rows = [
        {"canonical_id": "WI-1", "name": "Auth", "status": "DONE"},
        {"canonical_id": "WI-2", "name": "UI", "status": "OPEN"},
    ]
    virt_rows = [
        {"canonical_id": "WI-1", "name": "Auth", "status": "DONE"},
        {"canonical_id": "WI-2", "name": "UI", "status": "OPEN"},
    ]
    res = comp.compare(mat_rows, virt_rows)
    assert res["equivalent"] is True

    virt_rows_drift = [
        {"canonical_id": "WI-1", "name": "Auth", "status": "DONE"},
        {"canonical_id": "WI-2", "name": "UI", "status": "BLOCKED"},
    ]
    res_drift = comp.compare(mat_rows, virt_rows_drift)
    assert res_drift["equivalent"] is False
    assert res_drift["discrepancies_count"] == 1


# ===========================================================================
# CRA-024.7: SPARQL 1.1 Protocol endpoint GET/POST & unbounded path rejection
# ===========================================================================

@pytest.mark.req("CRA-024")
def test_cra_024_7_sparql_protocol():
    from eoip.query.sparql_backend import RdflibSparqlBackend

    rdf = RdflibSparqlBackend()
    rdf.load_turtle("<urn:i1> a <http://example.org/Item> ; <urn:p> <urn:o> .")
    handler = SparqlProtocolHandler(rdf_backend=rdf, enable_updates=False)
    # without a backend there is no fabricated result
    assert SparqlProtocolHandler().handle_request(method="GET", query_params={"query": "ASK { ?s ?p ?o }"})[0] == 503

    # 1. GET /sparql query with application/sparql-results+json
    status, headers, body = handler.handle_request(
        method="GET",
        query_params={"query": "SELECT ?s ?p ?o WHERE { ?s ?p ?o } LIMIT 10"},
        headers={"Accept": "application/sparql-results+json"},
    )
    assert status == 200
    assert "application/sparql-results+json" in headers["Content-Type"]
    data = json.loads(body)
    assert "head" in data and "results" in data

    # 2. POST /sparql with XML
    status_xml, headers_xml, body_xml = handler.handle_request(
        method="POST",
        headers={"Content-Type": "application/sparql-query", "Accept": "application/sparql-results+xml"},
        body="SELECT ?s WHERE { ?s a <http://example.org/Item> }",
    )
    assert status_xml == 200
    assert "application/sparql-results+xml" in headers_xml["Content-Type"]
    assert "<sparql" in body_xml

    # 3. ASK query
    status_ask, _, body_ask = handler.handle_request(
        method="GET",
        query_params={"query": "ASK { ?s ?p ?o }"},
        headers={"Accept": "application/sparql-results+json"},
    )
    assert status_ask == 200
    assert json.loads(body_ask).get("boolean") is True

    # 4. Updates rejected: the endpoint is read-only (D-CRA-024-02: 400 per the SPARQL 1.1 Protocol)
    status_upd, _, _ = handler.handle_request(
        method="POST",
        headers={"Content-Type": "application/sparql-update"},
        body="INSERT DATA { <urn:s> <urn:p> <urn:o> }",
    )
    assert status_upd == 400

    # 5. Unbounded property path strictly rejected with 422 UNSUPPORTED_CAPABILITY
    status_path, _, body_path = handler.handle_request(
        method="GET",
        query_params={"query": "SELECT * WHERE { ?s :knows* ?o }"},
    )
    assert status_path == 422
    assert "UNBOUNDED_PROPERTY_PATH" in body_path


# ===========================================================================
# CRA-024.8: Optional adapters: ANSI SQL views, openCypher, GraphQL
# ===========================================================================

@pytest.mark.req("CRA-024")
def test_cra_024_8_optional_adapters():
    # 1. ANSI SQL adapter
    sql_adapter = SQLOntologyAdapter()
    sql_rows = sql_adapter.execute_sql("SELECT canonical_id, name FROM WorkItem WHERE status = 'ACTIVE' LIMIT 5")
    assert len(sql_rows) > 0
    assert "canonical_id" in sql_rows[0]

    # Rejection of unsupported DDL
    with pytest.raises(UnsupportedCapabilityError):
        sql_adapter.execute_sql("TRUNCATE TABLE WorkItem")

    # 2. openCypher adapter
    cypher_adapter = OpenCypherAdapter()
    cypher_rows = cypher_adapter.execute_cypher("MATCH (w:WorkItem) RETURN w LIMIT 3")
    assert len(cypher_rows) > 0

    # Rejection of unbounded Cypher path
    with pytest.raises(UnsupportedCapabilityError):
        cypher_adapter.execute_cypher("MATCH (a)-[*]->(b) RETURN a, b")

    # 3. GraphQL adapter
    graphql_adapter = GraphQLShapeAdapter()
    sdl = graphql_adapter.generate_schema_sdl()
    assert "type WorkItem" in sdl
    gql_res = graphql_adapter.execute_graphql("{ workItems { canonical_id name } }")
    assert "workItems" in gql_res["data"]

    # Rejection of ungoverned mutation
    with pytest.raises(UnsupportedCapabilityError):
        graphql_adapter.execute_graphql("mutation { deleteItem(id: 1) }")


# ===========================================================================
# CRA-024.9: Default budgets & tenant quotas
# ===========================================================================

@pytest.mark.req("CRA-024")
def test_cra_024_9_default_budgets():
    default_budget = QueryBudget()
    assert default_budget.deadline_seconds == 30.0
    assert default_budget.memory_bytes == 4 * 1024 * 1024 * 1024  # 4 GiB
    assert default_budget.max_rows_per_page == 10000
    assert default_budget.max_traversal_depth == 3

    # Tenant quota can lower limits
    strict_quota = QueryBudget(
        deadline_seconds=10.0,
        memory_bytes=1024 * 1024 * 1024,
        max_rows_per_page=500,
        max_traversal_depth=2,
    )
    clamped = default_budget.clamp_with_quota(strict_quota)
    assert clamped.deadline_seconds == 10.0
    assert clamped.max_rows_per_page == 500
    assert clamped.max_traversal_depth == 2

    # Quota trying to exceed default budget cannot raise limits
    high_quota = QueryBudget(
        deadline_seconds=120.0,
        memory_bytes=16 * 1024 * 1024 * 1024,
        max_rows_per_page=50000,
        max_traversal_depth=10,
    )
    clamped2 = default_budget.clamp_with_quota(high_quota)
    assert clamped2.deadline_seconds == 30.0
    assert clamped2.memory_bytes == 4 * 1024 * 1024 * 1024
    assert clamped2.max_rows_per_page == 10000
    assert clamped2.max_traversal_depth == 3


# ===========================================================================
# CRA-024.10: BI Connectivity (Tableau & Power BI recorded session)
# ===========================================================================

@pytest.mark.req("CRA-024")
def test_cra_024_10_bi_connectivity(tmp_path):
    """Drive Tableau-like and Power BI-like sessions against the real PostgreSQL-wire BI endpoint."""
    pytest.importorskip("duckdb")
    pytest.importorskip("pg8000.native")
    import secrets

    from eoip.authn.credentials import CredentialStore
    from eoip.graph.memory import MemoryGraphStore
    from eoip.query.pg_wire import PgWireServer, credential_store_authenticator

    g = MemoryGraphStore()
    a = g.upsert_vertex("Service", {"canonical_id": "svc:a", "name": "a", "status": "live"})
    b = g.upsert_vertex("Service", {"canonical_id": "svc:b", "name": "b", "status": "beta"})
    g.upsert_edge("DEPENDS_ON", a["vid"], b["vid"], {})
    creds = CredentialStore(tmp_path / "creds.json")
    pw = secrets.token_urlsafe(18)
    creds.create_user("bi", pw, ["analyst"], tenant_id="t1")
    with PgWireServer({"t1": g}.__getitem__, credential_store_authenticator(creds),
                      allow_insecure_loopback=True) as srv:
        driver = BISessionDriver("127.0.0.1", srv.port, "bi", pw, "t1")
        tableau_session = driver.run_bi_session(tool_name="Tableau")
        pbi_session = driver.run_bi_session(tool_name="Power BI")
        legacy = BISessionEmulator(sql_adapter=driver).run_bi_session(tool_name="Tableau")
        assert [q.query_text for q in legacy.queries] == [q.query_text for q in tableau_session.queries]
        with pytest.raises(RuntimeError, match="no BI endpoint configured"):
            BISessionEmulator().run_bi_session()  # never fabricates a session without a server
        refused = BISessionDriver("127.0.0.1", srv.port, "bi", "wrong-" + pw, "t1")
        with pytest.raises(Exception, match="28P01|password"):
            refused.run_bi_session(tool_name="Tableau")
    assert tableau_session.connected is True
    assert len(tableau_session.queries) == 5
    assert tableau_session.metadata["server_version"].startswith("14.0")
    query_texts = [q.query_text for q in tableau_session.queries]
    assert "SELECT 1" in query_texts[0]
    assert "information_schema.tables" in query_texts[2]
    assert all(q.status_code == 200 for q in tableau_session.queries), tableau_session.queries
    # Row counts come from the server: one label (Service, 2 rows) in the aggregate.
    assert tableau_session.queries[-1].response_rows_count == 1
    assert all(q.status_code == 200 for q in pbi_session.queries), pbi_session.queries
    assert pbi_session.queries[-1].response_rows_count == 1  # one relation type: DEPENDS_ON


# ===========================================================================
# CRA-024.11: RDF backend port (Fuseki reference & GraphDB certified)
# ===========================================================================

@pytest.mark.req("CRA-024")
def test_cra_024_11_rdf_backend_ports():
    # 1. Fuseki config targeting
    fuseki_config = {
        "backend": "fuseki",
        "endpoint_url": "http://localhost:3030/ds",
        "dataset": "ds",
        "timeout": 30.0,
    }
    fuseki_store = create_rdf_store_from_config(fuseki_config)
    assert isinstance(fuseki_store, FusekiGraphStore)
    assert fuseki_store.dataset == "ds"
    assert fuseki_store.query_url == "http://localhost:3030/ds/sparql"

    # 2. GraphDB config targeting
    graphdb_config = {
        "backend": "graphdb",
        "endpoint_url": "http://customer-graphdb:7200",
        "repository": "enterprise_repo",
        "timeout": 30.0,
    }
    graphdb_store = create_rdf_store_from_config(graphdb_config)
    assert isinstance(graphdb_store, GraphDBGraphStore)
    assert graphdb_store.dataset == "enterprise_repo"
    assert "enterprise_repo" in graphdb_store.query_url

    assert graphdb_store.update_url.endswith("/repositories/enterprise_repo/statements")
    # CRUD round trips on live Fuseki and GraphDB Free: tests/query/test_rdf_store_backends.py (CI job rdf-stores)


# ===========================================================================
# CRA-024.A: Full Acceptance: Independent Result Corpus, SP2Bench, Federated Join
# ===========================================================================

@pytest.mark.req("CRA-024")
def test_cra_024_a_acceptance_oracle():
    service = QueryService()
    scope = TrustedScope(tenant_id="tenant_prod", principal_id="auditor_lead")

    # 1. Independent result corpus: optional/join/null/cardinality/path/aggregate/order/limit
    corpus = [
        ("SELECT canonical_id FROM WorkItem ORDER BY name LIMIT 10", "EOQL"),
        ("SELECT * FROM WorkItem JOIN MEMBER_OF", "EOQL"),
        ("TRAVERSE FROM urn:eoip:item:1 VIA BLOCKED_BY DEPTH 2", "EOQL"),
    ]
    for q_text, dialect in corpus:
        res = service.execute(q_text, dialect=dialect, scope=scope)
        assert res.status == "COMPLETED"
        assert res.profile.elapsed_ms < 30000.0  # within 30 s deadline

    # 2. SP2Bench in-scope query simulation under 30s
    sp2bench_q = "SELECT ?article ?title WHERE { ?article a <http://localhost/vocabulary/bench/Article> . ?article <http://purl.org/dc/elements/1.1/title> ?title } LIMIT 100"
    # (single SP2Bench-shaped query on a real engine; the in-scope SP2Bench set remains open, CRA-024.A.2)
    from eoip.query.sparql_backend import RdflibSparqlBackend

    rdf = RdflibSparqlBackend()
    rdf.load_turtle("\n".join(
        f"<urn:a{i}> a <http://localhost/vocabulary/bench/Article> ; <http://purl.org/dc/elements/1.1/title> \"T{i}\" ."
        for i in range(200)))
    handler = SparqlProtocolHandler(rdf_backend=rdf)
    t0 = time.perf_counter()
    status, _, body = handler.handle_request("GET", query_params={"query": sp2bench_q})
    elapsed = time.perf_counter() - t0
    assert status == 200 and len(json.loads(body)["results"]["bindings"]) == 100
    assert elapsed < 30.0

    # 3. Federated Jira x Snowflake join execution
    obda = OBDAFederationEngine()
    obda.register_source(
        FederatedDataSource(
            source_id="snowflake_billing",
            source_type="SNOWFLAKE",
            schema_hash="hash_snow_1",
            watermark_timestamp=time.time(),
        ),
        executor=lambda frag: [
            {"jira_key": "PROJ-1", "cost_usd": 1250.0},
            {"jira_key": "PROJ-2", "cost_usd": 3400.0},
        ],
    )
    local_jira = [
        {"jira_key": "PROJ-1", "title": "Database migration"},
        {"jira_key": "PROJ-2", "title": "Cache layer upgrade"},
    ]
    fed_res = obda.execute_federated_join(
        local_rows=local_jira,
        remote_source_id="snowflake_billing",
        join_key_local="jira_key",
        join_key_remote="jira_key",
    )
    assert fed_res.status == "SUCCESS"
    assert fed_res.total_rows == 2
    assert fed_res.rows[0]["remote_cost_usd"] == 1250.0
