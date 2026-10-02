"""Lineage service (FR-PROV-002).

Traces entities back to their source capture, ingestion run, and version.
"""

from __future__ import annotations

from eoip.graph.store import GraphStore
from eoip.graph.traversal import GraphTraversal

LINEAGE_EDGES = frozenset({"EVIDENCED_BY", "INGESTED_IN"})


class LineageService:
    def __init__(self, store: GraphStore, *, max_depth: int = 4, max_results: int = 100) -> None:
        self._store = store
        self._traversal = GraphTraversal(
            store,
            allowed_edges=LINEAGE_EDGES,
            max_depth=max_depth,
            max_results=max_results,
        )

    def trace(self, canonical_id: str, *, max_depth: int | None = None) -> dict:
        result = self._traversal.impact(
            canonical_id,
            max_depth=max_depth,
            direction="outgoing",
        )
        if result["source"] is None:
            return {"entity": None, "lineage": [], "truncated": False}

        lineage = []
        for item in result["impacted"]:
            vertex = item["vertex"]
            path_edges = item["path"]["edges"]
            lineage.append(
                {
                    "canonical_id": vertex["canonical_id"],
                    "label": vertex["label"],
                    "properties": vertex["properties"],
                    "depth": len(path_edges),
                    "edge_types": [e["label"] for e in path_edges],
                }
            )

        sources = [entry for entry in lineage if entry["label"] == "Evidence"]
        runs = [entry for entry in lineage if entry["label"] == "IngestionRun"]

        return {
            "entity": {
                "canonical_id": result["source"]["canonical_id"],
                "label": result["source"]["label"],
            },
            "lineage": lineage,
            "sources": sources,
            "ingestion_runs": runs,
            "truncated": result["truncated"],
        }
