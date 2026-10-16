"""Unit tests for WP 5.2: Ontology GitOps and Marketplace (GAP-GITOPS-002..008, GAP-MKT-002..008)."""

from __future__ import annotations

import json
import pytest

from eoip.graph.memory import MemoryGraphStore
from eoip.marketplace import (
    CapabilityKind,
    DependencyConflict,
    DependencyResolver,
    IntegrityError,
    PackageDependency,
    PackageInstaller,
    PackageManifest,
    PackageReader,
    PackageRegistry,
    build_package,
    default_install_key,
    package_agent_workflow,
    package_connector_mapping,
    package_dashboard,
    package_query_template,
    package_validation_rules,
    sign,
    sign_package_archive,
    verify_signature,
)
from eoip.ontology.gitops import (
    ADDITIVE,
    BREAKING,
    POTENTIALLY_BREAKING,
    OntologyGitOpsWorkflow,
    OntologyImpactReport,
    OntologyMigrationPlan,
    OntologyVersionStore,
    RollbackReceipt,
    SemanticDiff,
    compute_next_semver,
    current_manifest_snapshot,
    diff_manifests,
    generate_ontology_migration_script,
    package_ontology_release,
    rollback_ontology_version,
    run_ontology_impact_analysis,
    validate_ontology_change,
)

KEY = b"wp52-test-install-key"


def _make_base_manifest():
    return {
        "vertex_labels": {
            "Service": {"domain": "SYSTEM", "required": ["canonical_id"], "optional": ["name", "status"]},
            "WorkItem": {"domain": "WORK", "required": ["canonical_id"], "optional": ["title"]},
        },
        "edge_labels": {
            "DEPENDS_ON": {"out": ["Service"], "in": ["Service"]},
        },
        "property_keys": {
            "canonical_id": "STRING",
            "name": "STRING",
            "status": "STRING",
            "title": "STRING",
        },
    }


# ---------------------------------------------------------------------------
# GAP-GITOPS-002: Ontology branch, PR, review and merge workflows
# ---------------------------------------------------------------------------

@pytest.mark.req("GAP-GITOPS-002")
def test_gitops_branch_pr_review_merge_workflow():
    workflow = OntologyGitOpsWorkflow(base_snapshot=_make_base_manifest())
    assert "main" in workflow.list_branches()

    # 1. Create feature branch
    branch_info = workflow.create_branch("feature/add-epic", base_branch="main")
    assert branch_info["branch"] == "feature/add-epic"
    assert "feature/add-epic" in workflow.list_branches()

    # 2. Commit update to branch
    updated_manifest = _make_base_manifest()
    updated_manifest["vertex_labels"]["Epic"] = {
        "domain": "WORK",
        "required": ["canonical_id"],
        "optional": ["title"],
    }
    commit_res = workflow.commit_manifest(
        "feature/add-epic",
        updated_manifest,
        commit_message="Add Epic vertex label",
        author="alice@example.com",
    )
    assert commit_res["branch"] == "feature/add-epic"
    assert commit_res["diff_summary"]["additive"] > 0

    # 3. Create Pull Request
    pr = workflow.create_pull_request(
        title="Add Epic domain entity",
        source_branch="feature/add-epic",
        target_branch="main",
        author="alice",
    )
    assert pr.status == "open"
    assert len(workflow.list_pull_requests(status="open")) == 1

    # 4. Review Pull Request
    reviewed_pr = workflow.review_pull_request(
        pr.pr_id,
        reviewer="steward_bob",
        decision="approve",
        comment="Schema addition is valid and non-breaking",
    )
    assert reviewed_pr.status == "approved"

    # 5. Merge Pull Request
    merge_res = workflow.merge_pull_request(pr.pr_id, merger="ci_bot")
    assert merge_res["status"] == "MERGED"

    # Verify main branch now has Epic
    main_manifest = workflow.get_branch_manifest("main")
    assert "Epic" in main_manifest["vertex_labels"]


# ---------------------------------------------------------------------------
# GAP-GITOPS-003: Generate semantic diffs
# ---------------------------------------------------------------------------

