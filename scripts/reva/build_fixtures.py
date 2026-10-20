#!/usr/bin/env python3
"""Build the deterministic REVA archive fixtures (FT-F04 reva-fixtures lane).

python scripts/reva/build_fixtures.py [--out DIR] [--check-against DIR]

--check-against compares the fresh build with a previous build byte-for-byte and fails on any
difference, which is how the lane proves the fixtures are reproducible (NFR-012).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from tests.reva.support.archive_fixtures import build_fixtures, default_cache_dir


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--check-against", type=Path, default=None)
    args = parser.parse_args(argv)
    out = args.out or default_cache_dir()
    manifest = build_fixtures(out)
    print(f"built {len(manifest)} fixtures in {out}")
    for name, entry in sorted(manifest.items()):
        print(f"  {entry['sha256']}  {name}")
    if args.check_against is not None:
        previous = json.loads((args.check_against / "manifest.json").read_text(encoding="utf-8"))
        diffs = sorted(name for name in set(previous) | set(manifest)
                       if previous.get(name, {}).get("sha256") != manifest.get(name, {}).get("sha256"))
        if diffs:
            for name in diffs:
                print(f"::error::fixture {name} is not reproducible between builds")
            return 1
        print(f"determinism: PASS ({len(manifest)} fixtures byte-identical across two builds)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
