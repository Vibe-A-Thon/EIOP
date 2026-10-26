#!/usr/bin/env python3
"""Build evidence.json (proof policy 1.1.0) from pipeline facts — never from claims.

Inputs: requirements index, traceability detail, test_results/per_requirement.json, CI runs for the
audited commit, and audit-config.json (link templates + which workflows are L3-eligible).

Tier assignment (conservative):
  L1  code_link     — requirement id referenced in non-test code at the audited commit (anchors).
  L2  test_run      — mapped test cases executed locally at the audited commit; one item for passing,
                      one for failing (failing items never count as proof; mixed → Ambiguous).
  L3  ci_run        — only if an L3-eligible workflow (runs the real test suite) concluded `success`
                      on the audited commit; placeholder workflows are never eligible.
  L4/L5             — never auto-generated (runtime evidence / independent review are human steps).
The repo's own registry statuses and doc claims are NOT evidence and are ignored here.
Also writes residual_gaps.json used by update_audit_memory.py for Partially Implemented.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from proof_policy import PROOF_POLICY_VERSION  # noqa: E402


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def evi_id(rid: str, suffix: str) -> str:
    return "EVI-" + re.sub(r"[^0-9A-Za-z_-]", "_", rid) + "-" + suffix


def derive_severity(req: dict) -> str:
    pr = (req.get("priority") or "").upper()
    typ = req.get("type") or ""
    if pr == "P0":
        return "Critical" if typ == "Security" else "High"
    if pr == "P1":
        return "High" if typ == "Security" else "Medium"
    if pr in ("P2", "P3"):
        return "Low" if typ != "Security" else "Medium"
    return "Medium"


def code_link(tpl: str, commit: str, anchor: str) -> str:
    path, _, line = anchor.rpartition(":")
    if not line.isdigit():
        path, line = anchor, "1"
    return tpl.format(commit=commit, path=path, start=line, end=line)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--requirements", required=True, type=Path)
    ap.add_argument("--traceability-detail", required=True, type=Path)
    ap.add_argument("--test-results", type=Path, default=None, help="Dir with per_requirement.json + summary.json")
    ap.add_argument("--ci-runs", type=Path, default=None, help="JSON from the GitHub runs API for the commit")
    ap.add_argument("--config", type=Path, required=True)
    ap.add_argument("--commit", required=True)
    ap.add_argument("--agent-id", default="agent-audit-pipeline")
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--gaps-out", required=True, type=Path)
    args = ap.parse_args()

    cfg = json.loads(args.config.read_text(encoding="utf-8"))
    tpl = cfg["links"]["code_line_template"]
    run_tpl = cfg["ci"]["run_template"]
    eligible = cfg["ci"].get("l3_eligible_workflows", [])
    reqs = json.loads(args.requirements.read_text(encoding="utf-8"))["requirements"]
    detail = json.loads(args.traceability_detail.read_text(encoding="utf-8"))
    per_req, tsum = {}, {}
    if args.test_results:
        pr = args.test_results / "per_requirement.json"
        sm = args.test_results / "summary.json"
        per_req = json.loads(pr.read_text(encoding="utf-8")) if pr.is_file() else {}
        tsum = json.loads(sm.read_text(encoding="utf-8")) if sm.is_file() else {}

    green_l3: list[dict] = []
    ci_notes: list[str] = []
    if args.ci_runs and args.ci_runs.is_file():
        runs = json.loads(args.ci_runs.read_text(encoding="utf-8")).get("workflow_runs", [])
        for r in runs:
            wf = (r.get("path") or "").rsplit("/", 1)[-1]
            ok_commit = (r.get("head_sha") or "").lower() == args.commit.lower()
            is_eligible = any(fnmatch.fnmatch(wf, g) for g in eligible)
            ci_notes.append(f"{r.get('name')} ({wf}) run {r.get('id')}: {r.get('conclusion')}"
                            f"{'' if is_eligible else ' [not L3-eligible]'}")
            if ok_commit and is_eligible and r.get("conclusion") == "success":
                green_l3.append(r)

    items: list[dict] = []
    gaps: dict[str, list[str]] = {}
    sev: dict[str, str] = {}
    for req in reqs:
        rid = req["id"]
        sev[rid] = derive_severity(req)
        d = detail.get(rid, {})
        code = d.get("code") or []
        if code:
            items.append({
                "requirement_id": rid, "evidence_id": evi_id(rid, "L1"), "proof_tier": "L1", "type": "code_link",
                "summary": f"Requirement id referenced in {len(code)} code location(s); linkage only, not proof.",
                "links": [{"kind": "code", "url": code_link(tpl, args.commit, a), "label": a} for a in code[:5]],
                "repro_command": f"git grep -n -w '{rid}' {args.commit} -- ':!*.md' ':!tests'",
                "expected_result": "Implementation references the requirement id",
                "actual_result": f"{len(code)} reference(s)", "confidence": 0.3,
                "redaction_status": "clean", "git_commit": args.commit,
            })
        t = per_req.get(rid)
        g: list[str] = []
        if t:
            tests = t.get("tests", [])
            files = sorted({x.split("::")[0].rsplit(".", 1)[0].replace(".", "/") + ".py" for x in tests[:5]})
            repro = "pytest -q -p no:cacheprovider " + " ".join(files)
            if t.get("passed"):
                items.append({
                    "requirement_id": rid, "evidence_id": evi_id(rid, "L2P"), "proof_tier": "L2", "type": "test_run",
                    "summary": f"{t['passed']} mapped test case(s) passed locally at the audited commit.",
                    "links": [{"kind": "test", "url": x, "label": "pytest case"} for x in tests[:5]],
                    "repro_command": repro, "expected_result": "all mapped tests pass",
                    "actual_result": f"{t['passed']} passed, {t.get('failed', 0)} failed, {t.get('skipped', 0)} skipped",
                    "confidence": 0.6, "redaction_status": "clean", "git_commit": args.commit,
                    "notes": "Mapping via repo requirements-test-map.json / in-test id references; mapping fidelity not independently reviewed.",
                } if not t.get("failed") else {
                    "requirement_id": rid, "evidence_id": evi_id(rid, "L2P"), "proof_tier": "L2", "type": "test_run",
                    "summary": f"{t['passed']} mapped test case(s) passed locally.", "links": [],
                    "repro_command": repro, "expected_result": "all mapped tests pass",
                    "actual_result": f"{t['passed']} passed", "confidence": 0.5,
                    "redaction_status": "clean", "git_commit": args.commit,
                })
            if t.get("failed"):
                items.append({
                    "requirement_id": rid, "evidence_id": evi_id(rid, "L2F"), "proof_tier": "L2", "type": "test_run",
                    "summary": f"{t['failed']} mapped test case(s) FAILED locally at the audited commit.",
                    "links": [], "repro_command": repro, "expected_result": "all mapped tests pass",
                    "actual_result": f"{t['failed']} failed", "confidence": 0.8,
                    "redaction_status": "clean", "git_commit": args.commit,
                })
            if t.get("passed") and not t.get("failed"):
                if green_l3:
                    r = green_l3[0]
                    items.append({
                        "requirement_id": rid, "evidence_id": evi_id(rid, "L3"), "proof_tier": "L3", "type": "ci_run",
                        "summary": f"Eligible CI workflow '{r.get('name')}' green on audited commit.",
                        "links": [{"kind": "ci", "url": run_tpl.format(run_id=r["id"]), "label": r.get("name", "")}],
                        "repro_command": f"gh run view {r['id']} --repo {cfg['repo']['owner']}/{cfg['repo']['name']}",
                        "expected_result": "conclusion=success", "actual_result": "conclusion=success",
                        "confidence": 0.8, "redaction_status": "clean", "ci_job": r.get("name", ""),
                        "ci_run_id": str(r["id"]), "git_commit": args.commit,
                    })
                else:
                    g.append("No L3: no L3-eligible CI workflow green on the audited commit")
                g.append("No L4 non-prod runtime evidence")
                if sev[rid] == "Critical":
                    g.append("Critical: L5 independent dual-control review missing")
        if g:
            gaps[rid] = g

    bundle = {
        "schema_version": "1.1.0",
        "proof_policy_version": PROOF_POLICY_VERSION,
        "project": cfg.get("project", "EOIP (kgf)"),
        "git_commit": args.commit,
        "generated_at": now(),
        "generated_by": {"agent_id": args.agent_id, "role": "audit-pipeline"},
        "notes": ("Auto-built from pipeline facts. CI on commit: " + ("; ".join(ci_notes) or "not fetched")
                  + f". Local pytest: {tsum.get('counts', {})}")[:4000],
        "evidence_items": items,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(bundle, indent=1) + "\n", encoding="utf-8")
    args.gaps_out.write_text(json.dumps({"residual_gaps": gaps, "derived_severity": sev}, indent=1) + "\n", encoding="utf-8")
    tiers: dict[str, int] = {}
    for it in items:
        tiers[it["proof_tier"]] = tiers.get(it["proof_tier"], 0) + 1
    print(f"Wrote {len(items)} evidence items {tiers} -> {args.out}; L3-eligible green runs: {len(green_l3)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
