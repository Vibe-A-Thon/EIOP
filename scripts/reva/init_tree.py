from pathlib import Path

dirs = [
    "reva",
    "reva/core",
    "reva/kernel",
    "reva/pd",
    "reva/sandbox",
    "reva/extract",
    "reva/extract/artifacts",
    "reva/extract/provenance",
    "reva/extract/boundaries",
    "reva/extract/apisurface",
    "reva/extract/dbschema",
    "reva/workflows",
    "reva/views",
    "reva/graph",
    "reva/api",
    "reva/mcp",
    "reva/cli",
    "reva/obs",
    "reva/migrations",
    "tests/reva",
    "tests/reva/unit",
    "tests/reva/unit/scripts",
    "tests/reva/component",
    "tests/reva/integration",
    "tests/reva/acceptance",
    "tests/reva/conformance",
    "tests/reva/evaluation",
    "tests/reva/perf",
    "tests/reva/fixtures",
    "tests/reva/support",
    "docs/reva/obligations",
]

for d in dirs:
    p = Path(d)
    p.mkdir(parents=True, exist_ok=True)
    if d.startswith("reva"):
        init_file = p / "__init__.py"
        if not init_file.exists():
            init_file.write_text('"""REVA package module."""\n', encoding="utf-8")

print("Tree initialized.")
