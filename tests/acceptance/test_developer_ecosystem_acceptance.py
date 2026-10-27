"""Acceptance test suite for Public APIs, SDKs, MCP, and Developer Ecosystem (WP-039, CRA-039.1-039.8, CRA-039.A)."""

from __future__ import annotations

from _principals import provision_api_token
import json
from pathlib import Path
import pytest
from starlette.testclient import TestClient

from apps.api.main import create_app
from eoip.actions.contracts import ActionIntent, ActionState, RiskClass
from eoip.actions.engine import ActionEngine
from eoip.capabilities.model import CapabilityState
from eoip.graph.memory import MemoryGraphStore
from eoip.ontology.doc_generator import WidocoOntologyDocGenerator
from eoip.ontology.manifest import PROPERTY_KEYS, VERTEX_LABELS
from eoip.plugins.conformance import (
    ConnectorPluginTemplate,
    PluginConformanceRunner,
    SUPPORTED_PLATFORM_VERSIONS,
)
from eoip.plugins.sdk import PluginBase, PluginCapability, PluginManifest, PluginPermission, PluginStatus
from eoip.policies.ecosystem_policies import (
    CustomerContentSanitizer,
    CustomerDataLeakViolationError,
    EcosystemPolicyRegistry,
)
from eoip.sdk.openapi_generator import OpenAPIGenerator
from eoip.sdk.package_verifier import PackageNameVerifier
from eoip.sdk.python_client import EOIPClient, NotFoundError
from eoip.sdk.typescript_client import TypeScriptSDKGenerator
from eoip.sdk.versioning import APIVersionManager, VersionStatus
from eoip.tools_contract.mcp_server import (
    EOIPMCPServer,
    MCPBudgetExceededError,
    MCPIdentityViolationError,
)


@pytest.fixture
def populated_store():
    store = MemoryGraphStore()
    v1 = store.upsert_vertex("Project", {"canonical_id": "proj:apollo", "name": "Apollo Knowledge Platform"})
    v2 = store.upsert_vertex("WorkItem", {"canonical_id": "item:101", "name": "Implement MCP Server", "issue_key": "APOLLO-101"})
    store.upsert_edge("CONTAINS", v1["vid"], v2["vid"], {})
    return store


# ===========================================================================
# CRA-039.1: OpenAPI schema generation, route isolation & versioning
# ===========================================================================

@pytest.mark.req("CRA-039")
def test_cra_039_1_openapi_schema_generation_and_route_isolation():
    generator = OpenAPIGenerator()
    public_spec = generator.generate_public_contract(public_version="v1")

    # 1. Public routes are present
    assert "/api/v1/search" in public_spec["paths"]
    assert "/api/v1/entities/{canonical_id}" in public_spec["paths"]
    assert "/api/v1/query" in public_spec["paths"]

    # 2. Internal / admin routes are stripped
    assert "/admin/ingestion/trigger" not in public_spec["paths"]
    assert "/internal/debug/health" not in public_spec["paths"]

    # 3. Standard error and event schemas are present
    assert "StandardError" in public_spec["components"]["schemas"]
    assert "SourceEvent" in public_spec["components"]["schemas"]
    assert "GraphMutationEvent" in public_spec["components"]["schemas"]
    assert "GovernedAuditEvent" in public_spec["components"]["schemas"]

    # 4. Independent API versioning manager
    ver_mgr = APIVersionManager()
    v1_meta = ver_mgr.get_version("v1")
    assert v1_meta is not None
    headers = v1_meta.get_response_headers()
    assert headers["X-API-Version"] == "v1"
    assert headers["Deprecation"] == "true"
    assert "Sunset" in headers

    # 5. Digest derivation
    digest = generator.digest("v1")
    assert len(digest) == 64


# ===========================================================================
# CRA-039.2: MCP typed contracts, budgets & identity defense
# ===========================================================================

