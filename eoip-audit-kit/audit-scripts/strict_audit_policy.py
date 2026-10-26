"""Fail-closed evidence assessment for reproducible audit runs.

Keep this separate from the historical tracker policy: legacy manual decisions
are retained as history, never silently upgraded into current execution proof.
"""

from __future__ import annotations

import re
from typing import Any

VERSION = "1.1.0"
RANK = {f"L{i}": i for i in range(6)}
PASS = re.compile(r"\b(pass(?:ed)?|success|green|exit 0)\b", re.I)
FAIL = re.compile(r"\b(fail(?:ed|ure|s)?|errors?|timeout|cancelled)\b", re.I)


def outcome(item: dict[str, Any]) -> str:
    text = item.get("actual_result", "")
    text = re.sub(r"\b0\s+(?:failed|failures|errors)\b", "", text, flags=re.I)
    if FAIL.search(text):
        return "failed"
    return "passed" if PASS.search(text) else "unknown"


def assess(items: list[dict], *, commit: str, bundle_commit: str,
           severity: str, gaps: list[str], producer: str) -> dict:
    active, stale = [], []
    for item in items:
        own_commit = item.get("git_commit", bundle_commit)
        if not commit or bundle_commit != commit or own_commit != commit:
            stale.append(item)
        else:
            active.append(item)
    positive = []
    failed = []
    negative = []
    for item in active:
        tier = item.get("proof_tier")
        links = item.get("links") or []
        if item.get("type") == "negative_proof":
            if item.get("repro_command") and item.get("actual_result") and links:
                negative.append(item)
            continue
        valid = bool(links)
        if tier == "L2":
            valid &= item.get("type") == "test_run" and bool(item.get("repro_command"))
        elif tier == "L3":
            valid &= bool(item.get("ci_job") and item.get("ci_run_id"))
        elif tier == "L4":
            valid &= item.get("environment") in {"local-nonprod", "staging", "test"}
        elif tier == "L5":
            valid &= bool(producer and item.get("reviewer_id")
                          and item["reviewer_id"] != producer)
        else:
            continue
        if valid and outcome(item) == "passed":
            positive.append(item)
        elif valid and outcome(item) == "failed":
            failed.append(item)
    tiers = {item["proof_tier"] for item in positive}
    status = "Not Verified"
    if positive and (negative or failed):
        status = "Ambiguous"
    elif negative:
        status = "Not Implemented"
    elif "L2" in tiers:
        closed = not gaps and bool(tiers & {"L3", "L4"})
        if severity == "Critical":
            closed &= {"L3", "L5"} <= tiers
        status = "Implemented" if closed else "Partially Implemented" if gaps else "Not Verified"
    tier = max(tiers | ({"L1"} if any(i.get("proof_tier") == "L1" for i in active) else {"L0"}),
               key=RANK.get)
    return {"status": status, "proof_tier": tier, "stale_count": len(stale),
            "active_count": len(active), "proof_policy_version": VERSION}
