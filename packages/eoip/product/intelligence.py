"""Enterprise product-intelligence readiness scanner.

This module turns the "make this a first-choice enterprise product" ambition
into an executable control surface.  It does not load demo data.  Every finding
is derived from real implementation evidence: importable modules, repository
files, configured API routes, tests, config artifacts, and optional live graph
facts.
"""

from __future__ import annotations

import importlib.util
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable


@dataclass(frozen=True)
class ProductCapabilityDefinition:
    capability_id: str
    name: str
    category: str
    priority: str
    outcome: str
    required_modules: tuple[str, ...] = ()
    required_files: tuple[str, ...] = ()
    required_routes: tuple[str, ...] = ()
    required_tests: tuple[str, ...] = ()
    required_config_globs: tuple[str, ...] = ()
    required_graph_labels: tuple[str, ...] = ()


PRODUCT_CAPABILITY_CATALOG: tuple[ProductCapabilityDefinition, ...] = (
    ProductCapabilityDefinition(
        capability_id="PIC-001",
        name="Evidence-backed enterprise answering",
        category="Intelligence",
        priority="P0",
        outcome="Every answer can be grounded in graph, retrieval, citation, and evidence-manifest surfaces.",
        required_modules=(
            "eoip.retrieval.service",
            "eoip.retrieval.rag_suite",
            "eoip.provenance.evidence",
            "eoip.query.executor",
            "eoip.query.nlq",
        ),
        required_routes=(
            "/api/v1/rag/query",
            "/api/v1/retrieval/search",
            "/api/v1/evidence/manifest",
            "/api/v1/query/nl",
        ),
        required_tests=("tests/unit/test_retrieval*.py", "tests/unit/test_rag*.py"),
    ),
    ProductCapabilityDefinition(
        capability_id="PIC-002",
        name="Governed autonomous agent runtime",
        category="Agents",
        priority="P0",
        outcome="Agents are registered, bounded, permissioned, explainable, replayable, and approval-aware.",
        required_modules=(
            "eoip.agents.runtime",
            "eoip.agents.tools",
            "eoip.agents.firewall",
            "eoip.agents.proposals",
            "eoip.loops.core",
            "eoip.loops.approval",
        ),
        required_routes=(
            "/api/v1/agents",
            "/api/v1/agents/{agent_id}/runs",
            "/api/v1/agents/runs/{run_id}/explanation",
            "/api/v1/loops/catalog",
        ),
        required_tests=("tests/unit/test_agent*.py", "tests/unit/test_loops_library.py"),
        required_graph_labels=("AgentRun",),
    ),
    ProductCapabilityDefinition(
        capability_id="PIC-003",
        name="Living bitemporal enterprise graph",
        category="Knowledge Graph",
        priority="P0",
        outcome="The product models facts as a temporal, versioned, validated graph with ontology drift controls.",
        required_modules=(
            "eoip.graph.bitemporal",
            "eoip.graph.evolution",
            "eoip.graph.knowledge_debt",
            "eoip.ontology.drift",
            "eoip.ontology.gitops",
            "eoip.validation.gate",
        ),
        required_routes=(
            "/api/v1/ontology/drift",
            "/api/v1/ontology/proposals",
            "/api/v1/admin/schema",
            "/api/v1/knowledge-debt",
        ),
        required_tests=("tests/unit/test_bitemporal.py", "tests/unit/test_ontology*.py"),
        required_graph_labels=("EntityRevision", "GraphVersion", "BusinessCapability"),
    ),
    ProductCapabilityDefinition(
        capability_id="PIC-004",
        name="Low-code customization and extension marketplace",
        category="Customization",
        priority="P0",
        outcome="Customers can tailor ontologies, plugins, marketplace packages, branding, and layered configuration.",
        required_modules=(
            "eoip.marketplace.registry",
            "eoip.marketplace.installer",
            "eoip.plugins.runtime",
            "eoip.plugins.loader",
            "eoip.config.layered",
            "eoip.branding.router",
        ),
        required_routes=(
            "/api/v1/marketplace/installed",
            "/api/v1/ontology/packs",
            "/api/v1/config/definitions",
            "/api/v1/config/explain",
        ),
        required_config_globs=("config/domain-packs/*/pack.yaml", "config/domain-packs/*/ontology.yaml"),
        required_tests=("tests/unit/test_marketplace.py", "tests/unit/test_domain_packs*.py", "tests/unit/test_layered_config.py"),
    ),
    ProductCapabilityDefinition(
        capability_id="PIC-005",
        name="Enterprise integration fabric",
        category="Integration",
        priority="P0",
        outcome="The platform can connect to work, code, docs, ITSM, observability, file, API, and webhook sources.",
        required_modules=(
            "eoip.connectors.registry",
            "eoip.connectors.acquisition",
            "eoip.connectors.jira",
            "eoip.connectors.github",
            "eoip.connectors.gitlab",
            "eoip.connectors.confluence",
            "eoip.connectors.servicenow",
            "eoip.systems.registry",
        ),
        required_routes=(
            "/api/v1/connectors/catalog",
            "/api/v1/federation/sources",
            "/api/v1/systems/",
            "/api/v1/systems/known-types",
        ),
        required_tests=("tests/unit/test_*connector*.py", "tests/unit/test_acquisition_fabric.py"),
        required_graph_labels=("DataSource", "IngestionRun"),
    ),
    ProductCapabilityDefinition(
        capability_id="PIC-006",
        name="Security, governance, privacy and compliance cockpit",
        category="Governance",
        priority="P0",
        outcome="Security, policy, privacy, model governance, compliance packs, audit and egress controls are productized.",
        required_modules=(
            "eoip.authn",
            "eoip.authz.core",
            "eoip.audit.redaction",
            "eoip.compliance.packs",
            "eoip.egress.gateway",
            "eoip.models.governance",
            "eoip.privacy.classification",
        ),
        required_routes=(
            "/api/v1/auth/health",
            "/api/v1/authz/evaluate",
            "/api/v1/governance/models",
            "/api/v1/compliance/packs",
            "/api/v1/egress/endpoints",
        ),
        required_tests=("tests/unit/test_auth*.py", "tests/unit/test_compliance*.py", "tests/unit/test_model_governance.py"),
    ),
    ProductCapabilityDefinition(
        capability_id="PIC-007",
        name="Reliable scalable enterprise operations",
        category="Operations",
        priority="P0",
        outcome="The product exposes health, HA, preflight, recovery, tenancy, circuit breaker, and support-bundle controls.",
        required_modules=(
            "eoip.enterprise.health",
            "eoip.enterprise.circuit_breaker",
            "eoip.ops.preflight",
            "eoip.ops.production",
            "eoip.recovery_bundle",
            "eoip.tenancy.service",
            "eoip.ha",
        ),
        required_routes=(
            "/health/ready",
            "/api/v1/ops/preflight",
            "/api/v1/ops/support-bundle",
            "/api/v1/enterprise/health/ready",
            "/api/v1/tenancy/context",
            "/api/v1/tenancy/quotas",
        ),
        required_tests=("tests/unit/test_enterprise_resilience.py", "tests/unit/test_operational_recovery.py", "tests/unit/test_tenancy.py"),
    ),
    ProductCapabilityDefinition(
        capability_id="PIC-008",
        name="Polyglot query and database agnostic intelligence",
        category="Query",
        priority="P1",
        outcome="Users can query through NL, graph, semantic, observability, JSON, federation, and backend-neutral adapters.",
        required_modules=(
            "eoip.query.polyglot_engine",
            "eoip.qlang.taxonomy",
            "eoip.federation.planner",
            "eoip.graph.database_adapters",
            "eoip.adapters.manifests",
        ),
        required_routes=(
            "/api/v1/query",
            "/api/v1/query/eql",
            "/api/v1/query/nl",
            "/api/v1/graph/backends",
        ),
        required_tests=("tests/unit/test_query*.py", "tests/unit/test_graph_backends.py", "tests/unit/test_federation_planner.py"),
    ),
    ProductCapabilityDefinition(
        capability_id="PIC-009",
        name="Simulation, causal digital twin and what-if analysis",
        category="Decision Intelligence",
        priority="P1",
        outcome="Teams can simulate changes, reason over causal dependencies, and inspect blast radius before action.",
        required_modules=(
            "eoip.graph.simulation",
            "eoip.graph.causal",
            "eoip.graph.whatif",
            "eoip.graph.twin",
            "eoip.moonshot.causal_simulator",
        ),
        required_routes=(
            "/api/v1/simulation/create",
            "/api/v1/whatif/plan",
            "/api/v1/causal/prerequisites",
            "/api/v1/graph/blast-radius",
        ),
        required_tests=("tests/unit/test_simulation.py", "tests/unit/test_twin_domains.py", "tests/unit/test_kgr_whatif.py"),
    ),
    ProductCapabilityDefinition(
        capability_id="PIC-010",
        name="Role-based product experience and executive reporting",
        category="Experience",
        priority="P1",
        outcome="The product provides web/admin experiences, reports, dashboards, suggestions, and role-friendly exports.",
        required_modules=(
            "eoip.reports.router",
            "eoip.dashboards",
            "eoip.suggest.engine",
            "eoip.catalog.products",
        ),
        required_files=(
            "apps/web/src/App.jsx",
            "apps/web/src/admin/AdminDashboard.jsx",
            "apps/web/src/kgr/KGRExplorer.jsx",
        ),
        required_routes=(
            "/api/v1/reports",
            "/api/v1/catalog/products",
            "/api/v1/suggest",
        ),
        required_tests=("apps/web/tests/*.spec.js", "tests/unit/test_reports.py", "tests/unit/test_knowledge_products.py"),
        required_graph_labels=("KnowledgeProduct",),
    ),
)


