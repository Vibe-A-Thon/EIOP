"""Unified Semantic Query API (GAP-QUERY-001).

One entry point that routes a query to the right backend:

* ``gremlin``  - real interpreter for a Gremlin traversal subset over the graph store
* ``sparql``   - real interpreter for a SPARQL SELECT subset over an RDF triple view
* ``search``   - faceted full-text search (``eoip.search.facets``)
* ``vector``   - semantic vector similarity (``eoip.search.semantic``)
* ``federated``- federated query planner (``eoip.federation.planner``)
* ``eoql``     - Enterprise Object Query Language (``eoip.query.languages``)

Every mode returns the same envelope so callers do not care which backend ran.
No data is fabricated: results always come from the supplied store/index/planner.
"""
from __future__ import annotations

import re
import time
from dataclasses import dataclass, field
from typing import Any

MODES = ("auto", "gremlin", "sparql", "search", "vector", "federated", "eoql")

RDF_TYPE = "rdf:type"
ENTITY_NS = "eoip:entity/"
RELATION_NS = "eoip:relation/"
PROPERTY_NS = "eoip:property/"


class QueryError(ValueError):
    """Raised for syntactically or semantically invalid queries."""


@dataclass
class UnifiedQueryRequest:
    text: str = ""
    mode: str = "auto"
    params: dict[str, Any] = field(default_factory=dict)
    limit: int = 100


# ---------------------------------------------------------------------------
# Gremlin subset
# ---------------------------------------------------------------------------

def _split_args(raw: str) -> list[str]:
    args, buf, depth, quote = [], [], 0, ""
    for ch in raw:
        if quote:
            buf.append(ch)
            if ch == quote:
                quote = ""
            continue
        if ch in "'\"":
            quote = ch
            buf.append(ch)
        elif ch in "([":
            depth += 1
            buf.append(ch)
        elif ch in ")]":
            depth -= 1
            buf.append(ch)
        elif ch == "," and depth == 0:
            args.append("".join(buf).strip())
            buf = []
        else:
            buf.append(ch)
    tail = "".join(buf).strip()
    if tail:
        args.append(tail)
    return args


def _literal(token: str) -> Any:
    token = token.strip()
    if len(token) >= 2 and token[0] == token[-1] and token[0] in "'\"":
        return token[1:-1]
    low = token.lower()
    if low == "true":
        return True
    if low == "false":
        return False
    try:
        return int(token)
    except ValueError:
        pass
    try:
        return float(token)
    except ValueError:
        raise QueryError(f"unsupported literal: {token!r}") from None


def parse_gremlin(text: str) -> list[tuple[str, list[Any]]]:
    src = text.strip().rstrip(";")
    if not src.startswith("g."):
        raise QueryError("gremlin traversal must start with 'g.'")
    src = src[2:]
    steps: list[tuple[str, list[Any]]] = []
    i, n = 0, len(src)
    while i < n:
        m = re.match(r"([A-Za-z_]\w*)\(", src[i:])
        if not m:
            raise QueryError(f"invalid gremlin near: {src[i:i + 20]!r}")
        name = m.group(1)
        j = i + m.end()
        depth, quote, k = 1, "", j
        while k < n and depth:
            ch = src[k]
            if quote:
                if ch == quote:
                    quote = ""
            elif ch in "'\"":
                quote = ch
            elif ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
            k += 1
        if depth:
            raise QueryError("unbalanced parentheses in gremlin")
        steps.append((name, [_literal(a) for a in _split_args(src[j:k - 1])]))
        i = k
        if i < n:
            if src[i] != ".":
                raise QueryError(f"expected '.' at: {src[i:i + 10]!r}")
            i += 1
    if not steps:
        raise QueryError("empty gremlin traversal")
    return steps


