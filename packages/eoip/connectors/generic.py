"""Generic web and local-file connectors using the common SourceEvent v2 contract."""

from __future__ import annotations

import hashlib
import mimetypes
from collections.abc import Iterable, Iterator
from pathlib import Path

from eoip.connectors.base import (
    ConnectorHealth,
    DiscoveredResource,
    DiscoveryResult,
    DiscoveryScope,
)
from eoip.connectors.crawler import ControlledWebCrawler
from eoip.contracts.source_event import SourceEventV2, utc_now_iso
from eoip.contracts.source_registry import SourceCapabilities
from pydantic import BaseModel, ConfigDict, Field


class LocalFileScope(BaseModel):
    model_config = ConfigDict(extra="forbid")

    roots: list[str] = Field(min_length=1, max_length=100)
    suffixes: list[str] = Field(
        default_factory=lambda: [".md", ".txt", ".json", ".yaml", ".yml"], max_length=100
    )
    max_files: int = Field(default=10_000, ge=1, le=1_000_000)
    max_file_bytes: int = Field(default=5_000_000, ge=1, le=100_000_000)


class WebSourceConnector:
    def __init__(self, source_id: str, crawler: ControlledWebCrawler) -> None:
        self.source_id = source_id
        self.crawler = crawler

    def capabilities(self) -> SourceCapabilities:
        return SourceCapabilities(polling=True, reconciliation=True)

    def discover(self, scope: DiscoveryScope) -> DiscoveryResult:
        del scope
        resources = [
            DiscoveredResource(
                resource_id=url,
                resource_type="web-root",
                name=url,
                metadata={"allowed_hosts": self.crawler.scope.allowed_hosts},
            )
            for url in self.crawler.scope.start_urls
        ]
        return DiscoveryResult(source_id=self.source_id, resources=resources)

    def baseline(self, checkpoint: str | None = None) -> Iterator[SourceEventV2]:
        del checkpoint
        return iter(self.crawler.crawl())

    def poll_changes(self, checkpoint: str) -> Iterator[SourceEventV2]:
        del checkpoint
        return iter(self.crawler.crawl())

    def handle_event(self, event: dict) -> Iterator[SourceEventV2]:
        del event
        return iter(())

    def fetch_record(self, ref: str) -> SourceEventV2:
        scope = self.crawler.scope.model_copy(update={"start_urls": [ref], "max_depth": 0, "page_limit": 1})
        crawler = ControlledWebCrawler(
            self.source_id,
            scope,
            client=self.crawler._client,
            resolver=self.crawler._resolver,
            sleeper=self.crawler._sleeper,
            clock=self.crawler._clock,
        )
        events = crawler.crawl()
        if not events:
            raise LookupError(ref)
        return events[0]

    def health(self) -> ConnectorHealth:
        return ConnectorHealth(status="HEALTHY", checked_at=utc_now_iso())

    def replay(self, events: Iterable[SourceEventV2]) -> Iterator[SourceEventV2]:
        return iter(events)


class LocalFileConnector:
    def __init__(self, source_id: str, scope: LocalFileScope) -> None:
        self.source_id = source_id
        self.scope = scope
        self._roots = [Path(root).resolve(strict=True) for root in scope.roots]

    def capabilities(self) -> SourceCapabilities:
        return SourceCapabilities(polling=True, reconciliation=True)

    def discover(self, scope: DiscoveryScope) -> DiscoveryResult:
        del scope
        resources = [
            DiscoveredResource(
                resource_id=str(root),
                resource_type="directory",
                name=root.name or str(root),
                estimated_records=sum(1 for _ in self._files(root)),
            )
            for root in self._roots
        ]
        return DiscoveryResult(source_id=self.source_id, resources=resources)

    def baseline(self, checkpoint: str | None = None) -> Iterator[SourceEventV2]:
        del checkpoint
        return self._events()

    def poll_changes(self, checkpoint: str) -> Iterator[SourceEventV2]:
        del checkpoint
        return self._events()

    def handle_event(self, event: dict) -> Iterator[SourceEventV2]:
        path = event.get("path")
        return iter((self.fetch_record(str(path)),)) if path else iter(())

    def fetch_record(self, ref: str) -> SourceEventV2:
        path = Path(ref).resolve(strict=True)
        if not any(path.is_relative_to(root) for root in self._roots):
            raise ValueError("file is outside configured roots")
        return self._event(path)

    def health(self) -> ConnectorHealth:
        status = "HEALTHY" if all(root.is_dir() for root in self._roots) else "UNAVAILABLE"
        return ConnectorHealth(status=status, checked_at=utc_now_iso())

    def replay(self, events: Iterable[SourceEventV2]) -> Iterator[SourceEventV2]:
        return iter(events)

    def _events(self) -> Iterator[SourceEventV2]:
        count = 0
        for root in self._roots:
            for path in self._files(root):
                if count >= self.scope.max_files:
                    return
                count += 1
                yield self._event(path)

    def _files(self, root: Path) -> Iterator[Path]:
        for path in sorted(root.rglob("*")):
            if not path.is_file() or path.suffix.casefold() not in self.scope.suffixes:
                continue
            resolved = path.resolve(strict=True)
            if not resolved.is_relative_to(root):
                continue
            if resolved.stat().st_size <= self.scope.max_file_bytes:
                yield resolved

    def _event(self, path: Path) -> SourceEventV2:
        if path.stat().st_size > self.scope.max_file_bytes:
            raise ValueError("file exceeds max_file_bytes")
        content = path.read_bytes()
        content_hash = hashlib.sha256(content).hexdigest()
        captured_at = utc_now_iso()
        relative = next(str(path.relative_to(root)).replace("\\", "/") for root in self._roots if path.is_relative_to(root))
        event_id = hashlib.sha256(
            f"file:{self.source_id}:{relative}:{content_hash}".encode()
        ).hexdigest()
        return SourceEventV2(
            event_id=event_id,
            source_system="local_files",
            source_instance_id=self.source_id,
            source_record_id=relative,
            operation="UPSERT",
            source_version=str(path.stat().st_mtime_ns),
            event_time=captured_at,
            captured_at=captured_at,
            content_hash=content_hash,
            payload={
                "path": relative,
                "media_type": mimetypes.guess_type(path.name)[0] or "application/octet-stream",
                "text": content.decode("utf-8", errors="replace"),
            },
            metadata={"connector": "local-file/1.0", "size_bytes": len(content)},
        )
