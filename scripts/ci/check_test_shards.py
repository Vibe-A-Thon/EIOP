#!/usr/bin/env python3
"""Prove that sharded CI test jobs partitioned the suite: nothing lost, nothing run twice.

Usage: python scripts/ci/check_test_shards.py <manifest.json>... [--summary FILE]

Reads the manifests written by eoip.verification.pytest_shard (EOIP_TEST_SHARD_MANIFEST) and
fails unless: every shard 1..n reported exactly once; all shards collected the same test files
with the same number of tests in each; every file's tests were assigned to exactly one shard, all
of them; and the per-shard counts add up to the collected total. Shards are assigned by file, so
the check is made per file. A node id that differs between processes (e.g. a parametrize id built
from time.time()) cannot be compared across shards; it is reported as a warning naming the file,
not as a failure, because its file still ran in exactly one shard. A shard job that crashed
before collecting leaves no manifest and therefore fails this check instead of passing silently.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path


def _file(nodeid: str) -> str:
    return nodeid.split("::", 1)[0]


def check(manifests: list[dict]) -> tuple[list[str], list[str], list[tuple[int, int, int]]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not manifests:
        return ["no shard manifests found"], warnings, []
    totals = {m.get("total") for m in manifests}
    if len(totals) != 1:
        return [f"shards disagree on the shard count: {sorted(map(str, totals))}"], warnings, []
    total = totals.pop()
    seen = sorted(m.get("shard") for m in manifests)
    if seen != list(range(1, total + 1)):
        errors.append(f"expected shards 1..{total} exactly once, got {seen}")

    first = manifests[0]
    per_file = Counter(_file(n) for n in first["collected"])
    for m in manifests[1:]:
        other = Counter(_file(n) for n in m["collected"])
        if other != per_file:
            diff = sorted(f for f in per_file.keys() | other.keys() if per_file[f] != other[f])
            errors.append(f"shard {m['shard']} collected a different suite than shard {first['shard']} "
                          f"(files differing in test count: {diff[:5]})")
        unstable = sorted({_file(n) for n in set(m["collected"]) ^ set(first["collected"])})
        if unstable and other == per_file:
            warnings.append(f"node ids differ between processes in {unstable[:5]} "
                            "(non-deterministic parametrize ids; give them stable ids)")

    owner: dict[str, int] = {}
    for m in manifests:
        own = set(m["collected"])
        stray = [n for n in m["assigned"] if n not in own]
        if stray:
            errors.append(f"shard {m['shard']} ran {len(stray)} tests it did not collect, e.g. {stray[:3]}")
        assigned_per_file = Counter(_file(n) for n in m["assigned"])
        for name, count in assigned_per_file.items():
            if name in owner and owner[name] != m["shard"]:
                errors.append(f"{name} assigned to shards {owner[name]} and {m['shard']}")
            owner[name] = m["shard"]
            if count != per_file.get(name, 0):
                errors.append(f"shard {m['shard']} ran {count} of {per_file.get(name, 0)} tests in {name}")
    unassigned = sorted(set(per_file) - owner.keys())
    if unassigned:
        errors.append(f"{len(unassigned)} collected test files ran in no shard, e.g. {unassigned[:5]}")
    ran = sum(len(m["assigned"]) for m in manifests)
    if ran != sum(per_file.values()):
        errors.append(f"shards ran {ran} tests in total but {sum(per_file.values())} were collected")
    rows = [(m["shard"], len(m["assigned"]), len(m.get("files", {}))) for m in sorted(manifests, key=lambda m: m["shard"])]
    return errors, warnings, rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("manifests", nargs="*", type=Path)
    parser.add_argument("--summary", type=Path, help="append a Markdown table (e.g. $GITHUB_STEP_SUMMARY)")
    args = parser.parse_args(argv)
    manifests = []
    for path in args.manifests:
        try:
            manifests.append(json.loads(path.read_text(encoding="utf-8")))
        except (OSError, ValueError) as exc:
            print(f"unreadable manifest {path}: {type(exc).__name__}", file=sys.stderr)
            return 1
    errors, warnings, rows = check(manifests)
    collected = len(manifests[0]["collected"]) if manifests else 0
    lines = [f"Test shards: {len(rows)} shard(s), {collected} collected tests", "",
             "| shard | tests | files |", "|---:|---:|---:|", *(f"| {s} | {t} | {f} |" for s, t, f in rows)]
    print("\n".join(lines))
    if args.summary:
        with args.summary.open("a", encoding="utf-8") as out:
            out.write("\n".join(lines) + "\n\n" + "".join(f"> warning: {w}\n" for w in warnings)
                      + ("**Partition: FAIL**\n" if errors else "**Partition: PASS**\n"))
    for warning in warnings:
        print(f"::warning title=test shards::{warning}")
    for error in errors:
        print(f"FAIL: {error}", file=sys.stderr)
    if not errors:
        print("partition: PASS (every collected test file ran in exactly one shard, all of its tests)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
