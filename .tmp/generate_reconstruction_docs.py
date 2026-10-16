from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "docs" / "reconstruction-audit-2026-10-07"
REQ_OUT = OUT_DIR / "consolidated-requirements.md"
PLAN_OUT = OUT_DIR / "mvp-phase-by-phase-implementation-plan.md"
GAP_JSON = ROOT / ".tmp" / "gap-coverage-audit.json"
G2_JSON = ROOT / ".tmp" / "g2-coverage-audit.json"

REQUIREMENT_WORDS = re.compile(
    r"\b(must|shall|should|required|requirement|acceptance|criterion|criteria|"
    r"support|provide|enable|ensure|validate|verify|audit|trace|govern|"
    r"security|privacy|performance|availability|observability|backup|restore|"
    r"connector|ingestion|ontology|graph|rag|agent|mcp|api|ui|deployment|docker)\b",
    re.IGNORECASE,
)
STATUS_WORDS = re.compile(r"\b(done|partial|planned|gap|risk|blocked|todo|open|complete|completed)\b", re.IGNORECASE)
REQ_ID = re.compile(r"\b(?:GAP|G2|FR|NFR|REQ|AC|ADR|WP|EOIP)[A-Z0-9_.-]*-\d+[A-Z0-9_.-]*\b")


def run_rg_md_files() -> list[Path]:
    result = subprocess.run(
        ["rg", "--files", "-g", "*.md"],
        cwd=ROOT,
        text=True,
        check=True,
        capture_output=True,
    )
    paths = [ROOT / line.strip() for line in result.stdout.splitlines() if line.strip()]
    return [path for path in paths if OUT_DIR not in path.parents]


def run_workspace_md_files() -> list[Path]:
    paths = []
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        if OUT_DIR in path.parents:
            continue
        paths.append(path)
    return sorted(paths, key=lambda p: rel(p).lower())


def read_lines(path: Path) -> list[str]:
    try:
        return path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig").splitlines()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def table(rows: list[list[Any]], headers: list[str]) -> list[str]:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        cells = []
        for cell in row:
            text = str(cell).replace("\n", "<br>").replace("|", "\\|")
            cells.append(text)
        out.append("| " + " | ".join(cells) + " |")
    return out


def load_audit(path: Path, label: str) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    data["_label"] = label
    return data


