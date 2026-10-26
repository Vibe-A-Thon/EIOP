"""Run bounded, isolated pytest file shards with exact receipts, without xdist."""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    root, out = args.root.resolve(), args.out.resolve()
    paths = sorted(p.relative_to(root).as_posix() for p in (root / "tests/unit").rglob("test_*.py"))
    shards = [paths[index::6] for index in range(6)]
    manifest = {"method": "sorted test files round-robin across six isolated pytest processes",
                "files": len(paths), "shards": shards, "note": "No xdist; one evidence coordinator per shard."}
    (out / "evidence/unit-shards.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    processes = []
    for index, files in enumerate(shards):
        destination = out / "evidence" / f"unit-shard-{index + 1}"
        command = [sys.executable, str(Path(__file__).with_name("execute_audit_check.py")),
                   "--repo-root", str(root), "--out", str(destination), "--timeout", "660", "--",
                   "{python}", "-m", "pytest", *files, "--import-mode=importlib",
                   "--continue-on-collection-errors", "--timeout=120", "--show-capture=no",
                   "--override-ini", "addopts=", "--junitxml=" + str(destination / "tests.xml"),
                   "--run-evidence=" + str(destination / "receipt.json"),
                   "--requirements-map=" + str(destination / "requirements-map.json"), "-q"]
        processes.append(subprocess.Popen(command))
    codes = [process.wait() for process in processes]
    print(json.dumps({"shard_exit_codes": codes, "manifest": "evidence/unit-shards.json"}))
    return int(any(codes))


if __name__ == "__main__":
    raise SystemExit(main())
