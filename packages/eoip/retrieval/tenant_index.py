"""Tenant-scoped retrieval index backed by the tenant's own layers (SR-TEN-003, SR-PRV-002, CRA-025.3).

Keyword postings and dense vectors live in the tenant's search-index and vector-collection layers
(``TenantHandle``), so the data-subject workflow (locate/export/rectify/erase) reaches exactly what retrieval
serves, and one tenant's queries can never score another tenant's documents. Candidate generation only sees
the tenant's own entities; graph expansion is filtered through the same ownership predicate.
"""
from __future__ import annotations

import math
from typing import Any
from collections.abc import Callable

from eoip.retrieval.vectors import entity_text


def vertex_tenant(vertex: dict) -> str | None:
    """Owning tenant of a graph vertex: ``properties.tenant_id`` or the ``urn:eoip:<tenant>:`` namespace."""
    props = vertex.get("properties") or {}
    if props.get("tenant_id"):
        return str(props["tenant_id"])
    cid = str(vertex.get("canonical_id") or "")
    if cid.startswith("urn:eoip:"):
        parts = cid.split(":", 3)
        if len(parts) == 4 and parts[2]:
            return parts[2]
    return None


def owned_by(store: Any, tenant_id: str) -> Callable[[str], bool]:
    """Deny-by-default ownership predicate over canonical ids (unmarked vertices belong to nobody)."""
    def allowed(cid: str) -> bool:
        v = store.get_vertex_by_canonical_id(cid)
        return bool(v) and vertex_tenant(v) == tenant_id
    return allowed


def _cos(a: list[float], b: list[float]) -> float:
    if len(a) != len(b) or not a:
        return 0.0
    na, nb = math.sqrt(sum(x * x for x in a)), math.sqrt(sum(x * x for x in b))
    return sum(x * y for x, y in zip(a, b)) / (na * nb) if na and nb else 0.0


class TenantRetrievalIndex:
    """``SearchIndex`` port over one tenant's layers."""

    def __init__(self, handle: Any, embedder: Any | None = None) -> None:
        self.handle = handle
        if embedder is None:
            from eoip.models.embeddings import semantic_embedder

            embedder = semantic_embedder()
        self.embedder = embedder
        # Vectors from different models/families never mix: the id names the model, not just the class.
        self.embedder_id = (f"{type(self.embedder).__name__}:{getattr(self.embedder, 'model_name', '')}:"
                            f"{getattr(self.embedder, 'dimensions', '')}")

    @property
    def tenant_id(self) -> str:
        return self.handle.tenant_id

    def _embed(self, text: str) -> list[float]:
        fn = getattr(self.embedder, "embed_one", None) or self.embedder.embed
        return list(fn(text))

    def add(self, entity_id: str, text: str, meta: dict | None = None) -> None:
        meta = dict(meta or {})
        self.handle.search_add(entity_id, text, meta)
        vec = self._embed(text)
        self.handle.vector_upsert(entity_id, vec, {**meta, "text": text, "embedder": self.embedder_id, "dimension": len(vec)})

    def remove(self, entity_id: str) -> None:
        self.handle.search_remove(entity_id)
        self.handle.vector_delete(entity_id)

    def keyword_search(self, query: str, top_k: int = 10) -> list[tuple[str, float]]:
        return self.handle.search_index().keyword_search(query, top_k)

    def vector_search(self, query: str, top_k: int = 10) -> list[tuple[str, float]]:
        q = self._embed(query)
        scored = [(doc_id, _cos(q, vec)) for doc_id, (vec, payload) in self.handle.vector_items().items()
                  if payload.get("embedder") == self.embedder_id]  # never mix embedding families (CRA-025.8)
        scored = [s for s in scored if s[1] > 0]
        return sorted(scored, key=lambda kv: (-kv[1], kv[0]))[:top_k]

    def entity_ids(self) -> list[str]:
        return sorted(self.handle.search_docs())

    def sync_from_store(self, store: Any, *, limit: int = 10_000) -> dict[str, int]:
        """Index the tenant's own vertices; drop entries whose vertex vanished, changed owner or was deleted."""
        current = self.handle.search_docs()
        seen: set[str] = set()
        added = updated = removed = 0
        for vertex in store.find_vertices(limit=limit, include_deleted=False):
            if vertex_tenant(vertex) != self.tenant_id:
                continue
            cid = vertex["canonical_id"]
            text = entity_text(vertex["label"], vertex.get("properties") or {})
            if not text.strip():
                continue
            seen.add(cid)
            if cid in current and current[cid][0] == text:
                continue
            if cid in current:
                self.remove(cid)
                updated += 1
            else:
                added += 1
            self.add(cid, text, {"label": vertex["label"], "source_ref": cid})  # lineage for DSAR
        for cid in set(current) - seen:
            self.remove(cid)
            removed += 1
        return {"added": added, "updated": updated, "removed": removed}
