"""Isolation model registry (SR-TEN-002, SR-TEN-003).

Three selectable isolation models (SR-TEN-002):

- ``SILO``  — dedicated stack per tenant (compute + data).
- ``BRIDGE`` — shared compute, dedicated data stores/namespaces.
- ``POOL``  — shared everything, logical isolation only (P1).

Isolation must be enforced at *every layer* (SR-TEN-003): graph, vector,
search, relational, object storage, event topics, secrets, KMS keys,
caches, logs, backups, exports. ``IsolationPlacement`` therefore records a
placement value for every layer, and ``validate_placement`` fails closed
when any layer is missing or when two tenants would share a placement
value that their isolation model forbids sharing (physical co-location of
dedicated resources).

Physical enforcement at each backend (creating actual graph namespaces,
collections, schemas, buckets, KMS keys) is an *External gate*: this
module validates and records the placement contract only.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

# Every layer SR-TEN-003 requires isolation metadata for.
REQUIRED_LAYERS: frozenset[str] = frozenset({
    "graph_namespace",      # graph database / graph-space / namespace
    "vector_collection",    # vector store collection
    "search_index",         # search index
    "relational_schema",    # relational schema (+ row-level security)
    "object_prefix",        # object bucket/prefix
    "event_topic",          # event topics
    "secrets_path",         # secrets mount/path
    "kms_key",              # per-tenant KMS key (SR-TEN-005)
    "cache_key_prefix",     # cache key prefix
    "log_stream",           # log stream/labels
    "backup_bucket",        # backups
    "export_prefix",        # exports
})


class IsolationModel(StrEnum):
    SILO = "silo"
    BRIDGE = "bridge"
    POOL = "pool"

    @property
    def dedicated_layers(self) -> frozenset[str]:
        """Layers that must be physically dedicated for this model (SR-TEN-002)."""
        if self is IsolationModel.SILO:
            return frozenset(REQUIRED_LAYERS)
        if self is IsolationModel.BRIDGE:
            return frozenset(
                REQUIRED_LAYERS - {"cache_key_prefix", "log_stream", "event_topic"}
            )
        return frozenset()  # POOL: logical isolation only


@dataclass(frozen=True)
class IsolationPlacement:
    """Per-layer placement metadata for one tenant (SR-TEN-003)."""

    model: IsolationModel
    layers: dict[str, str]
    tenant_id: str = ""

    def layer(self, name: str) -> str:
        try:
            return self.layers[name]
        except KeyError as exc:
            raise PlacementValidationError(f"missing layer: {name}") from exc

    def to_dict(self) -> dict[str, Any]:
        return {
            "tenant_id": self.tenant_id,
            "model": self.model.value,
            "layers": dict(self.layers),
        }


class PlacementValidationError(ValueError):
    """Raised when placement metadata is incomplete or collides (SR-TEN-003)."""


def validate_placement(
    placement: IsolationPlacement,
    existing: list[IsolationPlacement] | None = None,
) -> IsolationPlacement:
    """Fail-closed validation of a placement descriptor (SR-TEN-003).

    1. Every required layer must have a non-empty value.
    2. For layers the tenant's model marks dedicated, the placement value
       must be unique across all other tenants (no physical sharing).
    """
    missing = sorted(REQUIRED_LAYERS - set(placement.layers))
    if missing:
        raise PlacementValidationError(
            f"incomplete placement, missing layers: {', '.join(missing)}"
        )
    for name, value in placement.layers.items():
        if not value or not value.strip():
            raise PlacementValidationError(f"layer {name} has empty placement value")
    dedicated = placement.model.dedicated_layers
    for other in existing or []:
        if placement.tenant_id and other.tenant_id == placement.tenant_id:
            continue
        for layer in dedicated:
            if other.layers.get(layer) == placement.layers[layer]:
                raise PlacementValidationError(
                    f"dedicated layer {layer} shared with tenant {other.tenant_id}"
                )
    return placement


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

@dataclass
class IsolationRegistry:
    """In-memory registry of tenant placements (SR-TEN-002/SR-TEN-003)."""

    placements: dict[str, IsolationPlacement] = field(default_factory=dict)

    def register(self, placement: IsolationPlacement) -> IsolationPlacement:
        if not placement.tenant_id:
            raise PlacementValidationError("placement requires tenant_id")
        validate_placement(placement, list(self.placements.values()))
        self.placements[placement.tenant_id] = placement
        return placement

    def get(self, tenant_id: str) -> IsolationPlacement:
        try:
            return self.placements[tenant_id]
        except KeyError as exc:
            raise PlacementValidationError(f"no placement for tenant {tenant_id}") from exc

    def to_list(self) -> list[dict[str, Any]]:
        return [p.to_dict() for p in self.placements.values()]


def model_catalog() -> list[dict[str, Any]]:
    """Describe the selectable isolation models (SR-TEN-002)."""
    return [
        {
            "model": m.value,
            "dedicated_layers": sorted(m.dedicated_layers),
            "shared_layers": sorted(REQUIRED_LAYERS - m.dedicated_layers),
        }
        for m in IsolationModel
    ]
