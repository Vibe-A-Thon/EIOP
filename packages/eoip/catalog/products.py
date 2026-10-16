"""Knowledge Product catalog (GAP-KP-001..005).

First-class Knowledge Product model with lifecycle states, CRUD, filtered
listing, JSON export/import of product definitions, and navigable lineage
(source graphs -> product -> consumers). Products are stored as
``KnowledgeProduct`` vertices in the graph store (FR-GRAPH-001); source graphs
and consumers are stored as vertex properties, which keeps lineage queries
deterministic and avoids bespoke edge-label schema changes.
"""

from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from eoip.graph.store import GraphStore

LABEL = "KnowledgeProduct"


class ProductState(str, Enum):
    """Lifecycle states for a knowledge product (GAP-KP-002)."""

    DRAFT = "Draft"
    EXPERIMENTAL = "Experimental"
    TRUSTED = "Trusted"
    CERTIFIED = "Certified"
    DEPRECATED = "Deprecated"


# Allowed state transitions (GAP-KP-002). Absence means the transition is rejected.
ALLOWED_TRANSITIONS: dict[ProductState, set[ProductState]] = {
    ProductState.DRAFT: {ProductState.EXPERIMENTAL, ProductState.DEPRECATED},
    ProductState.EXPERIMENTAL: {ProductState.TRUSTED, ProductState.DRAFT, ProductState.DEPRECATED},
    ProductState.TRUSTED: {ProductState.CERTIFIED, ProductState.EXPERIMENTAL, ProductState.DEPRECATED},
    ProductState.CERTIFIED: {ProductState.DEPRECATED},
    ProductState.DEPRECATED: set(),
}


class ProductValidationError(ValueError):
    """Invalid product definition or illegal state transition."""


class ProductNotFoundError(KeyError):
    """No knowledge product exists for the given id."""


class SLO(BaseModel):
    """A service-level objective with a numeric threshold and unit."""

    metric: str
    threshold: float
    unit: str = ""
    window: str = ""


class KnowledgeProduct(BaseModel):
    """Knowledge Product contract (GAP-KP-001)."""

    product_id: str = ""  # canonical id, assigned by the catalog on create
    name: str
    owner: str
    domain: str
    description: str = ""
    source_graphs: list[str] = Field(default_factory=list)
    ontology_version: str = ""
    quality_slo: SLO | None = None
    freshness_slo: SLO | None = None
    access_policy: str = "internal"
    apis: list[str] = Field(default_factory=list)
    dashboards: list[str] = Field(default_factory=list)
    consumers: list[str] = Field(default_factory=list)
    state: ProductState = ProductState.DRAFT
    created_at: str = ""
    updated_at: str = ""

    @property
    def canonical_id(self) -> str:
        return self.product_id


