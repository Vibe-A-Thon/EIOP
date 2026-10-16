"""GitOps and Marketplace REST Router (GAP-GITOPS-002..008, GAP-MKT-002..008)."""

from __future__ import annotations

import base64
from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from eoip.marketplace import (
    DependencyConflict,
    IntegrityError,
    PackageInstaller,
    PackageManifest,
    PackageRegistry,
    package_agent_workflow,
    package_connector_mapping,
    package_dashboard,
    package_query_template,
    package_validation_rules,
)
from eoip.ontology.gitops import (
    OntologyGitOpsWorkflow,
    OntologyVersionStore,
    current_manifest_snapshot,
    diff_manifests,
    generate_ontology_migration_script,
    package_ontology_release,
    rollback_ontology_version,
    run_ontology_impact_analysis,
    validate_ontology_change,
)

router = APIRouter(prefix="/api/v1", tags=["gitops_and_marketplace"])

# In-memory singletons for runtime operations
_workflow = OntologyGitOpsWorkflow()
_version_store = OntologyVersionStore("1.0.0", current_manifest_snapshot())
_registry = PackageRegistry()
_installer = PackageInstaller(_registry)


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

class CreateBranchRequest(BaseModel):
    branch_name: str
    base_branch: str = "main"


class CommitManifestRequest(BaseModel):
    branch_name: str
    manifest: dict[str, Any]
    commit_message: str
    author: str = "dev"


class CreatePRRequest(BaseModel):
    title: str
    source_branch: str
    target_branch: str = "main"
    author: str = "dev"


class ReviewPRRequest(BaseModel):
    reviewer: str
    decision: str = Field(..., pattern="^(approve|request_changes)$")
    comment: str = ""


class MergePRRequest(BaseModel):
    merger: str = "ci_bot"
    allow_breaking: bool = False


class DiffRequest(BaseModel):
    old: dict[str, Any] | None = None
    new: dict[str, Any] | None = None


class ImpactRequest(BaseModel):
    old: dict[str, Any] | None = None
    new: dict[str, Any] | None = None
    registered_queries: list[dict[str, Any]] | None = None
    registered_dashboards: list[dict[str, Any]] | None = None


class MigrationGenRequest(BaseModel):
    old: dict[str, Any] | None = None
    new: dict[str, Any] | None = None
    source_version: str = "1.0.0"
    target_version: str = "2.0.0"
    default_values: dict[str, Any] | None = None


class RollbackRequest(BaseModel):
    target_version: str
    allow_breaking: bool = False


class PackageReleaseRequest(BaseModel):
    manifest: dict[str, Any] | None = None
    current_version: str = "1.0.0"
    changelog: str = ""


class InstallPackageRequest(BaseModel):
    archive_b64: str
    key: str | None = None


class BuildMappingPackageRequest(BaseModel):
    name: str
    version: str
    mapping_id: str
    mapping_payload: dict[str, Any]


class BuildQueryTemplatePackageRequest(BaseModel):
    name: str
    version: str
    template_id: str
    query_text: str


class BuildValidatorPackageRequest(BaseModel):
    name: str
    version: str
    validator_id: str
    rules: dict[str, Any]


class BuildAgentWorkflowPackageRequest(BaseModel):
    name: str
    version: str
    workflow_id: str
    workflow_spec: dict[str, Any]


class BuildDashboardPackageRequest(BaseModel):
    name: str
    version: str
    dashboard_id: str
    dashboard_spec: dict[str, Any]


# ---------------------------------------------------------------------------
# GAP-GITOPS-002..008 Endpoints
# ---------------------------------------------------------------------------

@router.post("/ontology/gitops/branches")
def create_branch(req: CreateBranchRequest):
    """Create a new ontology branch (GAP-GITOPS-002)."""
    try:
        return _workflow.create_branch(req.branch_name, req.base_branch)
    except ValueError as exc:
        raise HTTPException(400, str(exc))


@router.get("/ontology/gitops/branches")
def list_branches():
    """List all ontology branches (GAP-GITOPS-002)."""
    return {"branches": _workflow.list_branches()}


