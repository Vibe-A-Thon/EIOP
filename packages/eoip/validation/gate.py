"""Hard validation gates on the graph mutation path (FR-VALID-002).

Soft rules (missing required properties, orphans, staleness, coverage) stay
in the post-ingestion ValidationEngine so seeded-invalid data can still be
inspected as findings. Hard invariants — known labels, valid edge endpoints,
present canonical_id, known property keys — are enforced BEFORE a write: a
blocked mutation raises ``MutationBlocked`` and the fact is never persisted
(MVP-FR-012: hard invalid edges are prevented, not swept later).

Both store implementations (HugeGraphStore, MemoryGraphStore) call these gates
inside their upsert paths, so every ingestion service is covered uniformly.
"""

from __future__ import annotations

from eoip.ontology.manifest import EDGE_LABELS, PROPERTY_KEYS, VERTEX_LABELS


class MutationBlocked(ValueError):
    """A proposed graph mutation violates a hard ontology invariant."""

    def __init__(self, reason: str, *, label: str | None = None) -> None:
        self.reason = reason
        self.label = label
        super().__init__(f"mutation blocked for {label or 'graph'}: {reason}")


def check_vertex(label: str, properties: dict) -> None:
    """Enforce hard vertex invariants before write.

    Raises MutationBlocked on: unknown label, missing/empty canonical_id,
    unknown property keys. Missing required properties are a SOFT rule handled
    by the ValidationEngine (seeded-invalid data must remain writable so the
    engine can report it as a finding).
    """
    spec = VERTEX_LABELS.get(label)
    if spec is None:
        raise MutationBlocked(f"unknown vertex label: {label}", label=label)
    cid = properties.get("canonical_id")
    if _is_empty(cid):
        raise MutationBlocked("canonical_id is required and must be non-empty", label=label)
    unknown = sorted(set(properties) - set(PROPERTY_KEYS))
    if unknown:
        raise MutationBlocked(
            f"unknown property keys: {unknown} (canonical_id={cid})",
            label=label,
        )


def check_edge(label: str, out_label: str, in_label: str, properties: dict) -> None:
    """Enforce hard edge invariants before write: known label + valid endpoints."""
    spec = EDGE_LABELS.get(label)
    if spec is None:
        raise MutationBlocked(f"unknown edge label: {label}", label=label)
    outs, ins, _props = spec
    if out_label not in outs or in_label not in ins:
        raise MutationBlocked(
            f"invalid endpoints for {label}: {out_label} -> {in_label}",
            label=label,
        )
    unknown = sorted(set(properties) - set(PROPERTY_KEYS))
    if unknown:
        raise MutationBlocked(
            f"unknown edge property keys: {unknown} ({label})",
            label=label,
        )


def _is_empty(value) -> bool:
    return value is None or (isinstance(value, str) and not value.strip())
