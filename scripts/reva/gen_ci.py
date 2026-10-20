"""Historical generator for the reva-* CI lane workflows.

FT-F04: this generator wrote echo-only placeholder workflows that reported green
without running anything. The lane files under .github/workflows are now
maintained by hand (real suites, or clearly marked NOT IMPLEMENTED placeholders),
so the generator refuses to overwrite them unless --force is given.
"""
import sys

if "--force" not in sys.argv[1:]:
    print("refusing to regenerate echo-only reva-* workflows (FT-F04); pass --force to override",
          file=sys.stderr)
    raise SystemExit(2)

from pathlib import Path

lanes = [
    ("reva-static", "Static checks, ruff, mypy, forbid placeholders, depth markers"),
    ("reva-unit", "Unit test suite under tests/reva/unit"),
    ("reva-component", "Component test suite under tests/reva/component"),
    ("reva-integration", "Integration test suite with containerized DBs"),
    ("reva-fixtures", "Fixture cache generation and validation"),
    ("reva-acceptance", "Acceptance journeys RJ-01..RJ-12"),
    ("reva-ledger", "Proof-of-Done ledger generation and verification"),
    ("reva-perf", "Performance and NFR benchmarks"),
    ("reva-mutation", "Mutation testing probe over reva modules"),
    ("reva-airgap", "Full non-perf suite under air-gapped network conditions"),
]

workflows_dir = Path(".github/workflows")
workflows_dir.mkdir(parents=True, exist_ok=True)

for name, desc in lanes:
    content = f"""name: {name}
on: [push, pull_request]

jobs:
  run:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: {desc}
        run: echo "Running {name}"
"""
    (workflows_dir / f"{name}.yml").write_text(content, encoding="utf-8")

print("Created 10 CI lane workflows.")
