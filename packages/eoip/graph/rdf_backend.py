"""RDF-store backend port: Apache Jena Fuseki reference and Ontotext GraphDB adapters (CRA-002.10, CRA-024.11, ONT-003).

Every GraphStore operation is executed on the RDF store over the SPARQL 1.1 Protocol (Query + Update);
there is no local cache. GPL/AGPL servers are reached only over their network protocol and are never linked,
vendored, or bundled.

Mapping (namespace ``urn:eoip:rdf#``): a vertex is ``<urn:eoip:v:{cid}> a :Vertex ; :label ; :canonicalId ;
:props (JSON) ; :p/{key} (one typed literal per scalar property) [; :deleted true]``. An edge is
``<urn:eoip:e:{eid}> a :Edge ; :label ; :out <v> ; :in <v> ; :props`` plus the navigable triple
``<out> <urn:eoip:rel#{label}> <in>``. Literals and IRIs are serialized by rdflib (no string splicing).
"""

from __future__ import annotations

import base64
import json
import logging
from collections.abc import Callable
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

from rdflib import Literal, URIRef

from eoip.graph.store import Edge, Vertex

logger = logging.getLogger(__name__)

NS = "urn:eoip:rdf#"
REL = "urn:eoip:rel#"
VERTEX_ID_PROPS = ("canonical_id",)

# transport(method, url, body: bytes|None, headers) -> (status, body bytes)
Transport = Callable[[str, str, bytes | None, dict[str, str]], tuple[int, bytes]]


class RDFStoreError(RuntimeError):
    """Raised on RDF store SPARQL protocol errors (unreachable store, rejected query/update)."""


def _t(name: str) -> str:
    return URIRef(NS + name).n3()


def _viri(cid: str) -> str:
    return URIRef("urn:eoip:v:" + quote(str(cid), safe="")).n3()


def _eiri(eid: str) -> str:
    return URIRef("urn:eoip:e:" + quote(str(eid), safe="")).n3()


def _lit(value: Any) -> str:
    return Literal(value).n3()


def _scalar(value: Any) -> bool:
    return isinstance(value, (str, int, float, bool)) and not (isinstance(value, str) and len(value) > 4000)


def _urllib_transport(timeout: float, username: str, password: str) -> Transport:
    auth = None
    if username:
        auth = "Basic " + base64.b64encode(f"{username}:{password}".encode()).decode()

    def send(method: str, url: str, body: bytes | None, headers: dict[str, str]) -> tuple[int, bytes]:
        req = Request(url, data=body, method=method, headers=dict(headers))
        if auth:
            req.add_header("Authorization", auth)
        try:
            with urlopen(req, timeout=timeout) as resp:  # noqa: S310 - configured store endpoint
                return resp.status, resp.read()
        except HTTPError as exc:
            return exc.code, exc.read()
        except (URLError, OSError, TimeoutError) as exc:
            raise RDFStoreError(f"RDF store unreachable at {url}: {exc}") from exc
    return send