def build_product_capability_report(
    *,
    repo_root: str | Path | None = None,
    store: Any | None = None,
    available_routes: set[str] | None = None,
) -> dict[str, Any]:
    """Return machine-checkable product capability readiness."""
    root = Path(repo_root) if repo_root is not None else Path.cwd()
    route_set = available_routes or set()
    capabilities = [
        _capability_report(defn, root, store=store, available_routes=route_set)
        for defn in PRODUCT_CAPABILITY_CATALOG
    ]
    weighted_score = _weighted_score(capabilities)
    missing_p0 = [
        cap["capability_id"]
        for cap in capabilities
        if cap["priority"] == "P0" and cap["status"] != "advanced_ready"
    ]
    next_requirements = _next_requirements(capabilities)
    return {
        "schema_version": "1.0",
        "source": "live-repository-and-runtime-scan",
        "capability_count": len(capabilities),
        "advanced_ready_count": sum(1 for cap in capabilities if cap["status"] == "advanced_ready"),
        "enterprise_grade_score": weighted_score,
        "first_choice_gate": {
            "passed": not missing_p0 and weighted_score >= 0.9,
            "policy": "all P0 capabilities advanced_ready and weighted score >= 0.90",
            "blocking_capability_ids": missing_p0,
        },
        "capabilities": capabilities,
        "next_requirements": next_requirements,
        "runtime_graph": _graph_summary(store),
    }


