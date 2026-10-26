"""Build an evidence-conscious, offline project audit and its three canonical views.

This is a snapshot generator, not a release verifier. It never promotes a
requirement from a source path, test path, or editable ledger state.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_DIRS = {".git", ".venv", "venv", "node_modules", "site-packages", "dist", "build", ".data", ".eoip-data", ".hypothesis", ".reva_run", ".tmp", ".pytest_cache", ".mypy_cache", ".ruff_cache", "playwright-report", "test-results", "__pycache__"}
OUTPUTS = {"EOIP-master-requirements.md", "EOIP-master-implementation-plan.md", "EOIP-master-dashboard.html"}
SOURCES = {"requirements-registry.json", "EOIP-programme-registry.json", ".audit-scratch/ledger.json"}
CODE_EXTENSIONS = {".py", ".jsx", ".tsx", ".js", ".ts", ".mjs", ".css", ".sql", ".yaml", ".yml"}
REQUIREMENT_RE = re.compile(r"\b(?:MUST|SHALL|REQUIRED|SHOULD|MAY|must|shall|required)\b")
ID_RE = re.compile(r"\b(?:CRA-\d{3}(?:\.\d+)?|PUR-[A-Z]+-\d{3}|ASPEII-RQ-\d+(?:\.C\d+)?|(?:FR|NFR|SR|GAP|G2|GUI|UI|CAP)-[A-Z0-9.-]+)\b")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def git_revision() -> str:
    result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=False)
    return result.stdout.strip() if result.returncode == 0 else "unknown"


def inventory():
    documents = []
    code = []
    unreadable = []
    seen = 0
    for base, dirs, files in os.walk(ROOT, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in EXCLUDED_DIRS and not (Path(base) / d).is_symlink())
        for name in sorted(files):
            seen += 1
            if seen % 10000 == 0:
                print(f"Scanned {seen:,} filesystem entries; current directory {Path(base).relative_to(ROOT)}", file=sys.stderr, flush=True)
            path = Path(base) / name
            if path.is_symlink():
                continue
            rel = path.relative_to(ROOT).as_posix()
            if rel in OUTPUTS:
                continue
            suffix = path.suffix.lower()
            if suffix not in CODE_EXTENSIONS and suffix != ".md":
                continue
            try:
                data = path.read_bytes()
                text = data.decode("utf-8-sig")
            except (OSError, UnicodeError) as exc:
                unreadable.append({"path": rel, "reason": type(exc).__name__})
                continue
            lines = text.splitlines()
            if suffix == ".md":
                category = "evidence" if rel.startswith(("evidence/", ".audit-scratch/")) else (
                    "requirement" if "requirement" in name.lower() or "specification" in name.lower() else (
                        "implementation" if "implementation" in name.lower() or "plan" in name.lower() else (
                            "research" if rel.startswith(("research/", "EOIP-engg-doc-pkg/competitive-research")) else "guide")))
                headings = []
                normative = 0
                ids = set()
                for number, line in enumerate(lines, 1):
                    if line.startswith("#"):
                        heading = line.lstrip("# ").strip()
                        if heading:
                            headings.append({"line": number, "title": heading[:180]})
                    if REQUIREMENT_RE.search(line):
                        normative += 1
                    ids.update(ID_RE.findall(line))
                documents.append({"path": rel, "category": category, "lines": len(lines), "bytes": len(data),
                                  "sha256": digest(data), "headings": headings, "normative_lines": normative,
                                  "referenced_ids": sorted(ids), "role": "historical" if name in OUTPUTS else "source"})
            else:
                code.append({"path": rel, "lines": len(lines), "bytes": len(data), "sha256": digest(data),
                             "test": rel.startswith(("tests/", "apps/web/tests/", "frontend/tests/"))})
    return documents, code, unreadable


def source_reference(value):
    if not value:
        return ""
    return str(value).strip().strip("`")


def existing_paths(values):
    result = []
    for value in values or []:
        if not isinstance(value, str):
            continue
        path = ROOT / value.strip().strip("`")
        try:
            if path.is_file() and path.resolve().is_relative_to(ROOT):
                result.append(value.replace("\\", "/"))
        except (OSError, ValueError):
            pass
    return result


def build_requirements(raw, programme, ledger):
    ledger_by_id = {x.get("id"): x for x in ledger if isinstance(x, dict)}
    records = {}

    def add(identifier, title, text, source, family, priority, origin, item=None):
        identifier = str(identifier or "").strip()
        if not identifier:
            return
        if identifier in records:
            records[identifier]["also_in"].append(origin)
            return
        item = item or {}
        implementation = item.get("implementation") or {}
        code_paths = existing_paths(item.get("code_paths", []))
        test_paths = existing_paths(item.get("test_files", []))
        claim = ledger_by_id.get(identifier, {})
        receipts = claim.get("receipts") or []
        receipt_state = "none"
        receipt_ref = ""
        if receipts:
            first = receipts[-1]
            receipt_ref = str(first.get("path", ""))
            path = ROOT / receipt_ref
            if path.is_file() and path.resolve().is_relative_to(ROOT):
                actual = digest(path.read_bytes())
                receipt_state = "hash_matches" if first.get("sha256") == actual else "hash_mismatch"
            else:
                receipt_state = "missing"
        reported = str(claim.get("state") or implementation.get("state") or item.get("status") or "UNTRIAGED").upper()
        if reported == "BLOCKED":
            state = "challenged"
        elif reported in {"DEFERRED", "WAIVED", "SUPERSEDED"}:
            state = "disposition_review"
        elif receipt_state in {"missing", "hash_mismatch"}:
            state = "evidence_invalid"
        elif reported in {"ACCEPTED", "VERIFIED"}:
            state = "claimed_accepted"
        elif code_paths:
            state = "code_observed"
        elif reported in {"IMPLEMENTED", "IN_PROGRESS"}:
            state = "claim_only"
        else:
            state = "untriaged"
        reference = source_reference(source)
        records[identifier] = {"id": identifier, "title": str(title or identifier).replace("\n", " ")[:280],
                               "text": str(text or title or ""), "source": reference, "family": str(family or "Other"),
                               "priority": str(priority or "UNSTATED").strip("`"), "origin": origin,
                               "also_in": [], "reported_state": reported, "audit_state": state,
                               "code_paths": code_paths, "test_paths": test_paths,
                               "receipt_state": receipt_state, "receipt_ref": receipt_ref,
                               "acceptance": str((item.get("audit_baseline") or {}).get("acceptance") or ""),
                               "owner": str(implementation.get("primary_package") or item.get("group") or "Unassigned")}

    for item in raw:
        if not isinstance(item, dict):
            continue
        baseline = item.get("audit_baseline") or {}
        add(item.get("id"), item.get("title"), baseline.get("requirement") or item.get("title"),
            baseline.get("source") or item.get("source_path"), item.get("family") or str(item.get("id", "")).split("-")[0],
            item.get("priority") or baseline.get("priority"), "requirements-registry.json", item)
    for item in programme:
        if not isinstance(item, dict):
            continue
        add(item.get("id"), item.get("text") or item.get("title"), item.get("text"), item.get("src"),
            item.get("prog"), item.get("priority"), "EOIP-programme-registry.json", item)
    for item in ledger:
        if not isinstance(item, dict):
            continue
        identifier = item.get("id")
        if identifier in records:
            record = records[identifier]
            record["reported_state"] = str(item.get("state", "UNTRIAGED"))
            record["also_in"].append(".audit-scratch/ledger.json")
            continue
        add(identifier, identifier, "Clause text requires source reconciliation", item.get("origin"),
            item.get("origin") or "Ledger", "UNSTATED", ".audit-scratch/ledger.json", item)
    return sorted(records.values(), key=lambda x: (x["family"], x["id"]))


def findings():
    # These are source observations. The generator does not assert exploitability or full runtime qualification.
    return [
        {"id": "AUD-001", "severity": "high", "area": "Evidence", "title": "Legacy master status promoted paths and editable claims", "detail": "The previous generator treated code plus test paths or an ACCEPTED ledger value as implementation proof. Re-evaluate every prior master completion count.", "source": "scripts/build_master_suite.py", "action": "Use independently observed, profile-bound acceptance evidence and reviewer verification."},
        {"id": "AUD-002", "severity": "high", "area": "Jobs", "title": "Result references are not persisted by durable commit", "detail": "DurableJobStore.commit_job accepts result but the inspected completion update does not store it. A successful status cannot establish a retrievable result.", "source": "packages/eoip/jobs.py:279", "action": "Persist result and receipt references transactionally, reconcile staged artifacts and test restart."},
        {"id": "AUD-003", "severity": "high", "area": "Jobs", "title": "Lease expiry needs a direct stale-worker gate", "detail": "The inspected heartbeat/checkpoint/commit predicates check holder, token and RUNNING but not unexpired lease time before a competing reclaim.", "source": "packages/eoip/jobs.py:231", "action": "Reject stale operations immediately at lease expiry and test before and after reclamation."},
        {"id": "AUD-004", "severity": "medium", "area": "Jobs", "title": "Cross-tenant pending-claim predicate has been corrected in the working tree", "detail": "The current predicate groups PENDING and expired RUNNING before applying tenant_id. This addresses the earlier observed OR-precedence defect; full worker/API isolation still requires verification.", "source": "packages/eoip/jobs.py:166", "action": "Retain regression coverage and qualify tenant scope across queue operations and deployments."},
        {"id": "AUD-005", "severity": "high", "area": "Processing", "title": "Logical operator catalog is broader than runtime integration", "detail": "The working tree registers ten logical units and several backend functions. Registration does not show governed API, durable worker, policy, artifact and model execution for every operator.", "source": "packages/eoip/processing/catalog.py", "action": "Run each operator through the real end-to-end processing contract and preserve receipts."},
        {"id": "AUD-006", "severity": "high", "area": "Processing", "title": "Classical quantum simulator diverges from the planned bounded library path", "detail": "The current backend hand-implements numerical simulation and accepts shots/method through paths needing stronger validation. The QPU specification requires a qualified established simulator and external resource bounds.", "source": "packages/eoip/processing/backends/quantum_sim.py:206", "action": "Enforce caps before allocation and use Qiskit Aer or document an approved revised design with analytic acceptance."},
        {"id": "AUD-007", "severity": "high", "area": "Language", "title": "Query proposals interpolate schema class names", "detail": "A class selected from caller-provided names is interpolated into Cypher, SPARQL and Gremlin strings. The inspected function does not establish identifier escaping or parser validation.", "source": "packages/eoip/processing/backends/text_local.py:184", "action": "Use an authorized schema registry and structured query AST, then validate through the existing parser."},
        {"id": "AUD-008", "severity": "medium", "area": "Language", "title": "Grounded status is based on produced citations", "detail": "The summarizer labels itself grounded when citation entries exist, including fallback text. This is not proof that cited facts answer the query or that the passage was authorized.", "source": "packages/eoip/processing/backends/text_local.py:124", "action": "Verify source authorization and cited span support independently; evaluate abstention."},
        {"id": "AUD-009", "severity": "high", "area": "Privacy", "title": "Application egress checks are not a network boundary", "detail": "The inspected privacy monitor records calls supplied to it. The egress gateway records DLP findings, but the inspected path explicitly denies canary hits. Deployment enforcement and observed network tests remain open.", "source": "packages/eoip/egress/gateway.py:260", "action": "Deny compute-worker egress at the OS/deployment boundary and observe hostile probes externally."},
        {"id": "AUD-010", "severity": "high", "area": "Capability truth", "title": "Editable ledger state can qualify a capability", "detail": "The registry reads local ACCEPTED status strings and require does not require a qualified state for every invocation.", "source": "packages/eoip/capabilities/registry.py:110", "action": "Bind verified receipts to exact profile and make production admission fail on unqualified state."},
        {"id": "AUD-011", "severity": "medium", "area": "Identity", "title": "Alternate frontend supplies a bootstrap principal on whoami failure", "detail": "The alternate frontend creates a bootstrap-admin UI principal after whoami failure. This source observation does not establish backend privilege escalation.", "source": "frontend/src/lib/auth.tsx:56", "action": "Remove the synthesized identity before adopting this frontend into the suite."},
        {"id": "AUD-012", "severity": "medium", "area": "Architecture", "title": "Two frontend implementations need a release decision", "detail": "The current suite plan records two substantial frontends. A screen's presence does not establish that it is the deployed, supported user path.", "source": "docs/EOIP-suite-architecture-plan.md", "action": "Reconcile routes, auth, tests and deployment before publishing a unified help claim."},
        {"id": "AUD-013", "severity": "medium", "area": "User interface", "title": "Graph service label contradicts the active memory backend", "detail": "In a local API run configured with EOIP_GRAPH_BACKEND=memory, the Administration service panel still displayed HugeGraph READY. The UI hard-codes HugeGraph and falls back to READY when stats exist; this can mislead operators about persistence and service health.", "source": "apps/web/src/App.jsx:718", "action": "Bind the service name and health to authoritative backend metadata, remove optimistic READY fallback, and verify the memory and HugeGraph profiles through browser journeys."},
    ]


def markdown_escape(value) -> str:
    return str(value or "").replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ").replace("\r", " ")


def md_link(path: str) -> str:
    value = path.split(":", 1)[0] if re.search(r":\d+$", path) else path
    if value and (ROOT / value).is_file() and not value.startswith(".audit-scratch/"):
        return f"[{markdown_escape(path)}]({value.replace(' ', '%20')})"
    return f"`{markdown_escape(path or 'unresolved')}`"


def generate_requirements(snapshot):
    reqs = snapshot["requirements"]
    documents = snapshot["documents"]
    output = ["# EOIP Master Requirements", "", f"Snapshot: {snapshot['timestamp']}  ",
              f"Source revision: `{snapshot['revision']}`  ", "Status: consolidated audit specification; no feature is certified by this document.", "",
              "## How to read this specification", "",
              "The requirement rows below retain their original IDs, text, source locations and reported states. The generated audit state records what this scan could observe. `claimed_accepted` is a historical ledger claim, `code_observed` means a referenced path exists, and `untriaged` means there is no adequate implementation evidence in this scan. None of these states means independently accepted production behavior.", "",
              "Original Markdown documents remain historical source records. This file is the sole maintained consolidated requirements view; it does not delete or silently supersede source obligations. A change to a source is reconciled by source hash and row ID before acceptance. Unmapped source prose remains visible in the inventory and is an open review task.", "",
              "## Product intent and scope", "",
              "EOIP/KnowGridFlow is a governed knowledge and intelligence platform. The requested suite spans acquisition, graph core, query, ontology, local AI, agents, reports, governance, operations, configuration and developer channels. The suite architecture and each original source retain their detailed domain contracts. Implemented screens, source files and tests are useful leads; they do not alone close a requirement.", "",
              "### Completion rule", "",
              "A requirement is accepted only for a named deployment profile, version and environment after real authorized entrypoint execution, correct persisted effects, negative cases, operational/security checks where applicable, and independently verified evidence. A file path, import, test name, editable ledger state, mock, screenshot or unchecked signature string is not enough. Missing hardware, licenses, credentials or representative data is BLOCKED, never passed.", "",
              "## Audit taxonomy", "",
              "| State | Meaning |", "|---|---|",
              "| `untriaged` | Requirement exists; no accepted outcome was established in this scan. |",
              "| `code_observed` | A referenced code path exists; behavior and integration remain to verify. |",
              "| `claim_only` | A source reports implementation without independently checked completion evidence. |",
              "| `claimed_accepted` | A ledger reports VERIFIED/ACCEPTED; receipt and runtime assertions require independent review. |",
              "| `evidence_invalid` | Referenced receipt is missing or its digest differs. |",
              "| `challenged` | A current ledger reports a blocker. |",
              "| `disposition_review` | Deferred/waived/superseded is a claim awaiting scope authority. |", "",
              "A `not needed` decision requires an authorized disposition, rationale, source IDs, alternative, and impact assessment. The generator never infers it from priority or absence of code.", "",
              "## Cross-cutting requirements", "",
              "1. Bind identity, tenant, workspace, classification and provenance to every request, derived artifact, report and model result. Reauthorize at effect and download time.",
              "2. Preserve deterministic Python-first execution. Use local models only for tasks that require them; deny unapproved external model egress and verify the actual network boundary.",
              "3. Keep the core graph/query product useful without optional GPU, NPU, LLM, quantum or vision dependencies. Report actual backend placement and fallback.",
              "4. Expose only qualified capabilities and real results; distinguish a logical catalog entry from an implemented operator, model quality and hardware support.",
              "5. Preserve the commercial first-party license while inventorying and honoring third-party runtime, model, data and font terms.",
              "6. Use one versioned authorization, job, artifact and evidence authority across portals, API, CLI, MCP, VS Code and agent tools.",
              "7. Make tenant isolation, retention, accessibility, offline installation, recovery, migration and observability measurable release gates.",
              "8. Treat plans, audits, competitive comparisons and roadmap estimates as intent until execution and independent review establish behavior.", "",
              "## Observed gaps and decisions", "",
              "These findings are targeted source observations, not an assertion that every runtime path has been exercised.", ""]
    for f in snapshot["findings"]:
        output.extend([f"### {f['id']} {f['title']}", "", f"Severity: **{f['severity']}**. Area: **{f['area']}**. Source: {md_link(f['source'])}.", "", f["detail"], "", f"Required closure: {f['action']}", ""])
    output.extend(["## Requirement index", "", f"{len(reqs):,} unique IDs from the requirement registry, programme registry and ledger. The original wording below is retained as data, including older claims that need review.", ""])
    families = defaultdict(list)
    for r in reqs:
        families[r["family"]].append(r)
    for family, items in sorted(families.items(), key=lambda x: (-len(x[1]), x[0])):
        output.extend([f"### {markdown_escape(family)} ({len(items):,})", ""])
        for r in items:
            text = markdown_escape(r["text"]).strip()
            output.append(f"- **{r['id']}** [{r['audit_state']}; reported `{r['reported_state']}`; priority {r['priority']}] {text} Source: {md_link(r['source'])}. Owner: `{markdown_escape(r['owner'])}`. Acceptance: {markdown_escape(r['acceptance']) or 'derive an explicit real-world scenario before closure'}. Code leads: {', '.join(md_link(p) for p in r['code_paths'][:3]) or 'none'}. Test leads: {', '.join(md_link(p) for p in r['test_paths'][:3]) or 'none'}. Receipt: `{r['receipt_state']}`.")
        output.append("")
    output.extend(["## Complete Markdown source inventory", "",
                   "Every listed Markdown file was read byte for byte, decoded as UTF-8, and counted line by line at the snapshot time. `normative_lines` and referenced IDs are search signals, not a claim that the line was fully interpreted or implemented. Evidence notes and historical research are indexed separately from active product obligations.", "",
                   "| File | Kind | Lines | Normative signals | SHA-256 |", "|---|---|---:|---:|---|"])
    for doc in documents:
        output.append(f"| {md_link(doc['path'])} | {doc['category']} | {doc['lines']} | {doc['normative_lines']} | `{doc['sha256']}` |")
    output.extend(["", "## Coverage and unresolved review", "",
                   f"Readable Markdown files: **{len(documents):,}**. Unreadable Markdown/source files: **{len(snapshot['unreadable']):,}**. Source code files inventoried: **{len(snapshot['code']):,}**. Registry requirements with a code lead: **{sum(bool(r['code_paths']) for r in reqs):,}**. Independently accepted requirements by this snapshot: **0** (no complete end-to-end certification was performed).", "",
                   "This index is mechanically complete for the discovered Markdown files; human clause reconciliation and product qualification remain open. Source documents can contain additional prose obligations without stable IDs. Those remain review work and are not silently waived. Use the implementation plan's source-line reconciliation gate to close that gap.", ""])
    return "\n".join(output)


def generate_plan(snapshot):
    reqs = snapshot["requirements"]
    output = ["# EOIP Master Implementation Plan", "", f"Snapshot: {snapshot['timestamp']}  ",
              f"Source revision: `{snapshot['revision']}`  ", "Status: work programme and acceptance contract; no phase is declared complete by its presence here.", "",
              "## Operating instructions for a coding agent", "",
              "Read `EOIP-master-requirements.md` and the linked original source for each assigned ID. Recheck the current branch; this snapshot can become stale. Preserve unrelated working-tree changes. Turn one requirement into explicit authorized entrypoints, inputs, outputs, errors, limits, security controls, tests and independent runtime observations. Report blocked work rather than inventing proof.", "",
              "### One requirement at a time", "",
              "1. Pin the source ID, SHA-256 and exact source lines. Resolve duplicate or conflicting text through an ADR. Do not silently choose the easier wording.",
              "2. Identify the owning service/repository in the suite plan. Trace API, worker, storage, UI and external channels. Record code and test paths as leads.",
              "3. Specify the success and denial journey, deployment profile, fixture, expected output, quality measure, resource envelope and applicable security boundary.",
              "4. Implement at the owning boundary, keeping one authority for auth, jobs, graph writes, evidence and artifacts. Add migrations and compatibility where necessary.",
              "5. Run tests plus a real entrypoint through the packaged product. Observe persisted outputs, exact backend placement, authorization and negative cases outside the component under test.",
              "6. Retain a reproducible bundle with source/build/model/config hashes, environment, raw results, failures, reviewer identity, verifier output and expiry. A hash or populated reviewer field is not an independent signature.",
              "7. Promote only the exact accepted profile. Revoke or requalify after code, dependency, model, policy or driver changes. Update this dashboard from source evidence, not manual count edits.", "",
              "## Delivery order", "",
              "| Wave | Ownership | Prerequisites | Required exit observation |", "|---|---|---|---|"]
    waves = [
        ("00", "Inventory, lineage and disagreement resolution", "none", "All Markdown files accounted for; stable IDs, line sources and conflicts reviewed"),
        ("01", "Evidence and capability truth", "00", "Forged/changed/missing receipts rejected by independent verifier; no file-path promotion"),
        ("02", "Identity, tenancy, source ACL and privacy", "00-01", "Cross-tenant and revoked-access end-to-end denials with derived data"),
        ("03", "Durable jobs, artifact authority and recovery", "01-02", "Concurrent claims, stale fences, persisted results and restart reconciliation"),
        ("04", "Graph acquisition, connectors, mappings and data quality", "02-03", "Real source-to-graph counts, provenance, rejected rows and reconciliation"),
        ("05", "Ontology, SHACL, bitemporal graph and governed writes", "02-04", "Actual validation, approved mutation, read-after-write and rollback effects"),
        ("06", "Query dialects, graph traversal and explorer", "02, 05", "Known-answer queries against each advertised backend plus unsupported cases"),
        ("07", "Optional numerical and processing profiles", "02-06", "All ten logical profiles run scoped CPU tasks; accelerators only with physical traces"),
        ("08", "Local models, retrieval, grounded answers and agents", "02-07", "Qualified model tasks, citations, no-egress and delegated action boundaries"),
        ("09", "Reports, analytics and export lifecycle", "02-08", "Snapshot/provenance, scheduled jobs, revocation and downloaded artifact controls"),
        ("10", "Suite portals, MCP, CLI and VS Code", "02-09", "Real user journeys across selected deployed frontend and same APIs"),
        ("11", "Install, license, migration, operations and scale", "00-10", "Clean offline package, restore drills, benchmark and supported topology matrix"),
        ("12", "Independent release acceptance", "all", "All scoped requirements have independently checked current evidence or are visibly blocked/excluded"),
    ]
    for ident, name, prereq, gate in waves:
        output.append(f"| W{ident} | {name} | {prereq} | {gate} |")
    output.extend(["", "## Priority audit repairs", ""])
    for f in snapshot["findings"]:
        output.append(f"- **{f['id']} {f['title']}** ({f['severity']}): {f['action']} Reproduce against {md_link(f['source'])}; retain positive and negative runtime observations.")
    output.extend(["", "## Requirement work queue", "",
                   "This queue retains one row per unique requirement and gives a first owning wave. The wave is a planning aid, not a guarantee of implementation status. Each row inherits the seven-step acceptance procedure above and the original source's detailed constraints.", "",
                   "| ID | Area | Lead wave | Audit state | Reported state | Source | Next proof |", "|---|---|---|---|---|---|---|"])
    wave_by_family = {"PUR": "W07", "UI": "W10", "GUI": "W10", "FR": "W04", "NFR": "W11", "CRA": "W01", "ASPEII": "W02", "GAP": "W00", "G2": "W00", "MS": "W11", "TEST": "W12", "COMPLY": "W11", "REL": "W12"}
    for r in reqs:
        lead = wave_by_family.get(r["family"], "W00")
        if r["id"].startswith("PUR-"):
            unit = r["id"].split("-")[1]
            lead = {"SEC": "W02", "RUN": "W03", "DAT": "W04", "LPU": "W08", "VER": "W12", "INT": "W10", "OPS": "W11"}.get(unit, "W07")
        proof = "reconcile source and design real acceptance" if r["audit_state"] == "untriaged" else (
            "independently verify claim and runtime" if r["audit_state"] == "claimed_accepted" else (
                "reproduce blocked scope or approve disposition" if r["audit_state"] in {"challenged", "disposition_review"} else
                "execute complete entrypoint and negative cases"))
        output.append(f"| `{r['id']}` | {markdown_escape(r['family'])} | {lead} | {r['audit_state']} | `{r['reported_state']}` | {md_link(r['source'])} | {proof} |")
    output.extend(["", "## Independent acceptance matrix", "",
                   "Run API-to-worker-to-store tests, UI/CLI/MCP/VS Code journeys, tenant revocation, crash/retry/cancel races, model task quality, no-egress probes, package/offline install, backup/restore and hardware placement only where advertised. Record observed outcomes and raw artifacts for every supported OS, backend, tenancy and model profile.", "",
                   "A focused passing test is evidence for that tested behavior only. Skipped hardware, missing customer integrations, unrun scale targets, unavailable vendor credentials and missing task datasets remain BLOCKED. Performance numbers require equal work, precision, environment and raw samples. A `not needed` decision requires an authorized rationale, alternative and impact record.", "",
                   "## Source reconciliation and change control", "",
                   "The source inventory in the master requirements lists every readable Markdown file with line count and hash. For each `requirement` document and any guide/research file containing normative signals, review every line against registry IDs. Add orphan clauses, resolve collisions and record deliberate dispositions. Compare file hashes on every rebuild; changed sources invalidate the previous mapping until reviewed. Historic files stay discoverable and unmodified.", "",
                   "The existing `requirements-registry.json` and `EOIP-programme-registry.json` remain machine input records. This plan and the master requirements are the only maintained consolidated Markdown pair. The HTML dashboard is the single project tracker. Neither the generated documents nor the dashboard should be used to edit an acceptance ledger directly.", ""])
    return "\n".join(output)


def payload_json(value):
    return json.dumps(value, ensure_ascii=True, separators=(",", ":")).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")


def generate_html(snapshot):
    compact = {key: snapshot[key] for key in ("timestamp", "revision", "documents", "requirements", "findings", "stats", "unreadable", "checks")}
    data = payload_json(compact)
    return DASHBOARD_TEMPLATE.replace("__DATA__", data)


def snapshot():
    documents, code, unreadable = inventory()
    raw = read_json(ROOT / "requirements-registry.json", [])
    programme = read_json(ROOT / "EOIP-programme-registry.json", {}).get("items", [])
    ledger = read_json(ROOT / ".audit-scratch/ledger.json", {}).get("items", [])
    requirements = build_requirements(raw, programme, ledger)
    checks = []
    for source in sorted(SOURCES):
        path = ROOT / source
        checks.append({"name": source, "result": "read" if path.is_file() else "missing", "sha256": digest(path.read_bytes()) if path.is_file() else ""})
    states = Counter(x["audit_state"] for x in requirements)
    categories = Counter(x["category"] for x in documents)
    return {"timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"), "revision": git_revision(),
            "documents": documents, "code": code, "unreadable": unreadable, "requirements": requirements,
            "findings": findings(), "checks": checks,
            "stats": {"documents": len(documents), "lines": sum(x["lines"] for x in documents),
                      "code_files": len(code), "code_lines": sum(x["lines"] for x in code),
                      "requirements": len(requirements), "states": dict(states), "categories": dict(categories),
                      "source_leads": sum(bool(x["code_paths"]) for x in requirements),
                      "test_leads": sum(bool(x["test_paths"]) for x in requirements),
                      "independently_accepted": 0}}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Scan and report counts without writing")
    args = parser.parse_args()
    data = snapshot()
    if not args.check:
        outputs = {
            "EOIP-master-requirements.md": generate_requirements(data),
            "EOIP-master-implementation-plan.md": generate_plan(data),
            "EOIP-master-dashboard.html": generate_html(data),
        }
        for name, content in outputs.items():
            target = ROOT / name
            staged = target.with_name(target.name + ".audit-tmp")
            staged.write_text("\n".join(line.rstrip() for line in content.splitlines()) + "\n", encoding="utf-8", newline="\n")
            staged.replace(target)
    print(json.dumps({"timestamp": data["timestamp"], "revision": data["revision"],
                      "stats": data["stats"], "unreadable": data["unreadable"], "written": [] if args.check else sorted(OUTPUTS)}, indent=2))
    return 0 if not data["unreadable"] else 2


DASHBOARD_TEMPLATE = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:; connect-src 'none'; object-src 'none'; base-uri 'none'">
<title>EOIP project status</title>
<style>
:root{color-scheme:light;--bg:#f5f8fb;--paper:#fff;--ink:#172332;--muted:#52677a;--line:#dce6ed;--blue:#1768a5;--green:#138764;--amber:#a9650c;--red:#bd444c;--teal:#118798;--violet:#7559a7;--shadow:0 2px 10px #23405b0d;font-family:Inter,Segoe UI,Arial,sans-serif;font-size:14px}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink)}button,input,select{font:inherit}button{cursor:pointer}a{color:var(--blue)}:focus-visible{outline:3px solid #e49524;outline-offset:2px}.shell{max-width:1620px;margin:auto;padding:0 24px 38px}.top{background:var(--paper);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:30;box-shadow:var(--shadow)}.top-inner{max-width:1620px;margin:auto;padding:15px 24px;display:flex;gap:24px;align-items:center;justify-content:space-between}.brand{display:flex;align-items:center;gap:12px}.brand-mark{width:40px;height:40px;border-radius:7px;display:grid;place-items:center;background:#1768a5;color:white;font-weight:800}.brand h1{font-size:18px;line-height:1.15;margin:0;font-weight:760}.brand p{font-size:12px;color:var(--muted);margin:3px 0 0}.top-meta{display:flex;align-items:center;gap:12px;color:var(--muted);font-size:12px}.pill{display:inline-flex;align-items:center;gap:6px;border:1px solid var(--line);background:white;border-radius:4px;padding:4px 8px;font-weight:650}.dot{width:7px;height:7px;border-radius:50%;background:var(--amber)}.nav{display:flex;gap:3px;overflow:auto;padding:0 24px;max-width:1620px;margin:auto;scrollbar-width:thin}.tab{display:flex;align-items:center;gap:7px;border:0;border-bottom:3px solid transparent;background:transparent;color:var(--muted);padding:13px 15px 11px;white-space:nowrap;font-weight:650}.tab:hover{background:#f1f7fb;color:var(--ink)}.tab.active{border-color:var(--blue);color:var(--blue);background:#f6faff}.tab svg,.icon-btn svg{width:16px;height:16px;stroke:currentColor;stroke-width:2;fill:none;stroke-linecap:round;stroke-linejoin:round}.section{animation:appear .24s ease both}@keyframes appear{from{opacity:.45;transform:translateY(5px)}to{opacity:1;transform:translateY(0)}}@media(prefers-reduced-motion:reduce){*,*:before,*:after{animation:none!important;transition:none!important;scroll-behavior:auto!important}}
.heading{display:flex;align-items:end;justify-content:space-between;gap:16px;margin:26px 0 17px}.heading h2{font-size:23px;margin:0 0 4px;letter-spacing:0}.heading p{color:var(--muted);margin:0;max-width:850px}.stamp{color:var(--muted);font-size:12px;white-space:nowrap}.notice{background:#fff9e8;border-left:4px solid #d89924;padding:12px 16px;margin:0 0 18px;line-height:1.55}.notice strong{color:#714a07}.kpis{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px;margin:0 0 18px}.kpi{border:1px solid var(--line);background:var(--paper);padding:15px 17px;min-height:102px;box-shadow:var(--shadow)}.kpi-label{text-transform:uppercase;color:var(--muted);font-weight:720;font-size:11px}.kpi-value{font-size:29px;line-height:1.1;font-weight:780;margin:8px 0 3px;font-variant-numeric:tabular-nums}.kpi-note{color:var(--muted);font-size:12px}.split{display:grid;grid-template-columns:minmax(0,1.45fr) minmax(280px,.85fr);gap:16px}.panel{border:1px solid var(--line);background:var(--paper);padding:18px;margin-bottom:16px;min-width:0}.panel h3{font-size:15px;margin:0 0 4px}.panel p{color:var(--muted);margin:0 0 14px}.panel-head{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:12px}.bars{display:grid;gap:12px}.bar-row{display:grid;grid-template-columns:165px 1fr 52px;gap:12px;align-items:center;font-size:12px}.bar-row strong{font-weight:650}.track{height:9px;border-radius:4px;background:#eaf0f4;overflow:hidden}.fill{height:100%;border-radius:4px;background:var(--blue);transition:width .5s}.mono{font-family:Consolas,SFMono-Regular,monospace;font-size:12px}.toolbar{display:flex;gap:9px;align-items:center;flex-wrap:wrap;margin:0 0 12px}.search{flex:1;min-width:220px;max-width:500px}.search,select{border:1px solid #cddde7;border-radius:4px;background:white;color:var(--ink);padding:9px 10px;min-height:38px}.action{border:1px solid #bfced8;background:white;color:var(--ink);border-radius:4px;padding:8px 11px;min-height:38px;display:inline-flex;align-items:center;gap:7px;font-weight:620}.action:hover{background:#eef7fc}.action.primary{background:var(--blue);border-color:var(--blue);color:white}.action.primary:hover{background:#0f527f}.table-wrap{overflow:auto;border:1px solid var(--line);background:white}.data-table{width:100%;border-collapse:collapse;min-width:760px}.data-table th{background:#eef4f8;text-align:left;color:#344a5a;font-size:11px;text-transform:uppercase;letter-spacing:0;padding:10px 12px;position:sticky;top:0;z-index:1}.data-table td{border-top:1px solid #e8eef2;padding:10px 12px;vertical-align:top;line-height:1.4}.data-table tbody tr:hover{background:#f7fbfd}.data-table .title-cell{min-width:250px}.rowbtn{border:0;background:none;color:var(--blue);text-align:left;font-weight:670;padding:0}.rowbtn:hover{text-decoration:underline}.status{font-size:11px;font-weight:700;white-space:nowrap;padding:4px 6px;border-radius:3px;display:inline-block}.status.untriaged{background:#eef2f5;color:#4f6070}.status.code_observed{background:#e9f2fa;color:#155884}.status.claimed_accepted{background:#f6f0e2;color:#89600e}.status.challenged,.status.evidence_invalid{background:#fbecea;color:#a53d38}.status.claim_only,.status.disposition_review{background:#f1eaf8;color:#6b4e88}.pager{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:12px 0;color:var(--muted);font-size:12px}.pager button{min-width:34px}.detail{position:fixed;z-index:50;inset:0;background:#17233280;display:flex;justify-content:flex-end}.detail[hidden],.section[hidden]{display:none}.drawer{width:min(620px,100%);height:100%;overflow:auto;background:white;box-shadow:-8px 0 30px #0002;padding:24px}.drawer header{display:flex;justify-content:space-between;align-items:start;gap:12px;border-bottom:1px solid var(--line);padding-bottom:15px;margin-bottom:17px}.drawer h2{font-size:19px;margin:0}.drawer p{line-height:1.58}.drawer dl{display:grid;grid-template-columns:130px 1fr;gap:10px;border-top:1px solid var(--line);padding-top:15px}.drawer dt{color:var(--muted)}.drawer dd{margin:0;min-width:0;overflow-wrap:anywhere}.drawer .full{grid-column:1/-1}.tag{font-size:11px;background:#eff4f7;border:1px solid var(--line);border-radius:3px;padding:3px 6px;display:inline-block;margin:2px}.risk-list{display:grid;gap:9px}.risk{display:grid;grid-template-columns:74px 1fr;gap:12px;padding:13px 0;border-top:1px solid var(--line)}.risk h4{margin:0 0 4px;font-size:13px}.risk p{margin:0;font-size:12px}.sev{font-size:11px;text-transform:uppercase;font-weight:750}.sev.high{color:var(--red)}.sev.medium{color:var(--amber)}.notes{font-size:12px;color:var(--muted);padding:10px 0}.legend{display:flex;flex-wrap:wrap;gap:7px}.tiny{font-size:12px;color:var(--muted)}.checklist{list-style:none;padding:0;margin:0}.checklist li{border-top:1px solid var(--line);padding:10px 0;display:flex;gap:10px}.checklist li:first-child{border-top:0}.check-dot{width:9px;height:9px;background:#d89924;border-radius:50%;margin-top:6px;flex:none}.empty{padding:28px;text-align:center;color:var(--muted)}.source-path{overflow-wrap:anywhere}.spark{display:flex;gap:2px;height:32px;align-items:end}.spark i{width:6px;background:#55a0ba;display:block;border-radius:2px 2px 0 0}.footer{color:var(--muted);font-size:12px;padding:20px 0}
@media(max-width:980px){.kpis{grid-template-columns:repeat(3,minmax(0,1fr))}.split{grid-template-columns:1fr}.top-meta .stamp{display:none}}@media(max-width:640px){.shell{padding:0 13px 25px}.top-inner{padding:12px 13px}.nav{padding:0 8px}.tab{padding:11px 12px}.heading{align-items:start;flex-direction:column}.heading h2{font-size:21px}.kpis{grid-template-columns:repeat(2,minmax(0,1fr))}.bar-row{grid-template-columns:120px 1fr 38px}.top-meta{display:none}.panel{padding:14px}.drawer{padding:16px}}
.split{align-items:start}
</style>
</head>
<body>
<header class="top"><div class="top-inner"><div class="brand"><div class="brand-mark" aria-hidden="true">K</div><div><h1>KnowGridFlow <span style="color:#7990a1;font-weight:500">/ EOIP</span></h1><p>Project audit and delivery tracker</p></div></div><div class="top-meta"><span class="pill"><i class="dot"></i>Evidence review pending</span><span id="headstamp"></span></div></div><nav class="nav" aria-label="Dashboard sections" id="nav"></nav></header>
<main class="shell" id="main"></main>
<div class="detail" id="detail" hidden><div class="drawer" role="dialog" aria-modal="true" aria-labelledby="drawer-title"><header><div><p class="tiny" id="drawer-kicker"></p><h2 id="drawer-title"></h2></div><button class="action" id="drawer-close" aria-label="Close details">Close</button></header><div id="drawer-body"></div></div></div>
<script id="audit-data" type="application/json">__DATA__</script>
<script>
const DATA=JSON.parse(document.getElementById('audit-data').textContent);
const ICON={overview:'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',requirements:'<path d="M4 4h16v16H4zM8 9h8M8 13h8M8 17h5"/>',gaps:'<path d="M12 3 2 21h20L12 3zM12 9v5M12 17h.01"/>',delivery:'<path d="M4 19V5m5 14V9m5 10V3m5 16v-7"/>',evidence:'<path d="M12 2 3 6v6c0 5 3.5 8 9 10 5.5-2 9-5 9-10V6l-9-4zM8 12l3 3 5-6"/>',sources:'<path d="M5 3h10l4 4v14H5zM15 3v5h4M8 12h8M8 16h8"/>',architecture:'<rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="8" y="14" width="8" height="7"/><path d="M6 10v4h6m6-4v4h-6"/>',checks:'<path d="M4 12l5 5L20 6"/>',decisions:'<circle cx="12" cy="12" r="9"/><path d="M12 8v4M12 16h.01"/>'};
const TABS=[['overview','Overview'],['requirements','Requirements'],['gaps','Gaps & risks'],['delivery','Delivery'],['evidence','Evidence'],['sources','Sources'],['architecture','Architecture'],['checks','Checks'],['decisions','Decisions']];
const ui={tab:'overview',query:'',state:'all',family:'all',page:0,sourceQuery:'',sourceKind:'all',sourcePage:0,gapFilter:'all'};
const $=id=>document.getElementById(id);const e=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function icon(name){return '<svg viewBox="0 0 24 24" aria-hidden="true">'+ICON[name]+'</svg>'}
function fmt(n){return Number(n||0).toLocaleString()}
function section(title,description,content){return '<section class="section"><div class="heading"><div><h2>'+e(title)+'</h2><p>'+e(description)+'</p></div><div class="stamp">Snapshot '+e(DATA.timestamp.replace('T',' ').replace('+00:00',' UTC'))+'</div></div>'+content+'</section>'}
function panel(title,description,body){return '<div class="panel"><h3>'+e(title)+'</h3><p>'+e(description)+'</p>'+body+'</div>'}
function status(value){return '<span class="status '+e(value)+'">'+e(value.replaceAll('_',' '))+'</span>'}
function bars(values,colors){let max=Math.max(1,...values.map(v=>v[1]));return '<div class="bars">'+values.map(([name,count],i)=>'<div class="bar-row"><strong>'+e(name.replaceAll('_',' '))+'</strong><div class="track"><div class="fill" style="width:'+Math.max(2,count/max*100)+'%;background:'+colors[i%colors.length]+'"></div></div><span class="mono">'+fmt(count)+'</span></div>').join('')+'</div>'}
function overview(){const s=DATA.stats,states=Object.entries(s.states).sort((a,b)=>b[1]-a[1]);let top=DATA.findings.filter(f=>f.severity==='high').slice(0,5);return section('Project status','Requirements, source coverage and accepted evidence at this snapshot.',
'<div class="notice"><strong>Completion is not certified.</strong> Reported ACCEPTED states and code/test paths are leads for review. This scan has not independently qualified the whole product. Local working-tree changes may be newer than the snapshot.</div>'+ 
'<div class="kpis"><div class="kpi"><div class="kpi-label">Requirements indexed</div><div class="kpi-value">'+fmt(s.requirements)+'</div><div class="kpi-note">Unique IDs across registries</div></div><div class="kpi"><div class="kpi-label">Markdown read</div><div class="kpi-value">'+fmt(s.documents)+'</div><div class="kpi-note">'+fmt(s.lines)+' lines inventoried</div></div><div class="kpi"><div class="kpi-label">Code files inventoried</div><div class="kpi-value">'+fmt(s.code_files)+'</div><div class="kpi-note">Existence is not completion</div></div><div class="kpi"><div class="kpi-label">High-risk findings</div><div class="kpi-value" style="color:var(--red)">'+fmt(DATA.findings.filter(f=>f.severity==='high').length)+'</div><div class="kpi-note">Targeted source observations</div></div><div class="kpi"><div class="kpi-label">Independently accepted</div><div class="kpi-value" style="color:var(--amber)">'+fmt(s.independently_accepted)+'</div><div class="kpi-note">By this snapshot audit</div></div></div>'+ 
'<div class="split">'+panel('Audit states','These categories describe available evidence, not completion.',bars(states,['#1768a5','#bd8a27','#8058a8','#bd444c','#138764']))+panel('Priority attention','Open a finding for its source and closure path.','<div class="risk-list">'+top.map(f=>'<div class="risk"><span class="sev '+e(f.severity)+'">'+e(f.severity)+'</span><div><h4><button class="rowbtn" data-detail="finding" data-id="'+e(f.id)+'">'+e(f.title)+'</button></h4><p>'+e(f.area)+' / '+e(f.id)+'</p></div></div>').join('')+'</div>')+'</div>'+ 
'<div class="split">'+panel('Source mix','Requirements, plans, guides, research and evidence notes are counted separately.',bars(Object.entries(s.categories).sort((a,b)=>b[1]-a[1]),['#118798','#7559a7','#1768a5','#db9742','#84a5b3']))+panel('Audit scope','The dashboard is a local, read-only snapshot. Working notes are stored only in this browser.','<ul class="checklist"><li><i class="check-dot"></i><span>All discovered project Markdown files were read and hashed line by line.</span></li><li><i class="check-dot"></i><span>Requirement statuses preserve the original claim and a separate audit state.</span></li><li><i class="check-dot"></i><span>Unmapped prose and unrun product journeys remain open review work.</span></li></ul>')+'</div>')}
function reqRows(items){return items.map(r=>'<tr><td class="mono"><button class="rowbtn mono" data-detail="requirement" data-id="'+e(r.id)+'">'+e(r.id)+'</button></td><td class="title-cell">'+e(r.title)+'</td><td>'+e(r.family)+'</td><td>'+status(r.audit_state)+'</td><td class="mono">'+e(r.reported_state)+'</td><td>'+e(r.priority)+'</td></tr>').join('')}
function pager(kind,page,total,pageSize){let pages=Math.max(1,Math.ceil(total/pageSize));return '<div class="pager"><span>'+fmt(total)+' results / page '+(page+1)+' of '+pages+'</span><div><button class="action" data-page="'+kind+'" data-offset="-1" '+(page===0?'disabled':'')+' aria-label="Previous page">Previous</button> <button class="action" data-page="'+kind+'" data-offset="1" '+(page>=pages-1?'disabled':'')+' aria-label="Next page">Next</button></div></div>'}
function requirements(){let families=[...new Set(DATA.requirements.map(r=>r.family))].sort();let values=DATA.requirements.filter(r=>(ui.state==='all'||r.audit_state===ui.state)&&(ui.family==='all'||r.family===ui.family)&&(!ui.query||[r.id,r.title,r.text,r.source,r.owner].join(' ').toLowerCase().includes(ui.query.toLowerCase())));let page=Math.min(ui.page,Math.max(0,Math.ceil(values.length/40)-1));ui.page=page;return section('Requirements','Search original IDs, wording and source leads. Open a row for the full available detail.',
'<div class="toolbar"><input class="search" id="req-search" type="search" aria-label="Search requirements" placeholder="Search ID, title, wording or source" value="'+e(ui.query)+'"><select id="req-state" aria-label="Filter by audit state"><option value="all">All audit states</option>'+Object.keys(DATA.stats.states).sort().map(x=>'<option value="'+e(x)+'" '+(ui.state===x?'selected':'')+'>'+e(x.replaceAll('_',' '))+'</option>').join('')+'</select><select id="req-family" aria-label="Filter by requirement family"><option value="all">All areas</option>'+families.map(x=>'<option value="'+e(x)+'" '+(ui.family===x?'selected':'')+'>'+e(x)+'</option>').join('')+'</select><button class="action" id="req-export">Export filtered CSV</button></div>'+ 
'<div class="table-wrap"><table class="data-table"><thead><tr><th>ID</th><th>Requirement</th><th>Area</th><th>Audit state</th><th>Reported</th><th>Priority</th></tr></thead><tbody>'+reqRows(values.slice(page*40,(page+1)*40))+'</tbody></table></div>'+pager('requirement',page,values.length,40)+'<p class="notes">A code path, test file or receipt hash is navigational evidence only. Open a row to see the distinction.</p>')}
function gaps(){let fs=DATA.findings.filter(f=>ui.gapFilter==='all'||f.severity===ui.gapFilter);return section('Gaps and risks','Targeted observations from the current source snapshot, with a concrete closure action.',
'<div class="toolbar"><select id="gap-filter" aria-label="Filter findings"><option value="all">All severities</option><option value="high" '+(ui.gapFilter==='high'?'selected':'')+'>High</option><option value="medium" '+(ui.gapFilter==='medium'?'selected':'')+'>Medium</option></select><span class="tiny">'+fs.length+' findings</span></div>'+ 
'<div class="panel"><div class="risk-list">'+fs.map(f=>'<div class="risk"><div class="sev '+e(f.severity)+'">'+e(f.severity)+'<div class="mono">'+e(f.id)+'</div></div><div><h4><button class="rowbtn" data-detail="finding" data-id="'+e(f.id)+'">'+e(f.title)+'</button></h4><p>'+e(f.detail)+'</p><p style="margin-top:7px"><strong>Next:</strong> '+e(f.action)+'</p><p class="tiny" style="margin-top:5px">'+e(f.source)+'</p></div></div>').join('')+'</div></div>')}
const WAVES=[['00','Inventory and source reconciliation'],['01','Evidence and capability truth'],['02','Identity, tenancy and privacy'],['03','Durable jobs and artifacts'],['04','Acquisition and quality'],['05','Ontology and governed graph writes'],['06','Query and explorer'],['07','Processing profiles'],['08','Local models, retrieval and agents'],['09','Reports and exports'],['10','Suite portals and channels'],['11','Distribution and operations'],['12','Independent release acceptance']];
function delivery(){let counts={};for(const r of DATA.requirements){let x=r.family==='PUR'?'W07':({'UI':'W10','GUI':'W10','FR':'W04','NFR':'W11','CRA':'W01','ASPEII':'W02','GAP':'W00','G2':'W00','MS':'W11','TEST':'W12'}[r.family]||'W00');if(r.id.startsWith('PUR-'))x=({'SEC':'W02','RUN':'W03','DAT':'W04','LPU':'W08','VER':'W12','INT':'W10','OPS':'W11'}[r.id.split('-')[1]]||'W07');counts[x]=(counts[x]||0)+1}return section('Delivery work','A practical order for closing gaps. Counts are assigned work, not completed work.','<div class="panel"><div class="table-wrap"><table class="data-table"><thead><tr><th>Wave</th><th>Responsibility</th><th>Assigned IDs</th><th>Gate</th></tr></thead><tbody>'+WAVES.map(([n,title])=>'<tr><td class="mono">W'+n+'</td><td>'+e(title)+'</td><td>'+fmt(counts['W'+n]||0)+'</td><td>Real workflow + independent evidence</td></tr>').join('')+'</tbody></table></div></div><p class="tiny">Read the master implementation plan for prerequisites, per-ID rows and acceptance steps.</p>')}
function evidence(){let values=Object.entries(DATA.stats.states);let invalid=DATA.requirements.filter(r=>r.receipt_state==='missing'||r.receipt_state==='hash_mismatch').length;return section('Evidence and confidence','Reported states are preserved, while this audit treats acceptance as unverified until an independent end-to-end review.',
'<div class="kpis"><div class="kpi"><div class="kpi-label">Claimed accepted</div><div class="kpi-value">'+fmt(DATA.stats.states.claimed_accepted||0)+'</div><div class="kpi-note">Ledger reported state</div></div><div class="kpi"><div class="kpi-label">Invalid receipt refs</div><div class="kpi-value">'+fmt(invalid)+'</div><div class="kpi-note">Missing or hash mismatch</div></div><div class="kpi"><div class="kpi-label">Code path leads</div><div class="kpi-value">'+fmt(DATA.stats.source_leads)+'</div><div class="kpi-note">No completion inference</div></div><div class="kpi"><div class="kpi-label">Test path leads</div><div class="kpi-value">'+fmt(DATA.stats.test_leads)+'</div><div class="kpi-note">No test execution inferred</div></div><div class="kpi"><div class="kpi-label">Accepted in this audit</div><div class="kpi-value">0</div><div class="kpi-note">Full product gate not run</div></div></div>'+ 
panel('Evidence ladder','Each step needs a verified artifact and a specific scope.','<ol class="checklist"><li><i class="check-dot"></i><span>Source and test paths lead to an implementation candidate.</span></li><li><i class="check-dot"></i><span>Run the installed application through an authorized user journey and observe correct outputs and denied cases.</span></li><li><i class="check-dot"></i><span>Bind the receipt to exact code, deployment, model, policy, data and environment versions.</span></li><li><i class="check-dot"></i><span>Independent verifier reviews raw outputs, signature trust and stale/forged evidence attempts.</span></li><li><i class="check-dot"></i><span>Promote only the tested profile and publish limits and residual gaps.</span></li></ol>')+panel('State distribution','The counts below are audit categories, not percent complete.',bars(values,['#1768a5','#bd8a27','#8058a8','#bd444c','#138764']))) }
function sources(){let values=DATA.documents.filter(d=>(ui.sourceKind==='all'||d.category===ui.sourceKind)&&(!ui.sourceQuery||d.path.toLowerCase().includes(ui.sourceQuery.toLowerCase())||d.headings.some(h=>h.title.toLowerCase().includes(ui.sourceQuery.toLowerCase()))));let page=Math.min(ui.sourcePage,Math.max(0,Math.ceil(values.length/35)-1));ui.sourcePage=page;let kinds=[...new Set(DATA.documents.map(d=>d.category))].sort();return section('Markdown sources','Every readable Markdown file is indexed with its line count and digest. Open a file to inspect headings and referenced IDs.',
'<div class="toolbar"><input class="search" id="source-search" type="search" aria-label="Search source files" placeholder="Search path or heading" value="'+e(ui.sourceQuery)+'"><select id="source-kind" aria-label="Filter source kind"><option value="all">All document kinds</option>'+kinds.map(x=>'<option value="'+e(x)+'" '+(ui.sourceKind===x?'selected':'')+'>'+e(x)+'</option>').join('')+'</select></div>'+ 
'<div class="table-wrap"><table class="data-table"><thead><tr><th>File</th><th>Kind</th><th>Lines</th><th>Normative signals</th><th>Digest</th></tr></thead><tbody>'+values.slice(page*35,(page+1)*35).map(d=>'<tr><td class="source-path"><button class="rowbtn" data-detail="source" data-id="'+e(d.path)+'">'+e(d.path)+'</button></td><td>'+e(d.category)+'</td><td>'+fmt(d.lines)+'</td><td>'+fmt(d.normative_lines)+'</td><td class="mono">'+e(d.sha256.slice(0,12))+'</td></tr>').join('')+'</tbody></table></div>'+pager('source',page,values.length,35)+'<p class="notes">Normative signals are word matches; some are quotation or historical text. Human clause reconciliation remains open.</p>')}
function architecture(){return section('Architecture','The working application and planned suite share a governed platform. A source module does not establish a deployed service.',
'<div class="split">'+panel('Current code areas','Inspected source paths that inform the audit.','<div class="bars">'+[['API and worker','apps/api / apps/worker'],['Knowledge core','packages/eoip/graph / query'],['Identity and policy','packages/eoip/authz / tenancy'],['Processing','packages/eoip/processing'],['User interface','apps/web and frontend'],['Developer channels','apps/mcp / apps/vscode-extension']].map(x=>'<div class="bar-row" style="grid-template-columns:150px 1fr"><strong>'+e(x[0])+'</strong><span class="mono">'+e(x[1])+'</span></div>').join('')+'</div>')+panel('Suite destinations','Portal boundaries from the existing architecture plan.','<div class="legend">'+['Home','Configuration','Administration','Database','Query','Explorer','Reports','Integration','Ontology','Catalog','Automation','Governance','Wisdom','Models','Operations','Developers','Extensions','Fleet'].map(x=>'<span class="tag">'+e(x)+'</span>').join('')+'</div><p class="notes">Future destinations are not automatically separate deployed apps.</p>')+'</div>'+panel('Processing truth','The ten requested processing labels identify workload profiles. Physical acceleration is optional and requires device-specific acceptance.','<div class="legend">'+['CPU','GPU','TPU','NPU','DPU','QPU simulation','APU','LPU','IPU','VPU'].map(x=>'<span class="tag">'+e(x)+'</span>').join('')+'</div>'))}
function checks(){return section('Audit checks','Snapshot source files and inventory health. This is a structural scan, not an application test run.',
'<div class="panel"><div class="table-wrap"><table class="data-table"><thead><tr><th>Input</th><th>Read</th><th>SHA-256</th></tr></thead><tbody>'+DATA.checks.map(x=>'<tr><td class="mono">'+e(x.name)+'</td><td>'+e(x.result)+'</td><td class="mono">'+e(x.sha256)+'</td></tr>').join('')+'</tbody></table></div></div>'+panel('Read failures','Unreadable files must be reconciled before any full-source claim.',DATA.unreadable.length?DATA.unreadable.map(x=>'<p>'+e(x.path)+' / '+e(x.reason)+'</p>').join(''):'<p>No unreadable source files in this inventory.</p>')+panel('Verification still needed','The next audit run must execute these real journeys.','<div class="legend">'+['Tenant boundaries','Durable jobs','Graph backend parity','Local model quality','No-egress','UI accessibility','MCP delegation','Restore','Offline install','Physical acceleration'].map(x=>'<span class="tag">'+e(x)+'</span>').join('')+'</div>'))}
function decisions(){return section('Decisions and notes','Local working notes do not change audited states or repository files.',panel('Open decisions','Record a short local note, then export it for review.','<div class="toolbar"><select id="decision-kind" aria-label="Decision area"><option>Architecture</option><option>Security</option><option>Product scope</option><option>Evidence</option><option>Deployment</option></select><input class="search" id="decision-text" maxlength="400" placeholder="Decision or question for review" aria-label="Decision or question"><button class="action primary" id="decision-add">Add note</button><button class="action" id="decision-export">Export notes</button></div><div id="decision-notes"></div>')+panel('Scope rules','A not-needed or superseded requirement needs an explicit authorized disposition. A blocked requirement needs its missing dependency and a retest condition.','<p>Notes in this browser are draft planning annotations and never promote acceptance.</p>'))}
const VIEWS={overview,requirements,gaps,delivery,evidence,sources,architecture,checks,decisions};
function nav(){ $('nav').innerHTML=TABS.map(([id,title])=>'<button class="tab '+(ui.tab===id?'active':'')+'" data-tab="'+id+'" aria-current="'+(ui.tab===id?'page':'false')+'">'+icon(id)+e(title)+'</button>').join('') }
function render(preserveFocus){let active=preserveFocus?document.activeElement?.id:null;let caret=active&&document.activeElement?.selectionStart;nav();$('main').innerHTML=VIEWS[ui.tab]();if(ui.tab==='decisions')renderNotes();if(active&&$(active)){let el=$(active);el.focus();if(typeof caret==='number'&&el.setSelectionRange)el.setSelectionRange(caret,caret)}}
function openDetail(type,id){let item=type==='requirement'?DATA.requirements.find(x=>x.id===id):type==='source'?DATA.documents.find(x=>x.path===id):DATA.findings.find(x=>x.id===id);if(!item)return;$('drawer-kicker').textContent=type.toUpperCase();$('drawer-title').textContent=item.title||item.path||item.id;let body='';if(type==='requirement'){body='<p>'+e(item.text)+'</p><dl><dt>Identifier</dt><dd class="mono">'+e(item.id)+'</dd><dt>Audit state</dt><dd>'+status(item.audit_state)+'</dd><dt>Reported state</dt><dd>'+e(item.reported_state)+'</dd><dt>Priority</dt><dd>'+e(item.priority)+'</dd><dt>Owner lead</dt><dd>'+e(item.owner)+'</dd><dt>Source</dt><dd class="mono">'+e(item.source||'unresolved')+'</dd><dt>Acceptance text</dt><dd>'+e(item.acceptance||'Requires explicit scenario')+'</dd><dt>Code leads</dt><dd>'+e(item.code_paths.join(', ')||'none')+'</dd><dt>Test leads</dt><dd>'+e(item.test_paths.join(', ')||'none')+'</dd><dt>Receipt ref</dt><dd>'+e(item.receipt_ref||'none')+'</dd><dt>Receipt check</dt><dd>'+e(item.receipt_state)+'</dd></dl><p class="notes">This row has not been accepted by this dashboard audit.</p>'}else if(type==='source'){body='<dl><dt>Kind</dt><dd>'+e(item.category)+'</dd><dt>Lines</dt><dd>'+fmt(item.lines)+'</dd><dt>Bytes</dt><dd>'+fmt(item.bytes)+'</dd><dt>SHA-256</dt><dd class="mono">'+e(item.sha256)+'</dd><dt>Normative signals</dt><dd>'+fmt(item.normative_lines)+'</dd><dt class="full">Headings</dt><dd class="full">'+(item.headings.slice(0,80).map(h=>'<div class="tiny">'+h.line+' '+e(h.title)+'</div>').join('')||'No headings')+'</dd><dt class="full">Referenced IDs</dt><dd class="full">'+(item.referenced_ids.slice(0,100).map(x=>'<span class="tag">'+e(x)+'</span>').join('')||'none')+'</dd></dl>'}else{body='<p>'+e(item.detail)+'</p><dl><dt>Severity</dt><dd>'+e(item.severity)+'</dd><dt>Area</dt><dd>'+e(item.area)+'</dd><dt>Source</dt><dd class="mono">'+e(item.source)+'</dd><dt>Closure action</dt><dd>'+e(item.action)+'</dd></dl>'}$('drawer-body').innerHTML=body;$('detail').hidden=false;$('drawer-close').focus()}
function closeDetail(){$('detail').hidden=true}
function csv(values){let headers=['id','family','title','audit_state','reported_state','priority','source','code_paths','test_paths','receipt_state'];return [headers.join(','),...values.map(r=>headers.map(k=>'"'+String(Array.isArray(r[k])?r[k].join('; '):r[k]??'').replaceAll('"','""')+'"').join(','))].join('\r\n')}
function download(name,type,content){let a=document.createElement('a');a.href=URL.createObjectURL(new Blob([content],{type}));a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000)}
function notes(){try{return JSON.parse(localStorage.getItem('eoip-audit-notes')||'[]')}catch{return []}}
function renderNotes(){let list=notes();$('decision-notes').innerHTML=list.length?list.map((x,i)=>'<div class="risk"><strong>'+e(x.kind)+'</strong><div><p>'+e(x.text)+'</p><span class="tiny">'+e(x.when)+'</span> <button class="rowbtn" data-note-remove="'+i+'">Remove</button></div></div>').join(''):'<div class="empty">No local notes yet.</div>'}
document.addEventListener('click',ev=>{let tab=ev.target.closest('[data-tab]');if(tab){ui.tab=tab.dataset.tab;location.hash=ui.tab;render();return}let detail=ev.target.closest('[data-detail]');if(detail){openDetail(detail.dataset.detail,detail.dataset.id);return}let pg=ev.target.closest('[data-page]');if(pg){let key=pg.dataset.page==='source'?'sourcePage':'page';ui[key]=Math.max(0,ui[key]+Number(pg.dataset.offset));render();return}if(ev.target.closest('#drawer-close')||ev.target===$('detail')){closeDetail();return}if(ev.target.closest('#req-export')){let values=DATA.requirements.filter(r=>(ui.state==='all'||r.audit_state===ui.state)&&(ui.family==='all'||r.family===ui.family)&&(!ui.query||[r.id,r.title,r.text,r.source,r.owner].join(' ').toLowerCase().includes(ui.query.toLowerCase())));download('eoip-requirements.csv','text/csv;charset=utf-8',csv(values));return}if(ev.target.closest('#decision-add')){let input=$('decision-text');let value=input.value.trim();if(!value)return;let list=notes();list.push({kind:$('decision-kind').value,text:value,when:new Date().toISOString()});localStorage.setItem('eoip-audit-notes',JSON.stringify(list));input.value='';renderNotes();return}if(ev.target.closest('#decision-export')){download('eoip-audit-notes.json','application/json',JSON.stringify(notes(),null,2));return}let remove=ev.target.closest('[data-note-remove]');if(remove){let list=notes();list.splice(Number(remove.dataset.noteRemove),1);localStorage.setItem('eoip-audit-notes',JSON.stringify(list));renderNotes()}});
document.addEventListener('input',ev=>{if(ev.target.id==='req-search'){ui.query=ev.target.value;ui.page=0;render(true)}if(ev.target.id==='source-search'){ui.sourceQuery=ev.target.value;ui.sourcePage=0;render(true)}});
document.addEventListener('change',ev=>{if(ev.target.id==='req-state'){ui.state=ev.target.value;ui.page=0;render()}if(ev.target.id==='req-family'){ui.family=ev.target.value;ui.page=0;render()}if(ev.target.id==='source-kind'){ui.sourceKind=ev.target.value;ui.sourcePage=0;render()}if(ev.target.id==='gap-filter'){ui.gapFilter=ev.target.value;render()}});
document.addEventListener('keydown',ev=>{if(ev.key==='Escape')closeDetail()});window.addEventListener('hashchange',()=>{let tab=location.hash.slice(1);if(VIEWS[tab]&&tab!==ui.tab){ui.tab=tab;render()}});
$('headstamp').textContent=DATA.revision.slice(0,10)+' / '+DATA.timestamp.slice(0,10);ui.tab=VIEWS[location.hash.slice(1)]?location.hash.slice(1):'overview';render();
</script>
<footer class="shell footer">EOIP project audit snapshot. Local data stays in this browser. Rebuild to refresh source coverage and reported states.</footer>
</body></html>'''


if __name__ == "__main__":
    raise SystemExit(main())