class GremlinInterpreter:
    """Executes a Gremlin subset: V, E, hasLabel, has, hasNot, out, in, both,
    outE, inE, outV, inV, values, id, label, limit, dedup, count."""

    _SUPPORTED = {
        "V", "E", "hasLabel", "has", "hasNot", "out", "in", "both", "outE", "inE",
        "outV", "inV", "values", "id", "label", "limit", "dedup", "count",
    }

    def __init__(self, store: Any) -> None:
        self.store = store

    def run(self, text: str) -> tuple[list[Any], list[str]]:
        steps = parse_gremlin(text)
        trail = [s for s, _ in steps]
        for name, _ in steps:
            if name not in self._SUPPORTED:
                raise QueryError(f"unsupported gremlin step: {name}")
        first, args = steps[0]
        if first == "V":
            if args:
                current: list[Any] = [
                    v for v in (self._vertex(a) for a in args) if v is not None
                ]
            else:
                current = self.store.find_vertices(limit=1_000_000)
        elif first == "E":
            current = self.store.find_edges(limit=1_000_000)
        else:
            raise QueryError("traversal must start with V() or E()")
        for name, args in steps[1:]:
            current = self._apply(name, args, current)
        return current, trail

    def _vertex(self, ident: Any) -> dict | None:
        return self.store.get_vertex_by_canonical_id(str(ident)) or self.store.get_vertex(str(ident))

    @staticmethod
    def _is_edge(item: Any) -> bool:
        return isinstance(item, dict) and "out_v" in item

    @staticmethod
    def _is_vertex(item: Any) -> bool:
        return isinstance(item, dict) and "canonical_id" in item and "out_v" not in item

    def _apply(self, name: str, args: list[Any], cur: list[Any]) -> list[Any]:
        labels = [str(a) for a in args]
        if name == "hasLabel":
            return [x for x in cur if isinstance(x, dict) and x.get("label") in labels]
        if name == "has":
            if len(args) == 2:
                key, val = args
                return [x for x in cur if isinstance(x, dict) and x["properties"].get(key) == val]
            if len(args) == 3:
                lab, key, val = args
                return [x for x in cur if isinstance(x, dict) and x.get("label") == lab
                        and x["properties"].get(key) == val]
            if len(args) == 1:
                return [x for x in cur if isinstance(x, dict) and args[0] in x["properties"]]
            raise QueryError("has() takes 1-3 arguments")
        if name == "hasNot":
            return [x for x in cur if isinstance(x, dict) and args[0] not in x["properties"]]
        if name in ("out", "in", "both"):
            out: list[Any] = []
            for v in cur:
                if not self._is_vertex(v):
                    raise QueryError(f"{name}() requires vertices")
                vid = v["vid"] if "vid" in v else v["canonical_id"]
                if name in ("out", "both"):
                    out += [self.store.get_vertex(e["in_v"]) for e in
                            self.store.edges_from(vid, labels or None)]
                if name in ("in", "both"):
                    out += [self.store.get_vertex(e["out_v"]) for e in
                            self.store.edges_to(vid, labels or None)]
            return [x for x in out if x is not None]
        if name in ("outE", "inE"):
            out = []
            for v in cur:
                vid = v["vid"] if "vid" in v else v["canonical_id"]
                out += (self.store.edges_from(vid, labels or None) if name == "outE"
                        else self.store.edges_to(vid, labels or None))
            return out
        if name in ("outV", "inV"):
            key = "out_v" if name == "outV" else "in_v"
            out = [self.store.get_vertex(e[key]) for e in cur if self._is_edge(e)]
            return [x for x in out if x is not None]
        if name == "values":
            out = []
            for x in cur:
                props = x["properties"] if isinstance(x, dict) else {}
                for k in (labels or list(props)):
                    if k in props:
                        out.append(props[k])
            return out
        if name == "id":
            return [x.get("canonical_id", x.get("eid")) for x in cur if isinstance(x, dict)]
        if name == "label":
            return [x["label"] for x in cur if isinstance(x, dict)]
        if name == "limit":
            return cur[: int(args[0])]
        if name == "dedup":
            seen, out = set(), []
            for x in cur:
                key = (x.get("canonical_id") or x.get("eid")) if isinstance(x, dict) else repr(x)
                if key not in seen:
                    seen.add(key)
                    out.append(x)
            return out
        if name == "count":
            return [len(cur)]
        raise QueryError(f"unsupported gremlin step: {name}")