@pytest.mark.req("GAP-GITOPS-003")
def test_gitops_generate_semantic_diffs():
    base = _make_base_manifest()
    mod = json.loads(json.dumps(base))

    # Additive: new optional vertex label and property
    mod["vertex_labels"]["Incident"] = {"domain": "INCIDENT", "required": ["canonical_id"], "optional": []}
    mod["property_keys"]["severity"] = "STRING"

    # Potentially breaking: new required property on Service
    mod["vertex_labels"]["Service"]["required"].append("tier")

    # Breaking: remove WorkItem
    del mod["vertex_labels"]["WorkItem"]

    diff = diff_manifests(base, mod)
    assert not diff.safe
    assert len(diff.breaking) == 1
    assert diff.breaking[0].change_type == "vertex_label_removed"
    assert diff.breaking[0].subject == "WorkItem"

    pot_breaking = diff.potentially_breaking
    assert any(c.change_type == "required_property_added" and "tier" in c.subject for c in pot_breaking)

    additive = diff.additive
    assert any(c.change_type == "vertex_label_added" and c.subject == "Incident" for c in additive)
    assert any(c.change_type == "property_key_added" and c.subject == "severity" for c in additive)

    diff_dict = diff.to_dict()
    assert diff_dict["safe"] is False
    assert diff_dict["counts"]["breaking"] == 1


# ---------------------------------------------------------------------------
# GAP-GITOPS-004: CI validates ontology before publishing
# ---------------------------------------------------------------------------

@pytest.mark.req("GAP-GITOPS-004")
def test_gitops_ci_validate_ontology_gate():
    base = _make_base_manifest()

    # Additive change passes CI gate
    additive = json.loads(json.dumps(base))
    additive["vertex_labels"]["Release"] = {"domain": "RELEASE", "required": ["canonical_id"], "optional": []}
    res_pass = validate_ontology_change(base, additive)
    assert res_pass["publishable"] is True
    assert res_pass["verdict"] == "PUBLISH_OK"

    # Breaking change fails CI gate
    breaking = json.loads(json.dumps(base))
    del breaking["vertex_labels"]["Service"]
    res_fail = validate_ontology_change(base, breaking)
    assert res_fail["publishable"] is False
    assert res_fail["verdict"] == "BREAKING_CHANGE_REFUSED"


# ---------------------------------------------------------------------------
# GAP-GITOPS-005: Run impact analysis for ontology changes
# ---------------------------------------------------------------------------

@pytest.mark.req("GAP-GITOPS-005")
def test_gitops_run_impact_analysis():
    store = MemoryGraphStore()
    store.upsert_vertex("Service", {"canonical_id": "srv-auth", "service_id": "auth-svc", "name": "Auth"})
    store.upsert_vertex("WorkItem", {"canonical_id": "wi-101", "issue_key": "PROJ-101", "summary": "Fix bug"})

    base = _make_base_manifest()
    new = json.loads(json.dumps(base))
    # Remove WorkItem (breaking) and add required 'env' property to Service
    del new["vertex_labels"]["WorkItem"]
    new["vertex_labels"]["Service"]["required"].append("env")

    diff = diff_manifests(base, new)
    queries = [
        {"name": "get_work_items", "text": "MATCH (w:WorkItem) RETURN w"},
        {"name": "get_services", "text": "MATCH (s:Service) RETURN s"},
    ]
    dashboards = [
        {"name": "Engineering Overview", "panels": [{"query": "MATCH (w:WorkItem) RETURN count(w)"}]},
    ]

    report = run_ontology_impact_analysis(
        diff,
        graph_store=store,
        registered_queries=queries,
        registered_dashboards=dashboards,
    )
    assert isinstance(report, OntologyImpactReport)
    assert report.affected_vertices_count > 0  # detected affected WorkItem and Service vertices
    assert "WorkItem" in report.affected_vertex_labels
    assert "get_work_items" in report.impacted_queries
    assert "Engineering Overview" in report.impacted_dashboards
    assert report.risk_level in ("HIGH", "CRITICAL")
    assert report.safe_to_proceed is False
    assert len(report.recommendations) > 0


# ---------------------------------------------------------------------------
# GAP-GITOPS-006: Generate migration scripts
# ---------------------------------------------------------------------------

