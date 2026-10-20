#!/usr/bin/env python3
"""Check that REVA CI lane definitions exist AND are real (T-005 / OBL-REVA-CI-01, FT-F04).

A lane file that only echoes, is marked NOT IMPLEMENTED, or does not run on push and
pull_request is a placeholder and fails the check.
"""

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

def placeholder_reason(text: str) -> str:
    """Return why a workflow is a placeholder, or "" when it runs real checks."""
    import yaml

    code = "\n".join(line for line in text.splitlines() if not line.lstrip().startswith("#"))
    if "NOT IMPLEMENTED" in code:
        return "marked NOT IMPLEMENTED"
    data = yaml.safe_load(text) or {}
    triggers = data.get("on", data.get(True, {})) or {}
    if isinstance(triggers, (str, list)):
        triggers = {t: None for t in ([triggers] if isinstance(triggers, str) else triggers)}
    if "push" not in triggers or "pull_request" not in triggers:
        return "does not run on push and pull_request"
    runs = [step.get("run", "") for job in (data.get("jobs") or {}).values() for step in job.get("steps", [])
            if isinstance(step, dict) and step.get("run")]
    real = [r for r in runs if any(tok in r for tok in ("python", "pytest", "ruff"))]
    if not real:
        return "no step runs python/pytest (echo-only)"
    return ""


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

    placeholders = []
    for lane in REQUIRED_LANES:
        lane_file = workflows_dir / f"{lane}.yml"
        if lane_file.exists():
            reason = placeholder_reason(lane_file.read_text(encoding="utf-8"))
            if reason:
                placeholders.append(f"{lane}: {reason}")
    if placeholders:
        print("Placeholder CI lanes:", file=sys.stderr)
        for p in placeholders:
            print(f"  - {p}", file=sys.stderr)
        return 1

    if missing:
        print("Missing CI lane workflows:", file=sys.stderr)
        for m in missing:
            print(f"  - {m}", file=sys.stderr)
        return 1

    print("CI lanes verification: PASS (all 10 lanes present)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
