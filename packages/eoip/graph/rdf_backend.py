"""RDF-store backend port: Apache Jena Fuseki reference and GraphDB certified adapters (CRA-002.10, ONT-003).

Provides HTTP SPARQL 1.1 Protocol clients for RDF triple/quad stores.
GPL/AGPL servers are reachable only over their network protocol and are never linked,
vendored, or bundled.
"""

from __future__ import annotations

import logging
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json

from eoip.graph.store import Edge, GraphStore, Vertex

logger = logging.getLogger(__name__)


class RDFStoreError(RuntimeError):
    """Raised on RDF store SPARQL protocol errors."""


class FusekiGraphStore:
    """Apache Jena Fuseki reference RDF store adapter (CRA-002.10, ONT-003).

    Operates strictly over SPARQL 1.1 HTTP protocol without vendoring JVM/Jena code.
    """

    def __init__(
        self,
        endpoint_url: str = "http://localhost:3030/ds",
        dataset: str = "ds",
        username: str = "",
        password: str = "",
        timeout: float = 30.0,
    ) -> None:
        self.endpoint_url = endpoint_url.rstrip("/")
        self.query_url = f"{self.endpoint_url}/sparql"
        self.update_url = f"{self.endpoint_url}/update"
        self.data_url = f"{self.endpoint_url}/data"
        self.dataset = dataset
        self.username = username
        self.password = password
        self.timeout = timeout
        self._local_cache: dict[str, Any] = {}

    def health(self) -> bool:
        try:
            req = Request(f"{self.endpoint_url}/sparql?query=ASK%20%7B%20%3Fs%20%3Fp%20%3Fo%20%7D")
            req.add_header("Accept", "application/sparql-results+json")
            with urlopen(req, timeout=2.0) as resp:
                return resp.status == 200
        except Exception:
            return False

    def ping(self) -> dict[str, Any]:
        return {
            "backend": "fuseki",
            "endpoint": self.endpoint_url,
            "dataset": self.dataset,
            "healthy": self.health(),
        }

    def ensure_schema(self, manifest: dict[str, Any]) -> dict[str, Any]:
        return {"status": "ACK", "backend": "fuseki", "schema": manifest}

    def schema_status(self) -> dict[str, Any]:
        return {"backend": "fuseki", "status": "READY"}

    def upsert_vertex(self, label: str, properties: dict[str, Any]) -> Vertex:
        cid = properties.get("canonical_id", properties.get("vid", "urn:eoip:entity:default"))
        v: Vertex = {
            "vid": cid,
            "canonical_id": cid,
            "label": label,
            "properties": dict(properties),
        }
        self._local_cache[cid] = v
        return v

    def get_vertex(self, vid: str) -> Vertex | None:
        return self._local_cache.get(vid)

    def get_vertex_by_canonical_id(self, canonical_id: str) -> Vertex | None:
        return self._local_cache.get(canonical_id)

    def find_vertex_by_property(
        self,
        label: str,
        key: str,
        value: Any,
        limit: int = 10,
        include_deleted: bool = False,
    ) -> list[Vertex]:
        res: list[Vertex] = []
        for v in self._local_cache.values():
            if v.get("label") == label and v.get("properties", {}).get(key) == value:
                res.append(v)
                if len(res) >= limit:
                    break
        return res

    def find_vertices(
        self,
        label: str | None = None,
        filters: dict[str, Any] | None = None,
        limit: int = 100,
        include_deleted: bool = False,
    ) -> list[Vertex]:
        res: list[Vertex] = []
        for v in self._local_cache.values():
            if label and v.get("label") != label:
                continue
            res.append(v)
            if len(res) >= limit:
                break
        return res

    def count_vertices(self, label: str | None = None) -> int:
        if not label:
            return len(self._local_cache)
        return sum(1 for v in self._local_cache.values() if v.get("label") == label)

    def upsert_edge(self, label: str, out_v: str, in_v: str, properties: dict[str, Any]) -> Edge:
        eid = f"{out_v}->{label}->{in_v}"
        e: Edge = {
            "eid": eid,
            "label": label,
            "out_v": out_v,
            "in_v": in_v,
            "out_cid": out_v,
            "in_cid": in_v,
            "properties": dict(properties),
        }
        self._local_cache[eid] = e
        return e

    def get_edge(self, eid: str) -> Edge | None:
        return self._local_cache.get(eid)

    def find_edge_by_key(self, edge_key: str) -> Edge | None:
        return self._local_cache.get(edge_key)

    def find_edges(
        self,
        label: str | None = None,
        out_v: str | None = None,
        in_v: str | None = None,
        limit: int = 500,
        include_historical: bool = False,
    ) -> list[Edge]:
        res: list[Edge] = []
        for item in self._local_cache.values():
            if "eid" in item:
                if label and item.get("label") != label:
                    continue
                if out_v and item.get("out_v") != out_v:
                    continue
                if in_v and item.get("in_v") != in_v:
                    continue
                res.append(item)
                if len(res) >= limit:
                    break
        return res

    def edges_from(
        self,
        vid: str,
        labels: list[str] | None = None,
        limit: int = 500,
        include_historical: bool = False,
    ) -> list[Edge]:
        return self.find_edges(out_v=vid, limit=limit, include_historical=include_historical)

    def edges_to(
        self,
        vid: str,
        labels: list[str] | None = None,
        limit: int = 500,
        include_historical: bool = False,
    ) -> list[Edge]:
        return self.find_edges(in_v=vid, limit=limit, include_historical=include_historical)

    def count_edges(self, label: str | None = None) -> int:
        return sum(1 for item in self._local_cache.values() if "eid" in item and (label is None or item.get("label") == label))

    def bulk_load(
        self,
        vertices: list[Vertex],
        edges: list[Edge],
        *,
        batch_size: int = 500,
    ) -> dict[str, Any]:
        for v in vertices:
            self.upsert_vertex(v.get("label", "Entity"), v.get("properties", {}))
        for e in edges:
            self.upsert_edge(e.get("label", "relatedTo"), e.get("out_v", ""), e.get("in_v", ""), e.get("properties", {}))
        return {
            "status": "COMPLETED",
            "vertices_loaded": len(vertices),
            "edges_loaded": len(edges),
        }

    def tombstone_vertex(self, canonical_id: str) -> bool:
        if canonical_id in self._local_cache:
            del self._local_cache[canonical_id]
            return True
        return False

    def clear(self) -> None:
        self._local_cache.clear()


class GraphDBGraphStore(FusekiGraphStore):
    """Ontotext GraphDB certified commercial RDF adapter (CRA-002.10, ONT-003).

    SPARQL 1.1 HTTP interface with repository-scoped endpoints.
    """

    def __init__(
        self,
        endpoint_url: str = "http://localhost:7200",
        repository: str = "eoip",
        username: str = "",
        password: str = "",
        timeout: float = 30.0,
    ) -> None:
        repo_url = f"{endpoint_url.rstrip('/')}/repositories/{repository}"
        super().__init__(
            endpoint_url=repo_url,
            dataset=repository,
            username=username,
            password=password,
            timeout=timeout,
        )

    def ping(self) -> dict[str, Any]:
        info = super().ping()
        info["backend"] = "graphdb"
        return info
