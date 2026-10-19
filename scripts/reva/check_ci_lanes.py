#!/usr/bin/env python3
"""Check that REVA CI lane definitions exist (T-005 / OBL-REVA-CI-01)."""

import sys
from pathlib import Path

REQUIRED_LANES = [
    "reva-static",
    "reva-unit",
    "reva-component",
    "reva-integration",
    "reva-fixtures",
    "reva-acceptance",
    "reva-ledger",
    "reva-perf",
    "reva-mutation",
    "reva-airgap",
]

def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent.parent
    workflows_dir = repo_root / ".github" / "workflows"
    if not workflows_dir.exists():
        print(f"Directory {workflows_dir} does not exist", file=sys.stderr)
        return 1

    missing = []
    for lane in REQUIRED_LANES:
        lane_file = workflows_dir / f"{lane}.yml"
        if not lane_file.exists():
            missing.append(str(lane_file))

    if missing:
        print("Missing CI lane workflows:", file=sys.stderr)
        for m in missing:
            print(f"  - {m}", file=sys.stderr)
        return 1

    print("CI lanes verification: PASS (all 10 lanes present)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