@router.post("/ontology/gitops/branches/commit")
def commit_branch(req: CommitManifestRequest):
    """Commit changes to an ontology branch (GAP-GITOPS-002)."""
    try:
        return _workflow.commit_manifest(req.branch_name, req.manifest, req.commit_message, req.author)
    except KeyError as exc:
        raise HTTPException(404, str(exc))


@router.post("/ontology/gitops/prs")
def create_pr(req: CreatePRRequest):
    """Create an ontology pull request (GAP-GITOPS-002)."""
    try:
        pr = _workflow.create_pull_request(req.title, req.source_branch, req.target_branch, req.author)
        return pr
    except KeyError as exc:
        raise HTTPException(404, str(exc))


@router.get("/ontology/gitops/prs")
def list_prs(status: str | None = None):
    """List ontology pull requests (GAP-GITOPS-002)."""
    return {"prs": _workflow.list_pull_requests(status)}


@router.post("/ontology/gitops/prs/{pr_id}/review")
def review_pr(pr_id: str, req: ReviewPRRequest):
    """Review an ontology pull request (GAP-GITOPS-002)."""
    try:
        return _workflow.review_pull_request(pr_id, req.reviewer, req.decision, req.comment)
    except KeyError:
        raise HTTPException(404, f"PR {pr_id} not found")
    except ValueError as exc:
        raise HTTPException(400, str(exc))


@router.post("/ontology/gitops/prs/{pr_id}/merge")
def merge_pr(pr_id: str, req: MergePRRequest):
    """Merge an approved ontology PR (GAP-GITOPS-002)."""
    try:
        return _workflow.merge_pull_request(pr_id, req.merger, req.allow_breaking)
    except KeyError:
        raise HTTPException(404, f"PR {pr_id} not found")
    except ValueError as exc:
        raise HTTPException(400, str(exc))


@router.post("/ontology/gitops/diff")
def generate_diff(req: DiffRequest):
    """Generate structural semantic diff between two snapshots (GAP-GITOPS-003)."""
    old = req.old or current_manifest_snapshot()
    new = req.new or current_manifest_snapshot()
    diff = diff_manifests(old, new)
    return diff.to_dict()


@router.post("/ontology/gitops/validate")
def validate_ontology(req: DiffRequest):
    """CI validates ontology before publishing (GAP-GITOPS-004)."""
    old = req.old or current_manifest_snapshot()
    new = req.new or current_manifest_snapshot()
    return validate_ontology_change(old, new)


@router.post("/ontology/gitops/impact")
def impact_analysis(req: ImpactRequest):
    """Run graph & query impact analysis for ontology changes (GAP-GITOPS-005)."""
    old = req.old or current_manifest_snapshot()
    new = req.new or current_manifest_snapshot()
    diff = diff_manifests(old, new)
    report = run_ontology_impact_analysis(
        diff,
        registered_queries=req.registered_queries,
        registered_dashboards=req.registered_dashboards,
    )
    return report.to_dict()


@router.post("/ontology/gitops/migration")
def generate_migration(req: MigrationGenRequest):
    """Generate Cypher and Python migration scripts (GAP-GITOPS-006)."""
    old = req.old or current_manifest_snapshot()
    new = req.new or current_manifest_snapshot()
    diff = diff_manifests(old, new)
    plan = generate_ontology_migration_script(
        diff,
        source_version=req.source_version,
        target_version=req.target_version,
        default_values=req.default_values,
    )
    return plan.to_dict()


@router.post("/ontology/gitops/rollback")
def rollback_version(req: RollbackRequest):
    """Rollback ontology version to a previous semantic release (GAP-GITOPS-007)."""
    try:
        receipt = _version_store.rollback_to_version(req.target_version, req.allow_breaking)
        return receipt.to_dict()
    except KeyError as exc:
        raise HTTPException(404, str(exc))
    except ValueError as exc:
        raise HTTPException(400, str(exc))