def materialize_product_capabilities(store: Any, report: dict[str, Any]) -> dict[str, Any]:
    """Persist capability readiness and generated requirements into the graph."""
    if store is None:
        raise ValueError("store is required")
    upserted = 0
    for cap in report.get("capabilities", []):
        store.upsert_vertex(
            "BusinessCapability",
            {
                "canonical_id": f"urn:eoip:product-capability:{cap['capability_id'].lower()}",
                "name": cap["name"],
                "description": cap["outcome"],
                "capability_level": _capability_level(cap["status"]),
                "business_domain": cap["category"],
                "status": cap["status"],
                "source_system": "eoip.product_intelligence",
            },
        )
        upserted += 1
    requirement_count = 0
    for req in report.get("next_requirements", []):
        store.upsert_vertex(
            "Requirement",
            {
                "canonical_id": f"urn:eoip:product-requirement:{req['requirement_id'].lower()}",
                "name": req["title"],
                "description": req["acceptance"],
                "priority": req["priority"],
                "status": "OPEN",
                "source_system": "eoip.product_intelligence",
            },
        )
        requirement_count += 1
    return {
        "upserted_capabilities": upserted,
        "upserted_requirements": requirement_count,
        "labels": ["BusinessCapability", "Requirement"],
    }


def _capability_report(
    defn: ProductCapabilityDefinition,
    repo_root: Path,
    *,
    store: Any | None,
    available_routes: set[str],
) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    checks.extend(_module_check(module) for module in defn.required_modules)
    checks.extend(_file_check(repo_root, target) for target in defn.required_files)
    checks.extend(_glob_check(repo_root, pattern, "test") for pattern in defn.required_tests)
    checks.extend(_glob_check(repo_root, pattern, "config") for pattern in defn.required_config_globs)
    checks.extend(_route_check(route, available_routes) for route in defn.required_routes)
    checks.extend(_graph_label_check(store, label) for label in defn.required_graph_labels)
    scored = [check for check in checks if not check.get("not_evaluated")]
    passed = sum(1 for check in scored if check["present"])
    score = round(passed / len(scored), 4) if scored else 0.0
    missing = [check for check in checks if check.get("present") is False]
    return {
        "capability_id": defn.capability_id,
        "name": defn.name,
        "category": defn.category,
        "priority": defn.priority,
        "outcome": defn.outcome,
        "status": _status(score, missing),
        "score": score,
        "checks_total": len(scored),
        "checks_passed": passed,
        "missing_count": len(missing),
        "checks": checks,
    }


