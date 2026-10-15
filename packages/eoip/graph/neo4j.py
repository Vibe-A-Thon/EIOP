"""Neo4j GraphStore adapter using the transactional Cypher HTTP API.

The adapter keeps EOIP's canonical GraphStore contract independent of the
underlying graph engine.  Vertices are keyed by ``canonical_id`` and the
portable ``eoip_vid`` property; relationships are keyed by deterministic
``edge_key`` values.
"""

from __future__ import annotations

import hashlib
import re
from threading import RLock
from typing import Any

import httpx
from eoip.contracts.source_event import utc_now_iso
from eoip.graph.memory import edge_key
from eoip.graph.store import BulkLoadError, GraphQueryTimeout, remaining_query_seconds
from eoip.ontology.manifest import EDGE_LABELS, VERTEX_LABELS

_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _name(value: str) -> str:
    if not _IDENTIFIER_RE.fullmatch(value):
        raise ValueError(f"Unsafe graph identifier: {value!r}")
    return f"`{value}`"


class Neo4jGraphStore:
    """GraphStore implementation for Neo4j over HTTP Cypher.

    This intentionally avoids requiring the optional Neo4j Python driver for
    the core product runtime. Deployments that prefer Bolt can still add a
    separate adapter behind the same GraphStore port later.
    """

    def __init__(
        self,
        url: str,
        *,
        database: str = "neo4j",
        username: str = "",
        password: str = "",
        verify: bool = True,
        timeout: float = 30.0,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self.database = database
        self.endpoint = f"/db/{database}/tx/commit"
        self.client = httpx.Client(
            base_url=url.rstrip("/"),
            timeout=timeout,
            auth=(username, password) if username or password else None,
            verify=verify,
            trust_env=False,
            transport=transport,
        )
        self._lock = RLock()

    def close(self) -> None:
        self.client.close()

    @staticmethod
    def vertex_id(canonical_id: str) -> str:
        return "eoip-" + hashlib.sha256(canonical_id.encode()).hexdigest()

    def _cypher(self, statement: str, parameters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        remaining = remaining_query_seconds()
        try:
            response = self.client.post(
                self.endpoint,
                json={
                    "statements": [
                        {
                            "statement": statement,
                            "parameters": parameters or {},
                            "resultDataContents": ["row"],
                        }
                    ]
                },
                timeout=max(0.001, remaining) if remaining is not None else None,
            )
        except httpx.TimeoutException as exc:
            if remaining is None:
                raise
            raise GraphQueryTimeout("Neo4j Cypher query exceeded the time budget") from exc
        response.raise_for_status()
        payload = response.json() if response.content else {}
        errors = payload.get("errors") or []
        if errors:
            message = errors[0].get("message") if isinstance(errors[0], dict) else str(errors[0])
            raise RuntimeError(f"Neo4j query failed: {message}")
        result = (payload.get("results") or [{}])[0]
        columns = result.get("columns") or []
        rows = []
        for item in result.get("data") or []:
            row = item.get("row") or []
            rows.append(dict(zip(columns, row, strict=False)))
        return rows

    def health(self) -> bool:
        try:
            self._cypher("RETURN 1 AS ok")
            return True
        except (httpx.HTTPError, RuntimeError, ValueError):
            return False

    def capabilities(self) -> dict[str, Any]:
        return {
            "backend": "neo4j",
            "models": ["property_graph"],
            "query_languages": ["Cypher"],
            "exports": ["cypher", "opencypher", "graphml", "csv", "canonical-json"],
            "native_query_language": "Cypher",
            "architecture": ["self_managed_or_managed", "property_graph"],
        }

    def ping(self) -> dict:
        return {
            "backend": "neo4j",
            "database": self.database,
            "status": "ok" if self.health() else "unavailable",
            "capabilities": self.capabilities(),
        }

    def ensure_schema(self, manifest: dict | None = None) -> dict:
        self._cypher("CREATE CONSTRAINT eoip_canonical_id IF NOT EXISTS FOR (n:EOIPEntity) REQUIRE n.canonical_id IS UNIQUE")
        self._cypher("CREATE INDEX eoip_vid_idx IF NOT EXISTS FOR (n:EOIPEntity) ON (n.eoip_vid)")
        return {"created": False, "initialized": True, "mode": "cypher-constraints"}

    def schema_status(self) -> dict:
        return {"initialized": True, "mode": "cypher-constraints"}

    def _vertex_from_row(self, row: dict[str, Any], prefix: str = "") -> dict:
        props = dict(row.get(f"{prefix}props") or {})
        label = row.get(f"{prefix}label") or props.get("entity_type")
        return {
            "vid": row.get(f"{prefix}vid") or props.get("eoip_vid") or self.vertex_id(props["canonical_id"]),
            "canonical_id": props.get("canonical_id"),
            "label": label,
            "properties": props,
        }

    def _edge_from_row(self, row: dict[str, Any], prefix: str = "") -> dict:
        props = dict(row.get(f"{prefix}props") or {})
        return {
            "eid": props.get("edge_key"),
            "label": row.get(f"{prefix}type") or props.get("relationship_type"),
            "out_v": props.get("out_v"),
            "in_v": props.get("in_v"),
            "out_cid": props.get("out_cid"),
            "in_cid": props.get("in_cid"),
            "properties": props,
        }

    def upsert_vertex(self, label: str, properties: dict) -> dict:
        from eoip.validation.gate import check_vertex

        check_vertex(label, properties)
        if label not in VERTEX_LABELS:
            raise ValueError("Unknown vertex label")
        props = {key: value for key, value in properties.items() if value is not None}
        props.setdefault("entity_type", label)
        props.setdefault("graph_domain", VERTEX_LABELS[label][0])
        props["eoip_vid"] = self.vertex_id(props["canonical_id"])
        with self._lock:
            rows = self._cypher(
                f"MERGE (n:EOIPEntity:{_name(label)} {{canonical_id: $canonical_id}}) "
                "SET n += $props "
                "RETURN properties(n) AS props, labels(n)[-1] AS label, n.eoip_vid AS vid",
                {"canonical_id": props["canonical_id"], "props": props},
            )
        return self._vertex_from_row(rows[0]) if rows else {
            "vid": props["eoip_vid"],
            "canonical_id": props["canonical_id"],
            "label": label,
            "properties": props,
        }

    def get_vertex(self, vid: str) -> dict | None:
        rows = self._cypher(
            "MATCH (n:EOIPEntity {eoip_vid: $vid}) "
            "RETURN properties(n) AS props, labels(n)[-1] AS label, n.eoip_vid AS vid LIMIT 1",
            {"vid": vid},
        )
        return self._vertex_from_row(rows[0]) if rows else None

    def get_vertex_by_canonical_id(self, canonical_id: str) -> dict | None:
        rows = self._cypher(
            "MATCH (n:EOIPEntity {canonical_id: $canonical_id}) "
            "RETURN properties(n) AS props, labels(n)[-1] AS label, n.eoip_vid AS vid LIMIT 1",
            {"canonical_id": canonical_id},
        )
        return self._vertex_from_row(rows[0]) if rows else None

    def find_vertex_by_property(
        self,
        label: str,
        key: str,
        value: Any,
        limit: int = 10,
        include_deleted: bool = False,
    ) -> list[dict]:
        return self.find_vertices(label=label, filters={key: value}, limit=limit, include_deleted=include_deleted)

    def find_vertices(
        self,
        label: str | None = None,
        filters: dict[str, Any] | None = None,
        limit: int = 100,
        include_deleted: bool = False,
    ) -> list[dict]:
        if label is not None and label not in VERTEX_LABELS:
            raise ValueError("Unknown vertex label")
        filters = filters or {}
        conditions = []
        params: dict[str, Any] = {"limit": limit}
        for index, (key, value) in enumerate(filters.items()):
            pname = f"p{index}"
            conditions.append(f"n.{_name(key)} = ${pname}")
            params[pname] = value
        if not include_deleted:
            conditions.append("(n.deleted_at IS NULL OR n.deleted_at = '')")
        match = f"MATCH (n:EOIPEntity:{_name(label)})" if label else "MATCH (n:EOIPEntity)"
        where = " WHERE " + " AND ".join(conditions) if conditions else ""
        rows = self._cypher(
            f"{match}{where} RETURN properties(n) AS props, labels(n)[-1] AS label, n.eoip_vid AS vid LIMIT $limit",
            params,
        )
        return [self._vertex_from_row(row) for row in rows]

    def count_vertices(self, label: str | None = None) -> int:
        if label is not None and label not in VERTEX_LABELS:
            raise ValueError("Unknown vertex label")
        match = f"MATCH (n:EOIPEntity:{_name(label)})" if label else "MATCH (n:EOIPEntity)"
        rows = self._cypher(f"{match} WHERE n.deleted_at IS NULL OR n.deleted_at = '' RETURN count(n) AS c")
        return int(rows[0]["c"]) if rows else 0

    def upsert_edge(self, label: str, out_v: str, in_v: str, properties: dict) -> dict:
        from eoip.validation.gate import check_edge

        if label not in EDGE_LABELS:
            raise ValueError("Unknown edge label")
        source = self.get_vertex(out_v)
        target = self.get_vertex(in_v)
        if not source or not target:
            raise ValueError(f"Invalid endpoint types for {label}")
        check_edge(label, source["label"], target["label"], properties)
        props = {key: value for key, value in properties.items() if value is not None}
        props.setdefault(
            "edge_key",
            edge_key(label, source["canonical_id"], target["canonical_id"], props.get("fact_key", "")),
        )
        props.setdefault("creation_status", "DETERMINISTIC")
        props.update(
            {
                "relationship_type": label,
                "out_v": source["vid"],
                "in_v": target["vid"],
                "out_cid": source["canonical_id"],
                "in_cid": target["canonical_id"],
            }
        )
        with self._lock:
            rows = self._cypher(
                "MATCH (a:EOIPEntity {eoip_vid: $out_v}), (b:EOIPEntity {eoip_vid: $in_v}) "
                f"MERGE (a)-[r:{_name(label)} {{edge_key: $edge_key}}]->(b) "
                "SET r += $props RETURN properties(r) AS props, type(r) AS type",
                {"out_v": source["vid"], "in_v": target["vid"], "edge_key": props["edge_key"], "props": props},
            )
        return self._edge_from_row(rows[0]) if rows else {
            "eid": props["edge_key"],
            "label": label,
            "out_v": source["vid"],
            "in_v": target["vid"],
            "out_cid": source["canonical_id"],
            "in_cid": target["canonical_id"],
            "properties": props,
        }

    def get_edge(self, eid: str) -> dict | None:
        return self.find_edge_by_key(eid)

    def find_edge_by_key(self, edge_key: str) -> dict | None:
        rows = self._cypher(
            "MATCH ()-[r {edge_key: $edge_key}]->() RETURN properties(r) AS props, type(r) AS type LIMIT 1",
            {"edge_key": edge_key},
        )
        return self._edge_from_row(rows[0]) if rows else None

    def find_edges(
        self,
        label: str | None = None,
        out_v: str | None = None,
        in_v: str | None = None,
        limit: int = 500,
        include_historical: bool = False,
    ) -> list[dict]:
        if label is not None and label not in EDGE_LABELS:
            raise ValueError("Unknown edge label")
        rel = f":{_name(label)}" if label else ""
        conditions = []
        params: dict[str, Any] = {"limit": limit}
        if out_v:
            conditions.append("a.eoip_vid = $out_v")
            params["out_v"] = out_v
        if in_v:
            conditions.append("b.eoip_vid = $in_v")
            params["in_v"] = in_v
        if not include_historical:
            conditions.append("(r.is_current IS NULL OR r.is_current <> false)")
        where = " WHERE " + " AND ".join(conditions) if conditions else ""
        rows = self._cypher(f"MATCH (a:EOIPEntity)-[r{rel}]->(b:EOIPEntity){where} RETURN properties(r) AS props, type(r) AS type LIMIT $limit", params)
        return [self._edge_from_row(row) for row in rows]

    def edges_from(
        self,
        vid: str,
        labels: list[str] | None = None,
        limit: int = 500,
        include_historical: bool = False,
    ) -> list[dict]:
        edges = self.find_edges(out_v=vid, limit=limit, include_historical=include_historical)
        return [edge for edge in edges if not labels or edge["label"] in labels]

    def edges_to(
        self,
        vid: str,
        labels: list[str] | None = None,
        limit: int = 500,
        include_historical: bool = False,
    ) -> list[dict]:
        edges = self.find_edges(in_v=vid, limit=limit, include_historical=include_historical)
        return [edge for edge in edges if not labels or edge["label"] in labels]

    def count_edges(self, label: str | None = None) -> int:
        if label is not None and label not in EDGE_LABELS:
            raise ValueError("Unknown edge label")
        rel = f":{_name(label)}" if label else ""
        rows = self._cypher(
            f"MATCH ()-[r{rel}]->() WHERE r.is_current IS NULL OR r.is_current <> false RETURN count(r) AS c"
        )
        return int(rows[0]["c"]) if rows else 0

    def bulk_load(self, vertices: list[dict], edges: list[dict], *, batch_size: int = 500) -> dict:
        if self.count_vertices() or self.count_edges():
            raise RuntimeError("bulk_load requires an empty graph; use an isolated deployment")
        vertices_committed = 0
        edges_committed = 0
        try:
            id_map: dict[str, str] = {}
            for vertex in vertices:
                created = self.upsert_vertex(vertex["label"], dict(vertex["properties"]))
                vertices_committed += 1
                for key in (vertex.get("vid"), vertex.get("canonical_id"), created["canonical_id"]):
                    if key:
                        id_map[key] = created["vid"]
            for edge in edges:
                self.upsert_edge(
                    edge["label"],
                    id_map.get(edge["out_v"], edge["out_v"]),
                    id_map.get(edge["in_v"], edge["in_v"]),
                    dict(edge["properties"]),
                )
                edges_committed += 1
        except Exception as exc:
            raise BulkLoadError(
                "Neo4j bulk load failed; discard the isolated graph and retry",
                vertices_committed=vertices_committed,
                edges_committed=edges_committed,
            ) from exc
        return {
            "vertices": vertices_committed,
            "edges": edges_committed,
            "vertex_batches": (vertices_committed + batch_size - 1) // batch_size,
            "edge_batches": (edges_committed + batch_size - 1) // batch_size,
            "batch_size": batch_size,
            "mode": "neo4j-cypher-upsert",
        }

    def tombstone_vertex(self, canonical_id: str) -> bool:
        vertex = self.get_vertex_by_canonical_id(canonical_id)
        if not vertex:
            return False
        self.upsert_vertex(vertex["label"], {**vertex["properties"], "deleted_at": utc_now_iso()})
        return True

    def clear(self) -> None:
        raise RuntimeError(
            "Runtime graph deletion is disabled; use an isolated test deployment for destructive tests"
        )
