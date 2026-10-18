"""Run a verification command and emit a receipt. Usage:
python tools/acceptance/run_and_receipt.py --clause CRA-020.2 --profile P0 \\
    --artifact dist/eoip-*.whl --backend memory-harness -- python -m pytest tests/semantic/test_shacl_strict.py \\
    --junitxml {junit}
"""
from __future__ import annotations
import argparse, glob, hashlib, json, os, platform, subprocess, sys, uuid
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def source_fingerprint() -> tuple[str, str, bool]:
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    staged = subprocess.check_output(["git", "ls-files", "-s"], text=True)
    dirty = subprocess.check_output(["git", "status", "--porcelain"], text=True)
    h = hashlib.sha256(staged.encode("utf-8"))
    for line in sorted(dirty.splitlines()):
        path = line[3:]
        if os.path.isfile(path):
            h.update(path.encode("utf-8"))
            h.update(sha256_file(Path(path)).encode("utf-8"))
    return commit, h.hexdigest(), bool(dirty.strip())

def parse_junit(path: Path) -> dict:
    root = ET.parse(path).getroot()
    suites = [root] if root.tag == "testsuite" else list(root.iter("testsuite"))
    tot = {"tests_total": 0, "tests_failed": 0, "tests_errors": 0, "tests_skipped": 0}
    for s in suites:
        tot["tests_total"] += int(s.get("tests", 0))
        tot["tests_failed"] += int(s.get("failures", 0))
        tot["tests_errors"] += int(s.get("errors", 0))
        tot["tests_skipped"] += int(s.get("skipped", 0))
    xfailed = sum(
        1 for tc in root.iter("testcase")
        for sk in tc.findall("skipped")
        if "xfail" in (sk.get("type", "") + (sk.get("message") or "")).lower()
    )
    tot["tests_xfailed"] = xfailed
    tot["tests_passed"] = tot["tests_total"] - tot["tests_failed"] - tot["tests_errors"] - tot["tests_skipped"]
    return tot

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--clause", required=True)
    ap.add_argument("--profile", required=True, choices=["P0", "P1", "P2"])
    ap.add_argument("--artifact", required=True, help="glob of the built artifact actually exercised")
    ap.add_argument("--backend", required=True)
    ap.add_argument("--engine", default="")
    ap.add_argument("--engine-version", default="")
    ap.add_argument("--fixture", default="")
    ap.add_argument("cmd", nargs=argparse.REMAINDER)
    a = ap.parse_args()
    cmd = [c for c in a.cmd if c != "--"]
    run_id = f"run-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:8]}"
    ev_dir = Path(".audit-scratch/evidence") / a.clause / run_id
    ev_dir.mkdir(parents=True, exist_ok=True)
    junit = ev_dir / "junit.xml"
    new_cmd = []
    i = 0
    while i < len(cmd):
        c = cmd[i]
        if "{junit}" in c:
            new_cmd.append(c.replace("{junit}", str(junit).replace("\\", "/")))
        elif c in ("--junitxml", "--junit-xml"):
            new_cmd.append(c)
            if i + 1 < len(cmd) and not cmd[i + 1].startswith("-") and cmd[i + 1] != "":
                new_cmd.append(cmd[i + 1].replace("{junit}", str(junit).replace("\\", "/")))
                i += 1
            else:
                new_cmd.append(str(junit).replace("\\", "/"))
        else:
            new_cmd.append(c)
        i += 1
    if any("pytest" in arg for arg in new_cmd) and not any("--junit" in arg for arg in new_cmd):
        new_cmd.extend(["--junitxml", str(junit).replace("\\", "/")])
    cmd = new_cmd
    arts = sorted(glob.glob(a.artifact))
    if len(arts) != 1:
        print(f"expected exactly one artifact for {a.artifact}, found {arts}", file=sys.stderr)
        return 2
    artifact = Path(arts[0])
    commit0, fp0, dirty0 = source_fingerprint()
    started = datetime.now(timezone.utc)
    with (ev_dir / "stdout.txt").open("w", encoding="utf-8") as out, (ev_dir / "stderr.txt").open("w", encoding="utf-8") as err:
        rc = subprocess.call(cmd, stdout=out, stderr=err)
    completed = datetime.now(timezone.utc)
    commit1, fp1, dirty1 = source_fingerprint()
    results = parse_junit(junit) if junit.exists() else {
        "tests_total": 0,
        "tests_passed": 0,
        "tests_failed": 0,
        "tests_skipped": 0,
        "tests_xfailed": 0,
        "tests_errors": 0,
    }
    files = [
        {"path": str(p).replace("\\", "/"), "sha256": sha256_file(p)}
        for p in sorted(ev_dir.iterdir())
        if p.is_file()
    ]
    receipt = {
        "$schema": "https://eoip.enterprise.internal/schemas/verification-receipt-v3.json",
        "receipt_id": f"rcpt-{uuid.uuid4()}",
        "requirement_clause": a.clause,
        "state_claimed": "VERIFIED",
        "profile": a.profile,
        "source_commit": commit0,
        "source_tree_dirty": dirty0 or dirty1,
        "source_fingerprint": fp0,
        "source_unchanged_during_run": (commit0, fp0) == (commit1, fp1),
        "artifact_digest": sha256_file(artifact),
        "artifact_path": str(artifact).replace("\\", "/"),
        "artifact_mtime": datetime.fromtimestamp(artifact.stat().st_mtime, timezone.utc).isoformat(),
        "runtime": {
            "os": platform.platform(),
            "python_version": platform.python_version(),
            "backend": a.backend,
            "engine": a.engine,
            "engine_version": a.engine_version,
        },
        "fixture": {"id": a.fixture},
        "execution": {
            "command": cmd,
            "exit_code": rc,
            "started_at": started.isoformat(),
            "completed_at": completed.isoformat(),
        },
        "results": results,
        "evidence_files": files,
        "verified_invariants": [],
        "negative_cases": [],
        "evidence_categories": {},
        "limitations": [],
        "producer": os.environ.get("EOIP_AGENT_ID", "antigravity-agent"),
        "reviewer": None,
        "review_signature": None,
    }
    out = Path(".audit-scratch/receipts") / a.clause / f"{run_id}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(out)
    return rc

if __name__ == "__main__":
    sys.exit(main())
