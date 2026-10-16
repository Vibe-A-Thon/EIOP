from pathlib import Path

for path in ["packages/eoip/graph/benchmark.py", "ci/pipeline.py", "docs"]:
    p = Path(path)
    print(f"{path}: exists={p.exists()}")
