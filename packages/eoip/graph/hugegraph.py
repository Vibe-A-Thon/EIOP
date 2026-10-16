"""Persistent HugeGraph REST adapter. MemoryGraphStore is never used here.

HugeGraph edge labels have one source/target label pair. Physical names encode
that pair; callers continue to see the ontology's logical relationship names.
Timestamps are stored as ISO-8601 TEXT to preserve the public contract exactly.
"""

from __future__ import annotations

import hashlib
import json
from threading import RLock
from time import monotonic, sleep
from urllib.parse import quote

import httpx
from eoip.contracts.source_event import utc_now_iso
from eoip.graph.memory import edge_key
from eoip.graph.store import BulkLoadError, GraphQueryTimeout, remaining_query_seconds
from eoip.ontology.manifest import (
    EDGE_LABELS,
    INDEXES,
    PROPERTY_KEYS,
    VERTEX_LABELS,
)


class HugeGraphStore:
    _IDENTITY_CACHE_LIMIT = 100_000

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
        self._identity_cache: dict[str, tuple[str, str]] = {}

    def close(self):
        self.client.close()

    def _request(self, method, path, **kwargs):
        remaining = remaining_query_seconds()
        if remaining is not None:
            configured_timeout = kwargs.pop("timeout", None)
            kwargs["timeout"] = max(
                0.001,
                min(remaining, configured_timeout) if configured_timeout is not None else remaining,
            )
        try:
            response = self.client.request(method, self.base + path, **kwargs)
        except httpx.TimeoutException as exc:
            if remaining is None:
                raise
            raise GraphQueryTimeout("Graph store request exceeded the traversal time budget") from exc
        response.raise_for_status()
        return response.json() if response.content else None

    def _wait_schema_task(self, response, timeout_seconds=60.0):
        task_id = response.get("task_id") if isinstance(response, dict) else None
        if task_id is None:
            return
        deadline = monotonic() + timeout_seconds
        while monotonic() < deadline:
            task = self._request("GET", f"/tasks/{quote(str(task_id), safe='')}")
            status = str(task.get("task_status", "")).casefold()
            if status == "success":
                return
            if status in {"failed", "cancelled", "canceled"}:
                raise RuntimeError(
                    f"HugeGraph schema task {task_id} {status}: {task.get('task_result')}"
                )
            sleep(0.05)
        raise TimeoutError(f"HugeGraph schema task {task_id} did not finish within {timeout_seconds}s")

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

    @staticmethod
    def _schema_definitions():
        all_keys = list(PROPERTY_KEYS)
        edges = [
            {
                "name": f"{label}__{out_label}__{in_label}",
                "source_label": out_label,
                "target_label": in_label,
                "frequency": "MULTIPLE",
                "sort_keys": ["edge_key"],
                "properties": all_keys,
                "nullable_keys": [key for key in all_keys if key != "edge_key"],
                "enable_label_index": True,
            }
            for label, (outs, ins, _) in EDGE_LABELS.items()
            for out_label in outs
            for in_label in ins
        ]
        indexes = []
        for idx in INDEXES:
            if idx.get("base_type") == "EDGE_LABEL":
                targets = [edge["name"] for edge in edges]
                base_type = "EDGE_LABEL"
            else:
                targets = [idx["label"]] if idx["label"] is not None else list(VERTEX_LABELS)
                base_type = "VERTEX_LABEL"
            for target in targets:
                indexes.append({
                    "name": idx["name"] if idx.get("label") is not None else f"{idx['name']}_{target}",
                    "base_type": base_type,
                    "base_value": target,
                    "index_type": idx["type"],
                    "fields": idx["fields"],
                })
        return {
            "propertykeys": [
                {"name": key, "data_type": "TEXT" if kind == "DATE" else kind, "cardinality": "SINGLE"}
                for key, kind in PROPERTY_KEYS.items()
            ],
            "vertexlabels": [
                {
                    "name": name,
                    "id_strategy": "CUSTOMIZE_STRING",
                    "primary_keys": [],
                    "properties": all_keys,
                    "nullable_keys": [key for key in all_keys if key != "canonical_id"],
                    "enable_label_index": True,
                }
                for name in VERTEX_LABELS
            ],
            "edgelabels": edges,
            "indexlabels": indexes,
        }

    @staticmethod
    def _check_schema_compatibility(definitions, existing):
        structural_fields = {
            "propertykeys": ("data_type", "cardinality"),
            "vertexlabels": ("id_strategy", "primary_keys", "enable_label_index"),
            "edgelabels": (
                "source_label", "target_label", "frequency", "sort_keys", "enable_label_index",
            ),
            "indexlabels": ("base_type", "base_value", "index_type", "fields"),
        }

        def incompatible(kind, name, field, actual, expected):
            raise ValueError(
                f"Incompatible HugeGraph schema {kind}/{name}: {field} is {actual!r}, "
                f"expected {expected!r}. Bootstrap refused before mutation; "
                "use an explicit, backed-up migration or a separate empty graph."
            )

        for kind, items in definitions.items():
            by_name = {item["name"]: item for item in existing[kind]}
            for item in items:
                current = by_name.get(item["name"])
                if current is None:
                    continue
                for field in structural_fields[kind]:
                    if current.get(field) != item[field]:
                        incompatible(kind, item["name"], field, current.get(field), item[field])
                if kind not in {"vertexlabels", "edgelabels"}:
                    continue
                for field in ("properties", "nullable_keys"):
                    if not isinstance(current.get(field), list):
                        incompatible(kind, item["name"], field, current.get(field), "a list")
                shared = set(item["properties"]) & set(current["properties"])
                actual_nullable = set(current["nullable_keys"]) & shared
                expected_nullable = set(item["nullable_keys"]) & shared
                if actual_nullable != expected_nullable:
                    incompatible(
                        kind, item["name"], "nullable_keys",
                        sorted(actual_nullable), sorted(expected_nullable),
                    )
                missing_required = (
                    set(item["properties"]) - set(item["nullable_keys"]) - set(current["properties"])
                )
                if missing_required:
                    incompatible(
                        kind, item["name"], "required properties", [], sorted(missing_required),
                    )

    def ensure_schema(self, manifest=None):
        created = False
        with self._lock:
            definitions = self._schema_definitions()
            existing_schema = {
                kind: self._request("GET", f"/schema/{kind}")[kind]
                for kind in definitions
            }
            self._check_schema_compatibility(definitions, existing_schema)

            def ensure(kind, items):
                nonlocal created
                existing_items = existing_schema[kind]
                if kind == "indexlabels":
                    # Clean up only the temporary additive names produced by
                    # the interrupted 2026-10 edge-index migration. They are
                    # redundant with idx_edge_key_* and contain no graph data.
                    obsolete = [
                        entry
                        for entry in existing_items
                        if entry["name"].startswith("idx_edge_key_lookup_")
                    ]
                    for entry in obsolete:
                        response = self._request(
                            "DELETE",
                            f"/schema/indexlabels/{quote(entry['name'], safe='')}",
                        )
                        self._wait_schema_task(response)
                        created = True
                    if obsolete:
                        obsolete_names = {entry["name"] for entry in obsolete}
                        existing_items = [
                            entry for entry in existing_items if entry["name"] not in obsolete_names
                        ]
                existing = {item["name"]: item for item in existing_items}
                for item in items:
                    current = existing.get(item["name"])
                    if current is None:
                        response = self._request("POST", f"/schema/{kind}", json=item)
                        if kind == "indexlabels":
                            self._wait_schema_task(response)
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

            for kind, items in definitions.items():
                ensure(kind, items)
        return {"created": created, "initialized": True}

    def _properties(self, properties):
        unknown = set(properties) - set(PROPERTY_KEYS)
        if unknown:
            raise ValueError(f"Unknown properties: {sorted(unknown)}")
        return {k: v for k, v in properties.items() if v is not None}

    def _vertex(self, raw):
        vertex = {
            "vid": raw["id"],
            "canonical_id": raw["properties"]["canonical_id"],
            "label": raw["label"],
            "properties": raw["properties"],
        }
        self._remember_identity(vertex)
        return vertex

    def _remember_identity(self, vertex):
        # Canonical IDs and labels are immutable by graph contract, so caching
        # only this pair cannot hide mutable property updates from other EOIP
        # processes. Clear-on-limit keeps the adapter bounded for large graphs.
        cache = getattr(self, "_identity_cache", None)
        if cache is None:
            cache = self._identity_cache = {}
        if len(cache) >= self._IDENTITY_CACHE_LIMIT and vertex["vid"] not in cache:
            cache.clear()
        cache[vertex["vid"]] = (vertex["canonical_id"], vertex["label"])

    def _vertex_identity(self, vid):
        cached = getattr(self, "_identity_cache", {}).get(vid)
        if cached is not None:
            return cached
        vertex = self.get_vertex(vid)
        if vertex is None:
            raise ValueError(f"Edge references missing vertex: {vid}")
        return vertex["canonical_id"], vertex["label"]

    def _edge(self, raw):
        source_cid, _source_label = self._vertex_identity(raw["outV"])
        target_cid, _target_label = self._vertex_identity(raw["inV"])
        return {
            "eid": raw["id"],
            "label": raw["label"].split("__")[0],
            "out_v": raw["outV"],
            "in_v": raw["inV"],
            "out_cid": source_cid,
            "in_cid": target_cid,
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
        from eoip.validation.gate import check_vertex

        check_vertex(label, properties)
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
                if existing["properties"].get("deleted_at") and "deleted_at" not in properties:
                    props["deleted_at"] = ""
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

    def find_vertex_by_property(
        self, label, key, value, limit=10, include_deleted=False
    ):
        if label not in VERTEX_LABELS:
            raise ValueError("Unknown vertex label")
        result = []
        property_filter = json.dumps({key: value}, separators=(",", ":"))
        for raw in self._pages("vertices", {"label": label, "properties": property_filter}):
            props = raw["properties"]
            if (not include_deleted and props.get("deleted_at")) or props.get(key) != value:
                continue
            result.append(self._vertex(raw))
            if len(result) >= limit:
                break
        return result

    def find_vertices(self, label=None, filters=None, limit=100, include_deleted=False):
        if label is not None and label not in VERTEX_LABELS:
            raise ValueError("Unknown vertex label")
        result = []
        for raw in self._pages("vertices", {"label": label} if label else None):
            props = raw["properties"]
            if (not include_deleted and props.get("deleted_at")) or (
                filters and any(props.get(k) != v for k, v in filters.items())
            ):
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
        from eoip.validation.gate import check_edge

        source, target = self.get_vertex(out_v), self.get_vertex(in_v)
        if not source or not target:
            raise ValueError(f"Invalid endpoint types for {label}")
        check_edge(label, source["label"], target["label"], properties)
        props = self._properties(properties)
        props.setdefault(
            "edge_key",
            edge_key(label, source["canonical_id"], target["canonical_id"], props.get("fact_key", "")),
        )
        props.setdefault("creation_status", "DETERMINISTIC")
        physical_label = f"{label}__{source['label']}__{target['label']}"
        with self._lock:
            existing = self.find_edge_by_key(props["edge_key"], physical_label=physical_label)
            if existing:
                raw = self._request(
                    "PUT",
                    "/graph/edges/" + self._id_path(existing["eid"]),
                    params={"action": "append"},
                    json={"properties": {key: value for key, value in props.items() if key != "edge_key"}},
                )
            else:
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

    def find_edge_by_key(self, edge_key, *, limit=50_000, physical_label=None):
        # Upserts know the physical edge label, allowing HugeGraph to use the
        # per-label edge_key secondary index instead of scanning the graph.
        if physical_label:
            property_filter = json.dumps({"edge_key": edge_key}, separators=(",", ":"))
            try:
                for raw in self._pages(
                    "edges", {"label": physical_label, "properties": property_filter}
                ):
                    if raw["properties"].get("edge_key") == edge_key:
                        return self._edge(raw)
                return None
            except httpx.HTTPStatusError as exc:
                # Pre-migration deployments may still have the old UNIQUE
                # edge index, which HugeGraph 1.7 refuses for property queries.
                if exc.response.status_code != 400 or "NoIndexException" not in exc.response.text:
                    raise
        # Callers without endpoint-label context retain the bounded fallback.
        for edge in self.find_edges(limit=limit, include_historical=True):
            if edge["properties"].get("edge_key") == edge_key:
                return edge
        return None

    def find_edges(self, label=None, out_v=None, in_v=None, limit=500, include_historical=False):
        params = {}
        if out_v or in_v:
            params = {"vertex_id": json.dumps(out_v or in_v), "direction": "OUT" if out_v else "IN"}
        result = []
        for raw in self._pages("edges", params):
            if label and raw["label"].split("__")[0] != label:
                continue
            if out_v and raw["outV"] != out_v or in_v and raw["inV"] != in_v:
                continue
            if not include_historical and raw["properties"].get("is_current") is False:
                continue
            result.append(self._edge(raw))
            if len(result) >= limit:
                break
        return result

    def edges_from(self, vid, labels=None, limit=500, include_historical=False):
        return [e for e in self.find_edges(out_v=vid, limit=limit, include_historical=include_historical) if not labels or e["label"] in labels]

    def edges_to(self, vid, labels=None, limit=500, include_historical=False):
        return [e for e in self.find_edges(in_v=vid, limit=limit, include_historical=include_historical) if not labels or e["label"] in labels]

    def count_edges(self, label=None):
        return sum(
            1
            for raw in self._pages("edges")
            if (not label or raw["label"].split("__")[0] == label)
            and raw["properties"].get("is_current") is not False
        )

    def find_search_candidates(
        self, *, properties, label=None, filters=None, limit=5000, include_deleted=False
    ):
        if label is not None and label not in VERTEX_LABELS:
            raise ValueError("Unknown vertex label")
        if not 1 <= limit <= 5000:
            raise ValueError("Search candidate limit must be between 1 and 5000")
        gremlin = "g.V()"
        if label is not None:
            gremlin += ".hasLabel(search_label)"
        if not include_deleted:
            gremlin += ".not(__.has('deleted_at', neq('')))"
        if filters:
            gremlin += """.filter { v -> filter_values.every { key, value ->
                (v.get().property(key).isPresent() ? v.get().value(key) : null) == value } }"""
        gremlin += """.limit(candidate_limit).project('id', 'label', 'properties')
            .by(id()).by(label()).by(valueMap(*search_properties))"""
        rows = self.execute_gremlin(gremlin, {
            "search_label": label,
            "include_deleted": include_deleted,
            "filter_values": filters or {},
            "candidate_limit": limit,
            "search_properties": sorted(set(properties) | {"canonical_id"}),
        })
        return [
            self._vertex({
                "id": row["id"],
                "label": row["label"],
                "properties": {key: values[0] for key, values in row["properties"].items()},
            })
            for row in rows
        ]

    def execute_gremlin(self, gremlin: str, bindings: dict | None = None) -> list:
        remaining = remaining_query_seconds()
        try:
            response = self.client.post(
                "/gremlin",
                json={
                    "gremlin": gremlin, "bindings": bindings or {}, "language": "gremlin-groovy",
                    "aliases": {"g": f"__g_DEFAULT-{self.graph}"},
                },
                timeout=max(0.001, remaining) if remaining is not None else 30,
            )
        except httpx.TimeoutException as exc:
            if remaining is None:
                raise
            raise GraphQueryTimeout("Graph traversal exceeded the query time budget") from exc
        response.raise_for_status()
        payload = response.json()
        status = payload.get("status", {})
        if status.get("code", 200) != 200:
            raise RuntimeError(f"HugeGraph traversal failed: {status.get('message', status)}")
        return payload["result"]["data"]

    def bulk_load(self, vertices, edges, *, batch_size=500):
        """Load a prevalidated logical snapshot through native batch POSTs.

        This is an offline baseline/restore path, not an online upsert path.
        HugeGraph 1.7 batch PUT conflicts with UNIQUE vertex indexes, while
        batch POST provides a single transaction per bounded request. The
        empty-graph guard makes retries explicit: discard the isolated volume
        after a partial failure and start again.
        """
        from eoip.validation.gate import check_edge, check_vertex

        if not 1 <= batch_size <= 1000:
            raise ValueError("batch_size must be between 1 and 1000")
        vertices = list(vertices)
        edges = list(edges)
        if not vertices:
            raise ValueError("bulk_load requires at least one vertex")
        if self.count_vertices() or self.count_edges():
            raise RuntimeError("bulk_load requires an empty graph; use an isolated deployment")

        normalized_vertices = []
        endpoints = {}
        canonical_ids = set()
        for vertex in vertices:
            label = vertex["label"]
            properties = dict(vertex["properties"])
            check_vertex(label, properties)
            canonical_id = properties["canonical_id"]
            if vertex.get("canonical_id", canonical_id) != canonical_id:
                raise ValueError("bulk vertex canonical_id does not match its properties")
            if canonical_id in canonical_ids:
                raise ValueError(f"duplicate canonical_id in bulk load: {canonical_id}")
            canonical_ids.add(canonical_id)
            properties = self._properties(properties)
            properties.setdefault("entity_type", label)
            properties.setdefault("graph_domain", VERTEX_LABELS[label][0])
            vid = self.vertex_id(canonical_id)
            normalized = {"id": vid, "label": label, "properties": properties}
            normalized_vertices.append(normalized)
            identity = (vid, canonical_id, label)
            for reference in {vertex.get("vid"), vertex.get("canonical_id"), canonical_id, vid}:
                if reference is not None:
                    endpoints[reference] = identity

        normalized_edges = []
        edge_keys = set()
        for edge in edges:
            try:
                out_vid, out_cid, out_label = endpoints[edge["out_v"]]
                in_vid, in_cid, in_label = endpoints[edge["in_v"]]
            except KeyError as exc:
                raise ValueError(f"bulk edge references missing vertex: {exc.args[0]}") from exc
            label = edge["label"]
            properties = dict(edge["properties"])
            check_edge(label, out_label, in_label, properties)
            properties = self._properties(properties)
            properties.setdefault(
                "edge_key",
                edge_key(label, out_cid, in_cid, properties.get("fact_key", "")),
            )
            properties.setdefault("creation_status", "DETERMINISTIC")
            if properties["edge_key"] in edge_keys:
                raise ValueError(f"duplicate edge_key in bulk load: {properties['edge_key']}")
            edge_keys.add(properties["edge_key"])
            normalized_edges.append(
                {
                    "label": f"{label}__{out_label}__{in_label}",
                    "outV": out_vid,
                    "outVLabel": out_label,
                    "inV": in_vid,
                    "inVLabel": in_label,
                    "properties": properties,
                }
            )

        self.ensure_schema({})
        vertices_committed = 0
        edges_committed = 0
        vertex_batches = 0
        edge_batches = 0
        try:
            for offset in range(0, len(normalized_vertices), batch_size):
                batch = normalized_vertices[offset : offset + batch_size]
                created = self._request(
                    "POST", "/graph/vertices/batch", json=batch, timeout=120
                )
                if not isinstance(created, list) or len(created) != len(batch):
                    raise RuntimeError("HugeGraph returned an invalid vertex batch result")
                vertices_committed += len(batch)
                vertex_batches += 1
                for item in batch:
                    self._remember_identity(
                        {
                            "vid": item["id"],
                            "canonical_id": item["properties"]["canonical_id"],
                            "label": item["label"],
                        }
                    )
            for offset in range(0, len(normalized_edges), batch_size):
                batch = normalized_edges[offset : offset + batch_size]
                created = self._request(
                    "POST",
                    "/graph/edges/batch",
                    params={"check_vertex": True},
                    json=batch,
                    timeout=120,
                )
                if not isinstance(created, list) or len(created) != len(batch):
                    raise RuntimeError("HugeGraph returned an invalid edge batch result")
                edges_committed += len(batch)
                edge_batches += 1
        except Exception as exc:
            raise BulkLoadError(
                "HugeGraph bulk load failed; discard the isolated graph and retry",
                vertices_committed=vertices_committed,
                edges_committed=edges_committed,
            ) from exc
        return {
            "vertices": vertices_committed,
            "edges": edges_committed,
            "vertex_batches": vertex_batches,
            "edge_batches": edge_batches,
            "batch_size": batch_size,
            "mode": "hugegraph-native-post",
        }

    def native_export(self):
        """Export all vertices and edges as raw HugeGraph JSON dicts (track-1)."""
        vertices = [raw for raw in self._pages("vertices")]
        edges = [raw for raw in self._pages("edges")]
        schema = {
            "vertexlabels": self._request("GET", "/schema/vertexlabels")["vertexlabels"],
            "edgelabels": self._request("GET", "/schema/edgelabels")["edgelabels"],
            "propertykeys": self._request("GET", "/schema/propertykeys")["propertykeys"],
            "indexlabels": self._request("GET", "/schema/indexlabels")["indexlabels"],
        }
        return {"schema": schema, "vertices": vertices, "edges": edges}

    def native_import(self, export_data, *, batch_size=500):
        """Restore raw HugeGraph vertices and edges from a native export (track-1).

        Requires an empty graph with schema already bootstrapped.
        """
        if self.count_vertices() or self.count_edges():
            raise RuntimeError("native_import requires an empty graph")
        self.ensure_schema({})
        vertices = export_data["vertices"]
        edges = export_data["edges"]
        for offset in range(0, len(vertices), batch_size):
            batch = vertices[offset:offset + batch_size]
            self._request("POST", "/graph/vertices/batch", json=batch, timeout=120)
        for offset in range(0, len(edges), batch_size):
            batch = edges[offset:offset + batch_size]
            self._request("POST", "/graph/edges/batch", params={"check_vertex": True}, json=batch, timeout=120)
        return {"vertices": len(vertices), "edges": len(edges)}

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
