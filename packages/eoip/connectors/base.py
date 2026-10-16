"""Common acquisition-fabric connector protocol (G2-T0005, FR-CONN-001)."""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from typing import Any, Literal, Protocol, runtime_checkable

from eoip.contracts.source_event import SourceEventV2
from eoip.contracts.source_registry import SourceCapabilities
from pydantic import BaseModel, ConfigDict, Field


class DiscoveryScope(BaseModel):
    model_config = ConfigDict(extra="forbid")

    include: list[str] = Field(default_factory=list, max_length=1000)
    exclude: list[str] = Field(default_factory=list, max_length=1000)
    options: dict[str, Any] = Field(default_factory=dict)


class DiscoveredResource(BaseModel):
    model_config = ConfigDict(extra="forbid")

    resource_id: str
    resource_type: str
    name: str
    estimated_records: int | None = Field(default=None, ge=0)
    metadata: dict[str, Any] = Field(default_factory=dict)


class DiscoveryResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_id: str
    resources: list[DiscoveredResource] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class ConnectorHealth(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Literal["HEALTHY", "DEGRADED", "UNAVAILABLE", "MISCONFIGURED"]
    checked_at: str
    latency_ms: float | None = Field(default=None, ge=0)
    detail: str | None = None


@runtime_checkable
class SourceConnector(Protocol):
    """The only interface source adapters expose to the common pipeline."""

    source_id: str

    def capabilities(self) -> SourceCapabilities: ...

    def discover(self, scope: DiscoveryScope) -> DiscoveryResult: ...

    def baseline(self, checkpoint: str | None = None) -> Iterator[SourceEventV2]: ...

    def poll_changes(self, checkpoint: str) -> Iterator[SourceEventV2]: ...

    def handle_event(self, event: dict[str, Any]) -> Iterator[SourceEventV2]: ...

    def fetch_record(self, ref: str) -> SourceEventV2: ...

    def health(self) -> ConnectorHealth: ...

    def replay(self, events: Iterable[SourceEventV2]) -> Iterator[SourceEventV2]: ...
