#!/usr/bin/env python3
"""Generate audit_gaps_requirements.md (+ requirements_status.csv) from kit outputs.

Inputs (all optional except --memory): audit-memory.json, requirements_index.json,
traceability_detail.json, test_results/summary.json, evidence/ci_runs.json,
evidence/static_summary.json, findings.json, audit-config.json, stack.json.

Statuses are read from audit-memory.json (computed by proof_policy.py); this script
never upgrades a status. Secrets: it only prints paths/lines, never file contents.
"""
from __future__ import annotations

import argparse
import collections
import re
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

KIT_ROOT = Path(__file__).resolve().parent.parent
STATUS_ORDER = ["Implemented", "Partially Implemented", "Ambiguous", "Not Verified", "Not Implemented"]


def load(p):
    if p and Path(p).is_file():
        return json.loads(Path(p).read_text(encoding="utf-8"))
    return None


def gh_link(cfg, commit, path, lines):
    tpl = ((cfg or {}).get("links") or {})
    if lines:
        t = tpl.get("code_line_template")
        if t:
            return t.format(commit=commit, path=path, start=lines[0], end=lines[1])
    t = tpl.get("file_template")
    return t.format(commit=commit, path=path) if t else path


def table(rows, headers):
    out = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    for r in rows:
        out.append("| " + " | ".join(str(c).replace("|", "\\|") for c in r) + " |")
    return "\n".join(out)



_N_TESTS_RE = re.compile(r"\((\d+) tests\)")


