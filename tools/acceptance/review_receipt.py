"""Record an independent reviewer signature on a receipt and optionally update the ledger."""
from __future__ import annotations
import argparse, hashlib, json, sys
from datetime import datetime, timezone
from pathlib import Path

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--receipt", required=True)
    ap.add_argument("--reviewer", required=True)
    ap.add_argument("--signature", required=True)
    ap.add_argument("--ledger", default=".audit-scratch/ledger.json")
    ap.add_argument("--state", default="ACCEPTED", choices=["VERIFIED", "ACCEPTED"])
    a = ap.parse_args()

    rcpt_path = Path(a.receipt)
    if not rcpt_path.exists():
        print(f"Receipt not found: {rcpt_path}", file=sys.stderr)
        return 1

    rcpt = json.loads(rcpt_path.read_text(encoding="utf-8"))
    producer = rcpt.get("producer")
    if producer and producer == a.reviewer:
        print(f"SELF_REVIEW rejected: reviewer '{a.reviewer}' matches producer", file=sys.stderr)
        return 2

    rcpt["reviewer"] = a.reviewer
    rcpt["review_signature"] = a.signature
    rcpt["state_claimed"] = a.state
    rcpt_path.write_text(json.dumps(rcpt, indent=2), encoding="utf-8")
    new_sha = sha256_file(rcpt_path)

    clause_id = rcpt.get("requirement_clause")
    led_path = Path(a.ledger)
    if led_path.exists() and clause_id:
        led = json.loads(led_path.read_text(encoding="utf-8"))
        norm_path = str(rcpt_path).replace("\\", "/")
        found = False
        for item in led.get("items", []):
            if item.get("id") == clause_id:
                found = True
                item["state"] = a.state
                item["updated_at"] = datetime.now(timezone.utc).isoformat()
                # Update or add receipt
                rcpt_refs = item.setdefault("receipts", [])
                matched_ref = False
                for r in rcpt_refs:
                    if r.get("path") == norm_path:
                        r["sha256"] = new_sha
                        matched_ref = True
                        break
                if not matched_ref:
                    rcpt_refs.append({"path": norm_path, "sha256": new_sha})
                break
        if found:
            led_path.write_text(json.dumps(led, indent=2), encoding="utf-8")
            print(f"Updated clause {clause_id} in {led_path} to {a.state}")

    print(f"Reviewed {rcpt_path} with signature {a.signature} (sha256: {new_sha})")
    return 0

if __name__ == "__main__":
    sys.exit(main())
