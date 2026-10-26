"""Shared pydantic models for graph-build results."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


def _urn(kind: str, fingerprint: str) -> str:
    import hashlib

    digest = hashlib.sha256(fingerprint.encode()).hexdigest()[:24]
    return f"urn:eoip:graphbuild:{kind}:{digest}"


class ProposedClass(BaseModel):
    """A class proposed by schema induction or hierarchy clustering."""

    model_config = ConfigDict(extra="forbid")

    class_id: str
    name: str
    source: str = "schema-induction"
    member_count: int = 0
    evidence: dict[str, Any] = Field(default_factory=dict)


class ProposedProperty(BaseModel):
    model_config = ConfigDict(extra="forbid")

    property_id: str
    name: str
    domain: str = ""
    range: str = ""
    functional: bool = False
    required: bool = False
    evidence: dict[str, Any] = Field(default_factory=dict)


class ProposedEdge(BaseModel):
    """A candidate edge (co-change, link prediction, coupling, etc.)."""

    model_config = ConfigDict(extra="forbid")

    edge_id: str
    label: str
    from_id: str
    to_id: str
    score: float = 0.0
    method: str = ""
    evidence: dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def make(cls, label: str, from_id: str, to_id: str, score: float, method: str, **evidence: Any) -> ProposedEdge:
        fingerprint = f"{label}|{from_id}|{to_id}|{method}|{score!r}"
        return cls(
            edge_id=_urn("edge", fingerprint),
            label=label,
            from_id=from_id,
            to_id=to_id,
            score=round(score, 6),
            method=method,
            evidence=evidence,
        )


class GraphDelta(BaseModel):
    """Validated additions produced by one builder run."""

    model_config = ConfigDict(extra="forbid")

    delta_id: str
    vertices: list[dict[str, Any]] = Field(default_factory=list)
    edges: list[ProposedEdge] = Field(default_factory=list)
    classes: list[ProposedClass] = Field(default_factory=list)
    properties: list[ProposedProperty] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)

    @classmethod
    def make(cls, kind: str, fingerprint: str, **kwargs: Any) -> GraphDelta:
        return cls(delta_id=_urn(kind, fingerprint + repr(sorted(kwargs.items()))), **kwargs)
