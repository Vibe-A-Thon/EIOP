"""Durable, replayable agent traces that intentionally exclude hidden reasoning."""

from __future__ import annotations

import json
import os
from hashlib import sha256
from pathlib import Path
from threading import RLock

from eoip.contracts.agent import AgentExecutionTrace


class AgentTraceStore:
    def __init__(self, root: str | Path | None = None) -> None:
        data_root = Path(root) if root else Path(os.getenv("EOIP_DATA_DIR", ".data"))
        self._root = data_root / "agent-traces"
        self._lock = RLock()

    def save(self, trace: AgentExecutionTrace) -> None:
        self._root.mkdir(parents=True, exist_ok=True)
        path = self._path(trace.run_id)
        temporary = path.with_suffix(".tmp")
        payload = trace.model_dump_json(indent=2)
        with self._lock:
            temporary.write_text(payload, encoding="utf-8")
            temporary.replace(path)

    def get(self, run_id: str) -> AgentExecutionTrace | None:
        path = self._path(run_id)
        if not path.is_file():
            return None
        return AgentExecutionTrace.model_validate_json(path.read_text(encoding="utf-8"))

    def replay(self, run_id: str) -> list[dict]:
        trace = self.get(run_id)
        return [] if trace is None else [event.model_dump() for event in trace.events]

    def list(self, *, limit: int = 100) -> list[AgentExecutionTrace]:
        if not self._root.exists():
            return []
        traces: list[AgentExecutionTrace] = []
        for path in sorted(self._root.glob("*.json"), reverse=True)[:limit]:
            try:
                traces.append(AgentExecutionTrace.model_validate(json.loads(path.read_text("utf-8"))))
            except (OSError, ValueError, json.JSONDecodeError):
                continue
        return traces

    def _path(self, run_id: str) -> Path:
        """Hash untrusted run identifiers so they cannot influence filesystem paths."""
        name = sha256(run_id.encode("utf-8")).hexdigest()
        return self._root / f"{name}.json"
