"""Ontology GitOps: semantic diff, CI validation, branches, PRs, impact analysis,
migration scripts, rollback, and SemVer release packaging (GAP-GITOPS-001..008).

Compares two ontology manifest snapshots and classifies every change as:

- ``additive`` — new optional vocabulary; existing facts remain valid.
- ``potentially_breaking`` — changed constraints or required properties; review.
- ``breaking`` — removed vocabulary or tightened required properties; existing
  graph facts may violate the new manifest and require a migration plan.

The diff is structural (manifest AST comparison), not a text diff. A manifest
snapshot is a dict of the shape produced by :func:`snapshot_manifest`.
"""

from __future__ import annotations

import copy
import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

ADDITIVE = "additive"
POTENTIALLY_BREAKING = "potentially_breaking"
BREAKING = "breaking"


@dataclass
class SemanticChange:
    change_type: str  # label_added | label_removed | property_added | ...
    subject: str
    detail: str
    classification: str


@dataclass
class SemanticDiff:
    changes: list[SemanticChange] = field(default_factory=list)

    @property
    def breaking(self) -> list[SemanticChange]:
        return [c for c in self.changes if c.classification == BREAKING]

    @property
    def potentially_breaking(self) -> list[SemanticChange]:
        return [c for c in self.changes if c.classification == POTENTIALLY_BREAKING]

    @property
    def additive(self) -> list[SemanticChange]:
        return [c for c in self.changes if c.classification == ADDITIVE]

    @property
    def safe(self) -> bool:
        return not self.breaking

    def to_dict(self) -> dict[str, Any]:
        return {
            "safe": self.safe,
            "counts": {
                "total": len(self.changes),
                BREAKING: len(self.breaking),
                POTENTIALLY_BREAKING: len(self.potentially_breaking),
                ADDITIVE: len(self.additive),
            },
            "changes": [asdict(change) for change in self.changes],
        }


def snapshot_manifest(
    vertex_labels: dict[str, tuple[str, list[str], list[str]]],
    edge_labels: dict[str, tuple[list[str], list[str], list[str]]],
    property_keys: dict[str, str],
) -> dict[str, Any]:
    """Capture a manifest in a JSON-serializable snapshot form."""
    return {
        "vertex_labels": {
            name: {"domain": spec[0], "required": sorted(spec[1]), "optional": sorted(spec[2])}
            for name, spec in vertex_labels.items()
        },
        "edge_labels": {
            name: {"out": sorted(spec[0]), "in": sorted(spec[1])}
            for name, spec in edge_labels.items()
        },
        "property_keys": dict(sorted(property_keys.items())),
    }


def current_manifest_snapshot() -> dict[str, Any]:
    from eoip.ontology.manifest import EDGE_LABELS, PROPERTY_KEYS, VERTEX_LABELS

    return snapshot_manifest(VERTEX_LABELS, EDGE_LABELS, PROPERTY_KEYS)


