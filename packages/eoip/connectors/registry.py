"""Durable, local source registry with atomic writes and no stored secret values."""

from __future__ import annotations

import json
import os
import threading
from pathlib import Path
from typing import Any

from eoip.contracts.source_event import utc_now_iso
from eoip.contracts.source_registry import SourceRegistryEntry


class SourceAlreadyExistsError(ValueError):
    pass


class SourceNotFoundError(KeyError):
    pass


class SourceRegistry:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self._lock = threading.RLock()

    def list(self) -> list[SourceRegistryEntry]:
        with self._lock:
            entries = self._read()
            return [entries[key] for key in sorted(entries)]

    def get(self, source_id: str) -> SourceRegistryEntry:
        with self._lock:
            try:
                return self._read()[source_id]
            except KeyError as exc:
                raise SourceNotFoundError(source_id) from exc

    def create(self, entry: SourceRegistryEntry) -> SourceRegistryEntry:
        with self._lock:
            entries = self._read()
            if entry.source_id in entries:
                raise SourceAlreadyExistsError(entry.source_id)
            entries[entry.source_id] = entry
            self._write(entries)
            return entry

    def update(self, source_id: str, changes: dict[str, Any]) -> SourceRegistryEntry:
        immutable = {"schema_version", "source_id", "created_at"}
        if immutable.intersection(changes):
            raise ValueError("schema_version, source_id and created_at are immutable")
        with self._lock:
            entries = self._read()
            if source_id not in entries:
                raise SourceNotFoundError(source_id)
            current = entries[source_id]
            updated = SourceRegistryEntry.model_validate(
                {**current.model_dump(mode="json"), **changes, "updated_at": utc_now_iso()}
            )
            entries[source_id] = updated
            self._write(entries)
            return updated

    def delete(self, source_id: str) -> SourceRegistryEntry:
        with self._lock:
            entries = self._read()
            try:
                removed = entries.pop(source_id)
            except KeyError as exc:
                raise SourceNotFoundError(source_id) from exc
            self._write(entries)
            return removed

    def _read(self) -> dict[str, SourceRegistryEntry]:
        if not self.path.exists():
            return {}
        document = json.loads(self.path.read_text(encoding="utf-8"))
        if not isinstance(document, dict) or document.get("schema_version") != "1.0":
            raise ValueError("unsupported or invalid source registry document")
        raw_entries = document.get("sources")
        if not isinstance(raw_entries, list):
            raise TypeError("source registry sources must be a list")
        entries = [SourceRegistryEntry.model_validate(item) for item in raw_entries]
        if len({entry.source_id for entry in entries}) != len(entries):
            raise ValueError("source registry contains duplicate source_id values")
        return {entry.source_id: entry for entry in entries}

    def _write(self, entries: dict[str, SourceRegistryEntry]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        document = {
            "schema_version": "1.0",
            "sources": [entries[key].model_dump(mode="json") for key in sorted(entries)],
        }
        temporary = self.path.with_name(f".{self.path.name}.{os.getpid()}.tmp")
        temporary.write_text(
            json.dumps(document, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        os.replace(temporary, self.path)
