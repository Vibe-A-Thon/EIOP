"""Common result contract for source connector synchronization."""

from __future__ import annotations

from dataclasses import dataclass

from eoip.contracts.source_event import SourceEvent, SourceEventV2


@dataclass(frozen=True)
class SyncBatch:
    events: list[SourceEvent | SourceEventV2]
    next_checkpoint: str
