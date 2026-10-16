"""CLI entry: run a graph-test suite file against the graph store.

Usage: python -m packages.eoip.graphtest <suite.yaml|suite.json>
"""

from __future__ import annotations

import argparse
import json
import sys


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="eoip.graphtest")
    parser.add_argument("suite", help="Path to a YAML or JSON graph-test suite")
    parser.add_argument("--store", default="memory", choices=["memory"],
                        help="Graph store backend (only in-memory is CLI-supported)")
    args = parser.parse_args(argv)

    from eoip.graph.memory import MemoryGraphStore
    from eoip.graphtest.framework import run_suite_file

    store = MemoryGraphStore()
    report = run_suite_file(store, args.suite)
    print(json.dumps(report.to_dict(), indent=2))
    return 0 if report.failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
