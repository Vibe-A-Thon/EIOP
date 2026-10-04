"""Execute a local command and persist conservative source-bound evidence.

Run as a module from the repository root. Command arguments must not contain
credentials; neither environment values nor child output are stored in receipts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import time
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from eoip.jobs import write_json

SCOPE_EXCLUSIONS = {
    "eoip-engg-doc-pkg/kgr-requirements.md",
    "eoip-engg-doc-pkg/kgr-implementation-plan.md",
}
RUNTIME_DIRECTORIES = {
    ".git", ".venv", "venv", "env", "node_modules", "__pycache__",
    ".pytest_cache", ".ruff_cache", "test-results", "build", "dist",
    ".data", ".cache", "runtime", "volumes", "raw", "state",
    "checkpoints", "dlq", "backups", "exports", "model-cache",
}


def _protected(path: Path) -> bool:
    parts = [part.casefold() for part in path.parts]
    return (
        path.as_posix().casefold() in SCOPE_EXCLUSIONS
        or any(part in {".git", "secrets", "secrets.example"} for part in parts)
        or any(part == ".env" or part.startswith(".env.") or part == ".envrc" for part in parts)
    )


def _git(root: Path, *arguments: str) -> str:
    return subprocess.run(
        ["git", "-C", str(root), *arguments], check=True,
        capture_output=True, encoding="utf-8",
    ).stdout


def _hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def capture_source(project_root: Path, *, excluded_paths: Sequence[Path] = ()) -> dict[str, Any]:
    root = Path(project_root).resolve()
    if Path(_git(root, "rev-parse", "--show-toplevel").strip()).resolve() != root:
        raise ValueError("project root must be the Git repository root")
    excluded = {path.relative_to(root).as_posix() for path in excluded_paths}
    names = set(_git(root, "ls-files", "-z", "--cached", "--others", "--exclude-standard").split("\0"))
    files: dict[str, dict[str, str]] = {}
    for name in sorted(names - {""}):
        relative = Path(name)
        if (
            name in excluded or _protected(relative)
            or any(part.casefold() in RUNTIME_DIRECTORIES for part in relative.parts)
        ):
            continue
        path = root / relative
        if any(parent.is_symlink() for parent in path.parents if parent != root):
            raise ValueError(f"source has a symlink ancestor: {name}")
        if path.is_symlink():
            files[name] = {
                "kind": "symlink",
                "sha256": hashlib.sha256(str(path.readlink()).encode("utf-8")).hexdigest(),
            }
        elif path.is_file():
            files[name] = {"kind": "file", "sha256": _hash(path)}
        elif not path.exists():
            files[name] = {"kind": "missing"}
        else:
            raise ValueError(f"source is not a regular file: {name}")
    canonical = json.dumps(files, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return {
        "git_head": _git(root, "rev-parse", "HEAD").strip(),
        "working_tree_dirty": bool(_git(root, "status", "--porcelain", "-z")),
        "files": files,
        "fingerprint_sha256": hashlib.sha256(canonical).hexdigest(),
    }


def _output_path(root: Path, path: Path, tracked: set[str]) -> Path:
    path = path if path.is_absolute() else root / path
    if path.is_symlink() or not path.resolve().is_relative_to(root):
        raise ValueError("receipt/artifact must be inside the repository without a symlink escape")
    path = path.resolve()
    relative = path.relative_to(root)
    if _protected(relative) or relative.as_posix().casefold() in {name.casefold() for name in tracked}:
        raise ValueError("receipt/artifact cannot overwrite protected or Git-tracked source")
    if path.exists() and not path.is_file():
        raise ValueError("receipt/artifact must be a regular file")
    return path


def _artifact_state(path: Path, root: Path) -> dict[str, Any] | None:
    if path.is_symlink() or not path.resolve().is_relative_to(root):
        raise ValueError("artifact changed to a symlink or escaped the repository")
    if not path.exists():
        return None
    if not path.is_file():
        raise ValueError("artifact is not a regular file")
    stat = path.stat()
    return {
        "sha256": _hash(path), "mtime_ns": stat.st_mtime_ns,
        "ctime_ns": stat.st_ctime_ns, "size": stat.st_size,
    }


def validate_command(
    project_root: Path,
    command: Sequence[str],
    *,
    output: Path,
    artifacts: Sequence[Path] = (),
    timeout: float | None = None,
) -> dict[str, Any]:
    if not command or any(not isinstance(argument, str) or not argument for argument in command):
        raise ValueError("an explicit nonempty command argument vector is required")
    if timeout is not None and timeout <= 0:
        raise ValueError("timeout must be positive")
    root = Path(project_root).resolve()
    tracked = set(_git(root, "ls-files", "-z").split("\0"))
    output = _output_path(root, Path(output), tracked)
    artifact_paths = [_output_path(root, Path(path), tracked) for path in artifacts]
    if len(set(artifact_paths)) != len(artifact_paths) or output in artifact_paths:
        raise ValueError("receipt and required artifacts must have distinct paths")
    excluded = [output, *artifact_paths]
    before = capture_source(root, excluded_paths=excluded)
    old_artifacts = {str(path): _artifact_state(path, root) for path in artifact_paths}
    started_at = datetime.now(UTC).isoformat()
    started_ns = time.time_ns()
    exit_code: int | None = None
    errors: list[str] = []
    execution_error: str | None = None
    try:
        exit_code = subprocess.run(list(command), cwd=root, timeout=timeout, check=False, shell=False).returncode
    except (OSError, subprocess.TimeoutExpired) as exc:
        execution_error = type(exc).__name__
        errors.append(f"command execution failed: {execution_error}")
    if exit_code is not None and exit_code != 0:
        errors.append(f"command exited with code {exit_code}")
    after: dict[str, Any] | None = None
    try:
        tracked = set(_git(root, "ls-files", "-z").split("\0"))
        after = capture_source(root, excluded_paths=excluded)
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        errors.append(f"post-command source capture failed: {type(exc).__name__}")
    unchanged = bool(
        after is not None and before["git_head"] == after["git_head"]
        and before["files"] == after["files"]
    )
    if not unchanged:
        errors.append("source inventory, contents or Git HEAD changed during execution")
    artifact_receipts: dict[str, Any] = {}
    for path in artifact_paths:
        key = str(path)
        try:
            _output_path(root, path, tracked)
            state = _artifact_state(path, root)
        except (OSError, ValueError) as exc:
            errors.append(f"artifact inspection failed for {key}: {type(exc).__name__}")
            continue
        fresh = bool(state and state != old_artifacts[key] and state["mtime_ns"] >= started_ns)
        artifact_receipts[key] = {**(state or {}), "fresh": fresh, "present": state is not None}
        if not fresh:
            errors.append(f"required artifact is missing or stale: {key}")
    artifacts_fresh = all(
        artifact_receipts.get(str(path), {}).get("fresh", False) for path in artifact_paths
    )
    receipt = {
        "schema_version": "1.0",
        "status": "FAIL" if errors else "PASS",
        "command": list(command), "command_exit_code": exit_code,
        "execution_error": execution_error, "started_at": started_at,
        "completed_at": datetime.now(UTC).isoformat(),
        "source_before": before, "source_after": after,
        "source_unchanged": unchanged, "source_content_bound": unchanged,
        "source_revision_bound": bool(
            unchanged and after is not None
            and not before["working_tree_dirty"] and not after["working_tree_dirty"]
        ),
        "artifacts": artifact_receipts, "artifacts_fresh": artifacts_fresh,
        "errors": errors,
        "limitations": [
            "Command success is not requirement completeness or live integration certification",
            "Inventory covers Git tracked and nonignored untracked files only",
            "Runtime/dependency directories, secret paths, environment files and KGR exclusions are not read",
            "Receipt and declared artifacts are excluded from source fingerprints",
            "Dirty worktrees are content-bound, not immutable revision-bound",
            "Before/after snapshots do not detect transient edits reverted during execution",
            "Command arguments must not contain credentials; environment and child output are not persisted",
        ],
    }
    # Recheck the destination after the child; it must not redirect the receipt.
    output = _output_path(root, output, tracked)
    write_json(output, receipt)
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--artifact", type=Path, action="append", default=[])
    parser.add_argument("--timeout", type=float)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    arguments = parser.parse_args()
    command = arguments.command
    if command[:1] == ["--"]:
        command = command[1:]
    try:
        receipt = validate_command(
            arguments.project_root, command, output=arguments.output,
            artifacts=arguments.artifact, timeout=arguments.timeout,
        )
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        parser.exit(2, f"Validation setup/receipt failure: {type(exc).__name__}: {exc}\n")
    print(f"Validation {receipt['status']}; receipt: {arguments.output}")
    if receipt["status"] != "PASS":
        for error in receipt["errors"]:
            print(error)
        code = receipt["command_exit_code"]
        raise SystemExit(code if isinstance(code, int) and 1 <= code <= 125 else 1)


if __name__ == "__main__":
    main()