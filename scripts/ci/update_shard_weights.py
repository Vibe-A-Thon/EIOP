#!/usr/bin/env python3
"""Rebuild tests/ci-shard-weights.json (seconds per test file) from JUnit XML results.

Usage: python scripts/ci/update_shard_weights.py test-results/*.xml [--out tests/ci-shard-weights.json]

Only balance depends on these numbers; a stale or missing entry never changes which tests run
(scripts/ci/check_test_shards.py proves the partition is complete either way).
"""

from __future__ import annotations

import argparse
import json
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path


def file_seconds(paths: list[Path]) -> dict[str, float]:
    totals: dict[str, float] = defaultdict(float)
    for path in paths:
        for case in ET.parse(path).getroot().iter("testcase"):
            if case.get("file"):
                name = case.get("file", "").replace("\\", "/")
            else:  # pytest junit: classname "tests.unit.test_x.TestY" -> tests/unit/test_x.py
                parts = case.get("classname", "").split(".")
                while parts and parts[-1][:1].isupper():
                    parts.pop()
                name = "/".join(parts) + ".py"
            totals[name] += float(case.get("time") or 0)
    return {name: round(seconds, 2) for name, seconds in sorted(totals.items()) if name != ".py"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("junit", nargs="+", type=Path)
    parser.add_argument("--out", type=Path, default=Path("tests/ci-shard-weights.json"))
    args = parser.parse_args()
    weights = file_seconds(args.junit)
    args.out.write_text(json.dumps(weights, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {len(weights)} file weights ({sum(weights.values()):.0f}s total) to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
