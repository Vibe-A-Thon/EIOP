"""Installed-package registry (GAP-MKT-006, GAP-MKT-008).

In-memory registry with optional JSON persistence. Tracks installed packages
(name → manifest + install metadata) and supports list/search plus simple
name/capability lookups used by the dependency resolver.
"""

from __future__ import annotations

import json
import threading
from datetime import datetime, timezone
from pathlib import Path

from eoip.marketplace.manifest import CapabilityKind, PackageManifest


class InstalledRecord:
    """An installed package entry in the registry."""

    def __init__(self, manifest: PackageManifest, installed_at: str | None = None) -> None:
        self.manifest = manifest
        self.installed_at = installed_at or datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> dict:
        return {
            "manifest": self.manifest.model_dump(mode="json"),
            "installed_at": self.installed_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "InstalledRecord":
        return cls(
            manifest=PackageManifest.model_validate(data["manifest"]),
            installed_at=data.get("installed_at"),
        )


class PackageRegistry:
    """Registry of installed packages; optionally JSON-persisted (GAP-MKT-008)."""

    def __init__(self, path: str | Path | None = None) -> None:
        self._lock = threading.Lock()
        self._path = Path(path) if path else None
        self._records: dict[str, InstalledRecord] = {}
        if self._path and self._path.exists():
            self._load()

    @property
    def path(self) -> Path | None:
        return self._path

    def _load(self) -> None:
        data = json.loads(self._path.read_text(encoding="utf-8"))
        for name, record in data.get("packages", {}).items():
            self._records[name] = InstalledRecord.from_dict(record)

    def _persist(self) -> None:
        if not self._path:
            return
        self._path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "packages": {name: rec.to_dict() for name, rec in sorted(self._records.items())}
        }
        tmp = self._path.with_suffix(self._path.suffix + ".tmp")
        tmp.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
        tmp.replace(self._path)

    # -- mutation -----------------------------------------------------------

    def install(self, manifest: PackageManifest) -> InstalledRecord:
        with self._lock:
            record = InstalledRecord(manifest)
            self._records[manifest.name] = record
            self._persist()
            return record

    def uninstall(self, name: str) -> bool:
        with self._lock:
            removed = self._records.pop(name, None) is not None
            if removed:
                self._persist()
            return removed

    # -- queries ------------------------------------------------------------

    def get(self, name: str) -> InstalledRecord | None:
        return self._records.get(name)

    def is_installed(self, name: str) -> bool:
        return name in self._records

    def installed_version(self, name: str) -> str | None:
        record = self._records.get(name)
        return record.manifest.version if record else None

    def list(self) -> list[InstalledRecord]:
        return [self._records[name] for name in sorted(self._records)]

    def search(self, query: str) -> list[InstalledRecord]:
        """Substring search over name and description (GAP-MKT-008)."""

        needle = query.lower().strip()
        if not needle:
            return self.list()
        return [
            record
            for record in self.list()
            if needle in record.manifest.name.lower()
            or needle in record.manifest.description.lower()
        ]

    def providers_of(self, kind: CapabilityKind) -> list[InstalledRecord]:
        return [
            record
            for record in self.list()
            if record.manifest.provides.get(kind)
        ]
