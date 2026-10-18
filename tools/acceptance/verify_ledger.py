"""Verify ledger and receipts against acceptance rules.
Exit non-zero on any violation.
"""
from __future__ import annotations
import argparse, hashlib, json, os, sys
from datetime import datetime
from pathlib import Path
import jsonschema

KNOWN_STATES = {
    "OPEN", "DESIGNED", "IMPLEMENTED", "VERIFIED", "ACCEPTED",
    "BLOCKED", "FAILED", "UNQUALIFIED", "DEFERRED", "WAIVED"
}

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def parse_iso(dt_str: str) -> datetime:
    return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))

def verify_ledger(ledger_path: Path, mode: str = "development", release_commit: str | None = None) -> list[dict]:
    violations: list[dict] = []
    
    if not ledger_path.exists():
        return [{"code": "LEDGER_NOT_FOUND", "message": f"Ledger not found at {ledger_path}"}]
        
    try:
        ledger_data = json.loads(ledger_path.read_text(encoding="utf-8"))
    except Exception as e:
        return [{"code": "LEDGER_PARSE_ERROR", "message": str(e)}]
        
    schema_path = Path("tools/acceptance/schemas/ledger.schema.json")
    if schema_path.exists():
        try:
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            jsonschema.validate(ledger_data, schema)
        except Exception as e:
            violations.append({"code": "LEDGER_SCHEMA", "message": str(e)})

    receipt_schema_path = Path("tools/acceptance/schemas/receipt.schema.json")
    receipt_schema = None
    if receipt_schema_path.exists():
        try:
            receipt_schema = json.loads(receipt_schema_path.read_text(encoding="utf-8"))
        except Exception:
            pass

    items = ledger_data.get("items", [])
    items_by_id = {i["id"]: i for i in items}
    
    # 1. State check
    for item in items:
        iid = item.get("id")
        st = item.get("state")
        if st not in KNOWN_STATES:
            violations.append({"item": iid, "code": "UNKNOWN_STATE", "message": f"Unknown state '{st}'"})

    # 11. Parent CRA-xxx.A check
    for item in items:
        iid = item.get("id", "")
        if item.get("kind") == "acceptance" or (iid.startswith("CRA-") and iid.endswith(".A")):
            if item.get("state") == "ACCEPTED":
                parent_prefix = iid[:-2]  # "CRA-xxx"
                children = [
                    c for c in items
                    if c.get("parent") == parent_prefix and c.get("id") != iid and c.get("kind") == "clause"
                ]
                for ch in children:
                    if ch.get("state") != "ACCEPTED":
                        violations.append({
                            "item": iid,
                            "code": "CHILD_OPEN",
                            "message": f"Parent {iid} is ACCEPTED but child {ch['id']} is {ch.get('state')}",
                        })

    # 12. Blocked check
    for item in items:
        iid = item.get("id")
        st = item.get("state")
        blocked_by = item.get("blocked_by", [])
        if blocked_by and st in ("VERIFIED", "ACCEPTED"):
            for b in blocked_by:
                b_item = items_by_id.get(b)
                if not b_item or b_item.get("state") != "ACCEPTED":
                    violations.append({
                        "item": iid,
                        "code": "BLOCKED",
                        "message": f"Item {iid} is {st} but blocked by unaccepted/unrecorded '{b}'",
                    })

    # Check receipts for VERIFIED and ACCEPTED items
    for item in items:
        iid = item.get("id")
        st = item.get("state")
        receipts = item.get("receipts", [])
        
        # Scenario/decision/conflict/research items might not have automated test receipts
        if item.get("kind") not in ("clause", "acceptance"):
            continue
            
        if st in ("VERIFIED", "ACCEPTED"):
            if not receipts:
                violations.append({"item": iid, "code": "MISSING_RECEIPT", "message": f"Item {iid} has no receipts"})
                continue
                
            for rcpt_ref in receipts:
                rcpt_path_str = rcpt_ref.get("path")
                expected_sha = rcpt_ref.get("sha256")
                if not rcpt_path_str:
                    violations.append({"item": iid, "code": "MISSING_RECEIPT", "message": "Receipt path empty"})
                    continue
                rcpt_path = Path(rcpt_path_str)
                if not rcpt_path.exists():
                    violations.append({
                        "item": iid,
                        "code": "MISSING_RECEIPT",
                        "message": f"Receipt file not found: {rcpt_path_str}",
                    })
                    continue
                    
                actual_sha = sha256_file(rcpt_path)
                if expected_sha and actual_sha != expected_sha:
                    violations.append({
                        "item": iid,
                        "code": "RECEIPT_HASH_MISMATCH",
                        "message": f"Receipt hash mismatch for {rcpt_path_str}: expected {expected_sha}, got {actual_sha}",
                    })
                    continue

                try:
                    rcpt = json.loads(rcpt_path.read_text(encoding="utf-8"))
                except Exception as e:
                    violations.append({"item": iid, "code": "RECEIPT_PARSE_ERROR", "message": str(e)})
                    continue

                # Receipt Schema validation
                if receipt_schema:
                    try:
                        jsonschema.validate(rcpt, receipt_schema)
                    except Exception as e:
                        violations.append({
                            "item": iid,
                            "code": "RECEIPT_SCHEMA",
                            "message": f"Receipt schema validation failed: {e.message}",
                        })

                # Check evidence_files
                for ev in rcpt.get("evidence_files", []):
                    ev_path_str = ev.get("path")
                    ev_sha = ev.get("sha256")
                    if not ev_path_str:
                        continue
                    ev_path = Path(ev_path_str)
                    if not ev_path.exists():
                        violations.append({
                            "item": iid,
                            "code": "EVIDENCE_MISSING",
                            "message": f"Evidence file {ev_path_str} missing",
                        })
                    else:
                        actual_ev_sha = sha256_file(ev_path)
                        if actual_ev_sha != ev_sha:
                            violations.append({
                                "item": iid,
                                "code": "EVIDENCE_HASH_MISMATCH",
                                "message": f"Evidence file {ev_path_str} hash mismatch",
                            })

                # Exit code check
                exec_info = rcpt.get("execution", {})
                if exec_info.get("exit_code") != 0:
                    violations.append({
                        "item": iid,
                        "code": "NONZERO_EXIT",
                        "message": f"Receipt execution exit_code={exec_info.get('exit_code')}",
                    })

                # Tests check
                res = rcpt.get("results", {})
                tests_tot = res.get("tests_total", 0)
                tests_failed = res.get("tests_failed", 0)
                tests_errors = res.get("tests_errors", 0)
                tests_skipped = res.get("tests_skipped", 0)
                tests_xfailed = res.get("tests_xfailed", 0)
                
                if tests_tot <= 0:
                    violations.append({
                        "item": iid,
                        "code": "NO_TESTS",
                        "message": f"Receipt has zero tests total for {iid}",
                    })
                if tests_failed > 0 or tests_errors > 0:
                    violations.append({
                        "item": iid,
                        "code": "TEST_FAILURE",
                        "message": f"Tests failed: {tests_failed}, errors: {tests_errors}",
                    })
                if tests_skipped > 0 or tests_xfailed > 0:
                    violations.append({
                        "item": iid,
                        "code": "SKIPPED_REQUIRED",
                        "message": f"Required test skipped: skipped={tests_skipped}, xfailed={tests_xfailed}",
                    })

                # Source unchanged
                if not rcpt.get("source_unchanged_during_run", False):
                    violations.append({
                        "item": iid,
                        "code": "SOURCE_CHANGED",
                        "message": f"Source was changed during run in receipt {rcpt.get('receipt_id')}",
                    })

                # Stale artifact check
                try:
                    completed_at = parse_iso(exec_info.get("completed_at"))
                    art_mtime = parse_iso(rcpt.get("artifact_mtime"))
                    if completed_at < art_mtime:
                        violations.append({
                            "item": iid,
                            "code": "STALE_ARTIFACT",
                            "message": f"completed_at ({completed_at}) earlier than artifact_mtime ({art_mtime})",
                        })
                except Exception:
                    pass

                # Reviewer check for ACCEPTED
                if st == "ACCEPTED":
                    rev = rcpt.get("reviewer")
                    sig = rcpt.get("review_signature")
                    prod = rcpt.get("producer")
                    if not rev or not sig:
                        violations.append({
                            "item": iid,
                            "code": "UNREVIEWED",
                            "message": f"ACCEPTED item {iid} lacks reviewer or signature in receipt",
                        })
                    elif rev == prod:
                        violations.append({
                            "item": iid,
                            "code": "SELF_REVIEW",
                            "message": f"ACCEPTED item {iid} has reviewer == producer ('{rev}')",
                        })

                # Release mode check
                if mode == "release":
                    if rcpt.get("source_tree_dirty"):
                        violations.append({
                            "item": iid,
                            "code": "DIRTY_TREE",
                            "message": f"Receipt {rcpt.get('receipt_id')} was run on dirty tree in release mode",
                        })
                    if release_commit and rcpt.get("source_commit") != release_commit:
                        violations.append({
                            "item": iid,
                            "code": "WRONG_COMMIT",
                            "message": f"Receipt commit {rcpt.get('source_commit')} != release {release_commit}",
                        })

    return violations

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ledger", default=".audit-scratch/ledger.json")
    ap.add_argument("--mode", default="development", choices=["development", "release"])
    ap.add_argument("--release-commit", default=None)
    a = ap.parse_args()
    
    violations = verify_ledger(Path(a.ledger), mode=a.mode, release_commit=a.release_commit)
    if violations:
        print(f"VERIFICATION FAILED: {len(violations)} violations found:")
        for v in violations:
            item_str = f"[{v['item']}] " if "item" in v else ""
            print(f"  - {v['code']}: {item_str}{v['message']}")
        return 1
    else:
        print(f"VERIFICATION PASSED: 0 violations ({a.mode} mode)")
        return 0

if __name__ == "__main__":
    sys.exit(main())