def _x10_label(x: dict) -> str:
    """'N tests in M items' for a grouped defect (e.g. X-10); '(4 tests)' in an item counts as 4."""
    items = x.get("items") or []
    n = 0
    for it in items:
        m = _N_TESTS_RE.search(it.get("test", ""))
        n += int(m.group(1)) if m else 1
    return f"{n} tests in {len(items)} items (see FT-X10)"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out-dir", type=Path, default=KIT_ROOT / "audit-output")
    ap.add_argument("--memory", type=Path)
    ap.add_argument("--requirements", type=Path)
    ap.add_argument("--traceability-detail", type=Path)
    ap.add_argument("--test-summary", type=Path)
    ap.add_argument("--ci-runs", type=Path)
    ap.add_argument("--static-summary", type=Path)
    ap.add_argument("--findings", type=Path)
    ap.add_argument("--stack", type=Path)
    ap.add_argument("--skipped", type=Path, help="JSON list of {item, reason}")
    ap.add_argument("--config", type=Path, default=KIT_ROOT / "audit-config.json")
    ap.add_argument("--out", type=Path)
    a = ap.parse_args()
    d = a.out_dir
    mem = load(a.memory or d / "audit-memory.json") or {}
    idx = load(a.requirements or d / "requirements_index.json") or {}
    trace = load(a.traceability_detail or d / "traceability_detail.json") or {}
    tests = load(a.test_summary or d / "test_results" / "summary.json") or {}
    ci = load(a.ci_runs or d / "evidence" / "ci_runs.json") or {}
    static = load(a.static_summary or d / "evidence" / "static_summary.json") or {}
    findings = load(a.findings or d / "findings.json") or {}
    stack = load(a.stack or d / "stack.json") or {}
    skipped = load(a.skipped or d / "skipped.json") or []
    cfg = load(a.config) or {}
    out = a.out or d / "audit_gaps_requirements.md"

    commit = mem.get("audited_commit") or mem.get("last_audited_commit") or findings.get("audited_commit") or "UNKNOWN"
    repo = (cfg.get("repo") or {})
    reqs = mem.get("requirements") or {}
    idx_by = {r["id"]: r for r in idx.get("requirements") or []}
    tr_by = {}
    if isinstance(trace, dict) and not (trace.get("requirements") or trace.get("rows")):
        for rid, r in trace.items():
            if isinstance(r, dict):
                code, tst, infra = r.get("code") or [], (r.get("tests") or []) + (r.get("test_map_nodeids") or []), r.get("infra") or []
                et = "+".join(x for x, v in (("code", code), ("test", tst), ("infra", infra)) if v) or "none"
                tr_by[rid] = {"evidence_type": et, "code_paths": code, "test_paths": tst}
    else:
        for r in (trace.get("requirements") or trace.get("rows") or []):
            tr_by[r.get("requirement_id") or r.get("id")] = r

    by_status = collections.Counter(v.get("status", "Not Verified") for v in reqs.values())
    by_tier = collections.Counter(v.get("proof_tier_achieved", "L0") for v in reqs.values())
    by_src = collections.defaultdict(collections.Counter)
    for rid, v in reqs.items():
        src = (idx_by.get(rid) or {}).get("source_file") or (v.get("source") or "?").rsplit(":", 1)[0]
        by_src[src][v.get("status", "Not Verified")] += 1
    by_sev = collections.Counter(v.get("severity", "?") for v in reqs.values())
    ev_types = collections.Counter((tr_by.get(r) or {}).get("evidence_type", "none") for r in reqs)

    L = []
    L.append(f"# EOIP audit: requirements gaps and risks (first pass)\n")
    L.append(f"- **Repository:** {repo.get('url','?')} (branch `{repo.get('branch','?')}`)")
    L.append(f"- **Audited commit:** `{commit}`" + (f" ([tree]({repo.get('url')}/tree/{commit}))" if repo.get("url") else ""))
    L.append(f"- **Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} by `generate_audit_report.py`")
    L.append(f"- **Proof policy:** {mem.get('proof_policy_version') or cfg.get('proof_policy_version','1.1.0')}. "
             "L1 never counts toward Partial or Implemented. Partial needs L2 plus residual gaps. Implemented needs L2 and (same-commit L3, or L4). Critical needs L3 plus an independent L5.")
    L.append(f"- **Reviewer:** {findings.get('reviewer','n/a')}")
    comp = [(lbl, f) for lbl, f in (("requirements catalogue", "requirements.md"), ("implementation status", "implementation.md"),
                                    ("dashboard", "tracker.html")) if (d / f).is_file()]
    if comp:
        L.append("- **Companion documents:** " + " · ".join(f"[{f}]({f}) ({lbl})" for lbl, f in comp))
    L.append("")
    L.append("> Honesty note: this is an automated first pass plus a limited manual read. No L4 (behavioural/E2E) or L5 (independent human review) evidence was produced, and no CI workflow that qualifies for L3 was green on this commit, so **no requirement can reach Implemented** under policy 1.1.\n")

    if stack:
        L.append("## 1. Stack summary\n")
        for k, v in stack.items():
            L.append(f"- **{k}:** {v}")
        L.append("")
    obj = stack.get("_objective") if isinstance(stack, dict) else None
    L.append("## 2. Core objective (from repo docs)\n")
    L.append(findings.get("core_objective") or obj or "_Not extracted._")
    L.append("")

    L.append("## 3. Requirement status (policy 1.1)\n")
    L.append(f"Total requirements indexed: **{len(reqs)}** from {len(by_src)} source documents.\n")
    L.append(table([(s, by_status.get(s, 0)) for s in STATUS_ORDER if by_status.get(s) or s in ("Implemented", "Not Verified")], ["Status", "Count"]))
    L.append("")
    L.append("What the statuses mean here: **Partially Implemented** = at least one mapped test passed in the local sandbox run (L2) on this commit, with residual gaps (always: no L3 CI, no L4 runtime proof). The req→test mapping comes from the repo's own `requirements-test-map.json` plus ID mentions in test files, and has not been independently reviewed, so treat it as a lead, not a closure. **Ambiguous** = passing and failing mapped tests on the same commit. **Not Verified** = L1 code reference only, or nothing. **Implemented: 0**, because no L3 or L4 evidence exists.\n")
    L.append(table(sorted(by_tier.items()), ["Highest proof tier", "Count"]))
    L.append("")
    L.append(table(by_sev.most_common(), ["Derived severity (from priority/type)", "Count"]))
    L.append("")
    L.append("Traceability (static ID references, i.e. L1 candidates only):\n")
    L.append(table(ev_types.most_common(), ["Evidence type", "Count"]))
    L.append("")
    L.append("Per source document (top 15 by size):\n")
    rows = []
    for src, c in sorted(by_src.items(), key=lambda kv: -sum(kv[1].values()))[:15]:
        rows.append((f"`{src}`", sum(c.values()), c.get("Partially Implemented", 0), c.get("Ambiguous", 0), c.get("Not Verified", 0), c.get("Implemented", 0)))
    L.append(table(rows, ["Source", "Reqs", "Partial", "Ambiguous", "Not Verified", "Implemented"]))
    L.append("\nFull per-requirement detail: `requirements_status.csv`, `audit-memory.json`, `tracker.html`.\n")

    L.append("## 4. CI status on the audited commit\n")
    runs = ci.get("runs") or ci.get("workflow_runs") or []
    elig = set((cfg.get("ci") or {}).get("l3_eligible_workflows") or [])
    if runs:
        rr = []
        tpl = (cfg.get("ci") or {}).get("run_template", "")
        for r in runs:
            link = tpl.format(run_id=r.get("id")) if tpl else r.get("html_url", "")
            wf = Path(r.get("path") or "").name
            rr.append((r.get("name") or r.get("workflow"), r.get("conclusion") or r.get("status"), "yes" if wf in elig else "no (placeholder/ineligible)", f"[{r.get('id')}]({link})"))
        L.append(table(rr, ["Workflow", "Conclusion", "L3-eligible", "Run"]))
    else:
        L.append("_No CI runs recorded._")
    L.append("")

    L.append("## 5. Local test results\n")
    if tests:
        keys = ["tests", "passed", "failed", "errors", "skipped", "duration_s"]
        L.append(table([(k, tests.get(k, "")) for k in keys if k in tests], ["Metric", "Value"]))
        if tests.get("notes"):
            L.append("\n" + str(tests["notes"]))
        L.append(f"\nRequirements with ≥1 passing mapped test (L2 candidates): **{tests.get('requirements_with_passing_tests','?')}**; with ≥1 failing mapped test: **{tests.get('requirements_with_failing_tests','?')}**.")
    else:
        L.append("_Tests not run._")
    L.append("")

    ext_dir = d / "test_results_extended"
    ext = load(ext_dir / "extended_summary.json")
    if ext:
        defects = load(ext_dir / "defects.json") or {}
        sc = load(ext_dir / "status_changes.json") or {}
        merged = (load(d / "test_results_merged" / "summary.json") or {}).get("counts") or {}
        ftj = load(d.parent / "remediation" / "findings_tasks.json") or {}
        x2t = collections.defaultdict(list)
        for t in ftj.get("tasks") or []:
            dx = (t.get("extended_run") or {}).get("defect") or ""
            for xid in re.findall(r"X-\d+", dx):
                x2t[xid].append(t["id"])
        L.append("## 5a. Extended test run\n")
        L.append(f"Second pass over the tests the first audit skipped, on the same commit `{(ext.get('commit') or commit)[:12]}`. "
                 f"Ran in {ext.get('run_location', 'a copy of the clone')}.\n")
        env = ext.get("environment") or {}
        L += [f"- **{k}:** {v}" for k, v in env.items() if k in ("python", "data_dir", "node", "stack")]
        if ext.get("environment", {}).get("stack_workarounds") or ext.get("stack_workarounds"):
            L.append("- **Workarounds in the copy (not fixes; worker C's D-01/D-02/D-03 = X-03/X-04/X-11):** " + "; ".join(ext.get("environment", {}).get("stack_workarounds") or ext.get("stack_workarounds")))
        L.append("")
        rows = []
        for name, v in (ext.get("suites") or {}).items():
            if isinstance(v, dict) and "tests" in v:
                rows.append((name, v.get("tests"), v.get("passed"), v.get("failed"), (v.get("note") or "").replace("|", "/")[:220]))
            elif isinstance(v, dict) and "journeys" in v:
                rows.append((name, f"{v['journeys']} journeys", v.get("passed"), v.get("failed"), (v.get("note") or "")[:220]))
            elif isinstance(v, dict) and "as_is" in v:
                a_, w_ = v["as_is"], v.get("with_auth_wrapper") or {}
                rows.append((name, f"{a_.get('requests')} req", 0, f"{a_.get('failures')} (as-is), {w_.get('failures')} (with auth)",
                             f"as-is: {a_.get('cause')}; with auth: {w_.get('cause')}. Median {v.get('median_ms')} ms"))
            else:
                rows.append((name, "", "", "", str(v)))
        L.append(table(rows, ["Suite", "Tests", "Passed", "Failed", "Note"]))
        L.append("")
        if merged:
            L.append(f"Merged pytest results (`test_results_merged/`, main run with extended results overriding the same test "
                     f"case): **{merged.get('cases')}** cases, **{merged.get('passed')}** passed, **{merged.get('failed')}** failed, "
                     f"**{merged.get('skipped')}** skipped. Evidence was rebuilt from these by `build_evidence.py` and merged with "
                     f"`evidence_extended.json` (de-duplicated by evidence_id). The pre-merge bundle is in `evidence/evidence.main-run.json`.\n")
        if sc.get("changes"):
            L.append("Status changes applied by `update_audit_memory.py --mode full` (policy 1.1, recomputed, not hand-edited):\n")
            L.append(table([(c["requirement_id"], c["before"], c["after"],
                             f"{c['tests'].get('passed')} passed / {c['tests'].get('failed')} failed") for c in sc["changes"]],
                           ["Requirement", "Before", "After", "Mapped tests (merged)"]))
            L.append("")
        if defects.get("real_defects"):
            L.append("Defects found or confirmed:\n")
            L.append(table([(x["id"], x.get("severity"), x["title"].replace("|", "/"),
                             "<br>".join(f"`{w}`" for w in (x.get("where") or [])[:3]) or _x10_label(x),
                             ", ".join(x2t.get(x["id"]) or ["UNMAPPED"])) for x in defects["real_defects"]],
                           ["ID", "Severity", "Defect", "Where", "Task(s)"]))
            L.append("")
        if defects.get("test_harness_defects"):
            L.append("Test-harness defects (tests that cannot pass as written):\n")
            L.append(table([(f"`{h['where']}`", h["issue"].replace("|", "/"), ", ".join(h.get("tests") or [])) for h in defects["test_harness_defects"]],
                           ["Where", "Issue", "Tests"]))
            L.append("")
            L.append("Tasks: FT-H01 (GUI npm), FT-D15 (governed_actions; diagnosis corrected), FT-D10 (test_authn order dependency).\n")
        if defects.get("env_only_resolved"):
            L.append("Environment-only failures that pass with the right environment: " +
                     "; ".join(f"`{e['test'].split('::')[-1]}` ({e['fix']})" for e in defects["env_only_resolved"]) + ".\n")
        if ext.get("blocked_or_not_run"):
            L.append("Still not run: " + "; ".join(ext["blocked_or_not_run"]) + ".\n")
        L.append("Diagnostic-only runs (e.g. worker isolation with `start_new_session=True` injected) confirm fixes but are **not** counted as evidence.\n")

    L.append("## 6. Static analysis\n")
    if static:
        L.append(table([(k, v) for k, v in static.items()], ["Tool", "Result"]))
    L.append("")

    L.append("## 7. Top findings (gaps and risks)\n")
    for f in findings.get("findings") or []:
        L.append(f"### {f['id']} [{f['severity']}] {f['title']}\n")
        L.append(f"*{f.get('category','')}*. {f['description']}\n")
        L.append("Evidence:")
        for e in f.get("evidence") or []:
            link = gh_link(cfg, commit, e["path"], e.get("lines"))
            rng = f":{e['lines'][0]}-{e['lines'][1]}" if e.get("lines") else ""
            L.append(f"- [`{e['path']}{rng}`]({link}): {e.get('note','')}")
        if f.get("ci_run"):
            tpl = (cfg.get("ci") or {}).get("run_template", "")
            L.append(f"- CI run [{f['ci_run']}]({tpl.format(run_id=f['ci_run']) if tpl else ''})")
        L.append(f"\n**Recommendation:** {f.get('recommendation','')}\n")
    if findings.get("positives"):
        L.append("### Positive observations\n")
        L += [f"- {p}" for p in findings["positives"]]
        L.append("")

    L.append("## 8. Skipped / not verified in this pass\n")
    L += [f"- **{s['item']}**: {s['reason']}" for s in skipped] or ["- none recorded"]
    L.append("")
    q = load(d / "audit_tasks.json")
    if q:
        L.append("## 9. Remediation queue\n")
        L.append(f"`audit_tasks.json`: **{q.get('count')}** tasks, by kind {q.get('by_kind')}, by priority {q.get('by_priority')}. "
                 "Details are in `remediation/` (README, rotation/purge plan, findings_tasks.md, epics/*.md, duplicate_id_tasks.md). "
                 "Do FT-F01/FT-F02 (secrets) first, then FT-F04 (CI), which unblocks L3 for every requirement task.\n")
    L.append("## 10. Sign-off\n")
    L.append("- Producer: automated kit run + first-pass reviewer (same agent). **No L5 independent review**, so nothing here may be treated as Critical-verified.")
    L.append("- Next steps: fix CI (F-04) so L3 becomes possible; get an independent reviewer (L5) for P0/security items; re-run with `--mode delta` against the new commit.")
    out.write_text("\n".join(L) + "\n", encoding="utf-8")

    csv_path = d / "requirements_status.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["requirement_id", "title", "source", "priority", "status", "proof_tier", "evidence_type", "code_paths", "test_paths", "residual_gaps", "git_commit"])
        for rid, v in sorted(reqs.items()):
            t = tr_by.get(rid) or {}
            def j(x):
                return ";".join(x) if isinstance(x, list) else (x or "")
            w.writerow([rid, (v.get("title") or "")[:200], v.get("source", ""), v.get("priority", ""), v.get("status", ""),
                        v.get("proof_tier_achieved", ""), t.get("evidence_type", ""), j(t.get("code_paths"))[:500],
                        j(t.get("test_paths"))[:500], " | ".join(v.get("residual_gaps") or [])[:500], commit])
    print(f"wrote {out} and {csv_path}")


if __name__ == "__main__":
    main()
