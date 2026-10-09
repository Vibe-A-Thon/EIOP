"""Behavioral evidence registry and pytest collector (SR-QA-010).

SR-QA-010: every ``SR-`` requirement maps to >= 1 executable acceptance test,
the mapping is stored as structured data, and references in comments or
docstrings never count as evidence.

The prior gate in ``eoip.gaps.coverage`` scanned source text for requirement
IDs, so a docstring mentioning ``SR-QA-010`` was indistinguishable from a real
test.  The registry here only records *explicit* entries: a test declares its
covered requirement IDs either via the ``eoip_requirement`` marker::

    @pytest.mark.eoip_requirement("SR-QA-010")
    def test_mapping_is_structured_data(): ...

or via an explicit runtime call::

    from eoip.qa import record_requirement
    def test_something():
        record_requirement("SR-QA-010")
        ...

Both paths land in the same collector JSON.  Nothing in this module ever
reads docstrings or comments.
"""

from __future__ import annotations

import json
import os
import re
import threading
from dataclasses import dataclass, field
from pathlib import Path

REQ_ID_RE = re.compile(r"^[A-Z][A-Z0-9]*-[A-Z0-9-]+-\d{3}$")
COLLECTOR_ENV_VAR = "EOIP_QA_COLLECTOR_OUT"
_current: list[str] = []
_current_lock = threading.Lock()


def requirement_ids_valid(ids: list[str]) -> list[str]:
    bad = [i for i in ids if not REQ_ID_RE.match(i)]
    if bad:
        raise ValueError(f"Invalid requirement IDs: {bad}")
    return ids


@dataclass
class EvidenceEntry:
    """One explicit requirement -> test mapping (structured data only)."""

    requirement_id: str
    test_id: str
    source: str = "marker"  # "marker" | "call" | "manual"
    recorded_at: str = ""

    def to_dict(self) -> dict:
        return {
            "requirement_id": self.requirement_id,
            "test_id": self.test_id,
            "source": self.source,
            "recorded_at": self.recorded_at,
        }


@dataclass
class CoverageResult:
    """Requirement coverage query result."""

    requirement_id: str
    test_ids: list[str] = field(default_factory=list)

    @property
    def covered(self) -> bool:
        return bool(self.test_ids)

    def to_dict(self) -> dict:
        return {
            "requirement_id": self.requirement_id,
            "covered": self.covered,
            "test_ids": sorted(self.test_ids),
        }


class BehavioralEvidenceRegistry:
    """JSON-file registry of requirement -> test mappings (SR-QA-010)."""

    def __init__(self, path: str | Path | None = None) -> None:
        self._lock = threading.RLock()
        self._path = Path(path) if path else Path(
            os.getenv("EOIP_DATA_DIR", ".data")
        ) / "state" / "qa-behavioral-evidence.json"
        self._entries: dict[str, EvidenceEntry] = {}
        self._load()

    @property
    def path(self) -> Path:
        return self._path

    def _load(self) -> None:
        if not self._path.exists():
            return
        data = json.loads(self._path.read_text(encoding="utf-8"))
        for item in data.get("entries", []):
            entry = EvidenceEntry(**item)
            self._entries[(entry.requirement_id, entry.test_id)] = entry

    def _save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"entries": [e.to_dict() for e in sorted(
            self._entries.values(),
            key=lambda e: (e.requirement_id, e.test_id),
        )]}
        self._path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    def register(self, requirement_id: str, test_id: str, *, source: str = "manual",
                 recorded_at: str = "") -> EvidenceEntry:
        """Explicitly record that ``test_id`` covers ``requirement_id``.

        This is the ONLY way evidence enters the registry — text references
        are never scanned (SR-QA-010; lesson from eoip.gaps.coverage's
        literal string matcher).
        """
        requirement_ids_valid([requirement_id])
        with self._lock:
            entry = EvidenceEntry(requirement_id=requirement_id, test_id=test_id,
                                  source=source, recorded_at=recorded_at)
            self._entries[(requirement_id, test_id)] = entry
            self._save()
            return entry

    def unregister(self, requirement_id: str, test_id: str) -> bool:
        with self._lock:
            removed = self._entries.pop((requirement_id, test_id), None) is not None
            if removed:
                self._save()
            return removed

    def coverage(self, requirement_id: str) -> CoverageResult:
        with self._lock:
            tests = sorted(
                e.test_id for e in self._entries.values() if e.requirement_id == requirement_id
            )
        return CoverageResult(requirement_id=requirement_id, test_ids=tests)

    def coverage_report(self, requirement_ids: list[str] | None = None) -> dict:
        with self._lock:
            by_req: dict[str, set[str]] = {}
            for e in self._entries.values():
                by_req.setdefault(e.requirement_id, set()).add(e.test_id)
        if requirement_ids is None:
            requirement_ids = sorted(by_req)
        else:
            requirement_ids_valid(list(requirement_ids))
        results = [
            CoverageResult(req_id, sorted(by_req.get(req_id, set()))).to_dict()
            for req_id in requirement_ids
        ]
        covered = sum(1 for r in results if r["covered"])
        return {
            "total_requirements": len(results),
            "requirements_with_behavioral_evidence": covered,
            "requirements_without_behavioral_evidence": len(results) - covered,
            # SR-QA-010 gate semantics: uncovered requirements are blockers.
            "gate_passed": len(results) - covered == 0,
            "requirements": results,
        }

    def all_entries(self) -> list[EvidenceEntry]:
        with self._lock:
            return sorted(self._entries.values(), key=lambda e: (e.requirement_id, e.test_id))

    def merge(self, entries: list[EvidenceEntry]) -> int:
        with self._lock:
            for entry in entries:
                self._entries[(entry.requirement_id, entry.test_id)] = entry
            self._save()
            return len(entries)


def record_requirement(requirement_id: str) -> None:
    """Explicit runtime declaration of a covered requirement (SR-QA-010).

    Call from inside a test; the pytest plugin (``eoip.qa.pytest_plugin``)
    attaches the declaration to the running test item at teardown and writes
    it to the collector output.  Falls back to a thread-local buffer when the
    plugin is not active (e.g. ad-hoc scripts).
    """
    requirement_ids_valid([requirement_id])
    with _current_lock:
        _current.append(requirement_id)


def drain_recorded_requirements() -> list[str]:
    with _current_lock:
        ids = list(_current)
        _current.clear()
        return ids


class RunCollector:
    """Collects explicit requirement declarations from a pytest run.

    Used by the pytest plugin: for every executed test it gathers marker
    declarations (``@pytest.mark.eoip_requirement("SR-...")``) and runtime
    ``record_requirement`` calls, then writes a structured mapping JSON that
    can be merged into a :class:`BehavioralEvidenceRegistry`.
    """

    def __init__(self) -> None:
        self.records: list[EvidenceEntry] = []

    def record_test(self, test_id: str, marker_ids: list[str], call_ids: list[str],
                    recorded_at: str = "") -> None:
        for req_id in dict.fromkeys([*marker_ids, *call_ids]):
            source = "marker" if req_id in marker_ids else "call"
            self.records.append(EvidenceEntry(
                requirement_id=req_id, test_id=test_id, source=source,
                recorded_at=recorded_at,
            ))

    def write(self, path: str | Path) -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        payload = {"entries": [e.to_dict() for e in self.records]}
        out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
        return out

    def merge_into(self, registry: BehavioralEvidenceRegistry) -> int:
        return registry.merge(self.records)


def load_collector_entries(path: str | Path) -> list[EvidenceEntry]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return [EvidenceEntry(**item) for item in data.get("entries", [])]