# ---------------------------------------------------------------------------
# SPARQL subset over an RDF triple view
# ---------------------------------------------------------------------------

def graph_triples(store: Any, limit: int = 100_000) -> list[tuple[str, str, Any]]:
    """Project the property graph into (subject, predicate, object) triples."""
    triples: list[tuple[str, str, Any]] = []
    for v in store.find_vertices(limit=limit):
        cid = v["canonical_id"]
        triples.append((cid, RDF_TYPE, ENTITY_NS + v["label"]))
        for k, val in v["properties"].items():
            if val is not None and isinstance(val, (str, int, float, bool)):
                triples.append((cid, PROPERTY_NS + k, val))
    for e in store.find_edges(limit=limit):
        triples.append((e["out_cid"], RELATION_NS + e["label"], e["in_cid"]))
    return triples


_SPARQL_RE = re.compile(
    r"^\s*(?:PREFIX\s+\w*:\s*<[^>]*>\s*)*SELECT\s+(?P<distinct>DISTINCT\s+)?(?P<vars>.+?)\s+"
    r"WHERE\s*\{(?P<body>.*)\}\s*(?:LIMIT\s+(?P<limit>\d+))?\s*$",
    re.IGNORECASE | re.DOTALL,
)
_TERM_RE = re.compile(r'"[^"]*"|<[^>]*>|[^\s]+')


def _sparql_term(tok: str) -> tuple[str, Any]:
    if tok.startswith("?"):
        return "var", tok[1:]
    if tok == "a":
        return "const", RDF_TYPE
    if tok.startswith("<") and tok.endswith(">"):
        return "const", tok[1:-1]
    if tok.startswith('"') and tok.endswith('"'):
        return "const", tok[1:-1]
    try:
        return "const", int(tok)
    except ValueError:
        pass
    try:
        return "const", float(tok)
    except ValueError:
        pass
    if tok in ("true", "false"):
        return "const", tok == "true"
    return "const", tok  # prefixed name


def _eq(a: Any, b: Any) -> bool:
    if a == b:
        return True
    return isinstance(a, (int, float, bool)) and str(a).lower() == str(b).lower()