@pytest.mark.req("GAP-GITOPS-006")
def test_gitops_generate_migration_scripts():
    base = _make_base_manifest()
    new = json.loads(json.dumps(base))
    del new["vertex_labels"]["WorkItem"]
    new["vertex_labels"]["Service"]["required"].append("tier")

    diff = diff_manifests(base, new)
    plan = generate_ontology_migration_script(
        diff,
        source_version="1.0.0",
        target_version="2.0.0",
        default_values={"tier": "tier-3"},
    )
    assert isinstance(plan, OntologyMigrationPlan)
    assert "WorkItem" in plan.cypher_script
    assert "tier" in plan.cypher_script
    assert "tier-3" in plan.cypher_script
    assert "def apply_migration" in plan.python_script
    assert len(plan.actions) >= 2


# ---------------------------------------------------------------------------
# GAP-GITOPS-007: Allow rollback to previous semantic version
# ---------------------------------------------------------------------------

@pytest.mark.req("GAP-GITOPS-007")
def test_gitops_rollback_to_previous_version():
    base = _make_base_manifest()
    v1_manifest = base
    v2_manifest = json.loads(json.dumps(base))
    v2_manifest["vertex_labels"]["Artifact"] = {"domain": "CODE", "required": ["canonical_id"], "optional": []}

    version_store = OntologyVersionStore("1.0.0", v1_manifest)
    version_store.publish_version("1.1.0", v2_manifest)
    assert version_store.active_version == "1.1.0"

    # Rollback to 1.0.0
    receipt = version_store.rollback_to_version("1.0.0", allow_breaking=True)
    assert isinstance(receipt, RollbackReceipt)
    assert receipt.success is True
    assert receipt.to_version == "1.0.0"
    assert version_store.active_version == "1.0.0"
    assert "Artifact" not in version_store.get_manifest("1.0.0")["vertex_labels"]

    # Also test standalone rollback helper
    hist = {"1.0.0": v1_manifest, "1.1.0": v2_manifest}
    res = rollback_ontology_version("1.1.0", "1.0.0", hist, allow_breaking=True)
    assert res.success is True
    assert res.to_version == "1.0.0"


# ---------------------------------------------------------------------------
# GAP-GITOPS-008: Package ontology releases using SemVer-like policy
# ---------------------------------------------------------------------------

@pytest.mark.req("GAP-GITOPS-008")
def test_gitops_package_ontology_release_semver_policy():
    base = _make_base_manifest()

    # Additive change triggers MINOR bump
    additive = json.loads(json.dumps(base))
    additive["vertex_labels"]["Team"] = {"domain": "ORG", "required": ["canonical_id"], "optional": []}
    diff_add = diff_manifests(base, additive)
    next_ver = compute_next_semver("1.0.0", diff_add)
    assert next_ver == "1.1.0"

    pkg_minor = package_ontology_release(additive, current_version="1.0.0", previous_manifest=base)
    assert pkg_minor["version"] == "1.1.0"
    assert pkg_minor["semver_type"] == "MINOR"
    assert "checksum_sha256" in pkg_minor

    # Breaking change triggers MAJOR bump
    breaking = json.loads(json.dumps(base))
    del breaking["vertex_labels"]["Service"]
    diff_break = diff_manifests(base, breaking)
    next_major = compute_next_semver("1.1.0", diff_break)
    assert next_major == "2.0.0"

    pkg_major = package_ontology_release(breaking, current_version="1.1.0", previous_manifest=base)
    assert pkg_major["version"] == "2.0.0"
    assert pkg_major["semver_type"] == "MAJOR"


# ---------------------------------------------------------------------------
# GAP-MKT-002: Package connector mappings
# ---------------------------------------------------------------------------

@pytest.mark.req("GAP-MKT-002")
def test_marketplace_package_connector_mappings():
    mapping_payload = {
        "connector": "jira",
        "rules": [
            {"source_field": "issue.key", "target_property": "canonical_id"},
            {"source_field": "issue.summary", "target_property": "title"},
        ],
    }
    archive_bytes = package_connector_mapping(
        name="jira-connector-pack",
        version="1.0.0",
        mapping_id="jira_to_workitem",
        mapping_payload=mapping_payload,
        description="Jira issue to WorkItem mapping",
    )
    assert len(archive_bytes) > 0

    reader = PackageReader(archive_bytes)
    manifest = reader.manifest()
    assert manifest.name == "jira-connector-pack"
    assert CapabilityKind.MAPPINGS in manifest.provides
    assert "jira_to_workitem" in manifest.provides[CapabilityKind.MAPPINGS]

    mappings = reader.get_mappings()
    assert any("jira_to_workitem" in k for k in mappings)
    assert "issue.summary" in json.dumps(mappings)


