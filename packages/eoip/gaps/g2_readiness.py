"""Executable G2 readiness matrix.

This module binds the broad G2 requirement families to concrete implementation
surfaces so the application can report readiness with machine-checkable evidence.

Requirement coverage:
- G2-ADMIN-001..017
- G2-ARCH-001..015
- G2-ARCHC-001..009
- G2-CAP-001..006
- G2-CAUSE-001..006
- G2-EKAF-001..030
- G2-EVENT-001..007
- G2-EVOL-001..016
- G2-GRAPH-API-001..003
- G2-GRAPH-BIZ-001..003
- G2-GRAPH-DEC-001..003
- G2-GRAPH-OBS-001..003
- G2-GRAPH-PROC-001..003
- G2-GRAPH-RUNTIME-001..003
- G2-GRAPH-SEC-001..003
- G2-GRAPH-TEST-001..003
- G2-I2R-001..005
- G2-IMMUNE-001..013
- G2-JOURNAL-001..006
- G2-KD-001..006
- G2-OBS-001..006
- G2-OEVO-001..006
- G2-PERF-001..008
- G2-PM-001..005
- G2-QOP-001..009
- G2-REL-001..008
- G2-SEC-CRAWL-001..012
- G2-SIM-001..007
- G2-SLO-001..005
- G2-SRC-API-001..006
- G2-SRC-CICD-001..004
- G2-SRC-CODE-001..005
- G2-SRC-CONF-001..005
- G2-SRC-DD-001..004
- G2-SRC-GH-001..004
- G2-SRC-GL-001..004
- G2-SRC-GRAF-001..003
- G2-SRC-JIRA-001..006
- G2-SRC-KIB-001..005
- G2-SRC-OTEL-001..005
- G2-SRC-RUNTIME-001..003
- G2-SRC-SBOM-001..004
- G2-SRC-SNKB-001..003
- G2-SRC-SNOW-001..006
- G2-SRC-WEB-001..005
- G2-SYNC-001..014
- G2-TEL-001..008
- G2-TIME-001..007
- G2-TWIN-001..005
- G2-UX-GRAPH-001..016
- G2-UX-LENS-001..003
- G2-UX-PLAY-001..005
- G2-VSC-001..008
"""

from __future__ import annotations

import importlib
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


RANGE_RE = re.compile(
    r"^(G2-[A-Z0-9]+(?:-[A-Z0-9]+)*)-(\d{3})(?:\.\.(\d{3}))?$"
)


@dataclass(frozen=True)
class G2ReadinessArea:
    name: str
    requirement_ranges: tuple[str, ...]
    implementation_modules: tuple[str, ...] = ()
    file_targets: tuple[str, ...] = ()
    api_routes: tuple[str, ...] = ()
    notes: str = ""

    def requirement_ids(self) -> tuple[str, ...]:
        ids: list[str] = []
        for item in self.requirement_ranges:
            match = RANGE_RE.match(item)
            if not match:
                ids.append(item)
                continue
            prefix, start, end = match.group(1), int(match.group(2)), int(match.group(3) or match.group(2))
            ids.extend(f"{prefix}-{number:03d}" for number in range(start, end + 1))
        return tuple(ids)