@pytest.mark.req("CRA-039")
def test_cra_039_2_mcp_typed_contracts_budgets_and_identity_defense(populated_store):
    server = EOIPMCPServer(graph_store=populated_store)

    # 1. Inspect tool contracts
    tools = server.list_tools()
    tool_names = {t["name"] for t in tools}
    assert "ontology_list_classes" in tool_names
    assert "graph_search" in tool_names
    assert "action_propose" in tool_names

    for t in tools:
        assert "inputSchema" in t
        assert "outputSchema" in t
        assert t["inputSchema"]["type"] == "object"

    # 2. Budget enforcement
    with pytest.raises(MCPBudgetExceededError) as exc_budget:
        server.invoke_tool(
            "graph_search",
            {"query": "Apollo", "limit": 99999},  # exceeds max 100 limit
            caller_identity={"user_id": "analyst-1", "tenant_id": "tenant-a"},
        )
    assert "exceeds tool budget" in str(exc_budget.value)

    # 3. Security invariant: natural language argument cannot alter trusted identity
    with pytest.raises(MCPIdentityViolationError) as exc_id:
        server.invoke_tool(
            "graph_search",
            {"query": "Apollo", "limit": 10, "tenant_id": "foreign-tenant", "override_role": "admin"},
            caller_identity={"user_id": "analyst-1", "tenant_id": "tenant-a"},
        )
    assert "cannot alter trusted identity" in str(exc_id.value)

    # 4. Provenance tracking on successful invocation
    res = server.invoke_tool(
        "graph_search",
        {"query": "Apollo", "limit": 10},
        caller_identity={"user_id": "analyst-1", "tenant_id": "tenant-a"},
    )
    assert "provenance" in res
    prov = res["provenance"]
    assert prov["caller_id"] == "analyst-1"
    assert prov["tenant_id"] == "tenant-a"
    assert len(prov["input_hash"]) == 64
    assert len(prov["output_hash"]) == 64


# ===========================================================================
# CRA-039.3: Plugin/connector templates, conformance runner & qualification
# ===========================================================================

@pytest.mark.req("CRA-039")
def test_cra_039_3_plugin_conformance_runner_and_qualification_process():
    # 1. Scaffolding template
    scaffold = ConnectorPluginTemplate.generate_scaffold("custom_jira", "Custom Jira Connector")
    assert "manifest.py" in scaffold
    assert "connector.py" in scaffold

    # 2. Conformance runner with certified maintainers
    runner = PluginConformanceRunner(certified_maintainers={"EOIP-Core-Team"})

    # Sample compliant plugin
    class CompliantPlugin(PluginBase):
        def activate(self) -> None:
            self._status = PluginStatus.ACTIVE

        def deactivate(self) -> None:
            self._status = PluginStatus.UNLOADED

    # Test community unqualified plugin
    community_manifest = PluginManifest(
        plugin_id="plugin.community.crm",
        name="Community CRM",
        version="1.0.0",
        author="External-Dev",
        description="A community plugin",
        capabilities=[PluginCapability.CONNECTOR],
        entry_point="crm:Plugin",
        permissions=[PluginPermission(resource="network", scope="https://api.crm.com", granted=True)],
        min_platform_version="1.0.0",
    )

    report1 = runner.run_conformance(CompliantPlugin, community_manifest)
    assert report1.passed is True
    # Uncertified community modules remain visibly UNQUALIFIED
    assert report1.qualification_state == CapabilityState.SUPPORTED_UNQUALIFIED

    # Test certified partner plugin
    certified_manifest = PluginManifest(
        plugin_id="plugin.certified.crm",
        name="Certified CRM",
        version="1.0.0",
        author="EOIP-Core-Team",
        description="Certified plugin",
        capabilities=[PluginCapability.CONNECTOR],
        entry_point="crm:Plugin",
        permissions=[PluginPermission(resource="network", scope="https://api.crm.com", granted=True)],
        min_platform_version="1.0.0",
    )
    report2 = runner.run_conformance(CompliantPlugin, certified_manifest)
    assert report2.passed is True
    assert report2.qualification_state == CapabilityState.SUPPORTED_QUALIFIED

    # Test broken plugin (unauthorized permission resource)
    bad_manifest = PluginManifest(
        plugin_id="plugin.bad",
        name="Bad Plugin",
        version="1.0.0",
        author="Unknown",
        description="Bad",
        capabilities=[PluginCapability.CONNECTOR],
        entry_point="bad:Plugin",
        permissions=[PluginPermission(resource="root_filesystem_escape", scope="/", granted=True)],
        min_platform_version="1.0.0",
    )
    report3 = runner.run_conformance(CompliantPlugin, bad_manifest)
    assert report3.passed is False
    assert report3.qualification_state == CapabilityState.UNSUPPORTED

    # Supported platform versions table
    assert "1.0.0" in SUPPORTED_PLATFORM_VERSIONS
    assert "1.2.0" in SUPPORTED_PLATFORM_VERSIONS