# ---------------------------------------------------------------------------
# GAP-MKT-003: Package query templates
# ---------------------------------------------------------------------------

@pytest.mark.req("GAP-MKT-003")
def test_marketplace_package_query_templates():
    query_text = "MATCH (s:Service)-[:DEPENDS_ON]->(d:Service) WHERE s.name = $svc RETURN d"
    archive_bytes = package_query_template(
        name="service-topology-queries",
        version="1.2.0",
        template_id="find_service_dependencies",
        query_text=query_text,
        description="Parameterized topology traversal query",
    )
    reader = PackageReader(archive_bytes)
    manifest = reader.manifest()
    assert manifest.name == "service-topology-queries"
    assert "find_service_dependencies" in manifest.provides[CapabilityKind.QUERY_TEMPLATES]

    templates = reader.get_query_templates()
    assert any("find_service_dependencies" in k for k in templates)
    assert "DEPENDS_ON" in list(templates.values())[0]


# ---------------------------------------------------------------------------
# GAP-MKT-004: Package validation rules
# ---------------------------------------------------------------------------

@pytest.mark.req("GAP-MKT-004")
def test_marketplace_package_validation_rules():
    rules = {
        "schema_checks": [
            {"entity": "Service", "require_edge": "OWNED_BY", "min_count": 1},
        ],
    }
    archive_bytes = package_validation_rules(
        name="production-readiness-rules",
        version="1.0.1",
        validator_id="service_ownership_validator",
        rules=rules,
        description="Enforces service ownership metadata",
    )
    reader = PackageReader(archive_bytes)
    manifest = reader.manifest()
    assert "service_ownership_validator" in manifest.provides[CapabilityKind.VALIDATORS]

    validators = reader.get_validators()
    assert any("service_ownership_validator" in k for k in validators)
    assert "require_edge" in list(validators.values())[0]


# ---------------------------------------------------------------------------
# GAP-MKT-005: Package agent workflows
# ---------------------------------------------------------------------------

@pytest.mark.req("GAP-MKT-005")
def test_marketplace_package_agent_workflows():
    workflow_spec = {
        "workflow_name": "incident_root_cause_analysis",
        "agent_roles": ["IncidentCorrelator", "TopologyInvestigator", "RemediationPlanner"],
        "max_iterations": 5,
    }
    archive_bytes = package_agent_workflow(
        name="incident-rca-workflow",
        version="2.0.0",
        workflow_id="incident_rca",
        workflow_spec=workflow_spec,
        description="Automated RCA triage loop",
    )
    reader = PackageReader(archive_bytes)
    manifest = reader.manifest()
    assert "incident_rca" in manifest.provides[CapabilityKind.AGENT_WORKFLOWS]

    workflows = reader.get_agent_workflows()
    assert any("incident_rca" in k for k in workflows)
    assert "TopologyInvestigator" in list(workflows.values())[0]


# ---------------------------------------------------------------------------
# GAP-MKT-006: Package dashboards
# ---------------------------------------------------------------------------

@pytest.mark.req("GAP-MKT-006")
def test_marketplace_package_dashboards():
    dashboard_spec = {
        "title": "Service Health & Blast Radius",
        "grid_columns": 12,
        "widgets": [
            {"type": "graph", "title": "Upstream Dependency Map", "w": 6, "h": 4},
            {"type": "kpi", "title": "Critical Incidents", "w": 6, "h": 2},
        ],
    }
    archive_bytes = package_dashboard(
        name="service-health-dashboard",
        version="1.0.0",
        dashboard_id="service_health",
        dashboard_spec=dashboard_spec,
        description="Ops monitoring layout",
    )
    reader = PackageReader(archive_bytes)
    manifest = reader.manifest()
    assert "service_health" in manifest.provides[CapabilityKind.DASHBOARDS]

    dashboards = reader.get_dashboards()
    assert any("service_health" in k for k in dashboards)
    assert "Upstream Dependency Map" in list(dashboards.values())[0]


# ---------------------------------------------------------------------------
# GAP-MKT-007: Dependency/version management
# ---------------------------------------------------------------------------

