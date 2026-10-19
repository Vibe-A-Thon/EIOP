#!/usr/bin/env python3
"""Assemble audit_gaps_requirements.md from requirements + traceability + evidence."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from proof_policy import PROOF_POLICY_VERSION, compute_status, max_tier  # noqa: E402


def load_requirements(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    reqs = data.get("requirements") or data
    if isinstance(reqs, dict):
        return list(reqs.values())
    return list(reqs)


def load_traceability(path: Path | None) -> dict[str, dict]:
    if not path or not path.is_file():
        return {}
    out = {}
    with path.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out[row["requirement_id"]] = row
    return out


def load_evidence(evidence_dir: Path) -> dict:
    p = evidence_dir / "evidence.json"
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))
    # also accept evidence_dir itself if file
    if evidence_dir.is_file():
        return json.loads(evidence_dir.read_text(encoding="utf-8"))
    return {}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--requirements", required=True, type=Path)
    ap.add_argument("--traceability", type=Path, default=None)
    ap.add_argument("--evidence", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--commit", default="UNKNOWN")
    ap.add_argument("--project", default="EOIP (kgf)")
    ap.add_argument("--memory", type=Path, default=None)
    args = ap.parse_args()

    reqs = load_requirements(args.requirements)
    trace = load_traceability(args.traceability)
    bundle = load_evidence(args.evidence)
    memory = {}
    if args.memory and args.memory.is_file():
        memory = json.loads(args.memory.read_text(encoding="utf-8")).get(
            "requirements", {}
        )

    by_ev: dict[str, list] = defaultdict(list)
    for it in bundle.get("evidence_items") or []:
        by_ev[it["requirement_id"]].append(it)

    producer = (bundle.get("generated_by") or {}).get("agent_id")
    audited = bundle.get("git_commit") or args.commit

    findings = []
    counts = defaultdict(int)
    for req in reqs:
        rid = req["id"]
        meta = memory.get(rid) or {}
        items = by_ev.get(rid) or []
        severity = meta.get("severity") or "Medium"
        gaps = list(meta.get("residual_gaps") or [])
        result = compute_status(
            severity=severity,
            evidence_items=items,
            residual_gaps=gaps,
            audited_commit=audited,
            bundle_commit=bundle.get("git_commit"),
            producer_agent_id=producer,
            current_status=meta.get("status"),
        )
        counts[result["status"]] += 1
        tr = trace.get(rid) or {}
        findings.append(
            {
                "req": req,
                "severity": severity,
                "result": result,
                "items": items,
                "trace": tr,
                "gaps": result.get("residual_gaps") or gaps,
            }
        )

    total = len(findings) or 1
    impl = counts.get("Implemented", 0)
    health = round((impl / total) * 100, 1)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    lines = [
        f"# Audit Gaps & Requirements — {args.project}",
        "",
        f"- **Repo commit:** `{args.commit}`",
        f"- **Audit date:** {now}",
        f"- **Proof policy:** {PROOF_POLICY_VERSION}",
        f"- **Evidence bundle commit:** `{bundle.get('git_commit', 'n/a')}`",
        f"- **Auditors:** _Audit Lead / Security Specialist / Product Owner — sign below_",
        "",
        "## Executive Summary",
        "",
        f"- Core objective: audit implementation against `.md` requirements for {args.project}.",
        f"- Health (Implemented %): **{health}%** ({impl}/{len(findings)}).",
        f"- Status counts: {dict(counts)}.",
        f"- Proof policy 1.1: L1 never closes Partial/Implemented; Partial needs L2+gaps; "
        f"Implemented needs L2+(L3|L4); Critical needs L5 dual-control.",
        "- Top risks: review Critical / Not Implemented findings below.",
        "",
        "## Core Objective",
        "",
        f"Verify that {args.project} meets documented requirements with reproducible evidence "
        f"at a fixed git commit under proof policy {PROOF_POLICY_VERSION}.",
        "",
        "## Traceability Summary",
        "",
        f"| Status | Count |",
        f"|---|---:|",
    ]
    for st in (
        "Implemented",
        "Partially Implemented",
        "Not Implemented",
        "Ambiguous",
        "Not Applicable",
    ):
        lines.append(f"| {st} | {counts.get(st, 0)} |")
    lines += ["", "## Detailed Findings", ""]

    for f in findings:
        req = f["req"]
        rid = req["id"]
        r = f["result"]
        lines += [
            f"### {rid} — {req.get('title', '')}",
            "",
            f"- **Requirement Text:** see `{req.get('source_file', '')}` lines {req.get('line_range', '')}",
            f"- **Type:** {req.get('type', '')}",
            f"- **Implementation Status:** {r['status']}",
            f"- **Proof tier achieved:** {r['proof_tier']}",
            f"- **Severity:** {f['severity']}",
            f"- **Evidence:**",
        ]
        if not f["items"]:
            lines.append("  - _None — proof placeholders pending_")
        for it in f["items"]:
            lines.append(
                f"  - `{it.get('evidence_id')}` [{it.get('proof_tier')}/{it.get('type')}] "
                f"{it.get('summary', '')} "
                f"(repro: `{it.get('repro_command', 'n/a')}`; commit `{it.get('git_commit', bundle.get('git_commit', ''))}`)"
            )
        tr = f["trace"]
        if tr:
            lines.append(
                f"- **Traceability:** code=`{tr.get('code_paths','')}` "
                f"tests=`{tr.get('test_paths','')}` confidence={tr.get('confidence_score','')}"
            )
        lines += [
            f"- **Gap Description:** {'; '.join(f['gaps']) if f['gaps'] else ('; '.join(r.get('warnings') or []) or 'None noted')}",
            f"- **Residual gaps:** {f['gaps'] or '[]'}",
            f"- **Remediation Recommendation:** Address residual gaps; attach L2+(L3|L4) evidence"
            + ("; obtain L5 dual-control" if f["severity"] == "Critical" else "")
            + ".",
            f"- **Estimated Effort:** {meta_est(memory.get(rid, {}))} — see audit_tasks.json",
            f"- **Acceptance Criteria:** {req.get('acceptance_criteria') or 'See source requirement'}",
            "",
        ]

    lines += [
        "## Sign-off",
        "",
        "| Role | Name / opaque id | Date | Commit | Signature |",
        "|---|---|---|---|---|",
        f"| Audit Lead |  |  | `{args.commit}` |  |",
        f"| Security Specialist |  |  | `{args.commit}` |  |",
        f"| Product Owner |  |  | `{args.commit}` |  |",
        "",
        "## Appendices",
        "",
        f"- Proof policy version: `{PROOF_POLICY_VERSION}`",
        "- Traceability matrix, evidence/, redaction logs, LLM usage logs (prompt hashes only).",
        "",
    ]

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote report → {args.out}")
    return 0


def meta_est(m: dict) -> str:
    h = m.get("estimate_hours")
    return f"{h}h" if h is not None else "UNKNOWN"


if __name__ == "__main__":
    raise SystemExit(main())