# ===========================================================================
# CRA-039.4: Offline ontology doc generation & content sanitization
# ===========================================================================

@pytest.mark.req("CRA-039")
def test_cra_039_4_offline_doc_generation_and_sanitization():
    generator = WidocoOntologyDocGenerator(
        title="EOIP Enterprise Ontology Specification",
        release_digest="9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08",
    )

    # Injected XSS vector and secret
    malicious_descriptions = {
        "Project": "Core project <script>alert('xss')</script> entity with auth Bearer 1234567890abcdef1234567890abcdef and <img src=x onerror='hack()'>",
    }

    html = generator.generate_html(custom_descriptions=malicious_descriptions)

    # 1. Sanitization verification: script tag and event handler stripped
    assert "<script>" not in html
    assert "alert('xss')" not in html
    assert "onerror=" not in html

    # 2. Secret token redacted
    assert "1234567890abcdef1234567890abcdef" not in html
    assert "[REDACTED_SECRET]" in html

    # 3. Offline no-egress: zero external scripts or css sheets
    assert "http://" not in html.lower()
    assert "https://" not in html.replace("https://ontology.eoip.io", "").lower()

    # 4. WIDOCO/LODE clean-room attribution
    assert "Widoco" in html or "WIDOCO" in html
    assert "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08" in html


# ===========================================================================
# CRA-039.5: Contribution, vulnerability disclosure & anti-leak policy
# ===========================================================================

@pytest.mark.req("CRA-039")
def test_cra_039_5_ecosystem_policies_and_customer_data_leak_guard():
    # 1. Policies inspection
    policies = EcosystemPolicyRegistry.get_all_policies()
    policy_ids = {p["policy_id"] for p in policies}
    assert "POL-CONTRIB-001" in policy_ids
    assert "POL-CVD-001" in policy_ids
    assert "POL-MKT-OWN-001" in policy_ids

    cvd = next(p for p in policies if p["policy_id"] == "POL-CVD-001")
    assert cvd["embargo_days"] == 90
    assert "security@eoip.internal" in cvd["contact"]

    # 2. Customer content sanitizer
    clean_sample = "Acme Corp demo configuration using https://example.com/api with user demo@example.com"
    assert CustomerContentSanitizer.validate_public_example(clean_sample) is True

    # Real customer tenant indicator should raise
    with pytest.raises(CustomerDataLeakViolationError):
        CustomerContentSanitizer.validate_public_example("Setup example for tenant_id: cust_ford_motor_co")

    # Real connection string with password should raise
    with pytest.raises(CustomerDataLeakViolationError):
        CustomerContentSanitizer.validate_public_example("connect to postgres://dbadmin:p@ssw0rd123@prod.internal.corp:5432/main")


# ===========================================================================
# CRA-039.6: Python and TypeScript SDKs, and package naming
# ===========================================================================