@pytest.mark.req("GAP-MKT-007")
def test_marketplace_dependency_and_version_management():
    registry = PackageRegistry()
    installer = PackageInstaller(registry, key=KEY)

    # 1. Install base package
    base_manifest = PackageManifest(
        id="urn:eoip:marketplace:package:core-ontology",
        name="core-ontology",
        version="1.4.0",
        description="Base schema library",
        provides={CapabilityKind.ONTOLOGIES: ["urn:eoip:ontology:core"]},
    )
    installer.install(build_package(base_manifest, {"core.ttl": b"# core"}))
    assert registry.is_installed("core-ontology")

    # 2. Install dependent package requiring >=1.0.0,<2.0.0
    app_manifest = PackageManifest(
        id="urn:eoip:marketplace:package:service-catalog-app",
        name="service-catalog-app",
        version="1.0.0",
        description="Catalog UI app",
        provides={CapabilityKind.DASHBOARDS: ["catalog_ui"]},
        dependencies=[PackageDependency(name="core-ontology", range=">=1.0.0,<2.0.0")],
    )
    installer.install(build_package(app_manifest, {"app.json": b"{}"}))
    assert registry.is_installed("service-catalog-app")

    # 3. Verify uninstall protection: cannot uninstall core-ontology while required by service-catalog-app
    with pytest.raises(DependencyConflict, match="cannot uninstall core-ontology"):
        installer.uninstall("core-ontology")

    # 4. Uninstall dependent first, then core succeeds
    assert installer.uninstall("service-catalog-app") is True
    assert installer.uninstall("core-ontology") is True
    assert not registry.is_installed("core-ontology")


# ---------------------------------------------------------------------------
# GAP-MKT-008: Signed packages in later phases
# ---------------------------------------------------------------------------

@pytest.mark.req("GAP-MKT-008")
def test_marketplace_signed_packages():
    registry = PackageRegistry()
    installer = PackageInstaller(registry, key=KEY)

    manifest = PackageManifest(
        id="urn:eoip:marketplace:package:signed-security-pack",
        name="signed-security-pack",
        version="1.0.0",
        description="Signed enterprise pack",
        provides={CapabilityKind.VALIDATORS: ["sec_rules"]},
    )
    raw_archive = build_package(manifest, {"sec.json": b'{"rule": "no_open_ports"}'})

    # Sign archive creating a self-contained archive with signature.bin
    signed_archive = sign_package_archive(raw_archive, KEY)
    assert len(signed_archive) > len(raw_archive)

    # Valid install using embedded signature
    installed_manifest = installer.install(signed_archive, key=KEY)
    assert installed_manifest.name == "signed-security-pack"
    assert registry.is_installed("signed-security-pack")

    # Verify search finds the installed package
    search_results = registry.search("security")
    assert len(search_results) == 1
    assert search_results[0].manifest.name == "signed-security-pack"

    # Reject install with invalid key
    with pytest.raises(IntegrityError, match="signature verification failed"):
        PackageInstaller(PackageRegistry(), key=b"wrong-key").install(signed_archive, key=b"wrong-key")


def test_gitops_marketplace_api_routes():
    from fastapi import FastAPI
    from starlette.testclient import TestClient
    from eoip.ontology.gitops_router import build_gitops_marketplace_router

    app = FastAPI()
    app.include_router(build_gitops_marketplace_router())
    client = TestClient(app)

    # 1. Branch routes
    res = client.get("/api/v1/ontology/gitops/branches")
    assert res.status_code == 200
    assert "main" in res.json()["branches"]

    # 2. Diff route
    res = client.post("/api/v1/ontology/gitops/diff", json={})
    assert res.status_code == 200
    assert res.json()["safe"] is True

    # 3. Validate route
    res = client.post("/api/v1/ontology/gitops/validate", json={})
    assert res.status_code == 200
    assert res.json()["verdict"] == "PUBLISH_OK"

    # 4. Impact route
    res = client.post("/api/v1/ontology/gitops/impact", json={})
    assert res.status_code == 200
    assert res.json()["safe_to_proceed"] is True

    # 5. Migration route
    res = client.post("/api/v1/ontology/gitops/migration", json={})
    assert res.status_code == 200
    assert "cypher_script" in res.json()

    # 6. Marketplace packages route
    res = client.get("/api/v1/marketplace/packages")
    assert res.status_code == 200

