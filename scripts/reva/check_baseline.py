#!/usr/bin/env python3
"""Verifier for docs/reva/BASELINE.md and DECISIONS.md (T-001 / OBL-REVA-P0-BASELINE)."""

import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = [
    "Repository & commit",
    "Backend root & package name",
    "FastAPI app object & router mount",
    "Settings system",
    "Relational DB (engine, URL var, migrations)",
    "Graph abstraction (classes, methods, backends supported, transaction model)",
    "Mutation gateway (exists? API)",
    "Auth & principal model",
    "Tenancy model",
    "ACL model in connectors",
    "Task queue",
    "Connectors (list, file-import support, coverage/watermark support)",
    "LLM abstraction & egress policy",
    "MCP server",
    "Frontend (framework, router, layout, design system, state mgmt, test tools)",
    "Compose (services, volumes, networks)",
    "Test runner & baseline results",
    "CI system",
    "Gaps vs REVA needs",
]

def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent.parent
    baseline_path = repo_root / "docs" / "reva" / "BASELINE.md"
    decisions_path = repo_root / "docs" / "reva" / "DECISIONS.md"

    if not baseline_path.exists():
        print(f"FAIL: {baseline_path} does not exist", file=sys.stderr)
        return 1

    if not decisions_path.exists():
        print(f"FAIL: {decisions_path} does not exist", file=sys.stderr)
        return 1

    content = baseline_path.read_text(encoding="utf-8")
    errors = []

    for sec in REQUIRED_SECTIONS:
        # Check header exists
        pattern = rf"^#+\s+{re.escape(sec)}"
        match = re.search(pattern, content, re.MULTILINE)
        if not match:
            errors.append(f"Missing section: '{sec}'")
            continue

        # Extract text until next section
        start = match.end()
        next_heading = re.search(r"^#+\s+", content[start:], re.MULTILINE)
        sec_content = content[start : start + next_heading.start()] if next_heading else content[start:]

        # Find path:line references
        refs = re.findall(r"([A-Za-z0-9_./\\-]+\.[A-Za-z0-9]+):(\d+)", sec_content)
        if not refs:
            errors.append(f"Section '{sec}' has no valid path:line references")
            continue

        for p_str, line_str in refs:
            # Normalize path
            ref_path = repo_root / p_str.replace("\\", "/")
            if not ref_path.exists():
                errors.append(f"Section '{sec}' references non-existent file: {p_str}")
                continue
            try:
                line_no = int(line_str)
                lines = ref_path.read_text(encoding="utf-8", errors="replace").splitlines()
                if line_no < 1 or line_no > len(lines):
                    errors.append(f"Section '{sec}' references out-of-range line {line_no} in {p_str} (file has {len(lines)} lines)")
            except Exception as exc:
                errors.append(f"Error checking {p_str}:{line_str}: {exc}")

    # Check decisions
    dec_content = decisions_path.read_text(encoding="utf-8")
    for i in range(1, 25):
        d_id = f"D-{i:02d}"
        if d_id not in dec_content:
            errors.append(f"Decision {d_id} not found in {decisions_path}")

    if errors:
        print("BASELINE check failed with errors:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print("BASELINE and DECISIONS verification: PASS")
    return 0

if __name__ == "__main__":
    sys.exit(main())
