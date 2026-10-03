"""Anomaly detection algorithms for graph structures.

Pure-Python implementations operating on the GraphStore port.
Detects outlier nodes (by degree z-score) and dense subgraphs.
"""

from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass
from typing import Any

from eoip.graph.store import GraphStore


@dataclass
class AnomalyResult:
    """A single detected anomaly."""

    canonical_id: str
    anomaly_type: str
    score: float
    details: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "canonical_id": self.canonical_id,
            "anomaly_type": self.anomaly_type,
            "score": self.score,
            "details": self.details,
        }


class AnomalyDetector:
    """Graph anomaly detection over an EOIP GraphStore."""

    def __init__(self, store: GraphStore) -> None:
        self._store = store

    # ------------------------------------------------------------------
    # Algorithms
    # ------------------------------------------------------------------

    def degree_zscore_outliers(self, threshold: float = 2.0) -> list[AnomalyResult]:
        """Find nodes whose total degree has a z-score above *threshold*.

        Total degree = in-degree + out-degree.  A z-score above the
        threshold in either direction (unusually high or unusually low)
        is flagged, though in practice only high-degree nodes are
        interesting anomalies.
        """
        vertices = self._store.find_vertices(limit=50_000)
        if not vertices:
            return []

        # Compute degrees
        degrees: list[tuple[dict, int]] = []
        for v in vertices:
            out_count = len(self._store.edges_from(v["vid"]))
            in_count = len(self._store.edges_to(v["vid"]))
            degrees.append((v, out_count + in_count))

        if len(degrees) < 2:
            return []

        # Mean and stddev
        deg_values = [d for _, d in degrees]
        n = len(deg_values)
        mean = sum(deg_values) / n
        variance = sum((d - mean) ** 2 for d in deg_values) / n
        stddev = math.sqrt(variance) if variance > 0 else 0.0

        if stddev == 0.0:
            return []

        results: list[AnomalyResult] = []
        for v, degree in degrees:
            zscore = (degree - mean) / stddev
            if abs(zscore) > threshold:
                cid = v["properties"]["canonical_id"]
                out_deg = len(self._store.edges_from(v["vid"]))
                in_deg = len(self._store.edges_to(v["vid"]))
                results.append(
                    AnomalyResult(
                        canonical_id=cid,
                        anomaly_type="degree_outlier",
                        score=round(zscore, 4),
                        details={
                            "degree": degree,
                            "in_degree": in_deg,
                            "out_degree": out_deg,
                            "mean_degree": round(mean, 2),
                            "stddev": round(stddev, 2),
                            "z_score": round(zscore, 4),
                            "label": v["label"],
                        },
                    )
                )

        results.sort(key=lambda r: -abs(r.score))
        return results

    def dense_subgraph_detection(self) -> list[AnomalyResult]:
        """Detect dense subgraphs by finding high-degree node clusters.

        Uses a greedy approach: start from high-degree nodes, expand to
        immediate neighbours, and measure local density.  Subgraphs
        whose density exceeds twice the global average are flagged.
        """
        vertices = self._store.find_vertices(limit=50_000)
        if not vertices:
            return []

        # Build adjacency and degree map
        vid_to_cid: dict[str, str] = {}
        vid_to_label: dict[str, str] = {}
        adj: dict[str, set[str]] = defaultdict(set)

        for v in vertices:
            cid = v["properties"]["canonical_id"]
            vid_to_cid[v["vid"]] = cid
            vid_to_label[v["vid"]] = v["label"]

        total_edges = 0
        for v in vertices:
            for edge in self._store.edges_from(v["vid"]):
                tgt_vid = edge["in_v"]
                if tgt_vid in vid_to_cid:
                    adj[v["vid"]].add(tgt_vid)
                    adj[tgt_vid].add(v["vid"])
                    total_edges += 1

        n = len(vertices)
        if n < 3 or total_edges == 0:
            return []

        global_density = (2.0 * total_edges) / (n * (n - 1)) if n > 1 else 0.0
        density_threshold = max(global_density * 2, 0.3)

        # Find clusters around high-degree nodes
        degree_list = [(vid, len(nbrs)) for vid, nbrs in adj.items() if nbrs]
        degree_list.sort(key=lambda x: -x[1])

        results: list[AnomalyResult] = []
        seen_clusters: set[frozenset[str]] = set()

        for vid, _ in degree_list[:20]:  # check top 20 hubs
            cluster = {vid} | adj[vid]
            if len(cluster) < 3:
                continue

            cluster_key = frozenset(cluster)
            if cluster_key in seen_clusters:
                continue
            seen_clusters.add(cluster_key)

            # Count internal edges
            internal_edges = 0
            cluster_list = list(cluster)
            for i, a in enumerate(cluster_list):
                for b in cluster_list[i + 1 :]:
                    if b in adj.get(a, set()):
                        internal_edges += 1

            k = len(cluster)
            max_edges = k * (k - 1) / 2
            local_density = internal_edges / max_edges if max_edges > 0 else 0.0

            if local_density >= density_threshold:
                hub_cid = vid_to_cid.get(vid, vid)
                member_cids = sorted(vid_to_cid.get(v, v) for v in cluster)
                results.append(
                    AnomalyResult(
                        canonical_id=hub_cid,
                        anomaly_type="dense_subgraph",
                        score=round(local_density, 4),
                        details={
                            "cluster_size": k,
                            "internal_edges": internal_edges,
                            "local_density": round(local_density, 4),
                            "global_density": round(global_density, 6),
                            "members": member_cids,
                        },
                    )
                )

        results.sort(key=lambda r: -r.score)
        return results

    def missing_expected_edges(self) -> list[AnomalyResult]:
        """Detect entity pairs that share neighbours but lack a direct edge.

        Uses common-neighbour count: if two nodes share >= 3 neighbours
        yet are not directly connected, the missing edge is flagged.
        """
        vertices = self._store.find_vertices(limit=50_000)
        if not vertices:
            return []

        vid_to_cid: dict[str, str] = {}
        adj: dict[str, set[str]] = defaultdict(set)

        for v in vertices:
            vid_to_cid[v["vid"]] = v["properties"]["canonical_id"]

        for v in vertices:
            for edge in self._store.edges_from(v["vid"]):
                tgt = edge["in_v"]
                if tgt in vid_to_cid:
                    adj[v["vid"]].add(tgt)
                    adj[tgt].add(v["vid"])

        results: list[AnomalyResult] = []
        vids = list(vid_to_cid.keys())
        seen: set[tuple[str, str]] = set()

        for i, u in enumerate(vids):
            for j in range(i + 1, len(vids)):
                w = vids[j]
                if w in adj.get(u, set()):
                    continue
                common = adj.get(u, set()) & adj.get(w, set())
                if len(common) >= 3:
                    pair = tuple(sorted([vid_to_cid[u], vid_to_cid[w]]))
                    if pair in seen:
                        continue
                    seen.add(pair)
                    results.append(
                        AnomalyResult(
                            canonical_id=vid_to_cid[u],
                            anomaly_type="missing_edge",
                            score=float(len(common)),
                            details={
                                "other_entity": vid_to_cid[w],
                                "common_neighbor_count": len(common),
                                "common_neighbors": sorted(
                                    vid_to_cid.get(v, v) for v in common
                                ),
                            },
                        )
                    )

        results.sort(key=lambda r: -r.score)
        return results

    def orphaned_entities(
        self, entity_types: list[str] | None = None
    ) -> list[AnomalyResult]:
        """Find entities with zero incoming edges (unreferenced).

        Excludes meta-graph entities (GraphDomain, OntologyVersion, DataSource).
        """
        META_LABELS = {"GraphDomain", "OntologyVersion", "DataSource"}
        vertices = self._store.find_vertices(limit=50_000)
        results: list[AnomalyResult] = []
        for v in vertices:
            if v["label"] in META_LABELS:
                continue
            if entity_types and v["label"] not in entity_types:
                continue
            incoming = self._store.edges_to(v["vid"])
            if len(incoming) == 0:
                cid = v["properties"]["canonical_id"]
                results.append(
                    AnomalyResult(
                        canonical_id=cid,
                        anomaly_type="orphaned",
                        score=0.0,
                        details={
                            "label": v["label"],
                            "in_degree": 0,
                            "out_degree": len(self._store.edges_from(v["vid"])),
                        },
                    )
                )
        return results

    def stale_entities(self, threshold_hours: int = 168) -> list[AnomalyResult]:
        """Find entities not updated within *threshold_hours*."""
        import datetime

        cutoff = datetime.datetime.now(datetime.UTC) - datetime.timedelta(
            hours=threshold_hours
        )
        cutoff_iso = cutoff.isoformat()
        vertices = self._store.find_vertices(limit=50_000)
        results: list[AnomalyResult] = []
        for v in vertices:
            props = v.get("properties", v)
            last_run = props.get("last_ingestion_run") or props.get("modified_at") or ""
            if last_run and last_run < cutoff_iso:
                cid = props.get("canonical_id", v.get("canonical_id", ""))
                results.append(
                    AnomalyResult(
                        canonical_id=cid,
                        anomaly_type="stale",
                        score=0.0,
                        details={
                            "label": v["label"],
                            "last_seen": last_run,
                            "threshold_hours": threshold_hours,
                        },
                    )
                )
        return results