def _slug(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug or "unnamed"


def _canonical_id(name: str) -> str:
    return f"urn:eoip:catalog:knowledge-product:{_slug(name)}"


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _props_from(product: KnowledgeProduct) -> dict[str, Any]:
    def _dumps(value: Any) -> str | None:
        return json.dumps(value, sort_keys=True) if value is not None else None

    return {
        "canonical_id": product.product_id,
        "name": product.name,
        "owner": product.owner,
        "domain": product.domain,
        "description": product.description,
        "source_graphs": json.dumps(list(product.source_graphs)),
        "ontology_version": product.ontology_version,
        "quality_slo": _dumps(product.quality_slo.model_dump() if product.quality_slo else None),
        "freshness_slo": _dumps(product.freshness_slo.model_dump() if product.freshness_slo else None),
        "access_policy": product.access_policy,
        "apis": json.dumps(list(product.apis)),
        "dashboards": json.dumps(list(product.dashboards)),
        "consumers": json.dumps(list(product.consumers)),
        "product_state": product.state.value,
        "created_at": product.created_at,
        "updated_at": product.updated_at,
    }


def _product_from(vertex_props: dict[str, Any]) -> KnowledgeProduct:
    def _slo(raw: Any) -> SLO | None:
        if isinstance(raw, dict):
            return SLO(**raw)
        if isinstance(raw, str) and raw:
            return SLO(**json.loads(raw))
        return None

    def _list(raw: Any) -> list[str]:
        if isinstance(raw, list):
            return list(raw)
        if isinstance(raw, str) and raw:
            return list(json.loads(raw))
        return []

    return KnowledgeProduct(
        product_id=vertex_props.get("canonical_id", ""),
        name=vertex_props.get("name", ""),
        owner=vertex_props.get("owner", ""),
        domain=vertex_props.get("domain", ""),
        description=vertex_props.get("description", ""),
        source_graphs=_list(vertex_props.get("source_graphs")),
        ontology_version=vertex_props.get("ontology_version", ""),
        quality_slo=_slo(vertex_props.get("quality_slo")),
        freshness_slo=_slo(vertex_props.get("freshness_slo")),
        access_policy=vertex_props.get("access_policy", "internal"),
        apis=_list(vertex_props.get("apis")),
        dashboards=_list(vertex_props.get("dashboards")),
        consumers=_list(vertex_props.get("consumers")),
        state=ProductState(vertex_props.get("product_state", ProductState.DRAFT.value)),
        created_at=vertex_props.get("created_at", ""),
        updated_at=vertex_props.get("updated_at", ""),
    )


class KnowledgeProductCatalog:
    """CRUD, lifecycle, export/import and lineage over the graph store (GAP-KP-001..005)."""

    def __init__(self, store: GraphStore) -> None:
        self._store = store

    # -- CRUD ---------------------------------------------------------------

    def create(self, product: KnowledgeProduct) -> KnowledgeProduct:
        """Create a product; assigns the canonical id. Raises on duplicate name."""
        product.product_id = _canonical_id(product.name)
        if self._store.get_vertex_by_canonical_id(product.product_id):
            raise ProductValidationError(
                f"Knowledge product already exists: {product.product_id}"
            )
        now = _now()
        product.created_at = product.created_at or now
        product.updated_at = now
        product.state = ProductState(product.state)
        self._store.upsert_vertex(LABEL, _props_from(product))
        return product

    def get(self, product_id: str) -> KnowledgeProduct:
        vertex = self._store.get_vertex_by_canonical_id(product_id)
        if not vertex or vertex["label"] != LABEL:
            raise ProductNotFoundError(product_id)
        if vertex["properties"].get("deleted_at"):
            raise ProductNotFoundError(product_id)
        return _product_from(vertex["properties"])

    def update(self, product: KnowledgeProduct) -> KnowledgeProduct:
        """Update mutable fields of an existing product (not its state)."""
        if not product.product_id:
            raise ProductValidationError("product_id is required for update")
        vertex = self._store.get_vertex_by_canonical_id(product.product_id)
        if not vertex or vertex["label"] != LABEL:
            raise ProductNotFoundError(product.product_id)
        existing = _product_from(vertex["properties"])
        product.state = existing.state  # state changes only via transition()
        product.created_at = existing.created_at
        product.updated_at = _now()
        self._store.upsert_vertex(LABEL, _props_from(product))
        return product

    def delete(self, product_id: str) -> bool:
        vertex = self._store.get_vertex_by_canonical_id(product_id)
        if not vertex or vertex["label"] != LABEL or vertex["properties"].get("deleted_at"):
            return False
        return self._store.tombstone_vertex(product_id)

    def list(
        self,
        *,
        owner: str | None = None,
        domain: str | None = None,
        state: ProductState | str | None = None,
        access_policy: str | None = None,
        consumer: str | None = None,
    ) -> list[KnowledgeProduct]:
        """List products with optional filters (GAP-KP-003)."""
        filters: dict[str, Any] = {}
        if owner is not None:
            filters["owner"] = owner
        if domain is not None:
            filters["domain"] = domain
        if access_policy is not None:
            filters["access_policy"] = access_policy
        if state is not None:
            filters["product_state"] = (
                state.value if isinstance(state, ProductState) else str(state)
            )
        vertices = self._store.find_vertices(label=LABEL, filters=filters or None, limit=10_000)
        products = [_product_from(v["properties"]) for v in vertices]
        if consumer is not None:
            products = [p for p in products if consumer in p.consumers]
        products.sort(key=lambda p: p.product_id)
        return products

    # -- Lifecycle ------------------------------------------------------------

    def transition(self, product_id: str, to_state: ProductState | str) -> KnowledgeProduct:
        """Apply a lifecycle transition (GAP-KP-002); rejects illegal transitions."""
        to = ProductState(to_state)
        product = self.get(product_id)
        allowed = ALLOWED_TRANSITIONS[product.state]
        if to not in allowed:
            raise ProductValidationError(
                f"Illegal transition: {product.state.value} -> {to.value}"
            )
        product.state = to
        product.updated_at = _now()
        self._store.upsert_vertex(LABEL, _props_from(product))
        return product

    def allowed_transitions(self, product_id: str) -> list[str]:
        product = self.get(product_id)
        return sorted(s.value for s in ALLOWED_TRANSITIONS[product.state])

    # -- Export / import --------------------------------------------------------

    def export_json(self, product_id: str) -> str:
        """Export a single product definition as JSON (GAP-KP-004)."""
        return self.get(product_id).model_dump_json(indent=2)

    def import_json(self, payload: str | dict) -> KnowledgeProduct:
        """Import a product definition (JSON string or dict).

        Re-importing an existing product id updates it in place, so definitions
        are portable across environments.
        """
        data = json.loads(payload) if isinstance(payload, str) else dict(payload)
        product = KnowledgeProduct(**data)
        product_id = _canonical_id(product.name)
        existing = self._store.get_vertex_by_canonical_id(product_id)
        if existing and existing["label"] == LABEL:
            product.product_id = product_id
            product.created_at = existing["properties"].get("created_at", "")
            product.updated_at = _now()
            self._store.upsert_vertex(LABEL, _props_from(product))
            return product
        product.product_id = product_id
        now = _now()
        product.created_at = product.created_at or now
        product.updated_at = product.updated_at or product.created_at
        product.state = ProductState(product.state)
        self._store.upsert_vertex(LABEL, _props_from(product))
        return product

    def export_all_json(self) -> str:
        return json.dumps(
            [p.model_dump() for p in self.list()], indent=2, default=str
        )

    # -- Lineage ------------------------------------------------------------

    def lineage(self, product_id: str) -> dict[str, Any]:
        """Navigable lineage: source graphs -> product -> consumers (GAP-KP-005)."""
        product = self.get(product_id)
        return {
            "product_id": product.product_id,
            "name": product.name,
            "state": product.state.value,
            "source_graphs": [
                {"source_graph": g, "direction": "upstream"}
                for g in product.source_graphs
            ],
            "consumers": [
                {"consumer": c, "direction": "downstream"}
                for c in product.consumers
            ],
        }

    def products_for_source_graph(self, source_graph: str) -> list[KnowledgeProduct]:
        """Reverse lineage: all products derived from a source graph."""
        return [
            p for p in self.list() if source_graph in p.source_graphs
        ]

    def products_for_consumer(self, consumer: str) -> list[KnowledgeProduct]:
        return self.list(consumer=consumer)
