"""CLI entry point: detect and report available OCI container runtimes.

Usage:
    python -m scripts.detect_runtime           # show active runtime
    python -m scripts.detect_runtime --all      # list every detected runtime
    python -m scripts.detect_runtime --json     # machine-readable output
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import sys

from eoip.enterprise.container_runtime import discover, discover_all, require


def main() -> None:
    parser = argparse.ArgumentParser(description="EOIP container-runtime probe")
    parser.add_argument("--all", action="store_true", help="List every detected runtime")
    parser.add_argument("--json", action="store_true", dest="as_json", help="JSON output")
    args = parser.parse_args()

    if args.all:
        runtimes = discover_all()
        if args.as_json:
            print(json.dumps([dataclasses.asdict(r) for r in runtimes], indent=2))
        elif runtimes:
            for i, r in enumerate(runtimes):
                marker = " (preferred)" if i == 0 else ""
                compose = f" | compose: {' '.join(r.compose.command)} {r.compose.version}" if r.compose else ""
                rootless = " [rootless]" if r.rootless else ""
                print(f"  {r.name} {r.version}{rootless}{compose}{marker}")
        else:
            print("No OCI container runtimes detected.", file=sys.stderr)
            sys.exit(1)
        return

    try:
        rt = require()
    except EnvironmentError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)

    if args.as_json:
        print(json.dumps(dataclasses.asdict(rt), indent=2))
    else:
        compose = f" | compose: {' '.join(rt.compose.command)} {rt.compose.version}" if rt.compose else " | compose: none"
        rootless = " [rootless]" if rt.rootless else ""
        print(f"EOIP Container Runtime: {rt.name} {rt.version}{rootless}{compose}")


if __name__ == "__main__":
    main()
