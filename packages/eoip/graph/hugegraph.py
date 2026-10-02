"""Persistent HugeGraph REST adapter. MemoryGraphStore is never used here.

HugeGraph edge labels have one source/target label pair. Physical names encode
that pair; callers continue to see the ontology's logical relationship names.
Timestamps are stored as ISO-8601 TEXT to preserve the public contract exactly.
"""

from __future__ import annotations

import hashlib
import json
from threading import RLock
from urllib.parse import quote

import httpx
from eoip.contracts.source_event import utc_now_iso
from eoip.graph.memory import edge_key
from eoip.ontology.manifest import (
    EDGE_LABELS,
    INDEXES,
    PROPERTY_KEYS,
    VERTEX_LABELS,
    edge_endpoints_valid,
)


class HugeGraphStore:
    def __init__(self, url: str, graph: str = "hugegraph", username: str = "admin", password: str = ""):
        self.client = httpx.Client(
            base_url=url.rstrip("/"),
            timeout=30,
            auth=(username, password) if password else None,
            trust_env=False,
        )
        self.base = f"/graphspaces/DEFAULT/graphs/{quote(graph, safe='')}"
        self.graph = graph
        self._lock = RLock()

    def close(self):
        self.client.close()

    def _request(self, method, path, **kwargs):
        response = self.client.request(method, self.base + path, **kwargs)
        response.raise_for_status()
        return response.json() if response.content else None

    def health(self):
        try:
            self._request("GET", "/schema/vertexlabels")
            return True
        except (httpx.HTTPError, ValueError):
            return False

    def ping(self):
        return {
            "backend": "hugegraph",
            "graph": self.graph,
            "status": "ok" if self.health() else "unavailable",
        }

    @staticmethod
    def vertex_id(cid):
        return "eoip-" + hashlib.sha256(cid.encode()).hexdigest()

    @staticmethod
    def _id_path(value, *, vertex=False):
        return quote(json.dumps(value) if vertex else str(value), safe="")

    def schema_status(self):
        labels = self._request("GET", "/schema/vertexlabels")["vertexlabels"]
        return {"initialized": set(VERTEX_LABELS).issubset({item["name"] for item in labels})}

    def ensure_schema(self, manifest=None):
        created = False
        with self._lock:

            def ensure(kind, items):
                nonlocal created
                existing_items = self._request("GET", f"/schema/{kind}")[kind]
                existing = {item["name"]: item for item in existing_items}
                for item in items:
                    current = existing.get(item["name"])
                    if current is None:
                        self._request("POST", f"/schema/{kind}", json=item)
                        created = True
                    elif kind in {"vertexlabels", "edgelabels"}:
                        missing_properties = sorted(
                            set(item["properties"]) - set(current.get("properties", []))
                        )
                        if missing_properties:
                            self._request(
                                "PUT",
                                f"/schema/{kind}/{quote(item['name'], safe='')}",
                                params={"action": "append"},
                                json={
                                    "name": item["name"],
                                    "properties": missing_properties,
                                    "nullable_keys": missing_properties,
                                },
                            )
                            created = True

            ensure(
                "propertykeys",
                [
                    {"name": key, "data_type": "TEXT" if kind == "DATE" else kind, "cardinality": "SINGLE"}
                    for key, kind in PROPERTY_KEYS.items()
                ],
            )
            all_keys = list(PROPERTY_KEYS)
            ensure(
                "vertexlabels",
                [
                    {
                        "name": name,
                        "id_strategy": "CUSTOMIZE_STRING",
                        "properties": all_keys,
                        "nullable_keys": [k for k in all_keys if k != "canonical_id"],
                        "enable_label_index": True,
                    }
                    for name in VERTEX_LABELS
                ],
            )
            edges = []
            for label, (outs, ins, _) in EDGE_LABELS.items():
                for out_label in outs:
                    for in_label in ins:
                        edges.append(
                            {
                                "name": f"{label}__{out_label}__{in_label}",
                                "source_label": out_label,
                                "target_label": in_label,
                                "frequency": "MULTIPLE",
                                "sort_keys": ["edge_key"],
                                "properties": all_keys,
                                "nullable_keys": [k for k in all_keys if k != "edge_key"],
                                "enable_label_index": True,
                            }
                        )
            ensure("edgelabels", edges)
            index_defs = []
            for idx in INDEXES:
                if idx["label"] is not None:
                    index_defs.append({
                        "name": idx["name"],
                        "base_type": "VERTEX_LABEL",
                        "base_value": idx["label"],
                        "index_type": idx["type"],
                        "fields": idx["fields"],
                    })
                else:
                    for vl in VERTEX_LABELS:
                        if all(f in PROPERTY_KEYS for f in idx["fields"]):
                            index_defs.append({
                                "name": f"{idx['name']}_{vl}",
                                "base_type": "VERTEX_LABEL",
                                "base_value": vl,
                                "index_type": idx["type"],
                                "fields": idx["fields"],
                            })
            ensure("indexlabels", index_defs)
        return {"created": created, "initialized": True}

    def _properties(self, properties):
        unknown = set(properties) - set(PROPERTY_KEYS)
        if unknown:
            raise ValueError(f"Unknown properties: {sorted(unknown)}")
        return {k: v for k, v in properties.items() if v is not None}

    def _vertex(self, raw):
        return {
            "vid": raw["id"],
            "canonical_id": raw["properties"]["canonical_id"],
            "label": raw["label"],
            "properties": raw["properties"],
        }

    def _edge(self, raw):
        source, target = self.get_vertex(raw["outV"]), self.get_vertex(raw["inV"])
        return {
            "eid": raw["id"],
            "label": raw["label"].split("__")[0],
            "out_v": raw["outV"],
            "in_v": raw["inV"],
            "out_cid": source["canonical_id"],
            "in_cid": target["canonical_id"],
            "properties": raw["properties"],
        }

    def get_vertex(self, vid):
        try:
            return self._vertex(self._request("GET", "/graph/vertices/" + self._id_path(vid, vertex=True)))
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                return None
            raise

    def get_vertex_by_canonical_id(self, canonical_id):
        return self.get_vertex(self.vertex_id(canonical_id))

    def upsert_vertex(self, label, properties):
        if label not in VERTEX_LABELS:
            raise ValueError(f"Unknown vertex label: {label}")
        required = VERTEX_LABELS[label][1]
        if any(properties.get(k) is None for k in required):
            raise ValueError(f"Missing required properties for {label}: {required}")
        props = self._properties(properties)
        props.setdefault("entity_type", label)
        props.setdefault("graph_domain", VERTEX_LABELS[label][0])
        vid = self.vertex_id(props["canonical_id"])
        with self._lock:
            existing = self.get_vertex(vid)
            if existing:
                if existing["label"] != label:
                    raise ValueError("Canonical identity cannot change vertex type")
                if "first_seen" in existing["properties"]:
                    props["first_seen"] = existing["properties"]["first_seen"]
                raw = self._request(
                    "PUT",
                    "/graph/vertices/" + self._id_path(vid, vertex=True),
                    params={"action": "append"},
                    json={"label": label, "properties": props},
                )
            else:
                raw = self._request(
                    "POST", "/graph/vertices", json={"id": vid, "label": label, "properties": props}
                )
        return self._vertex(raw)

    def _pages(self, kind, params=None):
        page = ""
        while True:
            data = self._request(
                "GET", f"/graph/{kind}", params={**(params or {}), "page": page, "limit": 500}
            )
            yield from data[kind]
            page = data.get("page")
            if not page:
                break

    def find_vertices(self, label=None, filters=None, limit=100):
        if label is not None and label not in VERTEX_LABELS:
            raise ValueError("Unknown vertex label")
        result = []
        for raw in self._pages("vertices", {"label": label} if label else None):
            props = raw["properties"]
            if props.get("deleted_at") or (filters and any(props.get(k) != v for k, v in filters.items())):
                continue
            result.append(self._vertex(raw))
            if len(result) >= limit:
                break
        return result

    def count_vertices(self, label=None):
        return sum(
            1
            for raw in self._pages("vertices", {"label": label} if label else None)
            if not raw["properties"].get("deleted_at")
        )

    def upsert_edge(self, label, out_v, in_v, properties):
        source, target = self.get_vertex(out_v), self.get_vertex(in_v)
        if not source or not target or not edge_endpoints_valid(label, source["label"], target["label"]):
            raise ValueError(f"Invalid endpoint types for {label}")
        props = self._properties(properties)
        props.setdefault(
            "edge_key",
            edge_key(label, source["canonical_id"], target["canonical_id"], props.get("fact_key", "")),
        )
        props.setdefault("creation_status", "DETERMINISTIC")
        physical_label = f"{label}__{source['label']}__{target['label']}"
        raw = self._request(
            "POST",
            "/graph/edges",
            json={
                "label": physical_label,
                "outV": out_v,
                "inV": in_v,
                "outVLabel": source["label"],
                "inVLabel": target["label"],
                "properties": props,
            },
        )
        return self._edge(raw)

    def get_edge(self, eid):
        try:
            return self._edge(self._request("GET", "/graph/edges/" + self._id_path(eid)))
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                return None
            raise

    def find_edges(self, label=None, out_v=None, in_v=None, limit=500):
        params = {}
        if out_v or in_v:
            params = {"vertex_id": json.dumps(out_v or in_v), "direction": "OUT" if out_v else "IN"}
        result = []
        for raw in self._pages("edges", params):
            if label and raw["label"].split("__")[0] != label:
                continue
            if out_v and raw["outV"] != out_v or in_v and raw["inV"] != in_v:
                continue
            result.append(self._edge(raw))
            if len(result) >= limit:
                break
        return result

    def edges_from(self, vid, labels=None, limit=500):
        return [e for e in self.find_edges(out_v=vid, limit=limit) if not labels or e["label"] in labels]

    def edges_to(self, vid, labels=None, limit=500):
        return [e for e in self.find_edges(in_v=vid, limit=limit) if not labels or e["label"] in labels]

    def count_edges(self, label=None):
        return sum(1 for raw in self._pages("edges") if not label or raw["label"].split("__")[0] == label)

    def tombstone_vertex(self, canonical_id):
        vertex = self.get_vertex_by_canonical_id(canonical_id)
        if not vertex:
            return False
        self.upsert_vertex(vertex["label"], {**vertex["properties"], "deleted_at": utc_now_iso()})
        return True

    def clear(self):
        raise RuntimeError(
            "Runtime graph deletion is disabled; use an isolated test deployment for destructive tests"
        )
