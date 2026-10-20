"""Replace missing or tampered ledger receipts with receipts from real test runs (FT-D08).

For every VERIFIED/ACCEPTED ledger item whose receipt files are missing or do not match
their recorded sha256:
- the clause's tests (tools/acceptance/clause_tests.py, or the command recorded in a
  surviving receipt for that clause) are run through run_and_receipt.py;
- a passing run sets the item to VERIFIED with the new receipt. Never ACCEPTED: that
  state needs an independent reviewer signature (tools/acceptance/review_receipt.py);
- a failing run sets FAILED (receipt kept as evidence);
- no runnable test: IMPLEMENTED with no receipt, and the reason in notes.
The ledger therefore only references receipts that exist and were produced by a run.

Usage: python tools/acceptance/regenerate_receipts.py --artifact 'dist/eoip-*.whl' [--jobs 4]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from clause_tests import clause_file_map, clause_test_map  # noqa: E402

LEDGER = Path(".audit-scratch/ledger.json")
RECEIPTS = Path(".audit-scratch/receipts")


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _valid(ref: dict) -> bool:
    path = Path(ref.get("path", ""))
    return path.is_file() and _sha(path) == ref.get("sha256")


def _recorded_command(clause: str) -> list[str] | None:
    """Test paths from a surviving receipt's command (other recorded args are dropped)."""
    folder = RECEIPTS / clause
    for receipt in sorted(folder.glob("*.json")) if folder.is_dir() else []:
        try:
            cmd = json.loads(receipt.read_text(encoding="utf-8"))["execution"]["command"]
        except (ValueError, KeyError):
            continue
        targets = [arg for arg in cmd if arg.startswith("tests/") and Path(arg.split("::")[0]).exists()]
        if targets:
            return _pytest(targets)
    return None


def _pytest(targets: list[str]) -> list[str]:
    return [sys.executable, "-m", "pytest", "-p", "no:cacheprovider", "-q", "-o", "addopts=", "--timeout=300", *targets]


def _run(clause: str, cmd: list[str], artifact: str) -> Path | None:
    before = set((RECEIPTS / clause).glob("*.json")) if (RECEIPTS / clause).is_dir() else set()
    env = dict(os.environ, EOIP_DATA_DIR=tempfile.mkdtemp(prefix=f"eoip-rcpt-{clause}-"))
    try:
        subprocess.run(
            [sys.executable, "tools/acceptance/run_and_receipt.py", "--clause", clause, "--profile", "P0",
             "--artifact", artifact, "--backend", "memory-harness", "--", *cmd],
            env=env, check=False, capture_output=True, text=True, timeout=1200,
        )
    except subprocess.TimeoutExpired:
        pass
    after = set((RECEIPTS / clause).glob("*.json"))
    new = sorted(after - before)
    return new[-1] if new else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--artifact", required=True)
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--only", nargs="*", help="limit to these clause IDs")
    args = ap.parse_args()

    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    tests = clause_test_map(Path("."))
    files = clause_file_map(Path("."))
    todo = [item for item in ledger["items"]
            if (args.only and item["id"] in args.only and item.get("state") in ("FAILED", "BLOCKED", "IMPLEMENTED", "VERIFIED"))
            or (item.get("state") in ("VERIFIED", "ACCEPTED") and item.get("receipts")
                and not all(_valid(ref) for ref in item["receipts"])
                and (not args.only or item["id"] in args.only))]

    def work(item: dict) -> tuple[dict, str, Path | None]:
        clause = item["id"]
        if clause in tests:
            cmd = _pytest(tests[clause])
        else:
            cmd = _recorded_command(clause) or (_pytest(files[clause]) if clause in files else None)
        if not cmd:
            return item, "no-test", None
        return item, "ran", _run(clause, cmd, args.artifact)

    now = datetime.now(timezone.utc).isoformat()
    counts: dict[str, int] = {}
    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        for item, kind, receipt in pool.map(work, todo):
            previous = item.get("state")
            if kind == "no-test" or receipt is None:
                item["state"], item["receipts"] = "IMPLEMENTED", []
                item["notes"] = (f"FT-D08 {now[:10]}: was {previous} but its receipt was missing/altered "
                                 "and no runnable test maps to this clause (by test name, docstring or file citation); needs a test and a new run.")
            else:
                data = json.loads(receipt.read_text(encoding="utf-8"))
                res, rc = data["results"], data["execution"]["exit_code"]
                passed = rc == 0 and res["tests_passed"] > 0 and not (res["tests_failed"] or res["tests_errors"])
                skipped_only = rc in (0, 5) and res["tests_passed"] == 0 and res["tests_skipped"] > 0
                item["state"] = "VERIFIED" if passed else ("BLOCKED" if skipped_only else "FAILED")
                item["receipts"] = [{"path": receipt.as_posix(), "sha256": _sha(receipt)}]
                item["notes"] = (f"FT-D08 {now[:10]}: was {previous} with a missing/altered receipt; "
                                 f"re-run produced this receipt ({res['tests_passed']} passed, "
                                 f"{res['tests_failed']} failed, {res['tests_skipped']} skipped). Independent review needed for ACCEPTED.")
            item["updated_at"] = now
            counts[item["state"]] = counts.get(item["state"], 0) + 1
    LEDGER.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"processed": len(todo), "states": counts}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
