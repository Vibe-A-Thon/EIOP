#!/usr/bin/env python3
"""Generate one remediation task per requirement (deterministic, no network, no LLM).

Inputs (audit-output/): requirements_index.json, traceability_detail.json,
test_results/per_requirement.json, test_results/failed_cases.json, residual_gaps.json,
audit-memory.json; plus remediation/findings_tasks.json (hand-written) and audit-config.json.
Optional --repo-root (read-only) classifies duplicate definition sites by reading the
source line (sub-clause numbering such as CRA-001.1 is NOT a duplicate).

Outputs (remediation/):
  requirement_tasks.json / .csv       one task per requirement ID (RT-<ID>)
  epics.json, epics/<EPIC>.md         batches by source doc x gap category (<= --epic-size tasks)
  duplicate_id_tasks.json / .md       one resolution task per truly re-defined ID
  findings_tasks.md                   rendering of the hand-written findings_tasks.json
  ../audit-output/audit_tasks.json    merged queue (finding tasks + requirement tasks)

Same inputs give the same outputs: sorted iteration, no timestamps except --generated-at.
"""
from __future__ import annotations

import argparse
import collections
import csv
import json
import os
import re
from pathlib import Path

KIT_ROOT = Path(__file__).resolve().parent.parent
PRIO_ORDER = ["P0", "P1", "P2", "P3"]

CATEGORIES = {
    "failing_tests": "Mapped tests fail on the audited commit (failing tests are never proof)",
    "ambiguous_tests": "Mapped tests both pass and fail on the audited commit",
    "untraced": "No code, test or infra reference to the ID anywhere",
    "code_no_test": "Code references the ID but no test is mapped",
    "tests_not_executed": "Tests are mapped/referenced but none ran in the audit (excluded or not collected)",
    "needs_ci_l3": "Passing mapped tests (L2); needs a same-commit green L3 CI run (or L4) to close",
}
CAT_ORDER = list(CATEGORIES)
CAT_ABBR = {"failing_tests": "FAIL", "ambiguous_tests": "AMB", "untraced": "UNTR", "code_no_test": "NOTEST",
            "tests_not_executed": "NOTRUN", "needs_ci_l3": "CI"}

SEC_KW = re.compile(r"\b(air[- ]?gap\w*|egress|auth\w*|token\w*|secret\w*|credential\w*|password\w*|rbac|abac|acl\w*|"
                    r"tenant[- ]isolation|cross[- ]tenant|encrypt\w*|kms|pii|privacy|gdpr|injection|xss|csrf|ssrf|sandbox\w*|"
                    r"isolation|signature\w*|signed|tamper\w*|audit[- ]log\w*|least[- ]privilege|permission\w*|redact\w*)\b", re.I)
REL_KW = re.compile(r"\b(data[- ]loss|durab\w*|idempoten\w*|backup|restore|failover|rollback|integrity|deadlock|timeout)\b", re.I)
NORMATIVE = re.compile(r"\b(must|shall|should|required?|requires|ensure[sd]?|never|always|reject\w*|support\w*|provide[sd]?|"
                       r"expose[sd]?|record[sd]?|enforce[sd]?|validate[sd]?|guarantee[sd]?|prevent\w*|block\w*|emit\w*|persist\w*)\b", re.I)


def load(p, default=None):
    p = Path(p)
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else default


