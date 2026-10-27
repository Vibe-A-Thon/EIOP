"""Data-subject request workflow across every tenant store (SR-PRV-002).

``SubjectRequestWorkflow`` runs locate, access/export, rectification and erasure with propagation
for one tenant. It works over the tenant's isolated layers (``eoip.tenancy.layers.TenantHandle``)
plus the graph store:

========================  ========================================  ===============================
surface                   located by                                erasure
========================  ========================================  ===============================
graph                     subject properties / any value mention    scrub values + tombstone
derived_graph             vertices of derived labels mentioning it  scrub values + tombstone
raw_capture               objects under ``raw/`` (tag or mention)   object deleted
vector (embeddings)       payload ``subject_ids`` or text mention   vector deleted
search                    doc meta ``subject_ids`` or text mention  doc removed from the index
cache                     value mentions the subject                entry deleted
summary                   ``summaries/`` source tagged/mentioning   regenerated without the subject
export                    tenant exports mentioning the subject     export deleted
backup                    decrypted tenant backups mentioning it    *flagged only*: retained until
                                                                    expiry / crypto-shred (SR-PRV-003)
========================  ========================================  ===============================

Every action returns a proof whose digest covers the before/after locate results; erasure also
re-runs locate and fails the proof (``verified=False``) if anything other than flagged backups
still holds the subject.
"""
from __future__ import annotations

import json
from typing import Any
from collections.abc import Callable

from pydantic import BaseModel, Field

from eoip.privacy.dsar import SubjectAccessReport, SubjectHit, proof_digest

ERASED = "[erased]"
FLAGGED_SURFACES = frozenset({"backup"})


class SubjectRequestProof(BaseModel):
    action: str
    subject_id: str
    tenant_id: str
    before: dict[str, int]
    after: dict[str, int]
    actions: list[dict[str, Any]] = Field(default_factory=list)
    flagged: list[str] = Field(default_factory=list)
    verified: bool
    digest: str


def _mentions(value: Any, needle: str) -> bool:
    if isinstance(value, str):
        return needle in value
    try:
        return needle in json.dumps(value, default=str)
    except (TypeError, ValueError):
        return needle in str(value)


def _tagged(meta: Any, subject_id: str) -> bool:
    return isinstance(meta, dict) and subject_id in (meta.get("subject_ids") or [])


def _replace(value: Any, old: str, new: str) -> Any:
    if isinstance(value, str):
        return value.replace(old, new)
    if isinstance(value, list):
        return [_replace(v, old, new) for v in value]
    if isinstance(value, dict):
        return {k: _replace(v, old, new) for k, v in value.items()}
    return value