def diff_manifests(old: dict[str, Any], new: dict[str, Any]) -> SemanticDiff:
    """Structural semantic diff between two manifest snapshots (GAP-GITOPS-003)."""
    diff = SemanticDiff()

    old_v = old.get("vertex_labels", {})
    new_v = new.get("vertex_labels", {})
    for name in sorted(set(new_v) - set(old_v)):
        diff.changes.append(SemanticChange("vertex_label_added", name, "new vertex label", ADDITIVE))
    for name in sorted(set(old_v) - set(new_v)):
        diff.changes.append(
            SemanticChange("vertex_label_removed", name, "existing graph facts may use it", BREAKING)
        )
    for name in sorted(set(old_v) & set(new_v)):
        o, n = old_v[name], new_v[name]
        for prop in sorted(set(n.get("required", [])) - set(o.get("required", []))):
            diff.changes.append(
                SemanticChange(
                    "required_property_added", f"{name}.{prop}",
                    "existing facts may lack the now-required property",
                    POTENTIALLY_BREAKING,
                )
            )
        for prop in sorted(set(o.get("required", [])) - set(n.get("required", []))):
            diff.changes.append(
                SemanticChange("required_property_removed", f"{name}.{prop}", "relaxed", ADDITIVE)
            )
        if o.get("domain") != n.get("domain"):
            diff.changes.append(
                SemanticChange(
                    "domain_changed", name, f"{o.get('domain')} -> {n.get('domain')}",
                    POTENTIALLY_BREAKING,
                )
            )

    old_e = old.get("edge_labels", {})
    new_e = new.get("edge_labels", {})
    for name in sorted(set(new_e) - set(old_e)):
        diff.changes.append(SemanticChange("edge_label_added", name, "new edge label", ADDITIVE))
    for name in sorted(set(old_e) - set(new_e)):
        diff.changes.append(
            SemanticChange("edge_label_removed", name, "existing edges may use it", BREAKING)
        )
    for name in sorted(set(old_e) & set(new_e)):
        o, n = old_e[name], new_e[name]
        removed_out = sorted(set(o.get("out", [])) - set(n.get("out", [])))
        removed_in = sorted(set(o.get("in", [])) - set(n.get("in", [])))
        if removed_out or removed_in:
            diff.changes.append(
                SemanticChange(
                    "edge_endpoints_narrowed", name,
                    f"removed out={removed_out} in={removed_in}",
                    POTENTIALLY_BREAKING,
                )
            )
        added_out = sorted(set(n.get("out", [])) - set(o.get("out", [])))
        added_in = sorted(set(n.get("in", [])) - set(o.get("in", [])))
        if added_out or added_in:
            diff.changes.append(
                SemanticChange(
                    "edge_endpoints_widened", name, f"added out={added_out} in={added_in}", ADDITIVE
                )
            )

    old_p = old.get("property_keys", {})
    new_p = new.get("property_keys", {})
    for key in sorted(set(new_p) - set(old_p)):
        diff.changes.append(SemanticChange("property_key_added", key, "new property", ADDITIVE))
    for key in sorted(set(old_p) - set(new_p)):
        diff.changes.append(
            SemanticChange("property_key_removed", key, "existing facts may set it", BREAKING)
        )
    for key in sorted(set(old_p) & set(new_p)):
        if old_p[key] != new_p[key]:
            diff.changes.append(
                SemanticChange(
                    "property_type_changed", key, f"{old_p[key]} -> {new_p[key]}",
                    POTENTIALLY_BREAKING,
                )
            )

    return diff


generate_semantic_diff = diff_manifests


def validate_ontology_change(old: dict[str, Any], new: dict[str, Any]) -> dict[str, Any]:
    """CI gate (GAP-GITOPS-004): pass only when no breaking changes are present."""
    result = diff_manifests(old, new).to_dict()
    result["publishable"] = result["safe"]
    result["verdict"] = "PUBLISH_OK" if result["safe"] else "BREAKING_CHANGE_REFUSED"
    return result


# ---------------------------------------------------------------------------
# GAP-GITOPS-002: Branch, Pull Request, Review, and Merge Workflows
# ---------------------------------------------------------------------------

class PullRequestStatus(str, Enum):
    OPEN = "open"
    APPROVED = "approved"
    CHANGES_REQUESTED = "changes_requested"
    MERGED = "merged"
    CLOSED = "closed"


@dataclass
class OntologyPullRequest:
    pr_id: str
    title: str
    source_branch: str
    target_branch: str
    author: str
    status: str
    diff: dict[str, Any]
    reviews: list[dict[str, Any]] = field(default_factory=list)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    updated_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


