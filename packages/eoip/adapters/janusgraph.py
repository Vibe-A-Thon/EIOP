"""JanusGraph adapter: TinkerPop Gremlin script HTTP over JanusGraph Server.

Real protocol-compatible adapter (no new deps — reuses ``httpx`` like
``eoip.graph.hugegraph``/``neptune``). JanusGraph exposes the standard
Gremlin Server HTTP endpoint (``POST {url}/gremlin`` with body
``{"gremlin": <script>, "bindings": {...}}`` and a ``result.data`` envelope),
so this adapter submits parameter-bound Gremlin scripts and normalizes the
GraphSON-ish vertex/edge payloads back onto the EOIP GraphStore contract:

* vertices keyed by ``canonical_id`` with deterministic ``eoip vid``,
* edges keyed by EOIP's deterministic ``edge_key``.

Backend-specific behavior is recorded in the manifest (SR-GDB-003): JanusGraph
does not enforce EOIP's ontology manifest; labels/properties are created on
first write (schema-flexible mode), and multi-valued properties are not used.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable
from typing import Any

import httpx

from eoip.graph.memory import edge_key
from eoip.graph.store import BulkLoadError, GraphQueryTimeout, remaining_query_seconds

Transport = Callable[[str, dict[str, Any]], dict[str, Any]]
"""Injectable request transport for tests/air-gap: (script, bindings) -> result envelope."""


class JanusGraphStore:
    """GraphStore implementation for JanusGraph via Gremlin HTTP scripts."""

    def __init__(
        self,
        url: str,
        graph: str = "g",
        traversal_source: str = "g",
        username: str = "",
        password: str = "",
        transport: Transport | None = None,
    ):
        self.url = url.rstrip("/")
        self.graph = graph
        self.traversal_source = traversal_source
        self._transport = transport
        if transport is None:
            self._client: httpx.Client | None = httpx.Client(
                timeout=30,
                auth=(username, password) if password else None,
                trust_env=False,
            )
        else:
            self._client = None

    # -- transport ------------------------------------------------------------
    def close(self):
        if self._client is not None:
            self._client.close()

    def _submit(self, script: str, bindings: dict[str, Any] | None = None) -> Any:
        """Submit a Gremlin script and return ``result.data``."""
        payload = {"gremlin": script, "bindings": bindings or {}}
        if self._transport is not None:
            envelope = self._transport(script, bindings or {})
            return self._unwrap(envelope)
        assert self._client is not None
        remaining = remaining_query_seconds()
        kwargs: dict[str, Any] = {}
        if remaining is not None:
            kwargs["timeout"] = max(0.001, remaining)
        try:
            response = self._client.post(f"{self.url}/gremlin", json=payload, **kwargs)
        except httpx.TimeoutException as exc:
            if remaining is None:
                raise
            raise GraphQueryTimeout("JanusGraph request exceeded the traversal time budget") from exc
        response.raise_for_status()
        return self._unwrap(response.json() if response.content else {})

    @staticmethod
    def _unwrap(envelope: dict[str, Any]) -> Any:
        if envelope.get("code", 200) >= 400 or envelope.get("status", {}).get("message"):
            message = envelope.get("message") or envelope.get("status", {}).get("message")
            raise RuntimeError(f"Gremlin error: {message}")
        result = envelope.get("result") or {}
        data = result.get("data", [])
        if isinstance(data, dict) and data.get("@type") == "g:List":
            data = data.get("@value", [])
        return data

    # -- identity ---------------------------------------------------------------
    @staticmethod
    def vertex_id(cid: str) -> str:
        return "eoip-" + hashlib.sha256(cid.encode()).hexdigest()

    @staticmethod
    def _gremlin_string(value: Any) -> str:
        if not isinstance(value, str) or not value:
            return json.dumps(value)
        if value.replace("_", "a").isalnum() and value[0].isalpha():
            return value
        return json.dumps(value)

    # -- normalization ----------------------------------------------------------
    @staticmethod
    def _to_vertex(raw: Any) -> dict | None:
        if raw is None:
            return None
        if isinstance(raw, list):
            raw = raw[0] if raw else None
        if raw is None:
            return None
        if not isinstance(raw, dict):
            return None
        props = raw.get("properties") if isinstance(raw.get("properties"), dict) else {
            k: v for k, v in raw.items() if k not in {"id", "label", "type"}
        }
        flat: dict[str, Any] = {}
        for key, value in props.items():
            if isinstance(value, list) and value and isinstance(value[0], dict) and "value" in value[0]:
                flat[key] = value[0]["value"]
            elif isinstance(value, dict) and "@value" in value:
                flat[key] = value["@value"]
            else:
                flat[key] = value
        label = raw.get("label", flat.get("entity_type", ""))
        vid = str(raw.get("id", ""))
        return {
            "vid": vid,
            "canonical_id": flat.get("canonical_id", vid),
            "label": label,
            "properties": flat,
        }

    @staticmethod
    def _to_edge(raw: Any) -> dict | None:
        if isinstance(raw, list):
            raw = raw[0] if raw else None
        if not isinstance(raw, dict):
            return None
        props = raw.get("properties") if isinstance(raw.get("properties"), dict) else {}
        flat: dict[str, Any] = {}
        for key, value in props.items():
            if isinstance(value, dict) and "@value" in value:
                flat[key] = value["@value"]
            else:
                flat[key] = value
        out_v = raw.get("outV") or raw.get("out_v") or ""
        in_v = raw.get("inV") or raw.get("in_v") or ""
        return {
            "eid": str(raw.get("id", "")),
            "label": raw.get("label", ""),
            "out_v": str(out_v),
            "in_v": str(in_v),
            "out_cid": flat.get("out_cid", ""),
            "in_cid": flat.get("in_cid", ""),
            "properties": flat,
        }

    # -- schema -------------------------------------------------------------------
    def ensure_schema(self, manifest: dict) -> dict:
        # JanusGraph is schema-flexible here; indexes/constraints are managed
        # out-of-band by deployment config (recorded in manifest notes).
        return {"created": False, "note": "schema-flexible mode; managed externally"}

    def schema_status(self) -> dict:
        return {"initialized": True, "mode": "schema-flexible"}

    # -- health -------------------------------------------------------------------
    def health(self) -> bool:
        try:
            self._submit(f"{self.traversal_source}.V().limit(1).count()")
            return True
        except Exception:  # noqa: BLE001 - any Gremlin/transport failure means unavailable
            return False

    def ping(self) -> dict:
        return {
            "backend": "janusgraph",
            "graph": self.graph,
            "status": "ok" if self.health() else "unavailable",
        }

    # -- vertices -------------------------------------------------------------------
    def upsert_vertex(self, label: str, properties: dict) -> dict:
        cid = properties.get("canonical_id")
        if not cid:
            raise ValueError("canonical_id is required")
        assigns = ", ".join(
            f".property({json.dumps('p_' + k)}, p_{k})" for k in properties
        )
        script = (
            f"{self.traversal_source}.V().hasLabel({json.dumps(label)})"
            f".has('canonical_id', cid).fold().coalesce("
            f"unfold(), addV({json.dumps(label)}).property('canonical_id', cid))"
            f"{assigns}.elementMap().toList()"
        )
        bindings = {"cid": cid, **{f"p_{k}": v for k, v in properties.items()}}
        data = self._submit(script, bindings)
        vertex = self._to_vertex(data)
        if vertex is None:
            raise RuntimeError(f"JanusGraph did not return a vertex for canonical_id={cid}")
        return vertex

    def get_vertex(self, vid: str) -> dict | None:
        script = f"{self.traversal_source}.V(vid).elementMap().toList()"
        return self._to_vertex(self._submit(script, {"vid": self._coerce_id(vid)}))

    def get_vertex_by_canonical_id(self, canonical_id: str) -> dict | None:
        script = (
            f"{self.traversal_source}.V().has('canonical_id', cid).elementMap().toList()"
        )
        return self._to_vertex(self._submit(script, {"cid": canonical_id}))

    def _coerce_id(self, vid: str) -> Any:
        try:
            return int(vid)
        except (TypeError, ValueError):
            return vid

    def find_vertex_by_property(
        self, label: str, key: str, value: Any, limit: int = 10, include_deleted: bool = False
    ) -> list[dict]:
        script = (
            f"{self.traversal_source}.V().hasLabel({json.dumps(label)}).has({json.dumps(key)}, val)"
            f".limit({int(limit)}).elementMap().toList()"
        )
        out = []
        for raw in self._submit(script, {"val": value}) or []:
            vertex = self._to_vertex(raw)
            if vertex is None:
                continue
            if not include_deleted and vertex["properties"].get("deleted_at"):
                continue
            out.append(vertex)
        return out

    def find_vertices(
        self,
        label: str | None = None,
        filters: dict[str, Any] | None = None,
        limit: int = 100,
        include_deleted: bool = False,
    ) -> list[dict]:
        traversal = f"{self.traversal_source}.V()"
        if label:
            traversal += f".hasLabel({json.dumps(label)})"
        bindings: dict[str, Any] = {}
        for i, (key, value) in enumerate(sorted((filters or {}).items())):
            traversal += f".has({json.dumps(key)}, f{i})"
            bindings[f"f{i}"] = value
        traversal += f".limit({int(limit)}).elementMap().toList()"
        out = []
        for raw in self._submit(traversal, bindings) or []:
            vertex = self._to_vertex(raw)
            if vertex is None:
                continue
            if not include_deleted and vertex["properties"].get("deleted_at"):
                continue
            out.append(vertex)
        return out

    def count_vertices(self, label: str | None = None) -> int:
        script = f"{self.traversal_source}.V(){'.hasLabel(' + json.dumps(label) + ')' if label else ''}.count().toList()"
        data = self._submit(script)
        if isinstance(data, list) and data:
            return int(data[0])
        return 0

    # -- edges ----------------------------------------------------------------------
    def upsert_edge(self, label: str, out_v: str, in_v: str, properties: dict) -> dict:
        key = properties.get("edge_key") or edge_key(label, properties.get("out_cid", out_v), properties.get("in_cid", in_v))
        props = {**properties, "edge_key": key}
        assigns = ", ".join(f".property({json.dumps('p_' + k)}, p_{k})" for k in props)
        script = (
            f"{self.traversal_source}.V(outV).as('o').V(inV).as('i')"
            f".select('o').outE({json.dumps(label)}).has('edge_key', key).inV().as('i2')"
            f".select('o', 'i2').where('i2', eq('i')).select('o')"
            f".outE({json.dumps(label)}).has('edge_key', key).fold().coalesce("
            f"unfold(), select('o').addE({json.dumps(label)}).to(select('i')).property('edge_key', key))"
            f"{assigns}.elementMap().toList()"
        )
        bindings = {
            "outV": self._coerce_id(out_v),
            "inV": self._coerce_id(in_v),
            "key": key,
            **{f"p_{k}": v for k, v in props.items()},
        }
        data = self._submit(script, bindings)
        edge = self._to_edge(data)
        if edge is None:
            raise RuntimeError(f"JanusGraph did not return an edge for edge_key={key}")
        return edge

    def get_edge(self, eid: str) -> dict | None:
        script = f"{self.traversal_source}.E(eid).elementMap().toList()"
        return self._to_edge(self._submit(script, {"eid": self._coerce_id(eid)}))

    def find_edge_by_key(self, key: str) -> dict | None:
        script = f"{self.traversal_source}.E().has('edge_key', key).elementMap().toList()"
        return self._to_edge(self._submit(script, {"key": key}))

    def _find_edges(
        self,
        label: str | None = None,
        out_v: str | None = None,
        in_v: str | None = None,
        limit: int = 500,
    ) -> list[dict]:
        script = f"{self.traversal_source}.E()"
        if label:
            script += f".hasLabel({json.dumps(label)})"
        if out_v:
            script += ".has('out_cid', outC)"
        if in_v:
            script += ".has('in_cid', inC)"
        script += f".limit({int(limit)}).elementMap().toList()"
        bindings: dict[str, Any] = {}
        if out_v:
            bindings["outC"] = out_v
        if in_v:
            bindings["inC"] = in_v
        out = []
        for raw in self._submit(script, bindings) or []:
            edge = self._to_edge(raw)
            if edge is not None:
                out.append(edge)
        return out

    def find_edges(
        self,
        label: str | None = None,
        out_v: str | None = None,
        in_v: str | None = None,
        limit: int = 500,
        include_historical: bool = False,
    ) -> list[dict]:
        return self._find_edges(label, out_v, in_v, limit)

    def edges_from(self, vid: str, labels: list[str] | None = None, limit: int = 500, include_historical: bool = False) -> list[dict]:
        label_filter = ",".join(json.dumps(l) for l in labels) if labels else ""
        script = (
            f"{self.traversal_source}.V(vid).outE({label_filter}).limit({int(limit)}).elementMap().toList()"
            if label_filter
            else f"{self.traversal_source}.V(vid).outE().limit({int(limit)}).elementMap().toList()"
        )
        return [e for raw in self._submit(script, {"vid": self._coerce_id(vid)}) or [] if (e := self._to_edge(raw))]

    def edges_to(self, vid: str, labels: list[str] | None = None, limit: int = 500, include_historical: bool = False) -> list[dict]:
        label_filter = ",".join(json.dumps(l) for l in labels) if labels else ""
        script = (
            f"{self.traversal_source}.V(vid).inE({label_filter}).limit({int(limit)}).elementMap().toList()"
            if label_filter
            else f"{self.traversal_source}.V(vid).inE().limit({int(limit)}).elementMap().toList()"
        )
        return [e for raw in self._submit(script, {"vid": self._coerce_id(vid)}) or [] if (e := self._to_edge(raw))]

    def count_edges(self, label: str | None = None) -> int:
        script = f"{self.traversal_source}.E(){'.hasLabel(' + json.dumps(label) + ')' if label else ''}.count().toList()"
        data = self._submit(script)
        if isinstance(data, list) and data:
            return int(data[0])
        return 0

    # -- maintenance ------------------------------------------------------------------
    def bulk_load(self, vertices: list[dict], edges: list[dict], *, batch_size: int = 500) -> dict:
        committed_v = 0
        committed_e = 0
        try:
            for start in range(0, len(vertices), batch_size):
                for vertex in vertices[start : start + batch_size]:
                    self.upsert_vertex(vertex.get("label", ""), dict(vertex.get("properties", {})))
                    committed_v += 1
            for start in range(0, len(edges), batch_size):
                for edge in edges[start : start + batch_size]:
                    self.upsert_edge(
                        edge.get("label", ""),
                        edge.get("out_v", ""),
                        edge.get("in_v", ""),
                        dict(edge.get("properties", {})),
                    )
                    committed_e += 1
        except Exception as exc:
            raise BulkLoadError(
                f"JanusGraph bulk load failed: {exc}",
                vertices_committed=committed_v,
                edges_committed=committed_e,
            ) from exc
        return {"vertices": committed_v, "edges": committed_e}

    def tombstone_vertex(self, canonical_id: str) -> bool:
        from eoip.contracts.source_event import utc_now_iso

        script = (
            f"{self.traversal_source}.V().has('canonical_id', cid)"
            f".property('deleted_at', {json.dumps(utc_now_iso())}).iterate()"
        )
        before = self.count_vertices()
        self._submit(script, {"cid": canonical_id})
        return self.count_vertices() <= before

    def clear(self) -> None:
        self._submit(f"{self.traversal_source}.V().drop().iterate()")
