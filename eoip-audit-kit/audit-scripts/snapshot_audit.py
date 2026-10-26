"""Inventory a fixed checkout and assemble an evidence-limited audit.

Only exact pytest receipt markers produce L2 links. Static ID mentions and AST
symbols are discovery aids. No acceptance, CI, runtime or reviewer is invented.
"""

from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import importlib.metadata
import json
import re
import shutil
import subprocess
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path

from parse_md_requirements import ID_RE, NORMATIVE_RE, extract, fallback_headings, is_req_id
from redact_sensitive import redact
from strict_audit_policy import assess

HERE = Path(__file__).resolve().parent
REPO = "https://github.com/Vibe-A-Thon/EIOP"
AGENT = "audit-local-20261020"


def read(path, default=None):
    return json.loads(path.read_text(encoding="utf-8-sig")) if path.exists() else default


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def git(root, *args):
    return subprocess.check_output(["git", *args], cwd=root).decode("utf-8").strip()


def table(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def role(path):
    low = path.lower()
    if any(term in low for term in ("audit-output/", "eoip-audit-kit/", "docs/generated/",
                                   "self-help-manual/", "master-requirement", "master-implementation",
                                   "/audits/", "/tickets/", "audit-gaps", "gaps-audit")):
        return "historical-or-generated-context"
    if "requirement" in low or "reqirement" in low:
        return "requirements"
    if "implementation" in low or "plan" in low:
        return "plan"
    return "supporting-document"


def kind(path):
    parts = path.lower().split("/")
    if any(part in {"tests", "test", "selftest"} for part in parts) or re.search(r"(test_|\.test\.|\.spec\.)", parts[-1]):
        return "tests"
    if parts[0] in {".github", "deploy", "config", "infra", "schemas"}:
        return "infra"
    return "code"


def inventory(root, out, prior):
    commit = git(root, "rev-parse", "HEAD")
    paths = git(root, "ls-files", "-z").split("\0")
    paths = [p for p in paths if p]
    files, candidates, references, symbols, syntax_errors, secret_hits = [], [], defaultdict(list), [], [], []
    unparsed = []
    docs = []
    for path in paths:
        target = root / path
        if not target.is_file():
            files.append({"path": path, "status": "not-a-regular-file"})
            continue
        raw = target.read_bytes()
        item = {"path": path, "sha256": digest(raw), "bytes": len(raw), "status": "read"}
        files.append(item)
        suffix = target.suffix.lower()
        if suffix not in {".md", ".txt", ".py", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".json",
                          ".yaml", ".yml", ".toml", ".sh", ".ps1", ".sql", ".tf", ".ini"}:
            continue
        try:
            text = raw.decode("utf-8-sig")
        except UnicodeDecodeError:
            item["status"] = "decode-error-replacement-used"
            text = raw.decode("utf-8", errors="replace")
        lines = text.splitlines()
        item["lines"] = len(lines)
        if suffix == ".md":
            records = extract(text, path)
            covered = {n for record in records for n in range(record["line_range"][0], record["line_range"][1] + 1)}
            fallback = fallback_headings(text, path, digest(path.encode())[:10].upper())
            for record in fallback:
                start, end = record["line_range"]
                if any(NORMATIVE_RE.search(lines[n - 1]) and n not in covered for n in range(start, end + 1)):
                    records.append(record)
                    covered.update(range(start, end + 1))
            for number, line in enumerate(lines, 1):
                if NORMATIVE_RE.search(line) and number not in covered:
                    unparsed.append({"source": path, "line": number,
                                     "text": line, "reason": "Normative text outside recognized definition; triage required"})
            for record in records:
                record["document_role"] = role(path)
                record["owner"] = "UNASSIGNED"
            candidates.extend(records)
            docs.append({**item, "role": role(path), "definitions": len(records)})
        else:
            for number, line in enumerate(lines, 1):
                for rid in set(ID_RE.findall(line)):
                    if is_req_id(rid):
                        references[rid].append({"path": path, "line": number, "kind": kind(path)})
            if suffix == ".py":
                try:
                    tree = ast.parse(text, filename=path)
                    for node in ast.walk(tree):
                        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                            symbols.append({"path": path, "line": node.lineno, "end_line": node.end_lineno,
                                            "symbol": node.name, "kind": type(node).__name__})
                except SyntaxError as exc:
                    syntax_errors.append({"path": path, "line": exc.lineno, "error": exc.msg})
            _, hits = redact(text)
            if hits:
                secret_hits.append({"path": path, "hits": len(hits),
                                    "note": "Heuristic candidates include fixtures/examples; values omitted; review locally"})
    # Original requirement documents win over generated mirrors and plans.
    order = {"requirements": 0, "plan": 1, "supporting-document": 2, "historical-or-generated-context": 3}
    candidates.sort(key=lambda r: (order[r["document_role"]], r["source_file"], r["line_range"][0]))
    by_id = {}
    context_only = []
    for record in candidates:
        rid = record["id"]
        site = {"source_file": record["source_file"], "line_range": record["line_range"],
                "raw_text": record["raw_text"], "document_role": record["document_role"]}
        if rid in by_id:
            by_id[rid].setdefault("duplicate_sites", []).append(site)
        elif record["document_role"] == "historical-or-generated-context":
            context_only.append(record)
        else:
            by_id[rid] = record
    requirements = list(by_id.values())
    index = {"schema_version": "snapshot-requirements-v1", "commit": commit, "count": len(requirements),
             "requirements": requirements,
             "limitations": ["Definition extraction is not semantic approval.",
                             "Read every tracked Markdown byte; excluded generated/context-only candidates remain in context-candidates.json.",
                             "Unrecognized normative lines require manual triage; no claim of exhaustive semantic decomposition."]}
    write(out / "requirements_index.json", index)
    table(out / "requirements_index.csv", requirements,
          ["id", "title", "type", "priority", "source_file", "line_range", "document_role", "synthetic_id"])
    write(out / "evidence/inventory/files.json", files)
    write(out / "evidence/inventory/markdown.json", docs)
    write(out / "evidence/inventory/context-candidates.json", context_only)
    write(out / "evidence/inventory/unparsed-normative-lines.json", unparsed)
    write(out / "evidence/inventory/python-symbols.json", symbols)
    write(out / "evidence/inventory/python-syntax-errors.json", syntax_errors)
    write(out / "evidence/security_scan/secret-candidates.json", secret_hits)
    write(out / "traceability_detail.json", dict(references))
    rows = []
    for req in requirements:
        refs = references.get(req["id"], [])
        rows.append({"requirement_id": req["id"],
                     **{f"{name}_paths": ";".join(sorted({f"{r['path']}:{r['line']}" for r in refs if r["kind"] == key}))
                        for name, key in (("code", "code"), ("test", "tests"), ("infra", "infra"))},
                     "evidence_type": "source-id-mention" if refs else "none",
                     "confidence_score": 0.25 if refs else 0,
                     "git_commit": commit})
    table(out / "traceability_matrix.csv", rows,
          ["requirement_id", "code_paths", "test_paths", "infra_paths", "evidence_type", "confidence_score", "git_commit"])
    changed = git(root, "diff", "--name-only", prior["baseline_commit"], commit).splitlines() if prior else []
    write(out / "evidence/inventory/delta.json", {
        "baseline_commit": prior.get("baseline_commit") if prior else None, "audited_commit": commit,
        "changed_files": changed, "prior_statuses": dict(Counter(r["status"] for r in prior.get("requirements", {}).values())),
        "method": "All prior evidence is stale at the new commit until re-executed; no inherited completion."})
    summary = {"git_commit": commit, "tracked_files": len(files), "markdown_files": len(docs),
               "markdown_lines": sum(d["lines"] for d in docs), "requirements": len(requirements),
               "definition_sites": len(candidates), "context_only_definitions": len(context_only),
               "unparsed_normative_lines": len(unparsed), "python_symbols": len(symbols),
               "python_syntax_errors": len(syntax_errors),
               "decode_errors": [f["path"] for f in files if "decode-error" in f["status"]]}
    write(out / "inventory-summary.json", summary)
    print(json.dumps(summary))


def python_sbom(out):
    packages = []
    for distribution in importlib.metadata.distributions():
        name = distribution.metadata.get("Name")
        if name:
            packages.append({"type": "library", "name": name, "version": distribution.version,
                             "purl": f"pkg:pypi/{name.lower().replace('_', '-')}@{distribution.version}",
                             "properties": [{"name": "audit:scope", "value": "installed-audit-environment"}]})
    packages.sort(key=lambda p: (p["name"].lower(), p["version"]))
    write(out / "evidence/sbom.json", {
        "bomFormat": "CycloneDX", "specVersion": "1.5", "version": 1,
        "metadata": {"properties": [{"name": "audit:limitation",
                                     "value": "Installed Python environment only; not a release/container/SaaS SBOM."}]},
        "components": packages})
    rows = []
    for distribution in importlib.metadata.distributions():
        name = distribution.metadata.get("Name")
        if not name:
            continue
        license_text = distribution.metadata.get("License-Expression") or distribution.metadata.get("License") or "UNKNOWN"
        rows.append({"name": name, "version": distribution.version,
                     "license_metadata": license_text, "review": "UNREVIEWED; metadata is not legal clearance"})
    table(out / "license_report.csv", rows, ["name", "version", "license_metadata", "review"])


def executions(out):
    return [{**read(p), "artifact": p.relative_to(out).as_posix()}
            for p in sorted((out / "evidence").glob("*/execution.json"))]


def receipt_evidence(root, out, commit):
    by_req = defaultdict(list)
    summaries, rejected = [], []
    for path in sorted((out / "evidence").glob("*/receipt.json")):
        data = read(path)
        execution = read(path.with_name("execution.json"), {})
        valid = (data.get("code_commit") == commit and data.get("source_unchanged") is True
                 and not data.get("collect_only") and execution.get("git_commit") == commit
                 and not execution.get("tracked_files_changed") and execution.get("exit_code") not in {124, 127})
        # Verify the receipt's integrity seal and every source file, not just the
        # producer's source_unchanged assertion.
        import sys
        sys.path.insert(0, str(root / "packages"))
        from eoip.verification.test_receipts import seal_receipt, source_manifest
        sealed = seal_receipt(data)
        valid &= bool(data.get("receipt_sha256")) and sealed["receipt_sha256"] == data["receipt_sha256"]
        valid &= bool(data.get("source_manifest")) and data["source_manifest"] == source_manifest(root)
        for rel, sha in data.get("source_manifest", {}).items():
            source = root / rel
            valid &= source.is_file() and digest(source.read_bytes()) == sha
        summaries.append({"artifact": path.relative_to(out).as_posix(), "eligible": bool(valid),
                          "counts": data.get("counts"), "exit_code": data.get("exit_code"),
                          "collection_errors": data.get("collection_errors", [])})
        if not valid:
            rejected.append(path.relative_to(out).as_posix())
            continue
        command = subprocess.list2cmdline(execution.get("command", []))
        for case in data.get("tests", []):
            if case["outcome"] not in {"PASSED", "FAILED"}:
                continue
            if case["outcome"] == "PASSED" and case.get("phases") != {
                "setup": "passed", "call": "passed", "teardown": "passed"
            }:
                continue
            # A marker is an explicit association, not a claim that all clauses
            # are covered. Per-requirement residual gaps retain that boundary.
            for rid in case.get("requirements", []):
                if not re.fullmatch(ID_RE, rid):
                    continue
                by_req[rid].append({
                    "requirement_id": rid, "evidence_id": "EVI-" + digest((str(path) + case["nodeid"] + rid).encode())[:24],
                    "proof_tier": "L2", "type": "test_run", "git_commit": commit,
                    "summary": f"Exact marked test case: {case['nodeid']}"[:500],
                    "repro_command": command,
                    "expected_result": "setup, call, teardown all pass for this exact case",
                    "actual_result": case["outcome"].lower(),
                    "confidence": 0.65, "redaction_status": "clean",
                    "links": [{"kind": "artifact", "url": path.relative_to(out).as_posix(), "label": case["nodeid"]},
                              {"kind": "artifact", "url": path.with_name("output.txt").relative_to(out).as_posix()}],
                    "notes": "Explicit marker only. Full acceptance coverage and independent verification remain open."
                })
    write(out / "evidence/test_results/summary.json", {"runs": summaries, "rejected_receipts": rejected})
    return by_req, summaries


def assemble(root, out, prior, findings_file):
    index = read(out / "requirements_index.json")
    commit = index["commit"]
    if commit != git(root, "rev-parse", "HEAD"):
        raise ValueError("Inventory and checkout commits differ")
    now = datetime.now(UTC).isoformat()
    refs = read(out / "traceability_detail.json")
    by_req, test_summary = receipt_evidence(root, out, commit)
    findings = read(findings_file, [])
    files = read(out / "evidence/inventory/markdown.json")
    data_inventory = read(out / "inventory-summary.json")
    python_sbom(out)
    mem = {}
    tasks = []
    details = []
    catalogue = [f"# EOIP Consolidated Requirements\n\nAudited commit: `{commit}`.\n",
                 "This is a definition catalogue, not approved scope or proof of completion. Original requirement files take precedence over plans and generated mirrors. All recognized duplicate sites are retained in the JSON index. Supporting normative prose is included as a candidate, not silently accepted as product scope.\n"]
    implementation = [f"# EOIP Implementation Audit\n\nAudited commit: `{commit}`.\n",
                      "L1 anchors are discovery only. L2 below is exact marker-to-executed-case evidence, not complete acceptance coverage. No local check is promoted to CI, staging, independent review, or release acceptance. Source inspection limits and architecture are in `audit_gaps_requirements.md` and `architecture_review.md`.\n"]
    missing = []
    for req in index["requirements"]:
        rid = req["id"]
        severity = "Critical" if req["priority"] == "P0" else "High" if req["priority"] == "P1" or req["type"] == "Security" else "Medium"
        links = refs.get(rid, [])
        source = f"{req['source_file']}:{req['line_range'][0]}"
        source_url = f"{REPO}/blob/{commit}/{req['source_file']}#L{req['line_range'][0]}-L{req['line_range'][1]}"
        if links:
            first = next((r for r in links if r["kind"] == "code"), links[0])
            by_req[rid].append({
                "requirement_id": rid, "evidence_id": "EVI-L1-" + digest(rid.encode())[:20],
                "proof_tier": "L1", "type": "code_link", "git_commit": commit,
                "summary": "Literal source ID reference; no behavioral claim", "confidence": 0.25,
                "redaction_status": "clean",
                "links": [{"kind": "code", "url": f"{REPO}/blob/{commit}/{first['path']}#L{first['line']}"}]})
        items = by_req.get(rid, [])
        has_pass = any(i["proof_tier"] == "L2" and i["actual_result"] == "passed" for i in items)
        gaps = ["Acceptance-clause coverage is not independently established.",
                "No requirement-bound same-commit CI or qualified non-production runtime proof was obtained."]
        if not has_pass:
            gaps.insert(0, "No qualifying passing exact-marker L2 case in this audit run; absence of linkage is not absence of code.")
            missing.append({"requirement_id": rid, "source": source,
                            "discovery": "Inspect the verbatim clauses and candidate code; write explicit marked tests at real boundaries."})
        if severity == "Critical":
            gaps.append("Critical closure requires independent L5 reviewer plus same-commit L3.")
        if not req["acceptance_criteria"]:
            gaps.append("Acceptance criteria not structurally extracted; review verbatim text and get product-owner approval.")
        assessment = assess(items, commit=commit, bundle_commit=commit, severity=severity, gaps=gaps, producer=AGENT)
        if req.get("synthetic_id"):
            gaps.append("Synthetic normative section: product-owner must confirm scope and stable ownership.")
        task_id = "TASK-" + rid
        task = {"id": task_id, "requirement_id": rid, "severity": severity, "status": "open",
                "title": req["title"], "owner": "UNASSIGNED", "complexity": "UNKNOWN",
                "estimate_hours": None, "estimate_discovery": "Measure after clause decomposition and runtime reproduction; no fabricated estimate.",
                "impact": "Acceptance and release readiness remain unproven for this requirement.",
                "likelihood": "UNKNOWN; evidence gaps do not establish defect frequency.",
                "residual_risk": gaps, "dependencies": sorted(set(ID_RE.findall(req["raw_text"])) - {rid}),
                "steps": [f"Read all clauses at {source} and all duplicate definitions in requirements_index.json.",
                          "Resolve contradictory scope and define observable API/UI/storage/error/security acceptance cases.",
                          "Inspect candidate anchors; identify actual integration boundaries before modifying code.",
                          "Add exact requirement markers to boundary tests; use synthetic data and isolated storage.",
                          "Execute tests, retain sealed receipt, redacted log and source manifest; test negative and recovery cases.",
                          "Obtain requirement-bound CI/runtime evidence and required independent review; rerun this audit."],
                "acceptance_criteria": req["acceptance_criteria"] or ["DERIVED: obtain approved testable criteria for every verbatim clause."],
                "proof_plan": "L2 + (same-commit L3 or non-prod L4); Critical also L3 + independent L5; no residual acceptance gaps."}
        tasks.append(task)
        mem[rid] = {"status": assessment["status"], "proof_tier_achieved": assessment["proof_tier"],
                    "last_verified_commit": commit, "severity": severity,
                    "type": req["type"] if req["type"] in {"Functional", "Non-Functional", "Security", "Compliance", "AI", "Infra"} else "Functional",
                    "title": req["title"], "priority": req["priority"], "source": source, "owners": ["UNASSIGNED"],
                    "evidence_ids": [i["evidence_id"] for i in items], "residual_gaps": gaps,
                    "files_touched": sorted({r["path"] for r in links}),
                    "notes": "last_verified_commit identifies this assessment, not acceptance. Prior proof is stale."}
        catalogue.extend([f"\n## {rid}: {req['title']}\n\nSource: [{source}]({source_url})\n",
                          f"Type: {req['type']}; priority: {req['priority']}; owner: UNASSIGNED; role: {req['document_role']}.\n",
                          "Dependency candidates (ID mentions, not approved ordering): " + (", ".join(task["dependencies"]) or "UNKNOWN; inspect owning workflow.") + "\n",
                          "Extracted acceptance criteria (verify against full context):\n" + ("\n".join("- " + criterion for criterion in req["acceptance_criteria"]) or "- Not structurally extracted; obtain approved testable criteria from the verbatim source.") + "\n",
                          f"Duplicate sites: {len(req.get('duplicate_sites', []))}; duplicate bodies are retained in JSON.\n" +
                          "\n".join(f"- [{site['source_file']}:{site['line_range'][0]}]({REPO}/blob/{commit}/{site['source_file']}#L{site['line_range'][0]}-L{site['line_range'][1]}) ({site['document_role']})" for site in req.get("duplicate_sites", [])),
                          "Verbatim source (untruncated):\n\n``````text\n" + req["raw_text"] + "\n``````\n"])
        implementation.extend([f"\n## {rid}: {req['title']}\n\nStatus: **{assessment['status']}**; tier: **{assessment['proof_tier']}**; severity: {severity} (triage hint, not observed impact).\n",
                               f"Requirement: [{source}]({source_url}); task: `{task_id}`.\n",
                               "Candidate source anchors: " + (", ".join(f"`{r['path']}:{r['line']}`" for r in links) or "None discovered by literal ID search.") + "\n",
                               "Executed mapped cases:\n" + ("\n".join(f"- `{i['summary']}`: {i['actual_result']}; `{i['evidence_id']}`" for i in items if i["proof_tier"] == "L2") or "- None eligible.") + "\n",
                               "Residual gaps:\n" + "\n".join(f"- {gap}" for gap in gaps) + "\n",
                               "Completion instructions: follow the per-ID task in `audit_tasks.json`; no estimate until discovery and no closure from paths alone.\n"])
        details.append({"id": rid, **mem[rid], "task": task_id, "source_url": source_url})
    known = set(mem)
    orphans = {rid: items for rid, items in by_req.items() if rid not in known}
    static_orphans = {rid: [ref for ref in locations if ref["kind"] == "tests"]
                      for rid, locations in refs.items() if rid not in known and any(ref["kind"] == "tests" for ref in locations)}
    write(out / "evidence/inventory/orphan-test-id-mentions.json", {
        "note": "Literal test-source mentions only, including negative fixtures. Not automatically product requirements or executed cases.",
        "ids": static_orphans})
    evidence_items = [item for items in by_req.values() for item in items]
    evidence = {"schema_version": "1.1.0", "proof_policy_version": "1.1.0", "project": "EOIP / KGF",
                "git_commit": commit, "baseline_commit": prior.get("baseline_commit", commit),
                "generated_at": now, "generated_by": {"agent_id": AGENT, "role": "local evidence auditor"},
                "notes": "Only source links and exact executed marked cases. No L3/L4/L5 or release acceptance claimed.",
                "evidence_items": evidence_items}
    counts = Counter(r["status"] for r in mem.values())
    tiers = Counter(r["proof_tier_achieved"] for r in mem.values())
    environment = {
        "local": {"audited": True, "commit": commit, "notes": "Windows; isolated data paths; Python checks. Not an OS-level or network sandbox."},
        "CI": {"audited": False, "notes": "Definitions inventoried; remote API probe does not establish requirement-bound green jobs."},
        "staging": {"audited": False, "notes": "No qualified deployment, credentials or synthetic staging dataset provided."},
        "production": {"audited": False, "notes": "Explicitly excluded; no production data or credentials requested."}}
    prompt_files = [HERE.parent / "ENHANCED_AUDIT_PROMPT.md", HERE.parents[1] / "docs/auditor prompt.txt"]
    prompts = [{"path": str(p.relative_to(HERE.parents[1])), "sha256": digest(p.read_bytes()),
                "lines": len(p.read_text(encoding="utf-8-sig").splitlines())} for p in prompt_files]
    prompt_hash = digest(json.dumps(prompts, sort_keys=True).encode())
    memory = {"schema_version": "1.1.0", "proof_policy_version": "1.1.0", "repo": REPO,
              "baseline_commit": commit, "audited_commit": commit, "last_audit_date": now,
              "health_score": round(100 * counts["Implemented"] / max(1, len(mem)), 2),
              "notes": "Health is strict accepted-completion percentage, NOT application quality, code coverage or defect rate. All unsigned gates remain open.",
              "requirements": mem, "environment_matrix": environment,
              "agents": [{"agent_id": AGENT, "role": "Audit automation", "timestamp": now,
                          "action": "delta_audit", "prompt_hash": prompt_hash,
                          "notes": "Single agent; no independent signoff. Historical evidence retained at its original location."}],
              "open_locks": [], "import_history": [],
              "changelog": [{"timestamp": now, "actor": AGENT, "change": "Fresh snapshot inventory and exact-marker execution audit; no inherited completion."}],
              "summary": {"statuses": dict(counts), "tiers": dict(tiers)},
              "orphan_evidence": {rid: {"evidence_ids": [i["evidence_id"] for i in items],
                                       "note": "Test marker without recognized authoritative definition; not counted as a product requirement."}
                                  for rid, items in orphans.items()}}
    write(out / "evidence/evidence.json", evidence)
    write(out / "audit-memory.json", memory)
    write(out / "audit_tasks.json", {"schema": "snapshot-audit-tasks-v1", "git_commit": commit, "tasks": tasks,
                                    "findings": findings, "estimates": "Unknown until scoped discovery, never zero by default."})
    write(out / "missing_tests.json", missing)
    write(out / "evidence/test_results/orphan-test-ids.json", orphans)
    write(out / "evidence/llm-log.json", {
        "prompts": prompts, "model": "Codex (GPT-5 family per runtime instructions)",
        "exact_model_version": "Not exposed by runtime", "human_verifier": "PENDING",
        "recording_limit": "Cannot reconstruct a separate model-call ledger or assert pre-redaction for IDE context supplied before this audit.",
        "automation": "No external LLM API called by audit scripts. Source parsing, hashing, scoring and document assembly are local.",
        "redacted_input_ref": "evidence/*/output.txt", "output_ref": "audit_gaps_requirements.md"})
    for name, content in (("requirements.md", catalogue), ("implementation.md", implementation)):
        (out / name).write_text("\n".join(content), encoding="utf-8")
    orphan_lines = ["\n## Orphan Test-Only IDs\n\nNot counted in requirement totals; resolve ownership before acceptance.\n"]
    orphan_lines.extend(f"- `{rid}`: {len(items)} executed case records." for rid, items in sorted(orphans.items()))
    orphan_lines.append(f"\nAdditional unresolved static test-ID mentions: {len(static_orphans)}. See `evidence/inventory/orphan-test-id-mentions.json`; these include negative fixtures and are not automatically requirements.")
    with (out / "requirements.md").open("a", encoding="utf-8") as stream:
        stream.write("\n".join(orphan_lines))
    runs = executions(out)
    summary = {**data_inventory, "generated_at": now, "statuses": dict(counts), "tiers": dict(tiers),
               "tests": test_summary, "checks": runs, "environment_matrix": environment,
               "orphan_test_ids": len(orphans), "findings": findings,
               "proof_policy": "No accepted requirement closures without full scope and independent evidence."}
    write(out / "summary.json", summary)
    report = [f"# EOIP / KGF Evidence Audit\n\nDate: {now}\n\nRepository: {REPO}\n\nAudited commit: `{commit}`; branch: `dev_local`.\n",
              "## Executive Summary\n\nEOIP is a local-first enterprise ontology, graph, query, ingestion and intelligence platform with HTTP, web, worker, MCP and IDE surfaces. This run assesses evidence and observable local behavior; it is not production certification or independent legal/security signoff.\n",
              f"Read and hashed all {len(files)} tracked Markdown files ({data_inventory['markdown_lines']:,} lines) and inventoried {data_inventory['tracked_files']:,} tracked files. Recognized {len(mem):,} candidate requirements. Automated reading is not a claim of line-by-line human semantic verification. {data_inventory['unparsed_normative_lines']} unmatched normative lines are retained for triage; {data_inventory['context_only_definitions']} generated/historical definition candidates are excluded from acceptance totals, not discarded.\n",
              f"Statuses: `{dict(counts)}`. Tiers: `{dict(tiers)}`. Strict accepted-completion health: {memory['health_score']}%. This is NOT an estimate of how much software works. Critical-open count: {sum(r['severity']=='Critical' and r['status']!='Implemented' for r in mem.values())}; severity is provisional priority-derived triage.\n",
              "## Top Risks and Findings\n"]
    for finding in findings:
        report.append(f"### {finding['id']}: {finding['title']}\n\nSeverity: {finding['severity']}. {finding['observation']}\n\nEvidence: "
                      + ", ".join(f"`{p}`" for p in finding["evidence"])
                      + f"\n\nRemediation: {finding['remediation']}\n\nAcceptance: {finding['acceptance']}\n")
    report.extend(["## Executed Checks\n", "| Check | Exit | Result | Artifact |\n|---|---:|---|---|"])
    report.extend(f"| {r['artifact'].split('/')[1]} | {r['exit_code']} | {r['status']} | `{r['artifact']}` |" for r in runs)
    report.extend(["\n## Proof and Scope Limits\n",
                   "- Every requirement has an assessment and a scoped task; Not Verified means insufficient evidence, not missing functionality.",
                   "- Exact per-case markers are the only L2 association. File-level IDs, passing sibling tests, source paths and successful collection are never substituted.",
                   "- All earlier-commit results are historical. Current working-tree QA/audit patches are outside the named application snapshot and need their own commit and rerun.",
                   "- Local synthetic memory-store checks do not qualify HugeGraph/Neo4j/Neptune, containers, multi-worker recovery, live connectors, LLM vendors, performance, accessibility or customer deployment.",
                   "- No qualified L3, L4 or L5 was attached to requirements. Independent Audit Lead, Security and Product Owner signoffs remain PENDING.",
                   "- Prior and current requirement counts are not directly comparable: this run includes plans/supporting normative sections and preserves dotted subclauses. Duplicate scope reconciliation is required.",
                   "- Enhanced prompt section 19 says schema 1.0.0; explicit rules and supplied schemas use 1.1.0. This run follows 1.1.0 with additive dotted-ID and environment support.",
                   "- Prompt hashes are retained. Exact model revision and prior IDE-context pre-redaction cannot be independently reconstructed; the LLM governance log states these limitations.",
                   "\n## Detailed Requirement Findings\n\nSee `implementation.md` for every status, mapped execution, source anchor and residual gap; `requirements.md` for untruncated verbatim definitions; `audit_tasks.json` for per-ID dependencies, instructions, acceptance and proof plans. No undocumented effort estimates are invented.",
                   "\n## Supporting Reviews\n\nSee `architecture_review.md`, `security_checklist.md`, `threat_model.json`, `data_classification.md`, `ai_governance.md`, `ai_inventory.json`, `compliance_gaps.md`, `a11y_checklist.md`, and `evidence/`.",
                   "\n## Signoff\n\nAudit Lead: PENDING. Security Specialist: PENDING. Product Owner: PENDING. Release approval: NOT GRANTED. No independent reviewer was simulated."])
    (out / "audit_gaps_requirements.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    tracker = {"summary": summary, "requirements": details, "tasks": tasks, "evidence": evidence}
    template = (HERE.parent / "templates/snapshot_tracker.html").read_text(encoding="utf-8")
    page = template.replace("__AUDIT_DATA__", json.dumps(tracker, separators=(",", ":")).replace("<", "\\u003c"))
    (out / "tracker.html").write_text(page, encoding="utf-8")
    # The root kit copy is identical and self-contained; its relative artifact
    # links are resolved using the embedded artifact-directory mapping.
    (HERE.parent / "tracker.html").write_text(page, encoding="utf-8")
    scripts = out / "audit-scripts"
    scripts.mkdir(exist_ok=True)
    for script in ("snapshot_audit.py", "strict_audit_policy.py", "parse_md_requirements.py",
                   "redact_sensitive.py", "execute_audit_check.py", "audit_safety_probes.py",
                   "audit_web_checks.py", "check_tracker.cjs", "summarize_audit_checks.py",
                   "summarize_test_results.py", "validate_snapshot_audit.py", "run_unit_shards.py"):
        shutil.copy2(HERE / script, scripts / script)
    manifest = [{"path": p.relative_to(out).as_posix(), "sha256": digest(p.read_bytes())}
                for p in sorted(out.rglob("*")) if p.is_file() and p.name != "artifact-manifest.json"]
    write(out / "artifact-manifest.json", {"git_commit": commit, "files": manifest})
    print(json.dumps({"statuses": dict(counts), "tiers": dict(tiers), "evidence_items": len(evidence_items)}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["inventory", "assemble"])
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--prior-memory", required=True, type=Path)
    parser.add_argument("--findings", type=Path, default=HERE.parent / "snapshot-findings.json")
    args = parser.parse_args()
    prior = read(args.prior_memory, {})
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    if args.mode == "inventory":
        inventory(args.root.resolve(), out, prior)
    else:
        assemble(args.root.resolve(), out, prior, args.findings)


if __name__ == "__main__":
    main()
