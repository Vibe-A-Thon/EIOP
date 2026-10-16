"""Read-only local source connector with root confinement and size limits."""

from __future__ import annotations

import hashlib
from pathlib import Path

from eoip.contracts.source_event import SourceEvent

SUPPORTED_EXTENSIONS = {".py", ".ts", ".tsx"}
IGNORED_DIRECTORIES = {".git", ".venv", "node_modules", "__pycache__", "dist", "build"}


class LocalCodeConnector:
    mapper_version = "local-code/1.0"

    def __init__(self, max_file_bytes: int = 1_000_000, max_files: int = 5000) -> None:
        if max_file_bytes < 1 or max_files < 1:
            raise ValueError("file and count limits must be positive")
        self.max_file_bytes = max_file_bytes
        self.max_files = max_files

    def events(self, source_root: str | Path, repo_id: str) -> list[SourceEvent]:
        root = Path(source_root).resolve(strict=True)
        if not root.is_dir():
            raise ValueError("source root must be a directory")
        events = []
        for candidate in sorted(root.rglob("*")):
            if not candidate.is_file() or any(part in IGNORED_DIRECTORIES for part in candidate.parts):
                continue
            if candidate.suffix.casefold() not in SUPPORTED_EXTENSIONS:
                continue
            resolved = candidate.resolve(strict=True)
            try:
                relative_path = resolved.relative_to(root).as_posix()
            except ValueError as exc:
                raise ValueError("source path escapes the configured repository root") from exc
            size = resolved.stat().st_size
            if size > self.max_file_bytes:
                raise ValueError(f"source file exceeds the {self.max_file_bytes}-byte limit: {relative_path}")
            content = resolved.read_bytes().decode("utf-8")
            content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
            record_id = f"{repo_id}:{relative_path}"
            event_id = hashlib.sha256(f"git:{record_id}:{content_hash}".encode()).hexdigest()
            events.append(
                SourceEvent(
                    event_id=event_id,
                    source_system="git",
                    source_record_id=record_id,
                    source_version=content_hash,
                    payload_hash=content_hash,
                    payload={"repo_id": repo_id, "path": relative_path, "content": content},
                    metadata={"mapper_version": self.mapper_version},
                )
            )
            if len(events) > self.max_files:
                raise ValueError(f"repository exceeds the {self.max_files}-file limit")
        return events