class SubjectRequestWorkflow:
    def __init__(self, handle: Any, *, graph_store: Any = None, graph_labels: tuple[str, ...] = ("Person",),
                 derived_labels: tuple[str, ...] = (), embed: Callable[[str], list[float]] | None = None,
                 summarize: Callable[[list[str]], str] | None = None) -> None:
        self.h, self.graph = handle, graph_store
        self.graph_labels, self.derived_labels = graph_labels, derived_labels
        self.embed, self.summarize = embed, summarize

    # -- locate ----------------------------------------------------------------
    def _graph_hits(self, sid: str) -> list[tuple[str, dict]]:
        out: list[tuple[str, dict]] = []
        if self.graph is None:
            return out
        for label in (*self.graph_labels, *self.derived_labels):
            surface = "derived_graph" if label in self.derived_labels else "graph"
            for v in self.graph.find_vertices(label=label, limit=10_000, include_deleted=True):
                owner = v["properties"].get("tenant_id")
                if owner is not None and owner != self.h.tenant_id:
                    continue  # another tenant's vertex in a shared graph
                props = {k: val for k, val in v["properties"].items() if k != "canonical_id"}
                if _mentions(props, sid):
                    out.append((surface, v))
        return out

    def locate(self, subject_id: str) -> SubjectAccessReport:
        sid, h = subject_id, self.h
        rep = SubjectAccessReport(subject_id=sid, tenant_id=h.tenant_id, unsearched_surfaces=[])

        def hit(surface: str, ref: str, kind: str = "") -> None:
            rep.hits.append(SubjectHit(surface=surface, ref=ref, kind=kind or surface, tenant_id=h.tenant_id))

        derived_from: set[str] = set()
        for surface, v in self._graph_hits(sid):
            hit(surface, v["canonical_id"], v["label"])
            derived_from.add(v["canonical_id"])
        for key in [*h.list_objects("raw/"), *h.list_objects("rectifications/")]:
            if _mentions(h.get_object(key).decode("utf-8", "replace"), sid):
                hit("raw_capture", key)
        for doc_id, (_, payload) in h.vector_items().items():
            if _tagged(payload, sid) or _mentions(payload, sid) or payload.get("source_ref") in derived_from:
                hit("vector", doc_id, "embedding")
        for doc_id, (text, meta) in h.search_docs().items():
            if _tagged(meta, sid) or sid in text or meta.get("source_ref") in derived_from:
                hit("search", doc_id, "search_doc")  # index entries derived from the subject's records
        for key, value in h.cache_items().items():
            if _mentions(value, sid):
                hit("cache", key)
        for key in h.list_objects("summaries/"):
            doc = json.loads(h.get_object(key))
            if any(_tagged(s, sid) or _mentions(s.get("text", ""), sid) for s in doc.get("sources", [])) \
                    or sid in doc.get("text", ""):
                hit("summary", key)
        for name in h.list_exports():
            if _mentions(h.read_export(name).decode("utf-8", "replace"), sid):
                hit("export", name)
        for path in h.list_backups():
            if _mentions(h.restore(path), sid):
                hit("backup", path.name)
        return rep

    # -- proof -----------------------------------------------------------------
    def _proof(self, action: str, sid: str, before: SubjectAccessReport, after: SubjectAccessReport,
               actions: list[dict], verified: bool) -> SubjectRequestProof:
        flagged = sorted(f"{x.surface}:{x.ref}" for x in after.hits if x.surface in FLAGGED_SURFACES)
        body = {"action": action, "subject_id": sid, "tenant_id": self.h.tenant_id,
                "before": sorted(f"{x.surface}:{x.ref}" for x in before.hits),
                "after": sorted(f"{x.surface}:{x.ref}" for x in after.hits), "actions": actions,
                "verified": verified}
        return SubjectRequestProof(action=action, subject_id=sid, tenant_id=self.h.tenant_id,
                                   before=before.surface_counts(), after=after.surface_counts(), actions=actions,
                                   flagged=flagged, verified=verified, digest=proof_digest(body))

    # -- access / export -------------------------------------------------------
    def access_export(self, subject_id: str, *, export_name: str | None = None) -> tuple[str, SubjectRequestProof]:
        rep, h, sid = self.locate(subject_id), self.h, subject_id
        bundle: dict[str, list] = {}
        graph = {v["canonical_id"]: v for _, v in self._graph_hits(sid)}
        vectors, docs, cache = h.vector_items(), h.search_docs(), h.cache_items()
        for x in rep.hits:
            if x.surface in ("graph", "derived_graph"):
                item = {"ref": x.ref, "label": graph[x.ref]["label"], "properties": graph[x.ref]["properties"]}
            elif x.surface in ("raw_capture", "summary"):
                item = {"ref": x.ref, "content": h.get_object(x.ref).decode("utf-8", "replace")}
            elif x.surface == "vector":
                item = {"ref": x.ref, "payload": vectors[x.ref][1]}  # the vector itself is not personal data
            elif x.surface == "search":
                item = {"ref": x.ref, "text": docs[x.ref][0]}
            elif x.surface == "cache":
                item = {"ref": x.ref, "value": cache[x.ref]}
            else:  # exports / backups are listed, not re-copied
                item = {"ref": x.ref, "note": "listed only" if x.surface == "export" else
                        "held in an encrypted backup until expiry"}
            bundle.setdefault(x.surface, []).append(item)
        name = export_name or f"dsar-{proof_digest({'s': sid})[:12]}.json"
        payload = json.dumps({"subject_id": sid, "tenant_id": h.tenant_id, "data": bundle},
                             sort_keys=True, default=str).encode()
        h.write_export(name, payload)
        proof = self._proof("access", sid, rep, rep, [{"surface": "export", "ref": name, "op": "written"}], True)
        return name, proof

    # -- rectification ---------------------------------------------------------
    def rectify(self, subject_id: str, old: str, new: str) -> SubjectRequestProof:
        h, before, actions = self.h, self.locate(subject_id), []
        for surface, v in self._graph_hits(subject_id):
            if _mentions(v["properties"], old):
                self._write_vertex(v, _replace(v["properties"], old, new))
                actions.append({"surface": surface, "ref": v["canonical_id"], "op": "rectified"})
        vectors = h.vector_items()
        for x in before.hits:
            if x.surface == "vector":
                vec, payload = vectors[x.ref]
                payload = _replace(payload, old, new)
                if self.embed is not None and "text" in payload:
                    vec = self.embed(payload["text"])  # embeddings recomputed from the corrected text
                h.vector_upsert(x.ref, vec, payload)
                actions.append({"surface": "vector", "ref": x.ref, "op": "re-embedded"})
            elif x.surface == "search":
                text, meta = h.search_docs()[x.ref]
                h.search_remove(x.ref)
                h.search_add(x.ref, text.replace(old, new), meta)
                actions.append({"surface": "search", "ref": x.ref, "op": "reindexed"})
            elif x.surface == "cache":
                h.cache_delete(x.ref)
                actions.append({"surface": "cache", "ref": x.ref, "op": "invalidated"})
            elif x.surface == "summary":
                self._resummarize(x.ref, lambda s: {**s, "text": s.get("text", "").replace(old, new)})
                actions.append({"surface": "summary", "ref": x.ref, "op": "regenerated"})
            elif x.surface == "raw_capture":
                # raw captures are immutable evidence: a rectification record is stored beside them
                h.put_object(f"rectifications/{x.ref}",
                             json.dumps({"subject_id": subject_id, "old": old, "new": new}).encode())
                actions.append({"surface": "raw_capture", "ref": x.ref, "op": "rectification-recorded"})
            elif x.surface == "export":
                actions.append({"surface": "export", "ref": x.ref, "op": "flagged-stale"})
        after = self.locate(subject_id)
        stale = [x for x in after.hits if x.surface in ("vector", "search", "cache", "summary", "graph",
                                                        "derived_graph") and self._still_has(x, old)]
        return self._proof("rectify", subject_id, before, after, actions, verified=not stale)

    def _still_has(self, x: SubjectHit, old: str) -> bool:
        h = self.h
        if x.surface == "vector":
            return _mentions(h.vector_items()[x.ref][1], old)
        if x.surface == "search":
            return old in h.search_docs()[x.ref][0]
        if x.surface == "cache":
            return _mentions(h.cache_items()[x.ref], old)
        if x.surface == "summary":
            return old in h.get_object(x.ref).decode()
        v = self.graph.get_vertex_by_canonical_id(x.ref)
        return bool(v) and _mentions(v["properties"], old)

    # -- erasure ---------------------------------------------------------------
    def erase(self, subject_id: str) -> SubjectRequestProof:
        h, sid, before, actions = self.h, subject_id, self.locate(subject_id), []
        graph = {v["canonical_id"]: v for _, v in self._graph_hits(sid)}
        for x in before.hits:
            op = "erased"
            if x.surface in ("graph", "derived_graph"):
                v = graph[x.ref]
                scrubbed = {k: (ERASED if k != "canonical_id" and _mentions(val, sid) else val)
                            for k, val in v["properties"].items()}
                self._write_vertex(v, scrubbed)
                self.graph.tombstone_vertex(x.ref)
                op = "scrubbed+tombstoned"
            elif x.surface == "raw_capture":
                h.delete_object(x.ref)
            elif x.surface == "vector":
                h.vector_delete(x.ref)
            elif x.surface == "search":
                h.search_remove(x.ref)
            elif x.surface == "cache":
                h.cache_delete(x.ref)
            elif x.surface == "summary":
                op = self._resummarize(x.ref, lambda s: None if (_tagged(s, sid) or _mentions(s, sid)) else s)
            elif x.surface == "export":
                h.delete_export(x.ref)
            else:
                op = "flagged"
            actions.append({"surface": x.surface, "ref": x.ref, "op": op})
        after = self.locate(sid)
        remaining = [x for x in after.hits if x.surface not in FLAGGED_SURFACES]
        return self._proof("erase", sid, before, after, actions, verified=not remaining)

    # -- helpers ---------------------------------------------------------------
    def _write_vertex(self, v: dict, props: dict) -> None:
        live = self.graph.get_vertex_by_canonical_id(v["canonical_id"])
        if live is not None and live.get("properties") is not None:
            live["properties"].clear()
            live["properties"].update(props)
        else:  # stores returning copies: write back through the upsert API
            self.graph.upsert_vertex(v["label"], {**props, "canonical_id": v["canonical_id"]})

    def _resummarize(self, key: str, transform: Callable[[dict], dict | None]) -> str:
        doc = json.loads(self.h.get_object(key))
        sources = [s for s in (transform(dict(s)) for s in doc.get("sources", [])) if s is not None]
        if not sources:
            self.h.delete_object(key)
            return "deleted (no remaining sources)"
        if self.summarize is None:
            self.h.delete_object(key)  # cannot regenerate safely: fail closed
            return "deleted (no summarizer)"
        doc.update(sources=sources, text=self.summarize([s.get("text", "") for s in sources]))
        self.h.put_object(key, json.dumps(doc, sort_keys=True).encode())
        return "regenerated"
