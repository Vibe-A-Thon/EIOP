#!/usr/bin/env python3
"""Generate tracker_data.json and optionally a standalone tracker HTML with embedded data."""

from __future__ import annotations

import argparse
import json
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


def tasks_to_requirements(tasks: list | dict | None, memory: dict | None, evidence: dict | None) -> list[dict]:
    reqs: dict[str, dict] = {}
    mem_reqs = (memory or {}).get("requirements") or {}
    for rid, m in mem_reqs.items():
        reqs[rid] = {
            "id": rid,
            "title": m.get("notes") and rid or rid,
            "type": m.get("type") or "Functional",
            "severity": m.get("severity") or "Medium",
            "status": m.get("status") or "Not Implemented",
            "proof_tier": m.get("proof_tier_achieved") or "L0",
            "owner": (m.get("owners") or [""])[0],
            "estimate": m.get("estimate_hours") or 0,
            "ac": "",
            "links": {"code": "", "test": "", "ci": ""},
            "comments": m.get("notes") or "",
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
                "status": t.get("status") or "Not Implemented",
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
    for rid, items in by.items():
        r = reqs.setdefault(
            rid,
            {
                "id": rid,
                "title": rid,
                "type": "Functional",
                "severity": "Medium",
                "status": "Not Implemented",
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
    ap.add_argument("--kit-tracker", type=Path, default=None,
                    help="Source tracker.html (default: kit tracker)")
    args = ap.parse_args()

    tasks = load_json(args.tasks)
    evidence = load_json(args.evidence_json) or {}
    memory = load_json(args.audit_memory) or {}
    requirements = tasks_to_requirements(tasks, memory, evidence)

    data = {
        "proof_policy_version": PROOF_POLICY_VERSION,
        "audited_commit": evidence.get("git_commit")
        or memory.get("audited_commit")
        or memory.get("baseline_commit"),
        "requirements": requirements,
        "evidence_bundle": evidence or None,
        "audit_memory": memory or None,
    }

    data_out = args.data_out
    if data_out is None:
        data_out = args.out.parent / "tracker_data.json"
    data_out.parent.mkdir(parents=True, exist_ok=True)
    data_out.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {data_out}")

    kit_tracker = args.kit_tracker or (KIT_ROOT / "tracker.html")
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
    if "</body>" in html:
        html = html.replace("</body>", embed + "</body>")
    else:
        html += embed

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(html, encoding="utf-8")
    print(f"Wrote standalone tracker → {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