class OntologyGitOpsWorkflow:
    """Ontology branch, pull-request/review and merge workflows (GAP-GITOPS-002)."""

    def __init__(self, base_snapshot: dict[str, Any] | None = None) -> None:
        initial = base_snapshot if base_snapshot is not None else current_manifest_snapshot()
        self._branches: dict[str, dict[str, Any]] = {"main": copy.deepcopy(initial)}
        self._prs: dict[str, OntologyPullRequest] = {}
        self._commit_history: dict[str, list[dict[str, Any]]] = {"main": []}

    def create_branch(self, branch_name: str, base_branch: str = "main") -> dict[str, Any]:
        """Create a new working branch off an existing branch."""
        if branch_name in self._branches:
            raise ValueError(f"Branch {branch_name!r} already exists")
        if base_branch not in self._branches:
            raise ValueError(f"Base branch {base_branch!r} does not exist")
        self._branches[branch_name] = copy.deepcopy(self._branches[base_branch])
        self._commit_history[branch_name] = []
        return {
            "branch": branch_name,
            "base_branch": base_branch,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

    def get_branch_manifest(self, branch_name: str) -> dict[str, Any]:
        if branch_name not in self._branches:
            raise KeyError(f"Branch {branch_name!r} not found")
        return copy.deepcopy(self._branches[branch_name])

    def commit_manifest(
        self,
        branch_name: str,
        manifest: dict[str, Any],
        commit_message: str,
        author: str = "dev",
    ) -> dict[str, Any]:
        """Commit an updated ontology manifest to a branch."""
        if branch_name not in self._branches:
            raise KeyError(f"Branch {branch_name!r} not found")
        commit_id = str(uuid.uuid4())[:8]
        old = self._branches[branch_name]
        diff = diff_manifests(old, manifest).to_dict()
        self._branches[branch_name] = copy.deepcopy(manifest)
        record = {
            "commit_id": commit_id,
            "branch": branch_name,
            "message": commit_message,
            "author": author,
            "diff_summary": diff["counts"],
            "committed_at": datetime.now(timezone.utc).isoformat(),
        }
        self._commit_history[branch_name].append(record)
        return record

    def create_pull_request(
        self,
        title: str,
        source_branch: str,
        target_branch: str = "main",
        author: str = "dev",
    ) -> OntologyPullRequest:
        """Create a PR comparing source_branch against target_branch."""
        if source_branch not in self._branches:
            raise KeyError(f"Source branch {source_branch!r} not found")
        if target_branch not in self._branches:
            raise KeyError(f"Target branch {target_branch!r} not found")

        diff = diff_manifests(
            self._branches[target_branch],
            self._branches[source_branch],
        ).to_dict()

        pr_id = f"pr-{uuid.uuid4().hex[:8]}"
        pr = OntologyPullRequest(
            pr_id=pr_id,
            title=title,
            source_branch=source_branch,
            target_branch=target_branch,
            author=author,
            status=PullRequestStatus.OPEN.value,
            diff=diff,
        )
        self._prs[pr_id] = pr
        return pr

    def review_pull_request(
        self,
        pr_id: str,
        reviewer: str,
        decision: str,  # "approve" | "request_changes"
        comment: str = "",
    ) -> OntologyPullRequest:
        """Review an ontology PR."""
        if pr_id not in self._prs:
            raise KeyError(f"PR {pr_id!r} not found")
        pr = self._prs[pr_id]
        if pr.status in (PullRequestStatus.MERGED.value, PullRequestStatus.CLOSED.value):
            raise ValueError(f"Cannot review PR in status {pr.status}")

        review = {
            "reviewer": reviewer,
            "decision": decision,
            "comment": comment,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        pr.reviews.append(review)
        if decision == "approve":
            pr.status = PullRequestStatus.APPROVED.value
        elif decision == "request_changes":
            pr.status = PullRequestStatus.CHANGES_REQUESTED.value
        pr.updated_at = datetime.now(timezone.utc).isoformat()
        return pr

    def merge_pull_request(
        self,
        pr_id: str,
        merger: str = "ci_bot",
        allow_breaking: bool = False,
    ) -> dict[str, Any]:
        """Merge an approved PR into the target branch."""
        if pr_id not in self._prs:
            raise KeyError(f"PR {pr_id!r} not found")
        pr = self._prs[pr_id]
        if pr.status != PullRequestStatus.APPROVED.value and not allow_breaking:
            raise ValueError(f"PR {pr_id} must be approved before merging (current: {pr.status})")

        # Check CI gate
        src = self._branches[pr.source_branch]
        tgt = self._branches[pr.target_branch]
        ci_validation = validate_ontology_change(tgt, src)
        if not ci_validation["safe"] and not allow_breaking:
            raise ValueError(
                f"PR {pr_id} contains breaking changes and cannot be merged without explicit allow_breaking override"
            )

        # Apply merge
        self._branches[pr.target_branch] = copy.deepcopy(src)
        pr.status = PullRequestStatus.MERGED.value
        pr.updated_at = datetime.now(timezone.utc).isoformat()

        return {
            "pr_id": pr_id,
            "status": "MERGED",
            "merged_by": merger,
            "target_branch": pr.target_branch,
            "source_branch": pr.source_branch,
            "timestamp": pr.updated_at,
        }

    def list_branches(self) -> list[str]:
        return sorted(self._branches.keys())

    def list_pull_requests(self, status: str | None = None) -> list[OntologyPullRequest]:
        prs = list(self._prs.values())
        if status:
            prs = [p for p in prs if p.status == status]
        return prs


# ---------------------------------------------------------------------------
# GAP-GITOPS-005: Ontology Change Impact Analysis
# ---------------------------------------------------------------------------

@dataclass
class OntologyImpactReport:
    diff: SemanticDiff
    affected_vertex_labels: list[str]
    affected_edge_labels: list[str]
    affected_properties: list[str]
    affected_vertices_count: int
    affected_edges_count: int
    impacted_queries: list[str]
    impacted_dashboards: list[str]
    risk_level: str  # "LOW", "MEDIUM", "HIGH", "CRITICAL"
    safe_to_proceed: bool
    recommendations: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "diff_summary": self.diff.to_dict()["counts"],
            "affected_vertex_labels": self.affected_vertex_labels,
            "affected_edge_labels": self.affected_edge_labels,
            "affected_properties": self.affected_properties,
            "affected_vertices_count": self.affected_vertices_count,
            "affected_edges_count": self.affected_edges_count,
            "impacted_queries": self.impacted_queries,
            "impacted_dashboards": self.impacted_dashboards,
            "risk_level": self.risk_level,
            "safe_to_proceed": self.safe_to_proceed,
            "recommendations": self.recommendations,
        }


def run_ontology_impact_analysis(
    diff: SemanticDiff,
    graph_store: Any = None,
    registered_queries: list[dict[str, Any]] | None = None,
    registered_dashboards: list[dict[str, Any]] | None = None,
) -> OntologyImpactReport:
    """Run full graph & query impact analysis for proposed ontology changes (GAP-GITOPS-005)."""
    removed_v = [c.subject for c in diff.changes if c.change_type == "vertex_label_removed"]
    removed_e = [c.subject for c in diff.changes if c.change_type == "edge_label_removed"]
    tightened_props = [c.subject for c in diff.changes if c.change_type == "required_property_added"]
    removed_props = [c.subject for c in diff.changes if c.change_type == "property_key_removed"]

    affected_vertices = 0
    affected_edges = 0

    if graph_store is not None:
        try:
            # Check vertices in store
            vertices = getattr(graph_store, "_vertices", None) or getattr(graph_store, "vertices", None)
            if callable(vertices):
                all_v = vertices()
            elif isinstance(vertices, dict):
                all_v = list(vertices.values())
            else:
                all_v = []

            for v in all_v:
                lbl = getattr(v, "label", None) or (v.get("label") if isinstance(v, dict) else None)
                if lbl in removed_v:
                    affected_vertices += 1
                elif tightened_props:
                    props = getattr(v, "properties", None) or (v.get("properties") if isinstance(v, dict) else {})
                    for p in tightened_props:
                        label_name, prop_name = p.split(".", 1) if "." in p else (lbl, p)
                        if lbl == label_name and prop_name not in props:
                            affected_vertices += 1

            # Check edges in store
            edges = getattr(graph_store, "_edges", None) or getattr(graph_store, "edges", None)
            if callable(edges):
                all_e = edges()
            elif isinstance(edges, dict):
                all_e = list(edges.values())
            else:
                all_e = []

            for e in all_e:
                lbl = getattr(e, "label", None) or (e.get("label") if isinstance(e, dict) else None)
                if lbl in removed_e:
                    affected_edges += 1
        except Exception:
            pass

    # Check queries impact
    impacted_queries: list[str] = []
    if registered_queries:
        all_changed_tokens = set(removed_v + removed_e + removed_props + tightened_props)
        for q in registered_queries:
            q_name = q.get("name", "query")
            q_text = str(q.get("text", "")).lower()
            if any(t.lower() in q_text for t in all_changed_tokens):
                impacted_queries.append(q_name)

    # Check dashboards impact
    impacted_dashboards: list[str] = []
    if registered_dashboards:
        all_changed_tokens = set(removed_v + removed_e + removed_props)
        for d in registered_dashboards:
            d_name = d.get("name", "dashboard")
            d_spec = json.dumps(d).lower()
            if any(t.lower() in d_spec for t in all_changed_tokens):
                impacted_dashboards.append(d_name)

    # Determine risk level
    if diff.breaking:
        risk_level = "CRITICAL" if (affected_vertices > 0 or affected_edges > 0) else "HIGH"
        safe = False
    elif diff.potentially_breaking:
        risk_level = "MEDIUM"
        safe = True
    else:
        risk_level = "LOW"
        safe = True

    recommendations: list[str] = []
    if removed_v:
        recommendations.append(f"Generate migration script to migrate {len(removed_v)} deleted vertex labels")
    if tightened_props:
        recommendations.append(f"Backfill default values for newly required properties: {tightened_props}")
    if impacted_queries:
        recommendations.append(f"Update {len(impacted_queries)} dependent query templates")
    if not recommendations:
        recommendations.append("All changes are additive; safe for automatic deployment")

    return OntologyImpactReport(
        diff=diff,
        affected_vertex_labels=removed_v,
        affected_edge_labels=removed_e,
        affected_properties=tightened_props + removed_props,
        affected_vertices_count=affected_vertices,
        affected_edges_count=affected_edges,
        impacted_queries=impacted_queries,
        impacted_dashboards=impacted_dashboards,
        risk_level=risk_level,
        safe_to_proceed=safe,
        recommendations=recommendations,
    )


# ---------------------------------------------------------------------------
# GAP-GITOPS-006: Ontology Migration Script Generation
# ---------------------------------------------------------------------------

@dataclass
class OntologyMigrationPlan:
    migration_id: str
    source_version: str
    target_version: str
    cypher_script: str
    python_script: str
    actions: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "migration_id": self.migration_id,
            "source_version": self.source_version,
            "target_version": self.target_version,
            "cypher_script": self.cypher_script,
            "python_script": self.python_script,
            "actions": self.actions,
        }


