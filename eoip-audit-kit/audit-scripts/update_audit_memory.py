#!/usr/bin/env python3
"""Merge evidence.json into audit-memory.json (statuses, tiers, changelog; no secrets)."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from proof_policy import PROOF_POLICY_VERSION, compute_status  # noqa: E402

SECRET_RES = [
    re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"ghp_[A-Za-z0-9]{36,}"),
]


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def assert_clean(obj: dict, label: str) -> None:
    raw = json.dumps(obj)
    for cre in SECRET_RES:
        if cre.search(raw):
            raise SystemExit(f"Refusing to write secrets into {label}")


def empty_memory(repo: str, commit: str) -> dict:
    return {
        "schema_version": "1.1.0",
        "proof_policy_version": PROOF_POLICY_VERSION,
        "repo": repo,
        "baseline_commit": commit,
        "audited_commit": commit,
        "last_audit_date": now(),
        "health_score": 0,
        "requirements": {},
        "agents": [],
        "import_history": [],
        "changelog": [],
        "open_locks": [],
    }


def health_score(reqs: dict) -> float:
    if not reqs:
        return 0.0
    total = len(reqs)
    impl = sum(1 for r in reqs.values() if r.get("status") == "Implemented")
    crit_open = sum(
        1
        for r in reqs.values()
        if r.get("severity") == "Critical" and r.get("status") != "Implemented"
    )
    tier_map = {"L0": 0, "L1": 1, "L2": 2, "L3": 3, "L4": 4, "L5": 5}
    avg = sum(tier_map.get(r.get("proof_tier_achieved", "L0"), 0) for r in reqs.values()) / total
    pct = (impl / total) * 100
    return round(
        max(0, min(100, pct * 0.5 + (5 - min(crit_open, 5)) * 10 + (avg / 5) * 30)),
        1,
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--mode", choices=["full", "delta"], default="full")
    ap.add_argument("--memory", required=True, type=Path)
    ap.add_argument("--evidence", required=True, type=Path)
    ap.add_argument("--commit", required=True)
    ap.add_argument("--baseline", default="")
    ap.add_argument("--repo", default="local")
    ap.add_argument("--agent-id", default="agent-update-memory")
    ap.add_argument("--requirements", type=Path, default=None,
                    help="requirements_index.json: seed every requirement (default status Not Verified)")
    ap.add_argument("--gaps", type=Path, default=None,
                    help="residual_gaps.json from build_evidence.py (gaps + derived severity)")
    ap.add_argument("--config", type=Path, default=None, help="audit-config.json (recorded as config_ref)")
    args = ap.parse_args()

    evidence = json.loads(args.evidence.read_text(encoding="utf-8"))
    assert_clean(evidence, "evidence")

    if args.memory.is_file():
        memory = json.loads(args.memory.read_text(encoding="utf-8"))
    else:
        memory = empty_memory(args.repo, args.baseline or args.commit)

    memory["schema_version"] = "1.1.0"
    memory["proof_policy_version"] = PROOF_POLICY_VERSION
    memory["audited_commit"] = args.commit
    if args.mode == "full":
        memory["baseline_commit"] = args.baseline or args.commit
    memory["last_audit_date"] = now()

    gaps_doc = json.loads(args.gaps.read_text(encoding="utf-8")) if args.gaps and args.gaps.is_file() else {}
    gap_map = gaps_doc.get("residual_gaps", {})
    sev_map = gaps_doc.get("derived_severity", {})
    if args.config:
        memory["config_ref"] = str(args.config)
    if args.requirements and args.requirements.is_file():
        idx = json.loads(args.requirements.read_text(encoding="utf-8"))
        for r in idx.get("requirements", []):
            rec = memory["requirements"].setdefault(r["id"], {
                "status": "Not Verified", "proof_tier_achieved": "L0",
                "owners": [], "evidence_ids": [], "residual_gaps": [],
                "last_verified_commit": args.commit, "files_touched": [], "notes": "",
            })
            rec["title"] = (r.get("title") or "")[:300]
            rec["source"] = f"{r.get('source_file')}:{r.get('line_range', [0])[0]}"
            rec["priority"] = r.get("priority") or "UNKNOWN"
            rec["type"] = r.get("type") if r.get("type") in (
                "Functional", "Non-Functional", "Security", "Compliance", "AI", "Infra") else "Functional"
            rec["severity"] = sev_map.get(r["id"], rec.get("severity") or "Medium")
            rec["last_verified_commit"] = args.commit
            if r["id"] in gap_map:
                rec["residual_gaps"] = list(gap_map[r["id"]])

    producer = (evidence.get("generated_by") or {}).get("agent_id")
    by_req: dict[str, list] = {}
    for it in evidence.get("evidence_items") or []:
        by_req.setdefault(it["requirement_id"], []).append(it)

    # Orphan guard: with a requirements index, evidence for IDs that no requirement
    # doc defines (test-map-only tags) is recorded separately, not as requirements.
    orphans: dict[str, list] = {}
    if args.requirements and args.requirements.is_file():
        known = {r["id"] for r in idx.get("requirements", [])}
        for rid in [k for k in by_req if k not in known and k not in memory["requirements"]]:
            orphans[rid] = by_req.pop(rid)
    if orphans:
        memory["orphan_evidence"] = {
            rid: {"evidence_ids": sorted(i["evidence_id"] for i in items),
                  "note": "ID used by tests/test map but not defined in any requirement doc; "
                          "not counted as a requirement (see remediation/orphan_test_ids.json)"}
            for rid, items in sorted(orphans.items())
        }

    changed = []
    for rid, items in by_req.items():
        rec = memory["requirements"].setdefault(
            rid,
            {
                "status": "Not Verified",
                "proof_tier_achieved": "L0",
                "severity": "Medium",
                "type": "Functional",
                "owners": [],
                "evidence_ids": [],
                "residual_gaps": [],
                "last_verified_commit": args.commit,
                "files_touched": [],
                "notes": "",
            },
        )
        gaps = list(rec.get("residual_gaps") or [])
        result = compute_status(
            severity=rec.get("severity") or "Medium",
            evidence_items=items,
            residual_gaps=gaps,
            audited_commit=args.commit,
            bundle_commit=evidence.get("git_commit"),
            producer_agent_id=producer,
        )
        prev = rec.get("status")
        rec["status"] = result["status"]
        rec["proof_tier_achieved"] = result["proof_tier"]
        rec["evidence_ids"] = sorted(
            set(rec.get("evidence_ids") or []) | {i["evidence_id"] for i in items}
        )
        rec["last_verified_commit"] = args.commit
        ft = set(rec.get("files_touched") or [])
        for it in items:
            for ln in it.get("links") or []:
                lab = ln.get("label") or ""
                if ln.get("kind") in ("code", "test") and "/" in lab:
                    ft.add(lab.split(":")[0].split("::")[0])
        rec["files_touched"] = sorted(ft)[:30]
        if result.get("residual_gaps"):
            rec["residual_gaps"] = result["residual_gaps"]
        # Clear gaps on full Implemented
        if rec["status"] == "Implemented":
            rec["residual_gaps"] = []
        if prev != rec["status"]:
            changed.append(rid)

    summ_status: dict[str, int] = {}
    summ_tier: dict[str, int] = {}
    for r in memory["requirements"].values():
        summ_status[r["status"]] = summ_status.get(r["status"], 0) + 1
        summ_tier[r.get("proof_tier_achieved", "L0")] = summ_tier.get(r.get("proof_tier_achieved", "L0"), 0) + 1
    memory["summary"] = {"total": len(memory["requirements"]), "by_status": summ_status, "by_tier": summ_tier}
    memory["health_score"] = health_score(memory["requirements"])
    memory["import_history"] = memory.get("import_history") or []
    memory["import_history"].insert(
        0,
        {
            "file": str(args.evidence.name),
            "imported_by": args.agent_id,
            "timestamp": now(),
            "git_commit": args.commit,
            "items_applied": sum(len(v) for v in by_req.values()),
            "conflicts": 0,
            "notes": f"mode={args.mode}",
        },
    )
    memory["changelog"] = memory.get("changelog") or []
    memory["changelog"].insert(
        0,
        {
            "timestamp": now(),
            "actor": args.agent_id,
            "change": f"update_audit_memory --mode {args.mode}; health={memory['health_score']}",
            "requirement_ids": changed or list(by_req.keys()),
        },
    )
    memory["agents"] = memory.get("agents") or []
    memory["agents"].append(
        {
            "agent_id": args.agent_id,
            "role": "memory-updater",
            "action": "delta_audit" if args.mode == "delta" else "full_audit",
            "scope": list(by_req.keys()),
            "timestamp": now(),
            "notes": f"Merged {args.evidence.name}",
        }
    )
    memory.setdefault("open_locks", [])

    assert_clean(memory, "audit-memory")
    args.memory.parent.mkdir(parents=True, exist_ok=True)
    args.memory.write_text(json.dumps(memory, indent=2) + "\n", encoding="utf-8")
    print(
        f"Updated {args.memory} (health={memory['health_score']}, "
        f"changed={len(changed)}, mode={args.mode})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