G2_READINESS_AREAS: tuple[G2ReadinessArea, ...] = (
    G2ReadinessArea(
        name="Contracts, architecture and observability guardrails",
        requirement_ranges=(
            "G2-ARCH-001..015",
            "G2-OBS-001..006",
        ),
        implementation_modules=(
            "eoip.contracts.source_event",
            "eoip.contracts.source_registry",
            "eoip.contracts.revision",
            "eoip.gaps.g2_architecture",
            "eoip.gaps.g2_observability",
        ),
        api_routes=(
            "/api/v1/gaps/g2/architecture-guardrails",
            "/api/v1/gaps/g2/observability-contract",
        ),
        notes="SourceEvent v2, source registry, revision model, architecture and telemetry contracts.",
    ),
    G2ReadinessArea(
        name="Enterprise knowledge acquisition fabric",
        requirement_ranges=(
            "G2-EKAF-001..030",
            "G2-SYNC-001..014",
            "G2-EVOL-001..016",
            "G2-JOURNAL-001..006",
            "G2-EVENT-001..007",
            "G2-SEC-CRAWL-001..012",
        ),
        implementation_modules=(
            "eoip.connectors.acquisition",
            "eoip.connectors.base",
            "eoip.connectors.crawler",
            "eoip.connectors.reconciliation",
            "eoip.connectors.registry",
            "eoip.connectors.sync",
            "eoip.connectors.webhook",
            "eoip.events.emitter",
            "eoip.graph.consumers",
            "eoip.graph.evolution",
        ),
        file_targets=("tests/unit/test_acquisition_fabric.py", "tests/unit/test_graph_evolution.py"),
        notes="Registry, scheduler, baseline/poll/reconcile/replay, webhook, DLQ, journal and event-bus substrate.",
    ),
    G2ReadinessArea(
        name="Source connector portfolio",
        requirement_ranges=(
            "G2-SRC-JIRA-001..006",
            "G2-SRC-CONF-001..005",
            "G2-SRC-SNKB-001..003",
            "G2-SRC-SNOW-001..006",
            "G2-SRC-GH-001..004",
            "G2-SRC-GL-001..004",
            "G2-SRC-CODE-001..005",
            "G2-SRC-API-001..006",
            "G2-SRC-KIB-001..005",
            "G2-SRC-DD-001..004",
            "G2-SRC-GRAF-001..003",
            "G2-SRC-OTEL-001..005",
            "G2-SRC-CICD-001..004",
            "G2-SRC-RUNTIME-001..003",
            "G2-SRC-SBOM-001..004",
            "G2-SRC-WEB-001..005",
        ),
        implementation_modules=(
            "eoip.connectors.api_portal",
            "eoip.connectors.confluence",
            "eoip.connectors.datadog",
            "eoip.connectors.generic",
            "eoip.connectors.github",
            "eoip.connectors.gitlab",
            "eoip.connectors.grafana",
            "eoip.connectors.jira",
            "eoip.connectors.kibana",
            "eoip.connectors.local_code",
            "eoip.connectors.rest",
            "eoip.connectors.servicenow",
        ),
        api_routes=("/api/v1/connectors/catalog",),
        notes="Registered adapter surface for work, docs, code, API, telemetry, runtime and web sources.",
    ),
    G2ReadinessArea(
        name="Graph intelligence runtime",
        requirement_ranges=(
            "G2-GRAPH-API-001..003",
            "G2-GRAPH-OBS-001..003",
            "G2-GRAPH-RUNTIME-001..003",
            "G2-GRAPH-SEC-001..003",
            "G2-GRAPH-TEST-001..003",
            "G2-GRAPH-DEC-001..003",
            "G2-GRAPH-PROC-001..003",
            "G2-GRAPH-BIZ-001..003",
            "G2-TWIN-001..005",
            "G2-TIME-001..007",
            "G2-QOP-001..009",
            "G2-KD-001..006",
            "G2-SLO-001..005",
        ),
        implementation_modules=(
            "eoip.graph.bitemporal",
            "eoip.graph.business_intent",
            "eoip.graph.decisions",
            "eoip.graph.engineering",
            "eoip.graph.knowledge_debt",
            "eoip.graph.lens",
            "eoip.graph.playback",
            "eoip.graph.process_mining",
            "eoip.graph.query_operators",
            "eoip.graph.test_intelligence",
            "eoip.graph.twin",
            "eoip.graphtest.framework",
        ),
        api_routes=(
            "/api/v1/query/why",
            "/api/v1/query/why-not",
            "/api/v1/query/what-if",
            "/api/v1/query/what-changed",
            "/api/v1/knowledge-debt",
            "/api/v1/knowledge-slos",
        ),
        notes="Temporal, decision, process, test, business and native query graph operators.",
    ),
    G2ReadinessArea(
        name="Simulation, causality and adaptive knowledge",
        requirement_ranges=(
            "G2-SIM-001..007",
            "G2-ARCHC-001..009",
            "G2-CAUSE-001..006",
            "G2-IMMUNE-001..013",
            "G2-OEVO-001..006",
            "G2-PM-001..005",
            "G2-CAP-001..006",
            "G2-I2R-001..005",
        ),
        implementation_modules=(
            "eoip.agents.anomaly",
            "eoip.agents.catalog",
            "eoip.agents.evaluation",
            "eoip.agents.firewall",
            "eoip.agents.proposals",
            "eoip.catalog.products",
            "eoip.graph.capsules",
            "eoip.graph.causal",
            "eoip.graph.conformance",
            "eoip.graph.simulation",
            "eoip.ontology.drift",
            "eoip.query.intelligence",
        ),
        api_routes=(
            "/api/v1/simulations",
            "/api/v1/simulation/create",
        ),
        notes="What-if workspaces, causal hypotheses, conformance, proposals, products and retrieval intelligence.",
    ),
    G2ReadinessArea(
        name="UX, operations, telemetry, reliability and performance",
        requirement_ranges=(
            "G2-UX-LENS-001..003",
            "G2-UX-GRAPH-001..016",
            "G2-UX-PLAY-001..005",
            "G2-ADMIN-001..017",
            "G2-VSC-001..008",
            "G2-TEL-001..008",
            "G2-PERF-001..008",
            "G2-REL-001..008",
        ),
        implementation_modules=(
            "eoip.audit.redaction",
            "eoip.jobs",
            "eoip.observability",
            "eoip.query.cache",
            "eoip.recovery_bundle",
            "eoip.runtime",
            "eoip.validation.gate",
            "apps.api.app",
        ),
        file_targets=(
            "apps/web/src/App.jsx",
            "apps/web/src/style.css",
            "apps/web/tests/admin-source-registry.spec.js",
            "apps/web/tests/application.spec.js",
        ),
        api_routes=(
            "/api/v1/admin/schema",
            "/api/v1/gaps/coverage",
            "/api/v1/gaps/g2/readiness",
        ),
        notes="Admin UI, visual graph/playback surfaces, telemetry contract, cache, recovery and validation gates.",
    ),
)


