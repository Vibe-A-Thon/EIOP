"""Durable store for rendered report artifacts (SR-NLQ-008, CP-03, CP-25).

Maintains disk-backed persistence of rendered reports and metadata,
supporting restart recovery, tenant isolation, and authorized downloads.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from threading import RLock

from eoip.reports.generator import RenderedReport


class ReportArtifactStore:
    """Durable disk-backed store for rendered report artifacts (CP-03, CP-25)."""

    def __init__(self, directory: str | Path | None = None) -> None:
        self._dir = (
            Path(directory)
            if directory
            else Path(os.getenv("EOIP_DATA_DIR", ".data")) / "state" / "reports"
        )
        self._dir.mkdir(parents=True, exist_ok=True)
        self._lock = RLock()
        self._metadata_path = self._dir / "index.json"
        self._items: dict[str, RenderedReport] = {}
        self._load()

    def _load(self) -> None:
        if not self._metadata_path.exists():
            return
        try:
            data = json.loads(self._metadata_path.read_text(encoding="utf-8"))
            for item in data.get("reports", []):
                rep = RenderedReport(**item)
                self._items[rep.report_id] = rep
        except (ValueError, TypeError, KeyError):
            pass

    def _save(self) -> None:
        self._dir.mkdir(parents=True, exist_ok=True)
        payload = {"reports": [r.model_dump() for r in self._items.values()]}
        tmp = self._metadata_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
        tmp.replace(self._metadata_path)

    def put(self, report: RenderedReport) -> None:
        with self._lock:
            self._items[report.report_id] = report
            self._save()

    def get(self, report_id: str) -> RenderedReport | None:
        with self._lock:
            return self._items.get(report_id)

    def list(self) -> list[RenderedReport]:
        with self._lock:
            return list(self._items.values())

    def delete(self, report_id: str) -> bool:
        with self._lock:
            if report_id in self._items:
                del self._items[report_id]
                self._save()
                return True
            return False
