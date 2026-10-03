"""In-process GraphStore implementation for tests and local developer harness.

Semantics mirror HugeGraphStore: idempotent upserts keyed by canonical_id
(vertices) and deterministic edge keys (edges). NOT a runtime substitute in
deployed environments (FR-GRAPH-001).
"""

from __future__ import annotations

import hashlib
import itertools
import logging
import threading
from typing import Any

from eoip.ontology.manifest import EDGE_LABELS, VERTEX_LABELS

log = logging.getLogger("eoip.graph")


def edge_key(label: str, out_cid: str, in_cid: str, fact_key: str = "") -> str:
    raw = f"{label}|{out_cid}|{in_cid}|{fact_key}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:32]


class MemoryGraphStore:
    def __init__(self) -> None:
        self._vids: dict[str, str] = {}  # canonical_id -> vid
        self._vertices: dict[str, dict] = {}
        self._edges: dict[str, dict] = {}
        self._adj_out: dict[str, list[str]] = {}
        self._adj_in: dict[str, list[str]] = {}
        self._schema: dict | None = None
        self._vid_seq = itertools.count(1)
        self._lock = threading.RLock()

    # -- schema --------------------------------------------------------------
    def health(self) -> bool:
        return True

    def ping(self) -> dict:
        return {"backend": "memory", "status": "ok"}

    def ensure_schema(self, manifest: dict) -> dict:
        with self._lock:
            if self._schema is None:
                self._schema = manifest
                return {"created": True}
            return {"created": False}

    def schema_status(self) -> dict:
        return {"initialized": self._schema is not None}

    # -- vertices --------------------------------------------------------------
    def upsert_vertex(self, label: str, properties: dict) -> dict:
        with self._lock:
            from eoip.validation.gate import check_vertex

            check_vertex(label, properties)
            cid = properties.get("canonical_id")
            existing = self._vids.get(cid)
            now = properties.get("modified_at")
            if existing is not None:
                props = self._vertices[existing]["properties"]
                first_seen = props.get("first_seen")
                props.update({k: v for k, v in properties.items() if v is not None})
                if first_seen is not None:
                    props["first_seen"] = first_seen
                if "deleted_at" not in properties:
                    props.pop("deleted_at", None)
                if now:
                    props["modified_at"] = now
                return self._vertices[existing]
            vid = f"v:{next(self._vid_seq)}"
            props = dict(properties)
            props.setdefault("entity_type", label)
            props.setdefault("graph_domain", VERTEX_LABELS[label][0])
            record = {"vid": vid, "canonical_id": cid, "label": label, "properties": props}
            self._vertices[vid] = record
            self._vids[cid] = vid
            self._adj_out.setdefault(vid, [])
            self._adj_in.setdefault(vid, [])
            return record

    def get_vertex(self, vid: str) -> dict | None:
        return self._vertices.get(vid)

    def get_vertex_by_canonical_id(self, canonical_id: str) -> dict | None:
        vid = self._vids.get(canonical_id)
        return self._vertices.get(vid) if vid else None

    def find_vertex_by_property(
        self,
        label: str,
        key: str,
        value: Any,
        limit: int = 10,
        include_deleted: bool = False,
    ) -> list[dict]:
        out = []
        for rec in self._vertices.values():
            if rec["label"] != label or rec["properties"].get(key) != value:
                continue
            if not include_deleted and rec["properties"].get("deleted_at"):
                continue
            out.append(rec)
            if len(out) >= limit:
                break
        return out

    def find_vertices(
        self,
        label: str | None = None,
        filters: dict[str, Any] | None = None,
        limit: int = 100,
        include_deleted: bool = False,
    ) -> list[dict]:
        out = []
        for rec in self._vertices.values():
            if label and rec["label"] != label:
                continue
            props = rec["properties"]
            if filters and any(props.get(k) != v for k, v in filters.items()):
                continue
            if not include_deleted and props.get("deleted_at"):
                continue
            out.append(rec)
            if len(out) >= limit:
                break
        return out

    def count_vertices(self, label: str | None = None) -> int:
        return len(self.find_vertices(label=label, limit=1_000_000))

    # -- edges ---------------------------------------------------------------
    def upsert_edge(self, label: str, out_v: str, in_v: str, properties: dict) -> dict:
        with self._lock:
            from eoip.validation.gate import check_edge

            if label not in EDGE_LABELS:
                raise ValueError(f"unknown edge label: {label}")
            out_vid = self._vids.get(out_v, out_v)
            in_vid = self._vids.get(in_v, in_v)
            out_rec = self._vertices[out_vid]
            in_rec = self._vertices[in_vid]
            check_edge(label, out_rec["label"], in_rec["label"], properties)
            eid = properties.get("edge_key") or edge_key(
                label, out_rec["canonical_id"], in_rec["canonical_id"], properties.get("fact_key", "")
            )
            existing = self._edges.get(eid)
            if existing is not None:
                existing["properties"].update({k: v for k, v in properties.items() if v is not None})
                return existing
            props = dict(properties)
            props.setdefault("edge_key", eid)
            props.setdefault("creation_status", "DETERMINISTIC")
            record = {
                "eid": eid,
                "label": label,
                "out_v": out_vid,
                "in_v": in_vid,
                "out_cid": out_rec["canonical_id"],
                "in_cid": in_rec["canonical_id"],
                "properties": props,
            }
            self._edges[eid] = record
            self._adj_out.setdefault(out_vid, []).append(eid)
            self._adj_in.setdefault(in_vid, []).append(eid)
            return record

    def get_edge(self, eid: str) -> dict | None:
        return self._edges.get(eid)

    def find_edge_by_key(self, edge_key: str) -> dict | None:
        for rec in self._edges.values():
            if rec["properties"].get("edge_key") == edge_key:
                return rec
        return None

    def find_edges(
        self,
        label: str | None = None,
        out_v: str | None = None,
        in_v: str | None = None,
        limit: int = 500,
        include_historical: bool = False,
    ) -> list[dict]:
        out = []
        for rec in self._edges.values():
            if label and rec["label"] != label:
                continue
            if out_v and rec["out_v"] != out_v:
                continue
            if in_v and rec["in_v"] != in_v:
                continue
            if not include_historical and rec["properties"].get("is_current") is False:
                continue
            out.append(rec)
            if len(out) >= limit:
                break
        return out

    def edges_from(self, vid: str, labels: list[str] | None = None, limit: int = 500, include_historical: bool = False) -> list[dict]:
        out = []
        for eid in self._adj_out.get(vid, []):
            rec = self._edges[eid]
            if labels and rec["label"] not in labels:
                continue
            if not include_historical and rec["properties"].get("is_current") is False:
                continue
            out.append(rec)
            if len(out) >= limit:
                break
        return out

    def edges_to(self, vid: str, labels: list[str] | None = None, limit: int = 500, include_historical: bool = False) -> list[dict]:
        out = []
        for eid in self._adj_in.get(vid, []):
            rec = self._edges[eid]
            if labels and rec["label"] not in labels:
                continue
            if not include_historical and rec["properties"].get("is_current") is False:
                continue
            out.append(rec)
            if len(out) >= limit:
                break
        return out

    def count_edges(self, label: str | None = None) -> int:
        return len(self.find_edges(label=label, limit=1_000_000))

    # -- maintenance -----------------------------------------------------------
    def tombstone_vertex(self, canonical_id: str) -> bool:
        vid = self._vids.get(canonical_id)
        if not vid:
            return False
        from eoip.contracts.source_event import utc_now_iso

        self._vertices[vid]["properties"]["deleted_at"] = utc_now_iso()
        return True

    def clear(self) -> None:
        with self._lock:
            self._vids.clear()
            self._vertices.clear()
            self._edges.clear()
            self._adj_out.clear()
            self._adj_in.clear()
            self._schema = None
