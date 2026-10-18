#!/usr/bin/env python3
"""CLI runner for independent ASPEII evidence verification."""

import argparse
import sys
from pathlib import Path

# Add packages to path
repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root / "packages"))

from eoip.aspeii.verifier import ASPEIIVerifier


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify ASPEII evidence bundle.")
    parser.add_argument("bundle", help="Path to .audit-scratch/aspeii/<run-id>/ bundle directory")
    parser.add_argument("--expected-clauses", type=int, default=216, help="Expected verified clause count")

    args = parser.parse_args()
    bundle_path = Path(args.bundle)

    if not bundle_path.exists():
        print(f"MALFORMED: bundle path does not exist: {bundle_path}", file=sys.stderr)
        return 2

    try:
        verifier = ASPEIIVerifier(expected_total_clauses=args.expected_clauses)
        res = verifier.verify_bundle(bundle_path)
    except Exception as exc:
        print(f"MALFORMED: verification failed: {exc}", file=sys.stderr)
        return 2

    print(f"ASPEII Verification: {res.verdict}")
    print(f"  Verified Clauses: {res.verified_clauses}/{res.total_clauses}")
    print(f"  Cases Executed  : {res.cases_executed}")
    print(f"  Failures        : {len(res.failures)}")

    if res.verdict == "PASS":
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