class SparqlInterpreter:
    def __init__(self, store: Any) -> None:
        self.store = store

    def run(self, text: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        m = _SPARQL_RE.match(text)
        if not m:
            raise QueryError("only 'SELECT ... WHERE { ... } [LIMIT n]' is supported")
        body = m.group("body")
        patterns: list[tuple[tuple[str, Any], ...]] = []
        for raw in re.split(r"\s\.\s*|\.\s*$|\.\s*\n", body.strip() + " "):
            raw = raw.strip()
            if not raw:
                continue
            toks = _TERM_RE.findall(raw)
            if len(toks) != 3:
                raise QueryError(f"triple pattern must have 3 terms: {raw!r}")
            patterns.append(tuple(_sparql_term(t) for t in toks))
        if not patterns:
            raise QueryError("empty graph pattern")
        proj = m.group("vars").strip()
        all_vars = sorted({v for p in patterns for k, v in p if k == "var"})
        select = all_vars if proj == "*" else [t.lstrip("?") for t in proj.split()]
        for s in select:
            if s not in all_vars:
                raise QueryError(f"variable ?{s} not used in WHERE")

        triples = graph_triples(self.store)
        by_pred: dict[str, list[tuple[str, str, Any]]] = {}
        for t in triples:
            by_pred.setdefault(t[1], []).append(t)

        solutions: list[dict[str, Any]] = [{}]
        for pat in patterns:
            nxt: list[dict[str, Any]] = []
            for sol in solutions:
                if pat[1][0] == "var" and pat[1][1] in sol:
                    pool = by_pred.get(sol[pat[1][1]], [])
                elif pat[1][0] == "const":
                    pool = by_pred.get(pat[1][1], [])
                else:
                    pool = triples
                for tr in pool:
                    new = dict(sol)
                    ok = True
                    for (kind, val), actual in zip(pat, tr):
                        if kind == "const":
                            if not _eq(actual, val):
                                ok = False
                                break
                        else:
                            if val in new:
                                if not _eq(new[val], actual):
                                    ok = False
                                    break
                            else:
                                new[val] = actual
                    if ok:
                        nxt.append(new)
            solutions = nxt
            if not solutions:
                break
        rows = [{v: s[v] for v in select} for s in solutions]
        if m.group("distinct"):
            seen, uniq = set(), []
            for r in rows:
                key = tuple(sorted(r.items(), key=lambda kv: kv[0]))
                key = tuple((k, repr(v)) for k, v in key)
                if key not in seen:
                    seen.add(key)
                    uniq.append(r)
            rows = uniq
        if m.group("limit"):
            rows = rows[: int(m.group("limit"))]
        return rows, {"patterns": len(patterns), "triples_scanned": len(triples),
                      "variables": select}


# ---------------------------------------------------------------------------
# Unified API
# ---------------------------------------------------------------------------

def _row(rec: Any) -> Any:
    if isinstance(rec, dict) and "vid" in rec and "label" in rec and "properties" in rec:
        return {"canonical_id": rec["canonical_id"], "label": rec["label"],
                "properties": dict(rec["properties"])}
    if isinstance(rec, dict) and "out_v" in rec:
        return {"edge": rec["label"], "out": rec["out_cid"], "in": rec["in_cid"],
                "properties": dict(rec["properties"])}
    return rec


def detect_mode(text: str, params: dict[str, Any] | None = None) -> str:
    params = params or {}
    t = (text or "").strip()
    if params.get("entity_types") and not t.startswith(("g.", "SELECT", "select")):
        return "federated"
    if t.startswith("g."):
        return "gremlin"
    up = t.upper()
    if re.match(r"^(PREFIX\s|SELECT\s)", up) and "{" in t:
        return "sparql"
    if up.startswith(("SELECT ", "TRAVERSE ", "AGGREGATE ")):
        return "eoql"
    if params.get("vector"):
        return "vector"
    return "search"


class UnifiedQueryAPI:
    """Routes queries to Gremlin / RDF / search / vector / federated / EOQL."""

    def __init__(self, store: Any, *, vector_index: Any = None,
                 federation: Any = None) -> None:
        self.store = store
        self._vector_index = vector_index
        self.federation = federation

    # -- vector index management ------------------------------------------
    def vector_index(self) -> Any:
        if self._vector_index is None:
            from eoip.search.semantic import SemanticVectorIndex

            self._vector_index = SemanticVectorIndex()
            self.reindex_vectors()
        return self._vector_index

    def reindex_vectors(self) -> int:
        from eoip.search.semantic import SemanticVectorIndex

        if self._vector_index is None:
            self._vector_index = SemanticVectorIndex()
        count = 0
        for v in self.store.find_vertices(limit=1_000_000):
            props = v["properties"]
            text = " ".join(str(props[k]) for k in
                            ("name", "title", "summary", "description", "issue_key")
                            if props.get(k))
            if not text:
                continue
            self._vector_index.index_entity(v["canonical_id"], text,
                                            entity_type=v["label"])
            count += 1
        return count

    # -- entry point --------------------------------------------------------
    def query(self, request: UnifiedQueryRequest | str | None = None, **kwargs: Any) -> dict:
        if not isinstance(request, UnifiedQueryRequest):
            request = UnifiedQueryRequest(text=request or "", **kwargs)
        if request.mode not in MODES:
            raise QueryError(f"unknown mode {request.mode!r}; expected one of {MODES}")
        if request.limit < 1:
            raise QueryError("limit must be >= 1")
        started = time.perf_counter()
        mode = request.mode
        auto = mode == "auto"
        if auto:
            mode = detect_mode(request.text, request.params)
        warnings: list[str] = []
        handler = getattr(self, f"_run_{mode.replace('-', '_')}")
        results, plan = handler(request, warnings)
        truncated = len(results) > request.limit
        if truncated:
            results = results[: request.limit]
            warnings.append(f"results truncated to limit={request.limit}")
        return {
            "mode": mode,
            "auto_routed": auto,
            "dialect": plan.pop("dialect", mode),
            "results": results,
            "count": len(results),
            "truncated": truncated,
            "plan": plan,
            "warnings": warnings,
            "elapsed_ms": round((time.perf_counter() - started) * 1000, 3),
        }

    # -- backends -------------------------------------------------------------
    def _run_gremlin(self, req: UnifiedQueryRequest, warnings: list[str]):
        recs, trail = GremlinInterpreter(self.store).run(req.text)
        return [_row(r) for r in recs], {"dialect": "gremlin", "steps": trail,
                                        "backend": "graph_store"}

    def _run_sparql(self, req: UnifiedQueryRequest, warnings: list[str]):
        rows, plan = SparqlInterpreter(self.store).run(req.text)
        plan.update(dialect="sparql", backend="rdf_triple_view")
        return rows, plan

    def _run_search(self, req: UnifiedQueryRequest, warnings: list[str]):
        from eoip.search.facets import FacetedSearch, SearchRequest

        sr = SearchRequest(
            query=req.text,
            entity_types=list(req.params.get("entity_types", [])),
            limit=min(max(req.limit, 1), 500),
        )
        resp = FacetedSearch(self.store).search(sr)
        plan = {"dialect": "faceted-search", "backend": "faceted_search",
                "total": resp.total,
                "facets": resp.facets.model_dump() if hasattr(resp.facets, "model_dump") else {}}
        return [h.model_dump() for h in resp.hits], plan

    def _run_vector(self, req: UnifiedQueryRequest, warnings: list[str]):
        if not req.text.strip():
            raise QueryError("vector mode requires query text")
        from eoip.search.semantic import embed_text

        index = self.vector_index()
        hits = index.similarity_search(
            embed_text(req.text, index.dim), top_k=req.limit,
            entity_type=req.params.get("entity_type"),
            min_score=float(req.params.get("min_score", 0.0)),
        )
        rows = [{"canonical_id": h.entity_id, "score": h.score, "text": h.text,
                 "entity_type": h.entity_type} for h in hits]
        return rows, {"dialect": "vector-similarity", "backend": "semantic_vector_index",
                      "indexed": index.stats().get("total_entities",
                                                    len(getattr(index, "_entities", {})))}

    def _run_federated(self, req: UnifiedQueryRequest, warnings: list[str]):
        if self.federation is None:
            raise QueryError("no federation planner configured")
        types = list(req.params.get("entity_types") or
                     [t.strip() for t in req.text.split(",") if t.strip()])
        if not types:
            raise QueryError("federated mode requires entity_types")
        out = self.federation.execute(
            types,
            filters=req.params.get("filters"),
            projection=req.params.get("projection"),
            **({"merge_key": req.params["merge_key"]} if "merge_key" in req.params else {}),
        )
        rows = list(out.get("rows", []))
        if out.get("degraded"):
            warnings.append("one or more federated sources were degraded")
        return rows, {"dialect": "federated", "backend": "federation_planner",
                      "federation": out.get("plan", {})}

    def _run_eoql(self, req: UnifiedQueryRequest, warnings: list[str]):
        from eoip.query.languages import parse_eoql

        out = parse_eoql(self.store, req.text)
        if isinstance(out, dict):
            if out.get("error"):
                raise QueryError(str(out["error"]))
            key = next((k for k in ("results", "rows", "data") if k in out), None)
            rows = list(out[key]) if key else [out]
            plan = {k: v for k, v in out.items() if k != key} if key else {}
        else:
            rows, plan = list(out), {}
        plan.update(dialect="eoql", backend="eoql_executor")
        return [_row(r) for r in rows], plan