def md_clean(s: str) -> str:
    s = re.sub(r"`([^`]*)`", r"\1", s or "")
    s = re.sub(r"\*\*?([^*]+)\*\*?", r"\1", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    return re.sub(r"\s+", " ", s).strip()


def summary_title(r: dict) -> str:
    raw = (r.get("raw_text") or "").strip()
    if r.get("definition_site") == "table_row" and raw.count("|") >= 3:
        cells = [md_clean(c) for c in raw.strip("|").split("|")]
        cells = [c for c in cells[1:] if c and c not in ("-", "—", "none")]
        return " · ".join(cells[:3])[:200] or r.get("title") or r["id"]
    return md_clean(r.get("title") or r["id"])[:200]


AC_LABELS = {"WHAT": "Delivers: {}", "COMPLETE WHEN": "Complete when: {}", "ACCEPTANCE": "{}", "ACCEPTANCE CRITERIA": "{}",
             "FAILURE": "Failure behaviour: {}", "FAILURE BEHAVIOR": "Failure behaviour: {}", "TEST": "Verified by: {}",
             "DATA / INTERFACES": "Interfaces: {}", "REQUIREMENT": "{}", "BASE STATEMENT": "{}", "DESCRIPTION": "{}"}
LABEL_RE = re.compile(r"^\s*[-*]?\s*\*\*([A-Za-z /&]{2,30}?):?\*\*:?\s*(.*)$")


def derive_acs(r: dict) -> list[str]:
    out: list[str] = []
    for line in (r.get("raw_text") or "").splitlines():
        m = LABEL_RE.match(line)
        if m and m.group(1).strip().upper() in AC_LABELS and len(m.group(2).split()) >= 2:
            out.append(AC_LABELS[m.group(1).strip().upper()].format(md_clean(m.group(2)))[:400])
    for a in r.get("acceptance_criteria") or []:
        a = md_clean(a)
        if a.count("|") >= 2 or len(a.split()) < 4 or a.lower().startswith("aggregated title"):
            continue
        out.append(a[:400])
    raw = r.get("raw_text") or ""
    labelled = bool(out)
    if labelled:
        pass
    elif r.get("definition_site") != "table_row":
        body = "\n".join(l for l in raw.splitlines()[1:] if not l.strip().startswith("|"))
        for sent in re.split(r"(?<=[.;])\s+|\n[-*] |\n\d+\. ", md_clean(body)):
            s = sent.strip(" -*")
            if 6 <= len(s.split()) <= 80 and NORMATIVE.search(s) and s not in out and not re.match(r"^[A-Z][A-Z /&]{1,30}:", s):
                out.append(s[:400])
    else:
        cells = [md_clean(c) for c in raw.strip("|").split("|")]
        out.insert(0, "Row contract holds exactly as specified: «" + " | ".join(c for c in cells if c)[:380] + "»")
        out = [o for o in out if o.startswith("Row contract") or len(o.split()) >= 4]
        for c in cells[1:]:
            if len(c.split()) >= 4 and c not in out:
                out.append(c[:400])
    seen, acs = set(), []
    for a in out:
        k = a.lower()
        if k not in seen:
            seen.add(k)
            acs.append(a)
    if not acs:
        body = md_clean(re.sub(r"^#+\s*", "", raw.replace("---", " ")))
        body = re.sub(r"^[-*]?\s*" + re.escape(r["id"]) + r"\s*[:.\-—]*\s*", "", body).strip()
        body = re.sub(r"^(—|-)?\s*[A-Z]{3,12}\s+(?=[A-Z])", "", body) if body.isupper() else body
        if len(body.split()) >= 2:
            acs = [f"Statement holds (verbatim requirement is the criterion): {body[:380]}"]
    if not acs:
        acs = [f"Behaviour stated in {r['source_file']}:{r['line_range'][0]} ('{summary_title(r)}') is demonstrably met. "
               f"Requirement text gives no testable criteria: discovery step: refine with the requirement owner (UNKNOWN)."]
    acs = acs[:12]
    acs.append("At least one automated test asserts each criterion above and is mapped to this ID (pytest mark or requirements-test-map.json)")
    return acs


def derive_priority(r: dict, cats: list[str], severity: str) -> tuple[str, str]:
    text = f"{r.get('title','')} {r.get('raw_text','')[:3000]}"
    doc_p = r.get("priority") if r.get("priority") in PRIO_ORDER else None
    base = {"Security": 1, "Compliance": 1}.get(r.get("type"), 2)
    reasons = [f"type {r.get('type')}"]
    if SEC_KW.search(text):
        base -= 1
        reasons.append("security keywords (" + ", ".join(sorted({m.lower() for m in SEC_KW.findall(text)})[:4]) + ")")
    elif REL_KW.search(text):
        base -= 0 if base <= 1 else 1
        reasons.append("reliability keywords")
    if "failing_tests" in cats or "ambiguous_tests" in cats:
        base = min(base, 1)
        reasons.append("failing tests")
    if severity == "Critical":
        base = min(base, 0)
        reasons.append("derived severity Critical")
    derived = PRIO_ORDER[max(0, min(3, base))]
    if doc_p:
        final = min(doc_p, derived, key=PRIO_ORDER.index) if (SEC_KW.search(text) or "failing_tests" in cats) else doc_p
        reasons.insert(0, f"doc priority {doc_p}")
    else:
        final = derived
        reasons.insert(0, "doc priority UNKNOWN")
    return final, "; ".join(reasons)


def classify_dups(r: dict, repo_root: Path | None, cache: dict) -> list[dict]:
    sites = []
    for s in r.get("also_defined_at") or []:
        f, _, n = s.rpartition(":")
        try:
            n = int(n)
        except ValueError:
            continue
        line = ""
        if repo_root:
            if f not in cache:
                p = repo_root / f
                cache[f] = p.read_text(encoding="utf-8", errors="ignore").splitlines() if p.is_file() else []
            L = cache[f]
            line = L[n - 1] if 0 < n <= len(L) else ""
        if line and re.search(re.escape(r["id"]) + r"\.\d", line):
            kind = "subclause_reference"
        elif f == r["source_file"]:
            kind = "same_doc_redefinition"
        else:
            kind = "cross_doc_redefinition"
        sites.append({"site": s, "kind": kind, "snippet": md_clean(line)[:140] if line else ""})
    return sites


def effort(cat: str, acs: int, raw_len: int, severity: str, dup: bool) -> dict:
    base = {"failing_tests": 2.0, "ambiguous_tests": 2.0, "untraced": 6.0, "code_no_test": 2.5,
            "tests_not_executed": 1.0, "needs_ci_l3": 0.5}[cat]
    mult = 1.0
    if acs > 6:
        mult += 0.5
    if raw_len > 1500:
        mult += 0.5
    h = base * mult + (1.0 if severity == "Critical" else 0) + (0.5 if dup else 0)
    band = "XS" if h <= 1 else "S" if h <= 4 else "M" if h <= 10 else "L"
    return {"hours": round(h, 1), "band": band, "confidence": "low" if cat == "untraced" else "medium",
            "basis": f"category {cat} base {base}h x{mult}" + (" +1h L5 review" if severity == "Critical" else "") + (" +0.5h dup" if dup else "")}


def next_steps(cat: str, rid: str, code: list, tests: list, failing: list, cfg: dict) -> list[str]:
    q = f"git grep -n -w '{rid}' -- packages apps reva scripts tests deploy"
    if cat == "failing_tests":
        s = [f"Reproduce: python -m pytest -q {' '.join(failing[:5]) or '<mapped tests>'}",
             "Classify each failure: product defect vs stale test vs environment (see remediation/findings_tasks.md FT-D* for already-diagnosed causes)",
             "Fix the defect (or update the test AND the requirement text together, never only the test)",
             "Re-run the mapped tests until all pass on one commit; attach junit as L2"]
    elif cat == "ambiguous_tests":
        s = [f"Run the mapped tests: python -m pytest -q {' '.join(failing[:5])}",
             "Fix the failing ones (passing tests do not cancel failing ones: policy 1.1 → Ambiguous)",
             "Confirm passing tests actually assert this requirement (not just mention the ID)"]
    elif cat == "untraced":
        s = [f"Discovery: search for an implementation under another name: {q}; then search by key terms from the requirement text",
             "If an implementation exists: add a trace (pytest.mark.req('" + rid + "') on tests; ID in docstring of the implementing module) and a test per acceptance criterion",
             "If none exists: implement behind the documented interfaces, or record a negative_proof (absence search + repro_command) → status Not Implemented, never silently",
             "If the requirement is obsolete or duplicated: get owner sign-off and mark it in the registry (do not delete silently)"]
    elif cat == "code_no_test":
        s = [f"Read the referenced code: {', '.join(code[:3])}",
             "Write one test per acceptance criterion; mark with @pytest.mark.req('" + rid + "') and add to requirements-test-map.json",
             "Run locally (L2), then via CI (L3)"]
    elif cat == "tests_not_executed":
        s = [f"Find why mapped tests did not run (marker integration/slow/performance excluded? not collected?): {', '.join(tests[:3])}",
             "Run them in the right environment (services via deploy/docker-compose.yml if integration): worker C scope for heavy suites",
             "Attach the junit (L2) and make the suite part of an L3-eligible workflow"]
    else:  # needs_ci_l3
        s = ["Depends on FT-F04 (real CI on dev_local). After it lands: confirm the mapped tests run in an L3-eligible workflow ("
             + ", ".join((cfg.get("ci") or {}).get("l3_eligible_workflows") or []) + ")",
             "Review that the passing tests actually assert the requirement (spot-check against acceptance criteria below); add missing assertions",
             "Record the green run id as L3 on the same commit as the L2 run"]
    return s


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--audit-output", type=Path, default=KIT_ROOT / "audit-output")
    ap.add_argument("--out-dir", type=Path, default=KIT_ROOT / "remediation")
    ap.add_argument("--config", type=Path, default=KIT_ROOT / "audit-config.json")
    ap.add_argument("--repo-root", type=Path, default=None, help="read-only clone, for duplicate-site classification")
    ap.add_argument("--epic-size", type=int, default=60)
    ap.add_argument("--generated-at", default="2026-10-19T00:00:00Z")
    a = ap.parse_args()
    O, R = a.audit_output, a.out_dir
    R.mkdir(parents=True, exist_ok=True)
    (R / "epics").mkdir(exist_ok=True)
    idx = load(O / "requirements_index.json", {})
    trace = load(O / "traceability_detail.json", {})
    # Prefer the merged main+extended results (an extended result overrides the same test case).
    TR = O / "test_results_merged" if (O / "test_results_merged" / "per_requirement.json").is_file() else O / "test_results"
    perreq = load(TR / "per_requirement.json", {})
    failed_cases = load(TR / "failed_cases.json", [])
    gaps = load(O / "residual_gaps.json", {}) or {}
    mem = load(O / "audit-memory.json", {}) or {}
    ft = load(R / "findings_tasks.json", {"tasks": [], "env_only_failures": []})
    cfg = load(a.config, {}) or {}
    commit = idx.get("commit") or mem.get("audited_commit")
    tpl = (cfg.get("links") or {}).get("code_line_template", "")
    memreq = mem.get("requirements") or {}
    sev_map = gaps.get("derived_severity") or {}
    gap_map = gaps.get("residual_gaps") or {}

    # failing test -> FT task
    test_to_ft = {}
    for t in ft.get("tasks", []):
        for nid in t.get("tests_covered") or []:
            test_to_ft[nid] = t["id"]
    for e in ft.get("env_only_failures", []):
        test_to_ft[e["test"]] = "ENV"
    def nodeid_of(fc):
        cls, name = fc.get("classname", ""), fc.get("name", "")
        parts = cls.split(".")
        for i in range(len(parts), 0, -1):
            path = "/".join(parts[:i]) + ".py"
            if (a.repo_root and (a.repo_root / path).is_file()) or i == len(parts) - (1 if parts[-1][:1].isupper() else 0):
                rest = parts[i:]
                return "::".join([path] + rest + [name])
        return f"{cls}::{name}"
    req_fail_ft = collections.defaultdict(set)
    req_fail_nodes = collections.defaultdict(list)
    for fc in failed_cases:
        nid = nodeid_of(fc)
        for rid in fc.get("mapped_requirements") or []:
            req_fail_nodes[rid].append(nid)
            if nid in test_to_ft:
                req_fail_ft[rid].add(test_to_ft[nid])

    cache: dict = {}
    tasks, dup_tasks = [], []
    for r in sorted(idx.get("requirements") or [], key=lambda x: x["id"]):
        rid = r["id"]
        m = memreq.get(rid, {})
        tr = trace.get(rid, {}) if isinstance(trace, dict) else {}
        code = sorted(set(tr.get("code") or []), key=lambda c: (0 if c.startswith(("packages/", "apps/", "reva/", "backend/")) else 1, c))
        infra = sorted(set(tr.get("infra") or []))
        tests = sorted(set((tr.get("tests") or []) + (tr.get("test_map_nodeids") or [])))
        pr = perreq.get(rid) or {}
        passed, failed = int(pr.get("passed") or 0), int(pr.get("failed") or 0)
        status, tier = m.get("status", "Not Verified"), m.get("proof_tier_achieved", "L0")
        severity = sev_map.get(rid) or m.get("severity") or "Medium"
        dsites = classify_dups(r, a.repo_root, cache)
        real_dups = [s for s in dsites if s["kind"] != "subclause_reference"]
        cats = []
        if failed and not passed:
            cats.append("failing_tests")
        if failed and passed:
            cats.append("ambiguous_tests")
        if not code and not infra and not tests:
            cats.append("untraced")
        if (code or infra) and not tests:
            cats.append("code_no_test")
        if tests and not (passed or failed):
            cats.append("tests_not_executed")
        if passed and not failed:
            cats.append("needs_ci_l3")
        if not cats:
            cats.append("untraced")
        primary = min(cats, key=CAT_ORDER.index)
        gap_list = [CATEGORIES[c] for c in cats]
        if real_dups:
            gap_list.append(f"ID defined at {len(real_dups)} other site(s): see duplicate task DUP-{rid}")
        gap_list += [g for g in gap_map.get(rid, []) if g not in gap_list] or [
            "No L3: no L3-eligible CI workflow green on the audited commit", "No L4 non-prod runtime evidence"]
        if severity == "Critical" and not any("L5" in g for g in gap_list):
            gap_list.append("Critical: L5 independent dual-control review missing")
        prio, prio_reason = derive_priority(r, cats, severity)
        acs = derive_acs(r)
        doc_abbr = re.sub(r"[^A-Z0-9]", "", Path(r["source_file"]).stem.upper().replace("REQUIREMENTS", "").replace("REQIREMENTS", ""))[:14] or "DOC"
        have = {"L1": bool(code or infra), "L2": bool(passed and not failed), "L3": False, "L4": False, "L5": False}
        need = ["L2", "L3 (same commit) or L4"] + (["L5 (reviewer ≠ producer)"] if severity == "Critical" else [])
        links = []
        for c in code[:25]:
            p, _, ln = c.rpartition(":")
            links.append(tpl.format(commit=commit, path=p, start=ln, end=ln) if tpl and ln.isdigit() else c)
        raw = r.get("raw_text") or ""
        t = {
            "task_id": f"RT-{rid}", "requirement_id": rid, "title": f"{rid}: {summary_title(r)}"[:240],
            "type": r.get("type"), "priority": prio, "priority_reason": prio_reason, "doc_priority": r.get("priority"),
            "derived_severity": severity,
            "source": f"{r['source_file']}:{r['line_range'][0]}-{r['line_range'][1]}", "definition_site": r.get("definition_site"),
            "statement_verbatim": raw[:6000], "statement_truncated": len(raw) > 6000,
            "current": {"status": status, "proof_tier": tier, "tests_passed": passed, "tests_failed": failed},
            "gap_category": primary, "gap_categories": cats, "gaps": gap_list,
            "next_steps": next_steps(primary, rid, code, tests, req_fail_nodes.get(rid, []), cfg)
                          + ([f"Resolve duplicate definition first: DUP-{rid}"] if real_dups else []),
            "mapped_paths": {"code": code[:50], "tests": tests[:50], "infra": infra[:25], "code_links": links,
                              "claimed_by_docs": (tr.get("claimed_existing") or [])[:25],
                              "failing_tests": sorted(set(req_fail_nodes.get(rid, [])))[:25]},
            "acceptance_criteria": acs,
            "proof_plan": {"policy": "1.1.0", "have": have, "needed_for_implemented": need,
                           "missing": [n for n in need if not have.get(n[:2])],
                           "evidence_template": "examples/evidence.json (items with requirement_id=" + rid + ")"},
            "depends_on": sorted(set(["FT-F04"] + list(req_fail_ft.get(rid, set())) + (["FT-F09"] if real_dups else []))),
            "estimated_effort": effort(primary, len(acs), len(raw), severity, bool(real_dups)),
            "epic_id": None, "status": "Open", "claimed_by": None,
        }
        t["_doc_abbr"] = doc_abbr
        tasks.append(t)
        if real_dups:
            dup_tasks.append({
                "task_id": f"DUP-{rid}", "requirement_id": rid, "primary_definition": t["source"],
                "sites": real_dups, "subclause_references_ignored": len(dsites) - len(real_dups),
                "kinds": dict(collections.Counter(s["kind"] for s in real_dups)),
                "resolution_steps": [
                    "Decide the canonical definition (default: requirements-registry.json entry, else the primary site above)",
                    "cross_doc_redefinition: rename the non-canonical ID with a document namespace (e.g. GUI-" + rid + ") or turn it into a reference 'see " + rid + " (" + r["source_file"] + ")'",
                    "same_doc_redefinition: merge the text into one definition or renumber the later one",
                    "Update requirements-test-map.json and pytest marks for any renamed ID",
                    "Re-run parse_md_requirements.py: this ID must show 0 redefinition sites"],
                "priority": "P2" if prio in ("P0", "P1") else "P3", "status": "Open",
            })

    known = {t["requirement_id"] for t in tasks}
    orphans = sorted(k for k in perreq if k not in known)
    (R / "orphan_test_ids.json").write_text(json.dumps({"count": len(orphans), "note":
        "IDs referenced by tests (marks/test map) that no requirement document defines; many are sub-clauses (X.C01). "
        "Either add them to a requirement doc / registry or fix the test reference (parent task FT-F09).",
        "ids": [{"id": k, "passed": perreq[k].get("passed", 0), "failed": perreq[k].get("failed", 0)} for k in orphans]}, indent=1), encoding="utf-8")

    # epics: (doc, category) chunks
    groups = collections.defaultdict(list)
    for t in tasks:
        groups[(t["_doc_abbr"], t["gap_category"], t["source"].split(":")[0])].append(t)
    epics = []
    for (abbr, cat, src), ts in sorted(groups.items(), key=lambda kv: (kv[0][0], CAT_ORDER.index(kv[0][1]))):
        ts.sort(key=lambda t: (PRIO_ORDER.index(t["priority"]), t["requirement_id"]))
        chunks = [ts[i:i + a.epic_size] for i in range(0, len(ts), a.epic_size)]
        for n, ch in enumerate(chunks, 1):
            eid = f"EPIC-{abbr}-{CAT_ABBR[cat]}" + (f"-{n:02d}" if len(chunks) > 1 else "")
            for t in ch:
                t["epic_id"] = eid
            epics.append({"epic_id": eid, "source_doc": src, "gap_category": cat, "category_meaning": CATEGORIES[cat],
                          "task_count": len(ch), "by_priority": dict(collections.Counter(t["priority"] for t in ch)),
                          "estimated_hours": round(sum(t["estimated_effort"]["hours"] for t in ch), 1),
                          "file": f"epics/{eid}.md", "task_ids": [t["task_id"] for t in ch]})
    for t in tasks:
        t.pop("_doc_abbr", None)

    # write requirement tasks
    (R / "requirement_tasks.json").write_text(json.dumps({"schema": "eoip-requirement-tasks/1.0", "audited_commit": commit,
        "generated_at": a.generated_at, "generator": "audit-scripts/generate_fix_tasks.py", "count": len(tasks),
        "categories": CATEGORIES, "tasks": tasks}, indent=1, ensure_ascii=False), encoding="utf-8")
    with (R / "requirement_tasks.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["task_id", "requirement_id", "epic_id", "priority", "gap_category", "status", "proof_tier", "source",
                    "type", "derived_severity", "effort_hours", "depends_on", "title", "first_next_step", "code_paths", "test_paths"])
        for t in tasks:
            w.writerow([t["task_id"], t["requirement_id"], t["epic_id"], t["priority"], t["gap_category"], t["current"]["status"],
                        t["current"]["proof_tier"], t["source"], t["type"], t["derived_severity"], t["estimated_effort"]["hours"],
                        ";".join(t["depends_on"]), t["title"], t["next_steps"][0], ";".join(t["mapped_paths"]["code"][:10]),
                        ";".join(t["mapped_paths"]["tests"][:10])])
    (R / "epics.json").write_text(json.dumps({"count": len(epics), "epics": epics}, indent=1), encoding="utf-8")
    (R / "duplicate_id_tasks.json").write_text(json.dumps({"count": len(dup_tasks), "note":
        "Only real redefinitions; '<ID>.<n>' sub-clause numbering is reported but not treated as a duplicate.",
        "tasks": dup_tasks}, indent=1, ensure_ascii=False), encoding="utf-8")

    # epic markdown
    by_id = {t["task_id"]: t for t in tasks}
    for e in epics:
        L = [f"# {e['epic_id']}: {e['source_doc']} · {e['gap_category']}", "",
             f"*{e['category_meaning']}.* {e['task_count']} tasks, ~{e['estimated_hours']} h, priorities {e['by_priority']}. "
             f"Audited commit `{commit}`.", "",
             "**How to work this epic:** claim it (remediation/README.md §2), then take tasks top-down (sorted by priority). "
             "For each: do the next steps, write tests for the acceptance criteria, produce evidence items, release the lock.", ""]
        for tid in e["task_ids"]:
            t = by_id[tid]
            L += [f"## {t['task_id']} [{t['priority']}] {t['title']}", "",
                  f"- **Source:** `{t['source']}` ({t['definition_site']}) · **Type:** {t['type']} · **Severity:** {t['derived_severity']}",
                  f"- **Now:** {t['current']['status']} / {t['current']['proof_tier']} (tests passed {t['current']['tests_passed']}, failed {t['current']['tests_failed']})",
                  f"- **Gaps:** " + "; ".join(t["gaps"]),
                  f"- **Depends on:** {', '.join(t['depends_on'])} · **Effort:** {t['estimated_effort']['hours']} h ({t['estimated_effort']['band']}, {t['estimated_effort']['confidence']} confidence)",
                  "", "<details><summary>Requirement text (verbatim)</summary>", "", "```text",
                  t["statement_verbatim"][:2500] + ("\n[… truncated, see requirement_tasks.json]" if len(t["statement_verbatim"]) > 2500 else ""),
                  "```", "</details>", "", "**Next steps**"]
            L += [f"{i}. {s}" for i, s in enumerate(t["next_steps"], 1)]
            L += ["", "**Acceptance criteria**"] + [f"- [ ] {c}" for c in t["acceptance_criteria"]]
            mp = t["mapped_paths"]
            if mp["code"] or mp["tests"] or mp["failing_tests"]:
                L += ["", "**Mapped paths**"]
                if mp["code"]:
                    L.append("- code: " + ", ".join(f"[`{c}`]({u})" if u.startswith("http") else f"`{c}`" for c, u in zip(mp["code"][:8], mp["code_links"][:8])))
                if mp["tests"]:
                    L.append("- tests: " + ", ".join(f"`{x}`" for x in mp["tests"][:8]))
                if mp["failing_tests"]:
                    L.append("- failing: " + ", ".join(f"`{x}`" for x in mp["failing_tests"][:8]))
            pp = t["proof_plan"]
            L += ["", f"**Proof plan (1.1):** have {[k for k, v in pp['have'].items() if v] or 'nothing'}; needs {pp['needed_for_implemented']}; missing {pp['missing']}", ""]
        (R / e["file"]).write_text("\n".join(L) + "\n", encoding="utf-8")

    # duplicate md
    L = ["# Duplicate requirement-ID resolution tasks", "",
         f"{len(dup_tasks)} IDs are defined at more than one site (sub-clause references like `CRA-001.1` excluded). Parent: FT-F09.", "",
         "| Task | ID | Primary | Other sites | Kinds | Priority |", "|---|---|---|---|---|---|"]
    for d in dup_tasks:
        L.append(f"| {d['task_id']} | `{d['requirement_id']}` | `{d['primary_definition']}` | "
                 + "<br>".join(f"`{s['site']}`" for s in d["sites"][:6]) + (f"<br>… +{len(d['sites'])-6}" if len(d["sites"]) > 6 else "")
                 + f" | {d['kinds']} | {d['priority']} |")
    L += ["", "Resolution steps (each task): see `resolution_steps` in duplicate_id_tasks.json."]
    (R / "duplicate_id_tasks.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    # findings tasks md
    F = ["# Finding & defect tasks (hand-written)", "",
         f"Audited commit `{commit}`. Source: findings_tasks.json. {len(ft.get('tasks', []))} tasks; "
         f"{len({n for t in ft.get('tasks', []) for n in (t.get('tests_covered') or [])})} failing test node(s) covered by a task; "
         f"{len(failed_cases)} test cases fail in `{TR.name}/`; "
         f"{len(ft.get('env_only_failures', []))} environment-only failure(s) remain.", ""]
    for t in ft.get("tasks", []):
        F += [f"## {t['id']} [{t['priority']}] {t['title']}", "",
              f"| Field | Value |", "|---|---|",
              f"| ID | {t['id']} (finding {t.get('finding') or 'n/a'}, epic {t.get('epic')}) |",
              f"| Type | {t['type']} |", f"| Priority | {t['priority']} |"]
        for key, label in [("description", "Description"), ("api_contracts", "API contracts"), ("data_model", "Data model"),
                           ("performance_targets", "Performance targets"), ("observability", "Observability"),
                           ("backward_compatibility", "Backward compatibility")]:
            F.append(f"| {label} | {str(t.get(key, 'UNKNOWN')).replace('|', '/')} |")
        for key, label in [("preconditions", "Preconditions"), ("acceptance_criteria", "Acceptance criteria"),
                           ("automated_tests", "Automated tests"), ("security_controls", "Security controls"),
                           ("implementation_notes", "Implementation notes (file:line)")]:
            F.append(f"| {label} | " + "<br>".join("• " + str(x).replace("|", "/") for x in (t.get(key) or ["UNKNOWN"])) + " |")
        F.append("| Proof plan | " + "<br>".join(f"**{k}**: {str(v).replace('|', '/')}" for k, v in (t.get("proof_plan") or {}).items()) + " |")
        ee = t.get("estimated_effort") or {}
        F.append(f"| Estimated effort | {ee.get('hours','UNKNOWN')} h ({ee.get('band','')}){(' – ' + ee['notes']) if ee.get('notes') else ''} |")
        if t.get("tests_covered"):
            F.append("| Failing tests covered | " + "<br>".join(f"`{x}`" for x in t["tests_covered"]) + " |")
        if t.get("parent"):
            F.append(f"| Parent | {t['parent']} |")
        if t.get("children"):
            F.append("| Child tasks | " + ", ".join(t["children"]) + " |")
        if t.get("status") and t["status"] != "Open":
            F.append(f"| Status | {t['status']} (owner {t.get('owner')}) |")
        if t.get("extended_run"):
            er = t["extended_run"]
            F.append(f"| Extended run ({er.get('defect')}) | " + str(er.get("evidence") or f"severity {er.get('severity', 'n/a')}; source {er.get('source')}").replace("|", "/") + " |")
        if t.get("sub_items"):
            F += ["", "| Sub-item test | Issue | Child task | Decision |", "|---|---|---|---|"]
            F += [f"| `{x['test']}` | {x['issue'].replace('|', '/')} | {x['child_task']} | {x['decision']} |" for x in t["sub_items"]]
        F.append("")
    F += ["## Environment-only failures (no product task)", "", "| Test | Reason |", "|---|---|"]
    F += [f"| `{e['test']}` | {e['reason']} |" for e in ft.get("env_only_failures", [])] or ["| (none) | |"]
    if ft.get("env_only_resolved"):
        F += ["", "## Environment-only failures resolved by the extended run", "", "| Test | Fix |", "|---|---|"]
        F += [f"| `{e['test']}` | {e['fix']} |" for e in ft["env_only_resolved"]]
    for rc in ft.get("reclassified", []):
        F += ["", f"Reclassified from {rc['from']} to **{rc['to']}**: " + ", ".join(f"`{x}`" for x in rc["tests"]) + f". {rc['why']}."]
    (R / "findings_tasks.md").write_text("\n".join(F) + "\n", encoding="utf-8")

    # merged audit_tasks.json
    queue = []
    for t in ft.get("tasks", []):
        kind = ("finding" if t["id"].startswith("FT-F") else "test_harness" if t["id"].startswith("FT-H")
                else "kit" if t["id"].startswith("FT-K") else "security" if t["id"].startswith("FT-SEC") else "defect")
        queue.append({"task_id": t["id"], "kind": kind, "requirement_id": t.get("finding"),
                      "title": t["title"], "priority": t["priority"], "epic_id": t.get("epic"), "gap_category": "finding",
                      "status": t.get("status", "Open"), "estimated_hours": (t.get("estimated_effort") or {}).get("hours"),
                      "source": "remediation/findings_tasks.json", "depends_on": sorted(set(t.get("depends_on") or []) | ({t["parent"]} if t.get("parent") else set())),
                      "parent": t.get("parent"), "children": t.get("children") or [], "claimed_by": None})
    for t in tasks:
        queue.append({"task_id": t["task_id"], "kind": "requirement", "requirement_id": t["requirement_id"], "title": t["title"],
                      "priority": t["priority"], "epic_id": t["epic_id"], "gap_category": t["gap_category"], "status": t["status"],
                      "estimated_hours": t["estimated_effort"]["hours"], "source": t["source"], "depends_on": t["depends_on"],
                      "current_status": t["current"]["status"], "proof_tier": t["current"]["proof_tier"], "claimed_by": None})
    for d in dup_tasks:
        queue.append({"task_id": d["task_id"], "kind": "duplicate_id", "requirement_id": d["requirement_id"],
                      "title": f"Resolve duplicate definitions of {d['requirement_id']}", "priority": d["priority"],
                      "epic_id": "EPIC-DUPLICATE-IDS", "gap_category": "duplicate_definition", "status": "Open",
                      "estimated_hours": 0.5 + 0.25 * len(d["sites"]), "source": d["primary_definition"],
                      "depends_on": ["FT-F09"], "claimed_by": None})
    (O / "audit_tasks.json").write_text(json.dumps({"schema": "eoip-audit-tasks/1.0", "audited_commit": commit,
        "generated_at": a.generated_at, "count": len(queue),
        "by_kind": dict(collections.Counter(q["kind"] for q in queue)),
        "by_priority": dict(sorted(collections.Counter(q["priority"] for q in queue).items())),
        "tasks": queue}, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"requirement_tasks": len(tasks), "finding_tasks": len(ft.get("tasks", [])), "duplicate_tasks": len(dup_tasks),
                      "epics": len(epics), "queue": len(queue),
                      "by_priority": dict(sorted(collections.Counter(t["priority"] for t in tasks).items())),
                      "by_category": dict(collections.Counter(t["gap_category"] for t in tasks))}))


if __name__ == "__main__":
    main()
