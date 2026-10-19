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

    producer = (evidence.get("generated_by") or {}).get("agent_id")
    by_req: dict[str, list] = {}
    for it in evidence.get("evidence_items") or []:
        by_req.setdefault(it["requirement_id"], []).append(it)

    changed = []
    for rid, items in by_req.items():
        rec = memory["requirements"].setdefault(
            rid,
            {
                "status": "Not Implemented",
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
        if result.get("residual_gaps"):
            rec["residual_gaps"] = result["residual_gaps"]
        # Clear gaps on full Implemented
        if rec["status"] == "Implemented":
            rec["residual_gaps"] = []
        if prev != rec["status"]:
            changed.append(rid)

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