def _module_check(module: str) -> dict[str, Any]:
    try:
        found = importlib.util.find_spec(module) is not None
    except Exception as exc:  # Some package __init__ files execute during find_spec.
        return {
            "kind": "module",
            "target": module,
            "present": False,
            "error": f"{type(exc).__name__}: {exc}",
        }
    return {"kind": "module", "target": module, "present": found}


def _file_check(repo_root: Path, target: str) -> dict[str, Any]:
    return {"kind": "file", "target": target, "present": (repo_root / target).exists()}


def _glob_check(repo_root: Path, pattern: str, kind: str) -> dict[str, Any]:
    matches = sorted(path.as_posix() for path in repo_root.glob(pattern))
    return {
        "kind": kind,
        "target": pattern,
        "present": bool(matches),
        "matches": matches[:25],
        "match_count": len(matches),
    }


def _route_check(route: str, available_routes: set[str]) -> dict[str, Any]:
    if not available_routes:
        return {"kind": "route", "target": route, "present": None, "not_evaluated": True}
    return {"kind": "route", "target": route, "present": route in available_routes}


def _graph_label_check(store: Any | None, label: str) -> dict[str, Any]:
    if store is None or not hasattr(store, "count_vertices"):
        return {"kind": "graph_label", "target": label, "present": None, "not_evaluated": True}
    try:
        count = int(store.count_vertices(label=label))
    except Exception as exc:  # pragma: no cover - backend-specific failure path.
        return {"kind": "graph_label", "target": label, "present": False, "error": str(exc), "count": 0}
    return {"kind": "graph_label", "target": label, "present": count > 0, "count": count}


def _status(score: float, missing: list[dict[str, Any]]) -> str:
    if not missing and score >= 1.0:
        return "advanced_ready"
    if score >= 0.75:
        return "implemented_with_gaps"
    if score >= 0.4:
        return "partial"
    return "planned"


def _weighted_score(capabilities: Iterable[dict[str, Any]]) -> float:
    total_weight = 0.0
    score = 0.0
    for cap in capabilities:
        weight = 2.0 if cap["priority"] == "P0" else 1.0
        total_weight += weight
        score += cap["score"] * weight
    return round(score / total_weight, 4) if total_weight else 0.0


def _next_requirements(capabilities: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    requirements: list[dict[str, Any]] = []
    for cap in capabilities:
        for check in cap["checks"]:
            if check.get("present") is not False:
                continue
            req_id = f"PIC-REQ-{len(requirements) + 1:03d}"
            requirements.append({
                "requirement_id": req_id,
                "capability_id": cap["capability_id"],
                "priority": cap["priority"],
                "title": f"Complete {check['kind']} evidence for {cap['name']}",
                "acceptance": f"{check['kind']} '{check['target']}' is present in the live product scan.",
            })
    return requirements


def _graph_summary(store: Any | None) -> dict[str, Any]:
    if store is None:
        return {"available": False}
    summary = {"available": True}
    for name, method in (("vertices", "count_vertices"), ("edges", "count_edges")):
        try:
            summary[name] = int(getattr(store, method)())
        except Exception as exc:  # pragma: no cover - backend-specific failure path.
            summary[name] = None
            summary[f"{name}_error"] = str(exc)
    return summary


def _capability_level(status: str) -> int:
    return {
        "advanced_ready": 4,
        "implemented_with_gaps": 3,
        "partial": 2,
        "planned": 1,
    }.get(status, 1)
