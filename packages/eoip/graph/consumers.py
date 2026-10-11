"""Durable local consumers for semantic change events (G2-T0242)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Protocol

from eoip.contracts.source_event import utc_now_iso
from eoip.graph.evolution import ChangeJournal, SemanticChangeEvent
from eoip.graph.store import GraphStore
from eoip.jobs import write_json
from eoip.validation.engine import ValidationEngine


class SemanticEventConsumer(Protocol):
    name: str

    def consume(self, events: list[SemanticChangeEvent]) -> None: ...


class QualityRecalculationConsumer:
    name = "quality-recalculation"

    def __init__(self, store: GraphStore, output: str | Path) -> None:
        self.validator = ValidationEngine(store)
        self.output = Path(output)

    def consume(self, events: list[SemanticChangeEvent]) -> None:
        if events:
            write_json(self.output, self.validator.run())


class CacheInvalidationConsumer:
    name = "semantic-cache-invalidation"

    def __init__(self, output: str | Path) -> None:
        self.output = Path(output)

    def consume(self, events: list[SemanticChangeEvent]) -> None:
        write_json(
            self.output,
            {
                "invalidated_at": utc_now_iso(),
                "through_cursor": events[-1].cursor,
                "graph_versions": sorted({event.graph_version for event in events}),
                "targets": sorted({event.target_id for event in events}),
            },
        )


class AdminTimelineConsumer:
    name = "admin-timeline"

    def __init__(self, output: str | Path, *, limit: int = 500) -> None:
        self.output = Path(output)
        self.limit = limit

    def consume(self, events: list[SemanticChangeEvent]) -> None:
        existing = []
        if self.output.exists():
            document = json.loads(self.output.read_text(encoding="utf-8"))
            existing = document.get("events", [])
        merged = (existing + [event.model_dump(mode="json") for event in events])[-self.limit :]
        write_json(self.output, {"updated_at": utc_now_iso(), "events": merged})


class SemanticConsumerRunner:
    def __init__(self, journal: ChangeJournal, state_root: str | Path) -> None:
        self.journal = journal
        self.state_root = Path(state_root)
        self._consumers: list[SemanticEventConsumer] = []

    def register(self, consumer: SemanticEventConsumer) -> None:
        if any(item.name == consumer.name for item in self._consumers):
            raise ValueError(f"duplicate semantic consumer: {consumer.name}")
        self._consumers.append(consumer)

    def run_once(self, *, batch_size: int = 1000) -> dict[str, dict]:
        results = {}
        for consumer in self._consumers:
            checkpoint_path = self.state_root / f"{consumer.name}.json"
            checkpoint = (
                json.loads(checkpoint_path.read_text(encoding="utf-8"))
                if checkpoint_path.exists()
                else {}
            )
            after = int(checkpoint.get("cursor", 0))
            events = self.journal.read(after=after, limit=batch_size)
            if events:
                try:
                    consumer.consume(events)
                    checkpoint = {
                        "consumer": consumer.name,
                        "cursor": events[-1].cursor,
                        "processed": int(checkpoint.get("processed", 0)) + len(events),
                        "status": "HEALTHY",
                        "updated_at": utc_now_iso(),
                    }
                except Exception as exc:
                    checkpoint = {
                        "consumer": consumer.name,
                        "cursor": after,
                        "processed": int(checkpoint.get("processed", 0)),
                        "status": "FAILED",
                        "error": str(exc),
                        "updated_at": utc_now_iso(),
                    }
                write_json(checkpoint_path, checkpoint)
            else:
                checkpoint = {
                    "consumer": consumer.name,
                    "cursor": after,
                    "processed": int(checkpoint.get("processed", 0)),
                    "status": "HEALTHY",
                    "updated_at": checkpoint.get("updated_at"),
                }
            results[consumer.name] = checkpoint
        return results


def run_default_consumers(store: GraphStore, data_root: str | Path) -> dict[str, dict]:
    root = Path(data_root)
    runner = SemanticConsumerRunner(
        ChangeJournal(root / "journal" / "semantic-changes.ndjson"),
        root / "state" / "event-consumers",
    )
    runner.register(QualityRecalculationConsumer(store, root / "state" / "validation.json"))
    runner.register(CacheInvalidationConsumer(root / "state" / "semantic-cache.json"))
    runner.register(AdminTimelineConsumer(root / "state" / "admin-timeline.json"))
    return runner.run_once()
