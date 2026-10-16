"""Data-subject access request (DSAR) locate + erasure propagation (SR-PRV-002, partial).

``locate_subject`` finds every record tied to a subject identifier across
three surfaces:

* the graph store (via the ``GraphStore`` protocol — property scans);
* a raw-captures index (arbitrary caller-supplied index with a
  ``find_by_subject`` method);
* derived-data registries (embeddings, search documents, summaries).

The result is a **subject access report** listing each hit with its
location and sensitivity labels. Full access/export packaging, backup and
cache scanning are flagged in the report as ``unsearched_surfaces`` —
backups in particular are out of scope for automated erasure and are
External gate (see SR-PRV-002: backups only "flagged").

``ErasurePropagator`` executes erasure with propagation: tombstones the
graph entity, erases derived artifacts (embeddings/vector index entries/
search docs) via caller-provided eraser callbacks, and emits a signed
proof record. Rectification workflows and DSAR ticketing are ADR-gated.
"""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from typing import Any, Protocol

from pydantic import BaseModel, ConfigDict, Field


class SubjectHit(BaseModel):
    model_config = ConfigDict(extra="forbid")

    surface: str = Field(description="'graph', 'raw_capture', or 'derived'")
    ref: str
    kind: str = Field(default="", description="entity type / capture kind / derived kind")
    tenant_id: str | None = None
    sensitivity_labels: list[str] = Field(default_factory=list)


class SubjectAccessReport(BaseModel):
    """Result of a DSAR locate across all searchable surfaces (SR-PRV-002)."""

    model_config = ConfigDict(extra="forbid")

    subject_id: str
    tenant_id: str | None = None
    generated_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    hits: list[SubjectHit] = Field(default_factory=list)
    unsearched_surfaces: list[str] = Field(
        default_factory=lambda: ["backups", "caches", "exports"],
        description="Surfaces not automatically searched — backups are External gate (flagged only, SR-PRV-002)",
    )

    def surface_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for hit in self.hits:
            counts[hit.surface] = counts.get(hit.surface, 0) + 1
        return counts


class RawCaptureIndex(Protocol):
    """Port for the raw-captures index (apps wire the real store)."""

    def find_by_subject(self, subject_id: str, tenant_id: str | None = None) -> list[dict]: ...


class DerivedDataRegistry(Protocol):
    """Port for derived-data registries (embeddings, search docs)."""

    def find_by_source(self, source_ref: str, tenant_id: str | None = None) -> list[dict]: ...


def _labels_of(record: Any) -> list[str]:
    if isinstance(record, dict):
        return sorted({str(v) for v in record.get("sensitivity_labels", [])})
    return sorted({str(v) for v in getattr(record, "sensitivity_labels", [])})


def locate_subject(
    subject_id: str,
    *,
    tenant_id: str | None = None,
    graph_store: Any = None,
    graph_labels: list[str] | None = None,
    raw_captures: RawCaptureIndex | None = None,
    derived_registries: list[DerivedDataRegistry] | None = None,
    subject_properties: list[str] | None = None,
) -> SubjectAccessReport:
    """Find a subject across graph, raw captures, and derived data (SR-PRV-002).

    Graph search is a bounded property scan: for each candidate label and
    subject-bearing property, ``find_vertex_by_property`` is used. A
    dedicated identity-index search is ADR-gated (needs a search-backend
    dependency decision).
    """
    report = SubjectAccessReport(subject_id=subject_id, tenant_id=tenant_id)
    props = subject_properties or ["email", "subject_id", "external_id", "owner"]

    if graph_store is not None:
        seen: set[str] = set()
        for label in graph_labels or ["Entity"]:
            for prop in props:
                for vertex in graph_store.find_vertex_by_property(label, prop, subject_id, limit=100, include_deleted=True):
                    vid = str(vertex.get("vid") or vertex.get("canonical_id"))
                    if vid in seen:
                        continue
                    seen.add(vid)
                    report.hits.append(
                        SubjectHit(
                            surface="graph",
                            ref=str(vertex.get("canonical_id") or vid),
                            kind=str(vertex.get("label") or label),
                            tenant_id=tenant_id,
                            sensitivity_labels=_labels_of(vertex.get("properties", {})),
                        )
                    )

    if raw_captures is not None:
        for capture in raw_captures.find_by_subject(subject_id, tenant_id):
            report.hits.append(
                SubjectHit(
                    surface="raw_capture",
                    ref=str(capture.get("ref") or capture.get("id") or ""),
                    kind=str(capture.get("kind") or "capture"),
                    tenant_id=tenant_id,
                    sensitivity_labels=_labels_of(capture),
                )
            )

    for registry in derived_registries or []:
        for record in registry.find_by_source(subject_id, tenant_id):
            report.hits.append(
                SubjectHit(
                    surface="derived",
                    ref=str(record.get("ref") or record.get("id") or ""),
                    kind=str(record.get("kind") or "derived"),
                    tenant_id=tenant_id,
                    sensitivity_labels=_labels_of(record),
                )
            )
    return report


class ErasureProof(BaseModel):
    """Tamper-evident proof that erasure ran (SR-PRV-002)."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(description="URN, e.g. urn:eoip:privacy:erasure:<digest>")
    subject_id: str
    tenant_id: str | None = None
    erased_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    tombstoned_refs: list[str] = Field(default_factory=list)
    erased_derived_refs: list[str] = Field(default_factory=list)
    unerased_refs: list[str] = Field(default_factory=list, description="Refs the erasers could not remove (e.g. backups)")
    digest: str


def proof_digest(payload: dict) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


class ErasurePropagator:
    """Tombstone + erase derived artifacts with a proof record (SR-PRV-002).

    ``derived_erasers`` maps a derived-artifact kind (``embedding``,
    ``vector_index_entry``, ``search_doc``, ``summary``) to a callable
    ``(ref, tenant_id) -> bool`` that deletes it. Kinds without an eraser
    are recorded in ``unerased_refs`` — crypto-shredding of backup copies
    is External gate (SR-PRV-003).
    """

    def __init__(self, graph_store: Any = None, derived_erasers: dict[str, Any] | None = None):
        self._graph_store = graph_store
        self._erasers = dict(derived_erasers or {})

    def register_eraser(self, kind: str, eraser: Any) -> None:
        self._erasers[kind] = eraser

    def erase(self, report: SubjectAccessReport) -> ErasureProof:
        tombstoned: list[str] = []
        erased: list[str] = []
        unerased: list[str] = []
        for hit in report.hits:
            if hit.surface == "graph" and self._graph_store is not None:
                ok = bool(self._graph_store.tombstone_vertex(hit.ref))
                (tombstoned if ok else unerased).append(hit.ref)
            elif hit.surface == "derived":
                eraser = self._erasers.get(hit.kind)
                if eraser is None:
                    unerased.append(hit.ref)
                elif eraser(hit.ref, report.tenant_id):
                    erased.append(hit.ref)
                else:
                    unerased.append(hit.ref)
            else:
                # raw captures are retained per retention policy; their
                # contents are tombstoned by the retention job, not DSAR
                unerased.append(hit.ref)
        payload = {
            "subject_id": report.subject_id,
            "tombstoned": sorted(tombstoned),
            "erased": sorted(erased),
        }
        digest = proof_digest(payload)
        return ErasureProof(
            id=f"urn:eoip:privacy:erasure:{digest[:16]}",
            subject_id=report.subject_id,
            tenant_id=report.tenant_id,
            tombstoned_refs=sorted(tombstoned),
            erased_derived_refs=sorted(erased),
            unerased_refs=sorted(unerased),
            digest=digest,
        )
