"""Normative predicate definitions and registration for REVA (T-106 / §10.4)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field

from reva.kernel.authority import Authority, Epistemic
from reva.kernel.registry import (
    PredicateEntry,
    PredicateRegistry,
    default_registry,
    get_predicate,
    has_predicate,
    list_predicates,
    register_predicate,
)



# Generic statement models for key predicates
class CommitStatement(BaseModel):
    model_config = ConfigDict(extra="ignore", strict=False)
    commit: str
    repo_hint: Optional[str] = None
    dirty: bool = False


class ArtifactInventoryStatement(BaseModel):
    model_config = ConfigDict(extra="ignore", strict=False)
    member_count: int
    uncompressed_bytes: int
    format: str


class DependencyStatement(BaseModel):
    model_config = ConfigDict(extra="ignore", strict=False)
    packages: List[Dict[str, Any]] = Field(default_factory=list)


class BoundaryStatement(BaseModel):
    model_config = ConfigDict(extra="ignore", strict=False)
    service: str
    boundary_type: str
    method: Optional[str] = None
    path_template: Optional[str] = None


class GenericStatement(BaseModel):
    model_config = ConfigDict(extra="allow", strict=False)


PREDICATE_DEFINITIONS = [
    ("reva.pred.source_record", GenericStatement, "Ingested record from system of record"),
    ("reva.pred.artifact_inventory", ArtifactInventoryStatement, "Extracted archive/container member inventory"),
    ("reva.pred.integrity_violation", GenericStatement, "Detected integrity mismatch between declared and actual"),
    ("reva.pred.go_buildinfo", DependencyStatement, "Go binary buildinfo dependencies and modules"),
    ("reva.pred.rust_dependencies", DependencyStatement, "Rust cargo-auditable dependency graph"),
    ("reva.pred.dotnet_assembly", GenericStatement, ".NET assembly metadata and dependencies"),
    ("reva.pred.jvm_archive", GenericStatement, "JVM archive pom.properties, MANIFEST.MF and coordinates"),
    ("reva.pred.python_distribution", DependencyStatement, "Python wheel/sdist METADATA and dependencies"),
    ("reva.pred.npm_package", DependencyStatement, "npm package.json and lockfile dependencies"),
    ("reva.pred.oci_image", GenericStatement, "OCI container image layers, labels and packages"),
    ("reva.pred.os_packages", DependencyStatement, "OS packages from dpkg/apk/rpm databases"),
    ("reva.pred.built_from_commit", CommitStatement, "Artifact built from specific VCS commit SHA"),
    ("reva.pred.dirty_build", GenericStatement, "Artifact was built with uncommitted local modifications"),
    ("reva.pred.vulnerability_match", GenericStatement, "Offline vulnerability advisory match"),
    ("reva.pred.service_identity", GenericStatement, "Identified deployable service boundary"),
    ("reva.pred.boundary", BoundaryStatement, "Application boundary route, RPC or message topic"),
    ("reva.pred.resource_access", GenericStatement, "Service resource access (DB, file, secret)"),
    ("reva.pred.endpoint_match", GenericStatement, "Matched outbound call to inbound service boundary"),
    ("reva.pred.api_operation", GenericStatement, "Observed HTTP API operation from HAR or OTel"),
    ("reva.pred.api_caller", GenericStatement, "Attributed caller of observed API operation"),
    ("reva.pred.openapi_alignment", GenericStatement, "Alignment between observed API and OpenAPI spec"),
    ("reva.pred.db_object", GenericStatement, "Introspected database schema table, column, view"),
    ("reva.pred.db_link", GenericStatement, "Foreign key or inferred relational link"),
    ("reva.pred.observed_as", GenericStatement, "Static declaration reconciled with runtime observation"),
    ("reva.pred.reconciliation_summary", GenericStatement, "Reconciliation summary across service boundary"),
    ("reva.pred.trace_result", GenericStatement, "Feature and impact trace result"),
    ("reva.pred.graph_diff", GenericStatement, "Version comparison diff between graph states"),
    ("reva.pred.drift_check", GenericStatement, "Discrepancy check between source and deployed artifact"),
    ("reva.pred.drift_verdict", GenericStatement, "Overall drift verdict (clean, dirty, drift)"),
    ("reva.pred.gap_revision", GenericStatement, "Revision event for knowledge gap"),
    ("reva.pred.contradiction_decision", GenericStatement, "Resolution decision for contradiction"),
    ("reva.pred.obligation_review", GenericStatement, "Human or authorized review of obligation definition"),
    ("reva.pred.waiver", GenericStatement, "Authorized waiver for obligation or mutant"),
    ("reva.pred.verifier_run", GenericStatement, "Execution record of verifier run in sandbox"),
    ("reva.pred.closure_decision", GenericStatement, "Proof-of-Done closure decision"),
    ("reva.pred.ledger", GenericStatement, "Consolidated Proof-of-Done ledger"),
    ("reva.pred.answer", GenericStatement, "Grounded answer with citations and limitations"),
    ("reva.pred.eval_result", GenericStatement, "Benchmark evaluation run result"),
    ("reva.pred.injection_attempt", GenericStatement, "Detected prompt injection attempt"),
    ("reva.pred.policy_change", GenericStatement, "Administrative policy modification"),
    ("reva.pred.key_event", GenericStatement, "Signing key activation, rotation or revocation"),
    ("reva.pred.human_assertion", GenericStatement, "Human-attested assertion or override"),
]


def register_all_predicates(reg: PredicateRegistry) -> None:
    """Register all 42 normative REVA predicates into registry."""
    for name, model, desc in PREDICATE_DEFINITIONS:
        req_cov = name in {
            "reva.pred.artifact_inventory",
            "reva.pred.boundary",
            "reva.pred.api_operation",
            "reva.pred.trace_result",
            "reva.pred.graph_diff",
        }
        reg.register_predicate(
            name=name,
            statement_model=model,
            requires_coverage=req_cov,
            description=desc,
        )


# Register into global default
register_all_predicates(default_registry)
