"""Seed .audit-scratch/ledger.json from the combined requirements document."""
from __future__ import annotations
import json, re, sys
from datetime import datetime, timezone
from pathlib import Path

REQ = Path(sys.argv[1] if len(sys.argv) > 1 else "CRAr_cpccaggcc-requirements.md")
OUT = Path(".audit-scratch/ledger.json")

def now() -> str:
    return datetime.now(timezone.utc).isoformat()

def main():
    text = REQ.read_text(encoding="utf-8")
    items: list[dict] = []
    for m in re.finditer(r"^- \*\*(CRA-\d{3})\.(\d+)\*\* `\[(\w+)\]` (.+?)\r?$", text, re.M):
        items.append({
            "id": f"{m[1]}.{m[2]}",
            "kind": "clause",
            "parent": m[1],
            "origin": m[3],
            "state": "OPEN",
            "owner": None,
            "blocked_by": [],
            "receipts": [],
            "notes": "",
            "updated_at": now(),
        })
    for rid in sorted({i["parent"] for i in items}):
        items.append({
            "id": f"{rid}.A",
            "kind": "acceptance",
            "parent": rid,
            "state": "OPEN",
            "owner": None,
            "blocked_by": [],
            "receipts": [],
            "notes": "",
            "updated_at": now(),
        })
    for kind, pat in (
        ("scenario", r"^\| (E\d{2}) \|"),
        ("decision", r"^\| (H-\d{2}) \|"),
        ("conflict", r"^\| (X-\d{2}) \|"),
        ("research", r"^\| (C\d{2}) \| "),
    ):
        for m in re.finditer(pat, text, re.M):
            iid = m[1] if kind != "research" else f"R-{m[1]}"
            items.append({
                "id": iid,
                "kind": kind,
                "parent": None,
                "state": "OPEN",
                "owner": None,
                "blocked_by": [],
                "receipts": [],
                "notes": "",
                "updated_at": now(),
            })
    seen, unique = set(), []
    for it in items:
        if it["id"] not in seen:
            seen.add(it["id"])
            unique.append(it)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    if OUT.exists():
        sys.exit(f"{OUT} exists; refusing to overwrite. Use a migration script to add new items.")
    OUT.write_text(json.dumps({"schema": "eoip-ledger-v3", "created_at": now(), "items": unique}, indent=2), encoding="utf-8")
    print(f"seeded {len(unique)} items")

if __name__ == "__main__":
    main()
