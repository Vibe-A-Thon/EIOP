"""Run one audit check with isolated runtime paths and redacted retained output."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import secrets
import shutil
import subprocess
import sys
import tempfile
from datetime import UTC, datetime
from pathlib import Path

from redact_sensitive import redact


def run(root: Path, out: Path, command: list[str], timeout: int) -> int:
    out.mkdir(parents=True, exist_ok=True)
    command = [sys.executable if part == "{python}" else part for part in command]
    command[0] = shutil.which(command[0]) or command[0]
    before = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    started = datetime.now(UTC).isoformat()
    with tempfile.TemporaryDirectory(prefix="eoip-audit-runtime-") as temporary:
        env = os.environ.copy()
        env.update({
            "EOIP_DATA_DIR": str(Path(temporary) / "data"),
            "EOIP_ASG_FILE": str(Path(temporary) / "empty.keys"),
            "EOIP_GRAPH_BACKEND": "memory", "EOIP_API_TOKEN": secrets.token_urlsafe(32),
            "REVA_ENABLED": "false", "PYTHONUTF8": "1",
            "PYTHONPATH": os.pathsep.join((str(root), str(root / "packages"))),
            "COVERAGE_FILE": str(out / ".coverage"),
        })
        with tempfile.TemporaryFile(mode="w+b") as log:
            process = None
            try:
                process = subprocess.Popen(command, cwd=root, env=env, stdout=log, stderr=subprocess.STDOUT)
                code = process.wait(timeout=timeout)
            except subprocess.TimeoutExpired:
                if process is not None:
                    if os.name == "nt":
                        subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"],
                                       capture_output=True, check=False)
                    else:
                        process.kill()
                    process.wait(timeout=20)
                code = 124
            except OSError:
                code = 127
            log.seek(0)
            raw = log.read().decode("utf-8", errors="replace")
        safe, redactions = redact(raw)
        safe = safe.replace(env["EOIP_API_TOKEN"], "[REDACTED_RUNTIME_CREDENTIAL]")
    (out / "output.txt").write_text(safe, encoding="utf-8")
    (out / "redaction.json").write_text(json.dumps({"count": len(redactions), "hits": redactions}, indent=2), encoding="utf-8")
    changes = subprocess.check_output(["git", "-c", "core.safecrlf=false", "diff", "--name-only", "HEAD"],
                                      cwd=root, text=True, stderr=subprocess.DEVNULL).splitlines()
    receipt = {
        "git_commit": before, "started_at": started, "finished_at": datetime.now(UTC).isoformat(),
        "command": command, "cwd": str(root), "exit_code": code,
        "status": "passed" if code == 0 else "blocked" if code == 127 else "failed",
        "platform": platform.platform(), "python": sys.version.split()[0],
        "tracked_files_changed": changes, "redacted_output_sha256": hashlib.sha256(safe.encode()).hexdigest(),
        "limitations": ["A process exit code alone does not establish per-requirement completion."],
    }
    (out / "execution.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: receipt[key] for key in ("git_commit", "status", "exit_code", "tracked_files_changed")}))
    print(f"Redacted evidence: {out}")
    return code


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=1800)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        parser.error("A command after -- is required")
    return run(args.repo_root.resolve(), args.out.resolve(), command, args.timeout)


if __name__ == "__main__":
    raise SystemExit(main())