@pytest.mark.req("CRA-039")
def test_cra_039_6_python_and_typescript_sdks_and_package_naming(tmp_path):
    # 1. Package Name & Trademark Verification
    pypi_check = PackageNameVerifier.verify_pypi_name("eoip-python")
    assert pypi_check.passed is True

    trademark_violation = PackageNameVerifier.verify_pypi_name("eoip-snowflake-adapter")
    assert trademark_violation.passed is False
    assert "trademark collision" in trademark_violation.rejection_reason

    npm_check = PackageNameVerifier.verify_npm_name("@eoip/sdk-typescript")
    assert npm_check.passed is True

    # 2. TypeScript SDK generator
    sdk_files = TypeScriptSDKGenerator.generate_bundle(tmp_path / "ts-sdk")
    assert "package.json" in sdk_files
    assert "src/client.ts" in sdk_files
    assert "src/types.ts" in sdk_files
    pkg_json = json.loads((tmp_path / "ts-sdk" / "package.json").read_text())
    assert pkg_json["name"] == "@eoip/sdk-typescript"

    # 3. Python SDK client typed invocation with mock transport
    def mock_handler(request):
        import httpx
        if request.url.path == "/api/v1/search":
            return httpx.Response(200, json={"results": [{"canonical_id": "proj:apollo"}]})
        elif request.url.path == "/api/v1/entities/proj:missing":
            return httpx.Response(404, json={"error": {"code": "NOT_FOUND", "message": "Entity not found"}})
        return httpx.Response(200, json={"status": "ok"})

    transport = pytest.importorskip("httpx").MockTransport(mock_handler)
    client = EOIPClient(base_url="http://mock-api", api_token="test-token", transport=transport)

    results = client.search("Apollo")
    assert len(results) == 1
    assert results[0]["canonical_id"] == "proj:apollo"

    with pytest.raises(NotFoundError):
        client.get_entity("proj:missing")
    client.close()


# ===========================================================================
# CRA-039.7: MCP server exposing ontology, graph & governed actions (ONT-011)
# ===========================================================================

@pytest.mark.req("CRA-039")
def test_cra_039_7_mcp_server_ontology_graph_and_governed_actions(populated_store):
    action_engine = ActionEngine(write_back_enabled=True)
    server = EOIPMCPServer(graph_store=populated_store, action_engine=action_engine)

    # 1. Ontology tools
    res_classes = server.invoke_tool("ontology_list_classes", {})
    assert "Project" in res_classes["result"]["classes"]
    assert "WORK" in res_classes["result"]["domains"]

    res_schema = server.invoke_tool("ontology_get_schema", {"label": "Project"})
    assert res_schema["result"]["valid"] is True

    # 2. Graph retrieval tool
    res_entity = server.invoke_tool("graph_get_entity", {"canonical_id": "proj:apollo"})
    assert res_entity["result"]["found"] is True
    assert res_entity["result"]["entity"]["canonical_id"] == "proj:apollo"

    # 3. Governed Actions through MCP: read-only action auto-approves
    res_ro = server.invoke_tool(
        "action_propose",
        {
            "action_type_id": "act_lookup_readonly",
            "idempotency_key": "idemp-lookup-1234567890",
            "arguments": {"target": "proj:apollo"},
        },
    )
    assert res_ro["result"]["state"] == ActionState.APPROVED.value

    # 4. Governed Actions through MCP: destructive/write action is STAGED for approval
    res_write = server.invoke_tool(
        "action_propose",
        {
            "action_type_id": "act_jira_create_issue",
            "idempotency_key": "idemp-create-issue-1234567890",
            "arguments": {"project": "APOLLO", "summary": "Urgent DB migration"},
        },
    )
    assert res_write["result"]["state"] == ActionState.STAGED.value
    assert res_write["result"]["requires_approval"] is True


# ===========================================================================
# CRA-039.8: Widoco-class HTML ontology documentation generator & route (ONT-014)
# ===========================================================================