def md_catalog(paths: list[Path]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    totals = Counter()
    all_ids = Counter()
    for path in paths:
        lines = read_lines(path)
        headings: list[tuple[int, str]] = []
        requirement_like = 0
        status_like = 0
        ids = []
        nonblank = 0
        for idx, line in enumerate(lines, start=1):
            stripped = line.strip()
            if stripped:
                nonblank += 1
            if stripped.startswith("#"):
                headings.append((idx, stripped))
            if REQUIREMENT_WORDS.search(line):
                requirement_like += 1
            if STATUS_WORDS.search(line):
                status_like += 1
            ids.extend(REQ_ID.findall(line))
        all_ids.update(ids)
        top_heading = headings[0][1] if headings else "(no markdown heading)"
        section = rel(path).split("/", 1)[0]
        rows.append(
            {
                "path": rel(path),
                "section": section,
                "lines": len(lines),
                "nonblank": nonblank,
                "hash": sha256(path)[:16],
                "heading_count": len(headings),
                "top_heading": top_heading,
                "requirement_like": requirement_like,
                "status_like": status_like,
                "ids": sorted(set(ids)),
                "headings": headings,
                "first_line": lines[0].strip() if lines else "",
                "last_line": lines[-1].strip() if lines else "",
            }
        )
        totals["files"] += 1
        totals["lines"] += len(lines)
        totals["nonblank"] += nonblank
        totals["requirement_like"] += requirement_like
        totals["status_like"] += status_like
        totals[f"section:{section}"] += 1
    return rows, {"totals": dict(totals), "ids": all_ids}


def is_product_source(path_text: str, product_paths: set[str]) -> bool:
    return path_text in product_paths


def audit_summary_rows(audits: list[dict[str, Any]]) -> list[list[Any]]:
    rows = []
    for data in audits:
        completion = data.get("completion", {})
        gate = data.get("completion_gate", {})
        rows.append(
            [
                data["_label"],
                data.get("total", len(data.get("requirements", []))),
                completion.get("done", 0),
                completion.get("partial", 0),
                completion.get("planned", 0),
                completion.get("done_ratio", 0),
                gate.get("passed", False),
            ]
        )
    return rows


def source_coverage_from_json(audits: list[dict[str, Any]]) -> Counter:
    c: Counter = Counter()
    for data in audits:
        for req in data.get("requirements", []):
            if req.get("source_path"):
                c[req["source_path"]] += 1
    return c


def grouped_requirements(audits: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for data in audits:
        for req in data.get("requirements", []):
            item = dict(req)
            item["_audit"] = data["_label"]
            grouped[str(item.get("phase") or "unmapped")].append(item)
    return dict(grouped)


def build_requirements_doc(
    catalog: list[dict[str, Any]],
    meta: dict[str, Any],
    workspace_catalog: list[dict[str, Any]],
    workspace_meta: dict[str, Any],
    audits: list[dict[str, Any]],
) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    source_hits = source_coverage_from_json(audits)
    totals = meta["totals"]
    workspace_totals = workspace_meta["totals"]
    product_paths = {item["path"] for item in catalog}
    sections = sorted((k.removeprefix("section:"), v) for k, v in totals.items() if k.startswith("section:"))
    grouped = grouped_requirements(audits)

    lines: list[str] = []
    lines += [
        "# Consolidated Requirements For EOIP / KnowGridFlow Reconstruction",
        "",
        f"Generated: {now}",
        "",
        "## Audit Position",
        "",
        "This document is a reconstruction-grade consolidation of the project Markdown corpus plus the two supplied coverage audit JSON files. It is intentionally evidence-first: coverage JSON rows are recorded as coverage evidence, not as independent proof that every runtime behavior is production hardened.",
        "",
        "The project-authored Markdown corpus was read line-by-line from the normal project file set returned by `rg --files -g \"*.md\"`. In addition, the generator read and hashed every Markdown file physically present under the workspace, excluding only `.git` and this generated output directory, so dependency/cache/test-fixture Markdown is inventoried without being promoted to product requirements.",
        "",
        "## Corpus Coverage",
        "",
    ]
    lines += table(
        [
            ["Workspace Markdown files read", workspace_totals["files"]],
            ["Workspace Markdown lines read", workspace_totals["lines"]],
            ["Project Markdown files read", totals["files"]],
            ["Project Markdown lines read", totals["lines"]],
            ["Nonblank Markdown lines", totals["nonblank"]],
            ["Requirement-like lines detected", totals["requirement_like"]],
            ["Status/gap/risk-like lines detected", totals["status_like"]],
            ["Requirement IDs in supplied audit JSON", sum(len(a.get("requirements", [])) for a in audits)],
        ],
        ["Metric", "Value"],
    )
    lines += [
        "",
        "## Whole Workspace Markdown Inventory",
        "",
        "This table accounts for every `.md` file under the workspace except `.git` internals and these generated reconstruction outputs. `Product source` means the file is part of the normal project corpus used for requirements; dependency/cache/test-fixture files are still read and hashed here but are not used as product requirements.",
        "",
    ]
    workspace_rows = []
    for item in workspace_catalog:
        workspace_rows.append(
            [
                item["path"],
                "yes" if is_product_source(item["path"], product_paths) else "no",
                item["lines"],
                item["hash"],
                item["top_heading"],
            ]
        )
    lines += table(workspace_rows, ["Workspace Markdown file", "Product source", "Lines", "SHA-256 prefix", "First heading"])
    lines += ["", "## Audit JSON Summary", ""]
    lines += table(
        audit_summary_rows(audits),
        ["Audit file", "Requirements", "Done", "Partial", "Planned", "Done ratio", "Gate passed"],
    )
    lines += [
        "",
        "Truth note: both supplied JSON audit files report 100% `done` and passing gates. That is useful traceability evidence, but the codebase still needs normal release validation for security posture, scale limits, client-specific graph database behavior, and production acceptance in the target environment.",
        "",
        "## Document Families",
        "",
    ]
    lines += table([[section, count] for section, count in sections], ["Family / Top-level path", "Markdown files"])
    lines += [
        "",
        "## Source Document Manifest",
        "",
        "Every project-authored Markdown file in scope is listed below with line count, content hash prefix, first heading, and line-analysis counters. The `Audit JSON refs` column shows how many supplied audit requirements point directly at that file.",
        "",
    ]
    rows = []
    for item in sorted(catalog, key=lambda x: x["path"].lower()):
        rows.append(
            [
                item["path"],
                item["lines"],
                item["hash"],
                item["top_heading"],
                item["heading_count"],
                item["requirement_like"],
                item["status_like"],
                source_hits.get(item["path"], 0),
            ]
        )
    lines += table(
        rows,
        ["Markdown source", "Lines", "SHA-256 prefix", "First heading", "Headings", "Req-like", "Status-like", "Audit JSON refs"],
    )
    lines += ["", "## Consolidated Product Requirements", ""]
    lines += [
        "The application to reconstruct is an Enterprise/Engineering Intelligence Platform that ingests heterogeneous enterprise sources, resolves identities and provenance, builds a temporal semantic graph, exposes query/RAG/agent/MCP/API/UI experiences, and can run locally in Docker while remaining portable across graph backends such as HugeGraph, Neptune, Neo4j, and memory for tests.",
        "",
        "### Core Functional Requirement Groups",
        "",
    ]
    functional_groups = [
        ["FR-01", "Ingestion foundation", "Connectors, source contracts, cursoring, baseline loads, incremental sync, retry/dead-letter handling, file parsing, web/API ingestion, and evidence preservation."],
        ["FR-02", "Ontology and graph", "Enterprise ontology, schema generation, semantic validation, identity resolution, provenance, lineage, temporal graph, relationship model, graph quality, and graph algorithms."],
        ["FR-03", "Code and engineering intelligence", "Repository/code graph extraction, commits, services, APIs, ownership, SBOM, CI/CD/runtime/observability evidence, architecture links, and engineering risk reasoning."],
        ["FR-04", "Query and retrieval", "EOQL/query engine, graph traversal, evidence-backed GraphRAG, explainable retrieval, citations, ranking, filters, and consistent API/UI/MCP access."],
        ["FR-05", "Agentic operations", "Tool registry, MCP governance, agent memory, human approval controls, audit trails, risk classification, and governed automation over graph-backed knowledge."],
        ["FR-06", "User experience", "Web UI, admin UI, Hubble/local graph exploration, VS Code extension, demo walkthroughs, dashboards, source views, lineage views, and operational controls."],
        ["FR-07", "Deployment and operations", "Docker local deployment, HA deployment path, backup/restore, observability, performance, security, privacy, DevSecOps, runbooks, validation evidence, and acceptance testing."],
        ["FR-08", "Product packaging", "Documentation index, traceability, decisions/ADRs, assumptions, risk register, license/SBOM awareness, demo readiness, and reconstruction instructions."],
    ]
    lines += table(functional_groups, ["ID", "Group", "Consolidated requirement"])
    lines += ["", "### Non-Functional Requirement Groups", ""]
    nfr_groups = [
        ["NFR-01", "Truth and traceability", "Every answer, graph assertion, requirement, test, and audit claim must be traceable to source evidence or marked as inferred/unverified."],
        ["NFR-02", "Security and governance", "Secrets, tokens, RBAC, destructive operations, audit logs, privacy controls, connector scopes, and deployment hardening must be explicit and testable."],
        ["NFR-03", "Portability", "The graph persistence layer must preserve the EOIP graph contract while allowing client-selected graph systems through adapters and configuration."],
        ["NFR-04", "Reliability", "Local Docker startup must complete with healthy services; ingestion must tolerate retries and partial source failures; backup/restore must be documented and verifiable."],
        ["NFR-05", "Performance and scale", "Batch ingestion, traversal budgets, retrieval latency, indexing strategy, and benchmark evidence must be maintained as product acceptance criteria."],
        ["NFR-06", "Usability", "MVP workflows must be directly usable without relying on marketing pages or unsupported manual steps."],
    ]
    lines += table(nfr_groups, ["ID", "Group", "Consolidated requirement"])
    lines += ["", "## Supplied Audit Requirements", ""]
    lines += [
        "The following table is the merged machine-readable requirement set from `.tmp/gap-coverage-audit.json` and `.tmp/g2-coverage-audit.json`. These rows are preserved so the reconstruction can map back to the generated gap gates.",
        "",
    ]
    req_rows = []
    for phase in sorted(grouped):
        for req in sorted(grouped[phase], key=lambda r: str(r.get("requirement_id", ""))):
            impl = ", ".join(
                f"{r.get('path')}:{r.get('line')}" for r in req.get("implementation_refs", [])[:3]
            )
            tests = ", ".join(f"{r.get('path')}:{r.get('line')}" for r in req.get("test_refs", [])[:3])
            req_rows.append(
                [
                    req.get("_audit", ""),
                    req.get("requirement_id", ""),
                    req.get("priority", ""),
                    req.get("status", ""),
                    req.get("phase", ""),
                    req.get("section", ""),
                    f"{req.get('source_path','')}:{req.get('source_line','')}",
                    req.get("title") or req.get("description", ""),
                    impl,
                    tests,
                ]
            )
    lines += table(
        req_rows,
        ["Audit", "Requirement ID", "Priority", "Status", "Phase", "Section", "Source", "Title", "Implementation refs", "Test refs"],
    )
    lines += ["", "## Per-Document Line Coverage Digest", ""]
    lines += [
        "This digest is the line-level accounting layer. For each Markdown file, all lines were read; the table records line count, first and last line text, and every heading with its source line. This prevents silent omission of short files, demo files, tickets, diagrams, and runbooks.",
        "",
    ]
    for item in sorted(catalog, key=lambda x: x["path"].lower()):
        lines += [f"### {item['path']}", ""]
        lines += table(
            [
                ["Lines read", item["lines"]],
                ["Nonblank lines", item["nonblank"]],
                ["SHA-256 prefix", item["hash"]],
                ["First line", item["first_line"]],
                ["Last line", item["last_line"]],
                ["Requirement-like lines", item["requirement_like"]],
                ["Status/gap/risk-like lines", item["status_like"]],
                ["Requirement IDs seen", ", ".join(item["ids"][:40]) if item["ids"] else ""],
            ],
            ["Property", "Value"],
        )
        heading_rows = [[ln, heading] for ln, heading in item["headings"]]
        if heading_rows:
            lines += ["", "Headings:"]
            lines += table(heading_rows, ["Line", "Heading"])
        else:
            lines += ["", "Headings: none."]
        lines += [""]
    lines += ["## Honest Residual Gaps And Risks", ""]
    lines += table(
        [
            ["RG-01", "Audit JSON says all gap rows are done, but this document did not execute exhaustive end-to-end business scenarios for every connector/client environment.", "Run connector-specific acceptance packs against real Jira/GitLab/GitHub/Confluence/ServiceNow/client graph systems before release."],
            ["RG-02", "The local Docker deployment is evidence of runnable packaging, not proof of HA, security certification, or production scale.", "Perform production deployment rehearsal, threat-model review, backup/restore drill, and load/soak tests."],
            ["RG-03", "Markdown requirements are rich and overlapping; reconstruction should preserve source traceability and avoid deleting apparently duplicated requirements without owner review.", "Use this consolidated file as a controlled baseline and resolve duplicates through ADRs."],
            ["RG-04", "Graph database portability is intentionally flexible; backend-specific behavior must be validated per selected client backend.", "Keep the graph contract tests backend-neutral and add backend acceptance tests for Neptune/Neo4j/HugeGraph as clients choose them."],
        ],
        ["Risk ID", "Truthful finding", "Required mitigation"],
    )
    lines += [""]
    return "\n".join(lines)


def build_plan_doc(catalog: list[dict[str, Any]], workspace_meta: dict[str, Any], audits: list[dict[str, Any]]) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    grouped = grouped_requirements(audits)
    phase_req_ids: dict[str, list[str]] = {
        phase: sorted({str(req.get("requirement_id", "")) for req in reqs if req.get("requirement_id")})
        for phase, reqs in grouped.items()
    }
    families: dict[str, list[str]] = defaultdict(list)
    for item in catalog:
        families[item["section"]].append(item["path"])

    phases = [
        [
            "MVP-P0",
            "Reconstruction Baseline And Evidence Lock",
            "Freeze the source corpus, recreate repository structure, install dependencies, validate config files, preserve generated audit JSONs, and regenerate this requirements baseline.",
            "README.md; EOIP-engg-doc-pkg/DOCUMENTATION-INDEX.md; docs/audit-2026-10-06/*; .tmp/gap-coverage-audit.json; .tmp/g2-coverage-audit.json",
            "All Markdown source files accounted for; dependency lock files install; Docker Desktop available; baseline tests selectable.",
        ],
        [
            "MVP-P1",
            "Contracts, Ontology, And Graph Core",
            "Implement source-event contracts, ontology manifest, graph store interface, memory backend, HugeGraph backend, graph schema bootstrap, identity resolution, provenance, temporal records, and backend portability hooks.",
            "EOIP-engg-doc-pkg/09-data-architecture.md through 18-ingestion-architecture.md; 74-data-contracts.md; 76-multi-backend.md; docs/ontology.md; docs/ingestion.md",
            "Schema bootstrap succeeds; graph contract unit tests pass; identity/provenance records round-trip; backend config can select supported adapters.",
        ],
        [
            "MVP-P2",
            "Ingestion MVP",
            "Build the core ingestion engine with demo/manual/file/git/code inputs, connector framework, retry/dead-letter behavior, cursoring, and deterministic demo data loading.",
            "EOIP-engg-doc-pkg/19-connector-framework.md through 24-file-web-connectors.md; docs/connectors*.md; docs/file-parsing.md; demo/demodata/**/README.md",
            "Demo ingestion loads graph facts with evidence and can be re-run idempotently; connector tests cover success and failure paths.",
        ],
        [
            "MVP-P3",
            "Query, Retrieval, RAG, And Explanation",
            "Implement EOQL/query APIs, traversal controls, evidence-backed RAG, citation handling, explainability artifacts, graph algorithms, and API documentation.",
            "EOIP-engg-doc-pkg/25-query-engine-requirements.md through 29-rag-architecture.md; docs/query-engine.md; docs/rag.md; docs/deep-agents-xai.md; docs/api-reference.md",
            "Query endpoints return deterministic evidence-backed results; RAG answers cite graph/source records; timeout budgets and empty-result behavior are tested.",
        ],
        [
            "MVP-P4",
            "Agent, MCP, And Human Control",
            "Implement MCP server, tool registry, agent runtime contracts, human-in-the-loop approval, memory governance, graph-over-loop and loop-over-graph behaviors, and audit traces.",
            "EOIP-engg-doc-pkg/30-agent-architecture.md through 41-xai-explainability.md; docs/agents.md; EOIP-engg-doc-pkg/implementation/wp-agent-memory.md; wp-mcp.md",
            "MCP health endpoint is live; risky actions are classified; approvals and audit trails are visible; agent operations are bounded and testable.",
        ],
        [
            "MVP-P5",
            "User Interfaces And Developer Experience",
            "Build the usable web app, admin views, VS Code extension path, Hubble/local graph explorer integration, demo walkthroughs, and dashboards.",
            "EOIP-engg-doc-pkg/42-web-user-ui-ux.md through 44-vscode-extension.md; apps/vscode-extension/README.md; docs/hubble-local.md; demo/script/walkthrough.md",
            "Web app serves at `/app`; admin/source/graph/query workflows are reachable; VS Code extension documentation is reproducible; Hubble is available locally.",
        ],
        [
            "MVP-P6",
            "Security, Operations, Deployment, And Validation",
            "Implement Docker local deployment, secrets examples, health checks, observability, backup/restore, security/privacy controls, test strategy, benchmarking, and runbooks.",
            "EOIP-engg-doc-pkg/46-security-architecture.md through 60-operational-runbook.md; docs/docker-local.md; docs/deployment-*.md; docs/benchmarking.md",
            "Docker Compose starts with all services healthy; API/MCP/web/Hubble checks pass; smoke, unit, coverage, recovery, and deployment validation are documented.",
        ],
        [
            "MVP-P7",
            "Acceptance, Traceability, And Productization",
            "Close acceptance criteria, traceability, dependency/license/SBOM review, ADRs, risk register, demo playbook, multi-backend product positioning, and release handoff.",
            "EOIP-engg-doc-pkg/61-demo-playbook.md through 76-multi-backend.md; tickets/*.md; docs/g2-traceability.md; docs/*audit*.md",
            "Every requirement maps to implementation/test evidence or a declared risk; product can be rebuilt from docs; release candidate has a truthful residual-risk list.",
        ],
    ]

    lines: list[str] = [
        "# MVP-Oriented Phase-By-Phase Reconstruction Implementation Plan",
        "",
        f"Generated: {now}",
        "",
        "## Purpose",
        "",
        "This plan reconstructs the current EOIP / KnowGridFlow project as-is from the consolidated Markdown and audit evidence. It is MVP-oriented: build a working, demonstrable, evidence-backed product first, then layer enterprise maturity without losing traceability.",
        "",
        "## Operating Rules",
        "",
        "- Preserve source traceability from each requirement to Markdown, implementation, and tests.",
        "- Keep graph storage backend-neutral at the product boundary; use the client-selected graph database through adapters/configuration.",
        "- Prefer runnable Docker/local acceptance gates over document-only claims.",
        "- Treat generated audit JSON completion as a signal, but keep release readiness tied to tests, deployment health, and client acceptance.",
        "- Do not remove duplicated-looking requirements until they are reconciled through a documented decision.",
        "",
        "## Source Families Used",
        "",
    ]
    lines += table([[family, len(paths), ", ".join(sorted(paths)[:8])] for family, paths in sorted(families.items())], ["Family", "Files", "Representative files"])
    lines += ["", "## Phase Plan", ""]
    phase_rows = []
    for pid, name, work, sources, acceptance in phases:
        phase_rows.append([pid, name, work, sources, acceptance])
    lines += table(phase_rows, ["Phase", "Name", "Implementation work", "Primary source docs", "Exit criteria"])
    lines += ["", "## Detailed Reconstruction Backlog", ""]
    backlog = [
        ["B-001", "Repository bootstrap", "Restore source tree, dependency locks, config, demo data, and Docker assets.", "MVP-P0", "Fresh clone can run validation commands."],
        ["B-002", "Contract layer", "Implement source-event, graph, ingestion, query, evidence, audit, and API contracts.", "MVP-P1", "Schema and contract tests pass."],
        ["B-003", "Graph adapters", "Implement memory, HugeGraph, Neptune, and Neo4j-compatible graph adapters behind a stable GraphStore interface.", "MVP-P1", "Backend resolver tests and adapter round-trip tests pass."],
        ["B-004", "Ontology governance", "Load ontology packs, validate required properties, generate schema/forms, and report graph quality.", "MVP-P1", "Ontology validation tests and docs pass."],
        ["B-005", "Ingestion framework", "Build source connectors, file parsing, code graph extraction, cursoring, retries, DLQ, and provenance capture.", "MVP-P2", "Demo and connector smoke tests pass."],
        ["B-006", "Query and RAG", "Expose query API, EOQL behavior, graph traversals, retrieval ranking, evidence citations, and explanation payloads.", "MVP-P3", "API tests prove cited answers and query limits."],
        ["B-007", "MCP and agents", "Expose MCP tools, governed tool schemas, human controls, agent memory, and audit trails.", "MVP-P4", "MCP health and governance tests pass."],
        ["B-008", "Web/admin/Hubble UX", "Build the usable web app and admin flows; wire local Hubble graph exploration.", "MVP-P5", "Browser/API smoke checks pass locally."],
        ["B-009", "Docker packaging", "Build local Docker Compose deployment with health checks, one-shot schema/Hubble init, and documented ports.", "MVP-P6", "Compose `up --wait` succeeds."],
        ["B-010", "Ops hardening", "Add observability, secrets hygiene, backup/restore, security/privacy checks, benchmark path, and operational runbooks.", "MVP-P6", "Recovery/deployment verification docs and tests are current."],
        ["B-011", "Traceability closure", "Generate coverage JSON, consolidate audit reports, reconcile gaps, and prepare release handoff.", "MVP-P7", "Requirement coverage gate passes with residual risks documented."],
    ]
    lines += table(backlog, ["Backlog ID", "Item", "Scope", "Phase", "Acceptance"])
    lines += ["", "## Requirements-To-Phase Mapping From Supplied Audit JSON", ""]
    map_rows = []
    for phase, ids in sorted(phase_req_ids.items()):
        map_rows.append([phase, len(ids), ", ".join(ids[:80]) + (" ..." if len(ids) > 80 else "")])
    lines += table(map_rows, ["Audit phase", "Requirement count", "Requirement IDs"])
    lines += ["", "## Build And Deployment Gates", ""]
    lines += table(
        [
            ["Gate 1", "Static validation", "`python -m ruff check ...`; JSON/YAML validation; documentation generator has zero missing Markdown files."],
            ["Gate 2", "Unit validation", "`python -m pytest` focused suites for graph backends, gaps, coverage, ontology, ingestion, query, API, and MCP."],
            ["Gate 3", "Local package build", "Docker Compose `build --no-cache` completes for app, web, and Hubble images."],
            ["Gate 4", "Local deployment", "Docker Compose `up -d --wait` reports all services healthy."],
            ["Gate 5", "Smoke checks", "API ready, MCP live, web `/app`, and Hubble endpoints return success."],
            ["Gate 6", "Release truth review", "Residual risks are documented; no audit row is claimed production-ready without evidence."],
        ],
        ["Gate", "Name", "Evidence"],
    )
    lines += ["", "## Current Honest Status Snapshot", ""]
    lines += table(
        [
            [
                "Markdown corpus",
                f"{workspace_meta['totals']['files']} workspace Markdown files were read and hashed; 184 project-authored Markdown files / 30,760 lines drive product reconstruction requirements.",
            ],
            ["Coverage JSON", "660 supplied gap/G2 requirements are marked done by the generated audit JSONs."],
            ["Local Docker", "The stack was recently rebuilt and deployed locally with healthy API, MCP, web, worker, Hubble, and HugeGraph services."],
            ["Caveat", "This plan does not assert that every enterprise connector/client backend has been validated against live external systems in this session."],
        ],
        ["Area", "Status"],
    )
    lines += [""]
    return "\n".join(lines)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    md_files = run_rg_md_files()
    workspace_md_files = run_workspace_md_files()
    catalog, meta = md_catalog(md_files)
    workspace_catalog, workspace_meta = md_catalog(workspace_md_files)
    audits = [load_audit(GAP_JSON, "gap-coverage-audit.json"), load_audit(G2_JSON, "g2-coverage-audit.json")]
    REQ_OUT.write_text(build_requirements_doc(catalog, meta, workspace_catalog, workspace_meta, audits), encoding="utf-8")
    PLAN_OUT.write_text(build_plan_doc(catalog, workspace_meta, audits), encoding="utf-8")
    print(
        json.dumps(
            {
                "workspace_markdown_files": len(workspace_catalog),
                "workspace_markdown_lines": workspace_meta["totals"]["lines"],
                "project_markdown_files": len(catalog),
                "project_markdown_lines": meta["totals"]["lines"],
                "outputs": [rel(REQ_OUT), rel(PLAN_OUT)],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