class FusekiGraphStore:
    """Apache Jena Fuseki reference RDF store adapter (CRA-002.10, ONT-003)."""

    backend = "fuseki"

    def __init__(
        self,
        endpoint_url: str = "http://localhost:3030/ds",
        dataset: str = "ds",
        username: str = "",
        password: str = "",
        timeout: float = 30.0,
        transport: Transport | None = None,
    ) -> None:
        self.endpoint_url = endpoint_url.rstrip("/")
        self.query_url = f"{self.endpoint_url}/sparql"
        self.update_url = f"{self.endpoint_url}/update"
        self.data_url = f"{self.endpoint_url}/data"
        self.dataset = dataset
        self.username = username
        self.password = password
        self.timeout = timeout
        self._send = transport or _urllib_transport(timeout, username, password)

    # -- protocol ---------------------------------------------------------------
    def _query(self, sparql: str) -> dict[str, Any]:
        status, body = self._send("POST", self.query_url, urlencode({"query": sparql}).encode(),
                                  {"Content-Type": "application/x-www-form-urlencoded",
                                   "Accept": "application/sparql-results+json"})
        if status != 200:
            raise RDFStoreError(f"SPARQL query rejected by {self.backend} (HTTP {status}): {body[:300]!r}")
        return json.loads(body)

    def _update(self, sparql: str) -> None:
        status, body = self._send("POST", self.update_url, urlencode({"update": sparql}).encode(),
                                  {"Content-Type": "application/x-www-form-urlencoded"})
        if status not in (200, 204):
            raise RDFStoreError(f"SPARQL update rejected by {self.backend} (HTTP {status}): {body[:300]!r}")

    def _rows(self, sparql: str) -> list[dict[str, str]]:
        return [{k: v["value"] for k, v in b.items()} for b in self._query(sparql)["results"]["bindings"]]

    def health(self) -> bool:
        try:
            return self._query("ASK { }").get("boolean") is not None
        except Exception:  # noqa: BLE001
            return False

    def ping(self) -> dict[str, Any]:
        return {"backend": self.backend, "endpoint": self.endpoint_url, "dataset": self.dataset,
                "healthy": self.health()}

    def ensure_schema(self, manifest: dict[str, Any]) -> dict[str, Any]:
        if not self.health():
            raise RDFStoreError(f"{self.backend} store at {self.endpoint_url} is not reachable")
        return {"status": "READY", "backend": self.backend, "schema": manifest,
                "note": "RDF stores are schemaless; the ontology is enforced by the validation gate"}

    def schema_status(self) -> dict[str, Any]:
        return {"backend": self.backend, "status": "READY" if self.health() else "UNAVAILABLE"}

    # -- vertices ---------------------------------------------------------------
    def _vertex_triples(self, label: str, cid: str, props: dict[str, Any], deleted: bool) -> str:
        v = _viri(cid)
        lines = [f"{v} a {_t('Vertex')} ; {_t('label')} {_lit(label)} ; {_t('canonicalId')} {_lit(cid)} ; "
                 f"{_t('props')} {_lit(json.dumps(props, sort_keys=True, default=str))} ."]
        for key, value in props.items():
            if _scalar(value):
                lines.append(f"{v} {URIRef(NS + 'p/' + quote(key, safe='')).n3()} {_lit(value)} .")
        if deleted:
            lines.append(f"{v} {_t('deleted')} {_lit(True)} .")
        return "\n".join(lines)

    def _load_vertex(self, cid: str, include_deleted: bool = True) -> Vertex | None:
        rows = self._rows(
            f"SELECT ?label ?props ?del WHERE {{ {_viri(cid)} {_t('label')} ?label ; {_t('props')} ?props . "
            f"OPTIONAL {{ {_viri(cid)} {_t('deleted')} ?del }} }} LIMIT 1")
        if not rows or (rows[0].get("del") == "true" and not include_deleted):
            return None
        return {"vid": cid, "canonical_id": cid, "label": rows[0]["label"], "properties": json.loads(rows[0]["props"])}

    def upsert_vertex(self, label: str, properties: dict[str, Any]) -> Vertex:
        cid = properties.get("canonical_id")
        if not cid:
            raise ValueError("canonical_id is required")
        existing = self._load_vertex(cid)
        props = dict(existing["properties"]) if existing else {}
        props.update({k: v for k, v in properties.items() if v is not None})
        if existing and "deleted_at" not in properties:
            props.pop("deleted_at", None)
        self._update(f"DELETE WHERE {{ {_viri(cid)} ?p ?o }} ;\n"
                     f"INSERT DATA {{ {self._vertex_triples(label, cid, props, False)} }}")
        return {"vid": cid, "canonical_id": cid, "label": label, "properties": props}

    def get_vertex(self, vid: str) -> Vertex | None:
        return self._load_vertex(vid, include_deleted=False)

    def get_vertex_by_canonical_id(self, canonical_id: str) -> Vertex | None:
        return self._load_vertex(canonical_id, include_deleted=False)

    def _find(self, label: str | None, filters: dict[str, Any], limit: int, include_deleted: bool) -> list[Vertex]:
        where = [f"?v a {_t('Vertex')} ; {_t('canonicalId')} ?cid ; {_t('label')} ?label ; {_t('props')} ?props ."]
        if label:
            where.append(f"?v {_t('label')} {_lit(label)} .")
        for key, value in (filters or {}).items():
            where.append(f"?v {URIRef(NS + 'p/' + quote(key, safe='')).n3()} {_lit(value)} .")
        if not include_deleted:
            where.append(f"FILTER NOT EXISTS {{ ?v {_t('deleted')} true }}")
        rows = self._rows(f"SELECT ?cid ?label ?props WHERE {{ {' '.join(where)} }} ORDER BY ?cid LIMIT {int(limit)}")
        return [{"vid": r["cid"], "canonical_id": r["cid"], "label": r["label"], "properties": json.loads(r["props"])}
                for r in rows]

    def find_vertex_by_property(self, label: str, key: str, value: Any, limit: int = 10,
                                include_deleted: bool = False) -> list[Vertex]:
        return self._find(label, {key: value}, limit, include_deleted)

    def find_vertices(self, label: str | None = None, filters: dict[str, Any] | None = None, limit: int = 100,
                      include_deleted: bool = False) -> list[Vertex]:
        return self._find(label, filters or {}, limit, include_deleted)

    def count_vertices(self, label: str | None = None) -> int:
        lab = f"?v {_t('label')} {_lit(label)} ." if label else ""
        rows = self._rows(f"SELECT (COUNT(?v) AS ?n) WHERE {{ ?v a {_t('Vertex')} . {lab} "
                          f"FILTER NOT EXISTS {{ ?v {_t('deleted')} true }} }}")
        return int(rows[0]["n"]) if rows else 0

    def tombstone_vertex(self, canonical_id: str) -> bool:
        if self._load_vertex(canonical_id, include_deleted=False) is None:
            return False
        self._update(f"INSERT DATA {{ {_viri(canonical_id)} {_t('deleted')} {_lit(True)} }}")
        return True

    # -- edges ------------------------------------------------------------------
    def upsert_edge(self, label: str, out_v: str, in_v: str, properties: dict[str, Any]) -> Edge:
        eid = f"{out_v}->{label}->{in_v}"
        e = _eiri(eid)
        props = dict(properties)
        rel = URIRef(REL + quote(label, safe="")).n3()
        self._update(
            f"DELETE WHERE {{ {e} ?p ?o }} ;\n"
            f"INSERT DATA {{ {e} a {_t('Edge')} ; {_t('label')} {_lit(label)} ; {_t('edgeId')} {_lit(eid)} ; "
            f"{_t('out')} {_viri(out_v)} ; {_t('in')} {_viri(in_v)} ; {_t('outId')} {_lit(out_v)} ; "
            f"{_t('inId')} {_lit(in_v)} ; {_t('props')} {_lit(json.dumps(props, sort_keys=True, default=str))} . "
            f"{_viri(out_v)} {rel} {_viri(in_v)} . }}")
        return {"eid": eid, "label": label, "out_v": out_v, "in_v": in_v, "out_cid": out_v, "in_cid": in_v,
                "properties": props}

    def find_edges(self, label: str | None = None, out_v: str | None = None, in_v: str | None = None,
                   limit: int = 500, include_historical: bool = False) -> list[Edge]:
        where = [f"?e a {_t('Edge')} ; {_t('edgeId')} ?eid ; {_t('label')} ?label ; {_t('outId')} ?o ; "
                 f"{_t('inId')} ?i ; {_t('props')} ?props ."]
        if label:
            where.append(f"?e {_t('label')} {_lit(label)} .")
        if out_v:
            where.append(f"?e {_t('outId')} {_lit(out_v)} .")
        if in_v:
            where.append(f"?e {_t('inId')} {_lit(in_v)} .")
        rows = self._rows(f"SELECT ?eid ?label ?o ?i ?props WHERE {{ {' '.join(where)} }} ORDER BY ?eid LIMIT {int(limit)}")
        return [{"eid": r["eid"], "label": r["label"], "out_v": r["o"], "in_v": r["i"], "out_cid": r["o"],
                 "in_cid": r["i"], "properties": json.loads(r["props"])} for r in rows]

    def get_edge(self, eid: str) -> Edge | None:
        rows = [e for e in self.find_edges(limit=1, **_edge_parts(eid)) if e["eid"] == eid]
        return rows[0] if rows else None

    def find_edge_by_key(self, edge_key: str) -> Edge | None:
        return self.get_edge(edge_key)

    def edges_from(self, vid: str, labels: list[str] | None = None, limit: int = 500,
                   include_historical: bool = False) -> list[Edge]:
        edges = self.find_edges(out_v=vid, limit=limit)
        return [e for e in edges if not labels or e["label"] in labels]

    def edges_to(self, vid: str, labels: list[str] | None = None, limit: int = 500,
                 include_historical: bool = False) -> list[Edge]:
        edges = self.find_edges(in_v=vid, limit=limit)
        return [e for e in edges if not labels or e["label"] in labels]

    def count_edges(self, label: str | None = None) -> int:
        lab = f"?e {_t('label')} {_lit(label)} ." if label else ""
        rows = self._rows(f"SELECT (COUNT(?e) AS ?n) WHERE {{ ?e a {_t('Edge')} . {lab} }}")
        return int(rows[0]["n"]) if rows else 0

    def bulk_load(self, vertices: list[Vertex], edges: list[Edge], *, batch_size: int = 500) -> dict[str, Any]:
        """Batched INSERT DATA (new entities; use upsert_* for merges)."""
        for i in range(0, len(vertices), batch_size):
            chunk = vertices[i:i + batch_size]
            body = "\n".join(self._vertex_triples(v.get("label", "Entity"), v["properties"]["canonical_id"],
                                                  dict(v["properties"]), False) for v in chunk)
            self._update(f"INSERT DATA {{ {body} }}")
        for e in edges:
            self.upsert_edge(e.get("label", "relatedTo"), e.get("out_v", ""), e.get("in_v", ""), e.get("properties", {}))
        return {"status": "COMPLETED", "vertices_loaded": len(vertices), "edges_loaded": len(edges),
                "vertices_in_store": self.count_vertices()}

    def clear(self) -> None:
        self._update("CLEAR DEFAULT")


