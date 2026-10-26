#!/usr/bin/env python3
"""Generate tracker_data.json and optionally a standalone tracker HTML with embedded data."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
KIT_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))
from proof_policy import PROOF_POLICY_VERSION, compute_status  # noqa: E402


def load_json(path: Path | None) -> dict | list | None:
    if not path or not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def slim_tasks(queue: dict, rem_dir: Path) -> list[dict]:
    """Compact task records for the tracker (details from requirement_tasks / findings_tasks)."""
    rt = {t["task_id"]: t for t in (load_json(rem_dir / "requirement_tasks.json") or {}).get("tasks", [])}
    ft = {t["id"]: t for t in (load_json(rem_dir / "findings_tasks.json") or {}).get("tasks", [])}
    dt = {t["task_id"]: t for t in (load_json(rem_dir / "duplicate_id_tasks.json") or {}).get("tasks", [])}
    ep = {e["epic_id"]: e["file"] for e in (load_json(rem_dir / "epics.json") or {}).get("epics", [])}
    out = []
    for q in queue.get("tasks", []):
        tid = q["task_id"]
        s = {"id": tid, "kind": q.get("kind"), "rid": q.get("requirement_id"), "title": (q.get("title") or "")[:180],
             "pr": q.get("priority"), "epic": q.get("epic_id"), "cat": q.get("gap_category"), "st": q.get("current_status") or "",
             "tier": q.get("proof_tier") or "", "h": q.get("estimated_hours"), "deps": q.get("depends_on") or [],
             "src": q.get("source"), "epic_file": ep.get(q.get("epic_id"))}
        if tid in rt:
            r = rt[tid]
            s["gaps"] = [g[:160] for g in r.get("gaps", [])[:3]]
            s["next"] = [n[:220] for n in r.get("next_steps", [])[:3]]
            s["acs"] = [a[:200] for a in r.get("acceptance_criteria", [])[:3]]
            s["paths"] = (r["mapped_paths"].get("code", [])[:3] + r["mapped_paths"].get("failing_tests", [])[:2])
        elif tid in ft:
            f = ft[tid]
            s["gaps"] = [f.get("description", "")[:400]]
            if (f.get("extended_run") or {}).get("evidence"):
                s["gaps"].append("Extended run: " + f["extended_run"]["evidence"][:300])
            s["next"] = [a[:220] for a in f.get("acceptance_criteria", [])[:4]]
            if f.get("sub_items"):
                s["next"] += [f"[{x['decision']}] {x['test']}: {x['issue']} -> {x['child_task']}"[:220] for x in f["sub_items"]]
            s["st"] = f.get("status") or ""
            s["paths"] = [n[:120] for n in f.get("implementation_notes", [])[:4]]
            s["src"] = "remediation/findings_tasks.md#" + tid.lower()
        elif tid in dt:
            d = dt[tid]
            s["gaps"] = [f"{len(d['sites'])} redefinition site(s): {d['kinds']}"]
            s["next"] = d.get("resolution_steps", [])[:3]
            s["paths"] = [x["site"] for x in d["sites"][:5]]
        out.append(s)
    return out


def tasks_to_requirements(tasks: list | dict | None, memory: dict | None, evidence: dict | None) -> list[dict]:
    reqs: dict[str, dict] = {}
    mem_reqs = (memory or {}).get("requirements") or {}
    for rid, m in mem_reqs.items():
        reqs[rid] = {
            "id": rid,
            "title": m.get("title") or rid,
            "type": m.get("type") or "Functional",
            "severity": m.get("severity") or "Medium",
            "status": m.get("status") or "Not Verified",
            "proof_tier": m.get("proof_tier_achieved") or "L0",
            "owner": (m.get("owners") or [""])[0],
            "estimate": m.get("estimate_hours") or 0,
            "ac": "",
            "links": {"code": "", "test": "", "ci": ""},
            "comments": " | ".join(x for x in (m.get("source"), m.get("priority") and f"priority {m.get('priority')}", m.get("notes")) if x),
            "evidence": [],
            "residual_gaps": list(m.get("residual_gaps") or []),
            "manual_override": None,
            "stale": False,
        }

    if isinstance(tasks, dict):
        tasks = tasks.get("tasks") or tasks.get("items") or list(tasks.values())
    for t in tasks or []:
        rid = t.get("requirement_id") or t.get("id")
        if not rid:
            continue
        r = reqs.setdefault(
            rid,
            {
                "id": rid,
                "title": t.get("title") or rid,
                "type": t.get("type") or "Functional",
                "severity": t.get("severity") or "Medium",
                "status": t.get("status") or "Not Verified",
                "proof_tier": "L0",
                "owner": t.get("owner") or "",
                "estimate": t.get("estimate_hours") or t.get("estimate") or 0,
                "ac": t.get("acceptance_criteria") or "",
                "links": {"code": t.get("code_link") or "", "test": t.get("test_link") or "", "ci": t.get("ci_link") or ""},
                "comments": t.get("comments") or "",
                "evidence": [],
                "residual_gaps": list(t.get("residual_gaps") or []),
                "manual_override": None,
                "stale": False,
            },
        )
        r["title"] = t.get("title") or r["title"]
        if t.get("acceptance_criteria"):
            r["ac"] = t["acceptance_criteria"] if isinstance(t["acceptance_criteria"], str) else json.dumps(t["acceptance_criteria"])

    # Attach evidence + recompute
    producer = ((evidence or {}).get("generated_by") or {}).get("agent_id")
    commit = (evidence or {}).get("git_commit") or (memory or {}).get("audited_commit")
    by = {}
    for it in (evidence or {}).get("evidence_items") or []:
        by.setdefault(it["requirement_id"], []).append(it)
    orphans = set((memory or {}).get("orphan_evidence") or {})
    for rid, items in by.items():
        if rid in orphans:  # test-only IDs, not requirements (audit-memory orphan_evidence)
            continue
        r = reqs.setdefault(
            rid,
            {
                "id": rid,
                "title": rid,
                "type": "Functional",
                "severity": "Medium",
                "status": "Not Verified",
                "proof_tier": "L0",
                "owner": "",
                "estimate": 0,
                "ac": "",
                "links": {"code": "", "test": "", "ci": ""},
                "comments": "",
                "evidence": [],
                "residual_gaps": [],
                "manual_override": None,
                "stale": False,
            },
        )
        r["evidence"] = items
        result = compute_status(
            severity=r["severity"],
            evidence_items=items,
            residual_gaps=r.get("residual_gaps") or [],
            audited_commit=commit,
            bundle_commit=(evidence or {}).get("git_commit"),
            producer_agent_id=producer,
        )
        r["status"] = result["status"]
        r["proof_tier"] = result["proof_tier"]
        r["stale"] = bool(result.get("stale_count"))
        if result.get("residual_gaps"):
            r["residual_gaps"] = result["residual_gaps"]

    return sorted(reqs.values(), key=lambda x: x["id"])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tasks", type=Path, default=None)
    ap.add_argument("--traceability", type=Path, default=None)
    ap.add_argument("--evidence-json", type=Path, default=None)
    ap.add_argument("--audit-memory", type=Path, default=None)
    ap.add_argument("--out", required=True, type=Path, help="Output HTML path")
    ap.add_argument("--data-out", type=Path, default=None, help="Also write tracker_data.json")
    ap.add_argument("--config", type=Path, default=KIT_ROOT / "audit-config.json")
    ap.add_argument("--remediation-dir", type=Path, default=KIT_ROOT / "remediation")
    ap.add_argument("--requirements", type=Path, default=None, help="requirements_index.json for acceptance text")
    ap.add_argument("--kit-tracker", type=Path, default=None,
                    help="Blank tracker template (default: templates/tracker_template.html)")
    ap.add_argument("--also-out", type=Path, action="append", default=[],
                    help="Write the same embedded tracker to this path too (repeatable)")
    ap.add_argument("--no-root-copy", action="store_true",
                    help="Do not also write <kit>/tracker.html when --out is <kit>/audit-output/tracker.html")
    args = ap.parse_args()

    tasks = load_json(args.tasks)
    evidence = load_json(args.evidence_json) or {}
    memory = load_json(args.audit_memory) or {}
    queue = None
    if isinstance(tasks, dict) and str(tasks.get("schema", "")).startswith("eoip-audit-tasks"):
        queue, tasks = tasks, None          # remediation queue: shown in the Tasks tab, not as requirements
    requirements = tasks_to_requirements(tasks, memory, evidence)
    for r in requirements:
        for ev in r.get("evidence") or []:
            for ln in ev.get("links") or []:
                kind = ln.get("kind")
                if kind in ("code", "test", "ci") and not r["links"].get(kind):
                    r["links"][kind] = ln.get("url", "")
    cfg = load_json(args.config) or {}
    idx = load_json(args.requirements) or {}
    by_id = {r["id"]: r for r in (idx.get("requirements") or [])}
    for r in requirements:
        src = by_id.get(r["id"])
        if src:
            r["ac"] = r.get("ac") or "; ".join(src.get("acceptance_criteria") or [])[:400]
            if not r["title"] or r["title"] == r["id"]:
                r["title"] = src.get("title") or r["id"]

    data = {
        "proof_policy_version": PROOF_POLICY_VERSION,
        "config": {
            "repo_url": (cfg.get("repo") or {}).get("url", ""),
            "branch": (cfg.get("repo") or {}).get("branch", ""),
            "code_line_template": (cfg.get("links") or {}).get("code_line_template", ""),
            "ci_run_template": (cfg.get("ci") or {}).get("run_template", ""),
        },
        "audited_commit": evidence.get("git_commit")
        or memory.get("audited_commit")
        or memory.get("baseline_commit"),
        "requirements": requirements,
        "tasks": slim_tasks(queue, args.remediation_dir) if queue else [],
        "evidence_bundle": evidence or None,
        "audit_memory": memory or None,
    }

    data_out = args.data_out
    if data_out is None:
        data_out = args.out.parent / "tracker_data.json"
    data_out.parent.mkdir(parents=True, exist_ok=True)
    data_out.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {data_out}")

    kit_tracker = args.kit_tracker or (KIT_ROOT / "templates" / "tracker_template.html")
    if not kit_tracker.is_file():
        print(f"WARN: kit tracker not found at {kit_tracker}; wrote data only", file=sys.stderr)
        return 0

    html = kit_tracker.read_text(encoding="utf-8")
    # Embed data before </body> / before script loadPersisted
    embed = (
        "<script>window.EOIP_TRACKER_DATA = "
        + json.dumps(data)
        + ";</script>\n"
    )
    # Must run BEFORE the tracker's main script, so inject into <head>.
    # The HTML only needs requirements + producer id; full bundle/memory stay in tracker_data.json.
    slim = dict(data)
    eb = data.get("evidence_bundle") or {}
    slim["evidence_bundle"] = {"generated_by": eb.get("generated_by"), "git_commit": eb.get("git_commit")}
    slim.pop("audit_memory", None)
    safe_json = json.dumps(slim, separators=(",", ":")).replace("</", "<\\/")
    embed = "<script>window.EOIP_TRACKER_DATA = " + safe_json + ";</script>\n"
    if "</head>" in html:
        html = html.replace("</head>", embed + "</head>", 1)
    else:
        html = embed + html

    outs = [args.out] + list(args.also_out)
    canonical = (KIT_ROOT / "audit-output" / "tracker.html").resolve()
    if not args.no_root_copy and args.out.resolve() == canonical:
        outs.append(KIT_ROOT / "tracker.html")
    docs = [("Audit report", "audit_gaps_requirements.md"), ("Requirements catalogue", "requirements.md"),
            ("Implementation status", "implementation.md"), ("Requirements (per doc)", "requirements/index.md"),
            ("Implementation (per doc)", "implementation/index.md")]
    doc_dir = args.out.resolve().parent
    for out in dict.fromkeys(o.resolve() for o in outs):
        links = []
        for label, rel in docs:
            target = doc_dir / rel
            if target.is_file():
                href = os.path.relpath(target, out.parent).replace(os.sep, "/")
                links.append(f'<a href="{href}" target="_blank" rel="noopener">{label}</a>')
        page = html.replace("<!--DOC_LINKS-->", ("Documents: " + " · ".join(links)) if links else "", 1)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page, encoding="utf-8")
        print(f"Wrote standalone tracker → {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