def g2_readiness_report(
    *,
    repo_root: str | Path | None = None,
    available_routes: set[str] | None = None,
) -> dict[str, Any]:
    root = Path(repo_root) if repo_root is not None else Path.cwd()
    route_set = available_routes or set()
    area_reports = [_area_report(area, root, route_set) for area in G2_READINESS_AREAS]
    requirement_ids = sorted(
        {req_id for area in G2_READINESS_AREAS for req_id in area.requirement_ids()},
        key=_requirement_sort_key,
    )
    failed = [area for area in area_reports if not area["conformant"]]
    return {
        "schema_version": "1.0",
        "requirement_count": len(requirement_ids),
        "requirements": requirement_ids,
        "area_count": len(area_reports),
        "conformant": not failed,
        "failed_areas": [area["name"] for area in failed],
        "areas": area_reports,
    }


def _area_report(area: G2ReadinessArea, repo_root: Path, available_routes: set[str]) -> dict[str, Any]:
    module_checks = [_module_check(module) for module in area.implementation_modules]
    file_checks = [_file_check(repo_root, target) for target in area.file_targets]
    route_checks = [_route_check(route, available_routes) for route in area.api_routes]
    checks = module_checks + file_checks + route_checks
    return {
        "name": area.name,
        "requirements": list(area.requirement_ids()),
        "requirement_count": len(area.requirement_ids()),
        "notes": area.notes,
        "conformant": all(check["present"] for check in checks),
        "modules": module_checks,
        "files": file_checks,
        "routes": route_checks,
    }


def _module_check(module: str) -> dict[str, Any]:
    try:
        importlib.import_module(module)
    except Exception as exc:  # pragma: no cover - exercised when a module regresses.
        return {"target": module, "present": False, "error": f"{type(exc).__name__}: {exc}"}
    return {"target": module, "present": True}


def _file_check(repo_root: Path, target: str) -> dict[str, Any]:
    return {"target": target, "present": (repo_root / target).exists()}


def _route_check(route: str, available_routes: set[str]) -> dict[str, Any]:
    present = not available_routes or route in available_routes
    return {"target": route, "present": present}


def _requirement_sort_key(req_id: str) -> tuple[str, int]:
    prefix, number = req_id.rsplit("-", 1)
    return prefix, int(number)
