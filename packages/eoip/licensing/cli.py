"""Offline license verification CLI entry point (SR-DEP-007).

Air-gapped installs verify a license file without any network access::

    python -m eoip.licensing.cli verify --license /etc/eoip/license.json --key-file /etc/eoip/vendor.key

The key can also come from the ``EOIP_LICENSE_KEY`` environment variable or be
passed directly for scripted use. Exit semantics live with the caller (the
function returns a report; a thin ``main`` wrapper maps it to exit codes).
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any, Sequence

from eoip.licensing.license_file import load_license_file


def verify_license_cli(license_path: str | Path, vendor_key: str | bytes | None = None, key_file: str | Path | None = None) -> dict[str, Any]:
    """Verify a license file offline and return a JSON-serialisable report.

    Exactly one of ``vendor_key`` / ``key_file`` must be provided (explicit
    arguments win over ``EOIP_LICENSE_KEY`` from the environment).
    """
    if vendor_key is None and key_file is None:
        env_key = os.getenv("EOIP_LICENSE_KEY")
        if env_key:
            vendor_key = env_key
    if vendor_key is None and key_file is not None:
        try:
            vendor_key = Path(key_file).read_text(encoding="utf-8").strip()
        except OSError:
            return {"ok": False, "reason": "unreadable_key_file"}
    if vendor_key is None:
        return {"ok": False, "reason": "missing_vendor_key"}

    result = load_license_file(license_path, vendor_key)
    report: dict[str, Any] = {"ok": result.ok, "license_path": str(license_path), "reason": result.reason}
    if result.payload is not None:
        payload = result.payload
        report["payload"] = {
            "license_id": payload.license_id,
            "customer": payload.customer,
            "edition": payload.edition,
            "model": payload.model,
            "modules": payload.modules,
            "size_tier": payload.size_tier,
            "max_tenants": payload.max_tenants,
            "max_seats": payload.max_seats,
            "max_records": payload.max_records,
            "issued_at": payload.issued_at.isoformat(),
            "expiry": payload.expiry.isoformat() if payload.expiry else None,
            "grace_days": payload.grace_days,
        }
    return report


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="eoip-licensing", description="Offline EOIP license utilities")
    sub = parser.add_subparsers(dest="command", required=True)
    verify = sub.add_parser("verify", help="Verify a signed license file offline (SR-DEP-007)")
    verify.add_argument("--license", required=True, help="Path to the signed license JSON file")
    verify.add_argument("--key-file", help="Path to the vendor key file")
    args = parser.parse_args(argv)

    if args.command == "verify":
        report = verify_license_cli(args.license, key_file=args.key_file)
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0 if report["ok"] else 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
