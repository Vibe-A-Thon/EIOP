"""Generate a machine-readable GAP requirement coverage report.

Requirement coverage:
- GAP-KGCI-001: CLI runnable in CI.
- GAP-KGCI-002: machine-readable report.
- GAP-KGCI-003: fail build on configured semantic regression.

Usage:
  python -m scripts.gap_coverage --project-root . --output gap-coverage.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "packages"))

from eoip.gaps.coverage import G2_IMPLEMENTATION_DOC, G2_REQUIREMENTS_DOC, build_gap_coverage_report


def main() -> int:
    parser = argparse.ArgumentParser(description="Build EOIP GAP requirement coverage report")
    parser.add_argument("--project-root", default=".", help="Repository root")
    parser.add_argument("--output", help="Optional JSON output path")
    parser.add_argument(
        "--doc-set",
        choices=("gap", "g2"),
        default="gap",
        help="Requirement document set to scan",
    )
    parser.add_argument(
        "--fail-on-planned-p0",
        action="store_true",
        help="Return exit code 1 when any P0 GAP requirement has no code/test evidence",
    )
    parser.add_argument(
        "--fail-on-gate",
        action="store_true",
        help="Return exit code 1 when the configured completion gate fails",
    )
    parser.add_argument(
        "--gate-priority",
        default="P0",
        help="Highest priority required by --fail-on-gate, e.g. P0 or P1",
    )
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    kwargs = (
        {"requirements_doc": G2_REQUIREMENTS_DOC, "implementation_doc": G2_IMPLEMENTATION_DOC}
        if args.doc_set == "g2"
        else {}
    )
    coverage = build_gap_coverage_report(root, **kwargs)
    report = coverage.to_dict()
    report["doc_set"] = args.doc_set
    report["completion_gate"] = coverage.completion_gate(
        max_priority=args.gate_priority,
        include_requirements=False,
    )
    payload = json.dumps(report, indent=2, sort_keys=True)
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)

    if args.fail_on_planned_p0:
        has_planned_p0 = any(
            item["priority"] == "P0" and item["status"] == "planned"
            for item in report["requirements"]
        )
        return 1 if has_planned_p0 else 0
    if args.fail_on_gate:
        return 0 if report["completion_gate"]["passed"] else 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