@router.post("/ontology/gitops/package-release")
def package_release(req: PackageReleaseRequest):
    """Package ontology release with SemVer-like policy (GAP-GITOPS-008)."""
    m = req.manifest or current_manifest_snapshot()
    prev = _version_store.get_manifest(_version_store.active_version)
    pkg = package_ontology_release(m, req.current_version, prev, req.changelog)
    _version_store.publish_version(pkg["version"], m)
    return pkg


# ---------------------------------------------------------------------------
# GAP-MKT-002..008 Marketplace Endpoints
# ---------------------------------------------------------------------------

@router.get("/marketplace/packages")
def list_marketplace_packages(q: str | None = None):
    """List installed packages with search support (GAP-MKT-006..008)."""
    records = _registry.search(q) if q else _registry.list()
    return {"packages": [r.to_dict() for r in records]}


@router.post("/marketplace/packages/install")
def install_package(req: InstallPackageRequest):
    """Install .eoipkg archive with integrity & dependency resolution (GAP-MKT-007, GAP-MKT-008)."""
    try:
        archive = base64.b64decode(req.archive_b64)
        key_bytes = req.key.encode("utf-8") if req.key else None
        manifest = _installer.install(archive, key=key_bytes)
        return {"installed": manifest.model_dump()}
    except (IntegrityError, DependencyConflict) as exc:
        raise HTTPException(400, str(exc))
    except Exception as exc:
        raise HTTPException(500, f"Installation failed: {exc}")


@router.delete("/marketplace/packages/{name}")
def uninstall_package(name: str):
    """Uninstall package respecting dependents (GAP-MKT-007)."""
    try:
        success = _installer.uninstall(name)
        if not success:
            raise HTTPException(404, f"Package {name} not found")
        return {"uninstalled": name, "success": True}
    except DependencyConflict as exc:
        raise HTTPException(400, str(exc))


@router.post("/marketplace/build/mapping")
def build_mapping_pkg(req: BuildMappingPackageRequest):
    """Package connector mappings (GAP-MKT-002)."""
    pkg_bytes = package_connector_mapping(req.name, req.version, req.mapping_id, req.mapping_payload)
    return {
        "name": req.name,
        "size_bytes": len(pkg_bytes),
        "archive_b64": base64.b64encode(pkg_bytes).decode("ascii"),
    }


@router.post("/marketplace/build/query-template")
def build_query_template_pkg(req: BuildQueryTemplatePackageRequest):
    """Package query templates (GAP-MKT-003)."""
    pkg_bytes = package_query_template(req.name, req.version, req.template_id, req.query_text)
    return {
        "name": req.name,
        "size_bytes": len(pkg_bytes),
        "archive_b64": base64.b64encode(pkg_bytes).decode("ascii"),
    }


@router.post("/marketplace/build/validator")
def build_validator_pkg(req: BuildValidatorPackageRequest):
    """Package validation rules (GAP-MKT-004)."""
    pkg_bytes = package_validation_rules(req.name, req.version, req.validator_id, req.rules)
    return {
        "name": req.name,
        "size_bytes": len(pkg_bytes),
        "archive_b64": base64.b64encode(pkg_bytes).decode("ascii"),
    }


@router.post("/marketplace/build/agent-workflow")
def build_agent_workflow_pkg(req: BuildAgentWorkflowPackageRequest):
    """Package agent workflows (GAP-MKT-005)."""
    pkg_bytes = package_agent_workflow(req.name, req.version, req.workflow_id, req.workflow_spec)
    return {
        "name": req.name,
        "size_bytes": len(pkg_bytes),
        "archive_b64": base64.b64encode(pkg_bytes).decode("ascii"),
    }


@router.post("/marketplace/build/dashboard")
def build_dashboard_pkg(req: BuildDashboardPackageRequest):
    """Package dashboards (GAP-MKT-006)."""
    pkg_bytes = package_dashboard(req.name, req.version, req.dashboard_id, req.dashboard_spec)
    return {
        "name": req.name,
        "size_bytes": len(pkg_bytes),
        "archive_b64": base64.b64encode(pkg_bytes).decode("ascii"),
    }


def build_gitops_marketplace_router() -> APIRouter:
    return router