@pytest.mark.req("CRA-039")
def test_cra_039_8_widoco_html_ontology_docs_and_route_serving(monkeypatch, tmp_path):
    # 1. Generator validation
    generator = WidocoOntologyDocGenerator()
    html = generator.generate_html()

    assert "Enterprise Ontology &amp; Intelligence Platform Specification" in html
    assert "Ontology Version:" in html
    assert "#classes" in html
    assert "#properties" in html
    assert "#overview" in html
    assert "#provenance" in html

    # Verify all VERTEX_LABELS are present
    for label in VERTEX_LABELS:
        assert f"Class: {label}" in html

    # 2. HTTP route serving at GET /ontology/docs
    monkeypatch.setenv("EOIP_API_TOKEN", "x" * 32)
    provision_api_token(monkeypatch, "x" * 32)
    monkeypatch.setenv("EOIP_ENV", "test")
    monkeypatch.setenv("EOIP_DATA_ROOT", str(tmp_path))
    monkeypatch.setenv("EOIP_GRAPH_BACKEND", "memory")
    app = create_app()
    client = TestClient(app)

    resp = client.get("/ontology/docs")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]
    assert "Enterprise Ontology &amp; Intelligence Platform Specification" in resp.text
    assert generator.release_digest in resp.text

    # Also test /api/v1/ontology/docs alias
    resp_alias = client.get("/api/v1/ontology/docs")
    assert resp_alias.status_code == 200


# ===========================================================================
# CRA-039.A: Integrated Developer Ecosystem Acceptance
# ===========================================================================

@pytest.mark.req("CRA-039")
def test_cra_039_a_developer_ecosystem_acceptance_integrated(tmp_path, populated_store):
    # 1. Independently build client and sample plugin from released schemas/templates
    scaffold = ConnectorPluginTemplate.generate_scaffold("sample_cmdb", "Sample CMDB Connector")
    assert "manifest.py" in scaffold
    plugin_manifest = PluginManifest(
        plugin_id="sample_cmdb",
        name="Sample CMDB",
        version="1.0.0",
        author="External-Dev",
        description="Sample CMDB plugin",
        capabilities=[PluginCapability.CONNECTOR],
        entry_point="cmdb:Plugin",
        permissions=[PluginPermission(resource="network", scope="https://cmdb.local", granted=True)],
        min_platform_version="1.0.0",
    )

    class SamplePlugin(PluginBase):
        def activate(self):
            self._status = PluginStatus.ACTIVE
        def deactivate(self):
            self._status = PluginStatus.UNLOADED

    runner = PluginConformanceRunner()
    conf_report = runner.run_conformance(SamplePlugin, plugin_manifest)
    assert conf_report.passed is True
    assert conf_report.qualification_state == CapabilityState.SUPPORTED_UNQUALIFIED

    # 2. External agent (Claude/LangGraph client simulation) queries the MCP server
    action_engine = ActionEngine(write_back_enabled=True)
    mcp_server = EOIPMCPServer(graph_store=populated_store, action_engine=action_engine)

    # External agent answers business question: "What is the entity for Project Apollo?"
    search_res = mcp_server.invoke_tool(
        "graph_search",
        {"query": "Apollo Knowledge Platform", "limit": 5},
        caller_identity={"user_id": "claude-subagent-1", "tenant_id": "tenant-enterprise"},
    )
    assert search_res["result"]["count"] >= 1
    found_entity = search_res["result"]["results"][0]
    assert found_entity["canonical_id"] == "proj:apollo"

    # 3. External agent attempts a destructive / write action via MCP -> held for human approval
    staged_action = mcp_server.invoke_tool(
        "action_propose",
        {
            "action_type_id": "act_jira_create_issue",
            "idempotency_key": "idemp-agent-destruct-1234567890",
            "arguments": {"project": "APOLLO", "summary": "Delete production index"},
        },
        caller_identity={"user_id": "claude-subagent-1", "tenant_id": "tenant-enterprise"},
    )
    assert staged_action["result"]["state"] == ActionState.STAGED.value
    assert staged_action["result"]["requires_approval"] is True

    # 4. Compare generated docs with actual runtime artifact digest
    doc_gen = WidocoOntologyDocGenerator()
    runtime_html = doc_gen.generate_html()
    assert doc_gen.release_digest in runtime_html