def generate_ontology_migration_script(
    diff: SemanticDiff,
    source_version: str = "1.0.0",
    target_version: str = "2.0.0",
    default_values: dict[str, Any] | None = None,
) -> OntologyMigrationPlan:
    """Generate executable Cypher and Python migration scripts for ontology changes (GAP-GITOPS-006)."""
    defaults = default_values or {}
    actions: list[dict[str, Any]] = []
    cypher_lines: list[str] = [
        f"// Migration from {source_version} to {target_version}",
        "// Automatically generated by EOIP Ontology GitOps",
    ]
    py_lines: list[str] = [
        f"# Migration script: {source_version} -> {target_version}",
        "def apply_migration(graph_store):",
    ]

    migration_id = f"mig-{uuid.uuid4().hex[:8]}"

    for change in diff.changes:
        if change.change_type == "vertex_label_removed":
            actions.append({"type": "deprecate_vertex_label", "label": change.subject})
            cypher_lines.append(f"MATCH (n:{change.subject}) SET n._deprecated = true, n._deprecated_version = '{target_version}';")
            py_lines.append(f"    # Deprecate vertices with label {change.subject}")
            py_lines.append(f"    for v in graph_store.find_vertices_by_label('{change.subject}'):")
            py_lines.append("        v.properties['_deprecated'] = True")

        elif change.change_type == "required_property_added":
            parts = change.subject.split(".", 1)
            v_label = parts[0] if len(parts) > 1 else "Node"
            prop = parts[1] if len(parts) > 1 else change.subject
            default_val = defaults.get(prop, "UNKNOWN")
            actions.append({"type": "backfill_required_property", "label": v_label, "property": prop, "default": default_val})
            cypher_lines.append(
                f"MATCH (n:{v_label}) WHERE n.{prop} IS NULL SET n.{prop} = '{default_val}';"
            )
            py_lines.append(f"    # Backfill required property {prop} on {v_label}")
            py_lines.append(f"    for v in graph_store.find_vertices_by_label('{v_label}'):")
            py_lines.append(f"        if '{prop}' not in v.properties:")
            py_lines.append(f"            v.properties['{prop}'] = {default_val!r}")

        elif change.change_type == "edge_label_removed":
            actions.append({"type": "deprecate_edge_label", "edge": change.subject})
            cypher_lines.append(f"MATCH ()-[r:{change.subject}]->() SET r._deprecated = true;")
            py_lines.append(f"    # Deprecate edges with label {change.subject}")
            py_lines.append(f"    for e in graph_store.find_edges_by_label('{change.subject}'):")
            py_lines.append("        e.properties['_deprecated'] = True")

    if not actions:
        cypher_lines.append("// No migration operations needed: changes are purely additive.")
        py_lines.append("    pass  # No data transformation required.")

    return OntologyMigrationPlan(
        migration_id=migration_id,
        source_version=source_version,
        target_version=target_version,
        cypher_script="\n".join(cypher_lines),
        python_script="\n".join(py_lines),
        actions=actions,
    )


