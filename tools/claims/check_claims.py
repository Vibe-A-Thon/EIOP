#!/usr/bin/env python3
"""CI claims check tool (WP-041, CRA-041.A).
Scans docs, release notes, and markdown sources for standards, competitor,
patent, or scorecard claims and validates against the Claims Register and Ledger.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Add packages to path
repo_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(repo_root / "packages"))

from eoip.claims.registry import ClaimsRegistry
from eoip.claims.scanner import ClaimsScanner


def main() -> int:
    parser = argparse.ArgumentParser(description="Check claims governance in documentation and sources.")
    parser.add_argument(
        "--claims-register",
        default="docs/claims/claims-register.yaml",
        help="Path to claims register YAML",
    )
    parser.add_argument(
        "--patent-register",
        default="docs/restricted/patent-candidates.yaml",
        help="Path to restricted patent candidate register YAML",
    )
    parser.add_argument(
        "--ledger",
        default=".audit-scratch/ledger.json",
        help="Path to ledger JSON",
    )
    parser.add_argument(
        "--docs-dir",
        default="docs",
        help="Directory to scan for claims",
    )
    parser.add_argument(
        "--scan-file",
        action="append",
        dest="scan_files",
        help="Specific file(s) to scan",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        default=True,
        help="Exit non-zero if any violations found",
    )

    args = parser.parse_args()

    reg_path = Path(args.claims_register)
    pat_path = Path(args.patent_register)
    ledger_path = Path(args.ledger)

    if not reg_path.exists():
        print(f"ERROR: Claims register not found at {reg_path}", file=sys.stderr)
        return 1

    registry = ClaimsRegistry.load_from_yaml(reg_path, pat_path)
    scanner = ClaimsScanner(registry=registry, ledger_path=ledger_path)

    violations = []

    if args.scan_files:
        for f in args.scan_files:
            violations.extend(scanner.scan_file(f))
    else:
        docs_dir = Path(args.docs_dir)
        if docs_dir.exists():
            violations.extend(scanner.scan_directory(docs_dir))

    if violations:
        print(f"\n[CLAIMS CHECK FAILED] {len(violations)} violation(s) detected:\n")
        for v in violations:
            print(f"  [{v.violation_type}] {v.file_path}:{v.line_number}")
            print(f"    Matched: '{v.matched_text}'")
            print(f"    Reason : {v.message}\n")
        if args.strict:
            return 1
    else:
        print("\n[CLAIMS CHECK PASSED] 0 violations found. All claims conform to governance.\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
