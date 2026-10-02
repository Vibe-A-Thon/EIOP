"""Common result contract for source connector synchronization."""

from __future__ import annotations

from dataclasses import dataclass

from eoip.contracts.source_event import SourceEvent


@dataclass(frozen=True)
class SyncBatch:
    events: list[SourceEvent]
    next_checkpoint: str