def _edge_parts(eid: str) -> dict[str, str]:
    parts = eid.split("->")
    return {"out_v": parts[0], "label": parts[1], "in_v": parts[2]} if len(parts) == 3 else {}


class GraphDBGraphStore(FusekiGraphStore):
    """Ontotext GraphDB adapter (repository-scoped RDF4J/SPARQL endpoints; tested on GraphDB Free)."""

    backend = "graphdb"

    def __init__(
        self,
        endpoint_url: str = "http://localhost:7200",
        repository: str = "eoip",
        username: str = "",
        password: str = "",
        timeout: float = 30.0,
        transport: Transport | None = None,
    ) -> None:
        repo_url = f"{endpoint_url.rstrip('/')}/repositories/{repository}"
        super().__init__(endpoint_url=repo_url, dataset=repository, username=username, password=password,
                         timeout=timeout, transport=transport)
        self.server_url = endpoint_url.rstrip("/")
        self.query_url = repo_url
        self.update_url = f"{repo_url}/statements"
        self.data_url = f"{repo_url}/statements"


def create_rdf_store_from_config(config: dict[str, Any]) -> FusekiGraphStore | GraphDBGraphStore:
    """Instantiate an RDF store backend by configuration alone (CRA-024.11, ONT-003)."""
    backend = config.get("backend", "fuseki").lower()
    endpoint = config.get("endpoint_url", "http://localhost:3030/ds" if backend == "fuseki" else "http://localhost:7200")
    username = config.get("username", "")
    password = config.get("password", "")
    timeout = float(config.get("timeout", 30.0))
    if backend == "graphdb":
        return GraphDBGraphStore(endpoint_url=endpoint, repository=config.get("repository", "eoip"),
                                 username=username, password=password, timeout=timeout)
    if backend == "fuseki":
        return FusekiGraphStore(endpoint_url=endpoint, dataset=config.get("dataset", "ds"),
                                username=username, password=password, timeout=timeout)
    raise ValueError(f"Unsupported RDF backend: {backend}. Supported: 'fuseki', 'graphdb'")