# ---------------------------------------------------------------------------
# GAP-GITOPS-007: Rollback to Previous Semantic Version
# ---------------------------------------------------------------------------

@dataclass
class RollbackReceipt:
    rollback_id: str
    from_version: str
    to_version: str
    success: bool
    restored_manifest: dict[str, Any]
    reverse_diff: SemanticDiff
    warnings: list[str]
    timestamp: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "rollback_id": self.rollback_id,
            "from_version": self.from_version,
            "to_version": self.to_version,
            "success": self.success,
            "reverse_diff_summary": self.reverse_diff.to_dict()["counts"],
            "warnings": self.warnings,
            "timestamp": self.timestamp,
        }


class OntologyVersionStore:
    """Version store tracking historical ontology snapshots for rollback (GAP-GITOPS-007)."""

    def __init__(self, initial_version: str = "1.0.0", initial_manifest: dict[str, Any] | None = None) -> None:
        init_m = initial_manifest if initial_manifest is not None else current_manifest_snapshot()
        self._versions: dict[str, dict[str, Any]] = {initial_version: copy.deepcopy(init_m)}
        self._active_version: str = initial_version

    @property
    def active_version(self) -> str:
        return self._active_version

    def publish_version(self, version: str, manifest: dict[str, Any]) -> None:
        """Publish a new semantic release."""
        self._versions[version] = copy.deepcopy(manifest)
        self._active_version = version

    def get_manifest(self, version: str) -> dict[str, Any]:
        if version not in self._versions:
            raise KeyError(f"Version {version!r} not found in store")
        return copy.deepcopy(self._versions[version])

    def list_versions(self) -> list[str]:
        return sorted(self._versions.keys())

    def rollback_to_version(self, target_version: str, allow_breaking: bool = False) -> RollbackReceipt:
        """Rollback active ontology to target_version."""
        if target_version not in self._versions:
            raise KeyError(f"Target version {target_version!r} not found")

        current_manifest = self._versions[self._active_version]
        target_manifest = self._versions[target_version]

        reverse_diff = diff_manifests(current_manifest, target_manifest)
        warnings: list[str] = []

        if reverse_diff.breaking and not allow_breaking:
            raise ValueError(
                f"Rollback to {target_version} causes breaking changes ({len(reverse_diff.breaking)} breaking). Pass allow_breaking=True to force."
            )

        if reverse_diff.breaking:
            warnings.append(f"Rollback contains {len(reverse_diff.breaking)} breaking change(s)")
        if reverse_diff.potentially_breaking:
            warnings.append(f"Rollback contains {len(reverse_diff.potentially_breaking)} potentially breaking change(s)")

        self._active_version = target_version
        receipt = RollbackReceipt(
            rollback_id=f"rb-{uuid.uuid4().hex[:8]}",
            from_version=self._active_version,
            to_version=target_version,
            success=True,
            restored_manifest=copy.deepcopy(target_manifest),
            reverse_diff=reverse_diff,
            warnings=warnings,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        return receipt


def rollback_ontology_version(
    current_version: str,
    target_version: str,
    version_history: dict[str, dict[str, Any]],
    allow_breaking: bool = False,
) -> RollbackReceipt:
    """Allow rollback to previous semantic version (GAP-GITOPS-007)."""
    if current_version not in version_history:
        raise KeyError(f"Current version {current_version!r} not in history")
    if target_version not in version_history:
        raise KeyError(f"Target version {target_version!r} not in history")

    curr_m = version_history[current_version]
    tgt_m = version_history[target_version]
    reverse_diff = diff_manifests(curr_m, tgt_m)

    warnings: list[str] = []
    if reverse_diff.breaking and not allow_breaking:
        raise ValueError(f"Rollback to {target_version} is breaking; set allow_breaking=True")
    if reverse_diff.breaking:
        warnings.append(f"Rollback is breaking: {len(reverse_diff.breaking)} breaking changes")

    return RollbackReceipt(
        rollback_id=f"rb-{uuid.uuid4().hex[:8]}",
        from_version=current_version,
        to_version=target_version,
        success=True,
        restored_manifest=copy.deepcopy(tgt_m),
        reverse_diff=reverse_diff,
        warnings=warnings,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


# ---------------------------------------------------------------------------
# GAP-GITOPS-008: SemVer Release Packaging Policy
# ---------------------------------------------------------------------------

def compute_next_semver(current_version: str, diff: SemanticDiff) -> str:
    """Compute next SemVer string based on semantic diff (GAP-GITOPS-008)."""
    parts = current_version.split("-")[0].split("+")[0].split(".")
    major = int(parts[0]) if len(parts) > 0 else 1
    minor = int(parts[1]) if len(parts) > 1 else 0
    patch = int(parts[2]) if len(parts) > 2 else 0

    if diff.breaking:
        return f"{major + 1}.0.0"
    elif diff.potentially_breaking or diff.additive:
        return f"{major}.{minor + 1}.0"
    else:
        return f"{major}.{minor}.{patch + 1}"


def package_ontology_release(
    manifest: dict[str, Any],
    current_version: str,
    previous_manifest: dict[str, Any] | None = None,
    changelog: str = "",
) -> dict[str, Any]:
    """Package an ontology release using SemVer-like policy (GAP-GITOPS-008)."""
    import hashlib

    diff = diff_manifests(previous_manifest or manifest, manifest)
    next_ver = compute_next_semver(current_version, diff) if previous_manifest else current_version
    manifest_bytes = json.dumps(manifest, sort_keys=True).encode("utf-8")
    checksum = hashlib.sha256(manifest_bytes).hexdigest()

    return {
        "version": next_ver,
        "previous_version": current_version,
        "manifest": manifest,
        "checksum_sha256": checksum,
        "diff_summary": diff.to_dict()["counts"],
        "changelog": changelog or f"Ontology release {next_ver}",
        "release_timestamp": datetime.now(timezone.utc).isoformat(),
        "semver_type": "MAJOR" if diff.breaking else ("MINOR" if diff.additive or diff.potentially_breaking else "PATCH"),
    }


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("old", help="Path to the old manifest snapshot JSON ('-' for current)")
    parser.add_argument("new", help="Path to the new manifest snapshot JSON ('-' for current)")
    args = parser.parse_args(argv)

    def load(path: str) -> dict[str, Any]:
        if path == "-":
            return current_manifest_snapshot()
        return json.loads(open(path, encoding="utf-8").read())

    result = validate_ontology_change(load(args.old), load(args.new))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["publishable"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
