"""Real SPARQL execution for the /sparql endpoint and query services (CRA-024.2/.3/.7/.9, CRA-024.A.1).

Two executors share one contract:

* ``FusekiSparqlBackend`` - Apache Jena Fuseki (the qualified reference RDF backend) over the SPARQL 1.1
  protocol, with the server-side ``timeout`` so a cancelled/expired query releases backend resources;
* ``RdflibSparqlBackend`` - rdflib's SPARQL engine over an in-memory graph (embedded/offline use).

Every query is parsed into SPARQL algebra first (``validate_query``): updates, SERVICE federation to
unapproved endpoints and unbounded property paths (``*``/``+``) are rejected with a clear error before any
backend sees the text; parameters are bound as typed RDF terms (``bind_parameters``), never concatenated.
Budgets default to CRA-024.9 (deadline 30 s, 10,000 rows per page) and can only be lowered.
"""
from __future__ import annotations

import json
import re
import time
import urllib.parse
from dataclasses import dataclass, field
from typing import Any

import httpx
from rdflib import Graph, Literal, URIRef
from rdflib.paths import MulPath, Path as RdfPath
from rdflib.plugins.sparql import prepareQuery

DEADLINE_MS = 30_000
MAX_ROWS = 10_000


class SparqlRejected(ValueError):
    def __init__(self, code: str, detail: str) -> None:
        super().__init__(f"{code}: {detail}")
        self.code, self.detail = code, detail

    def to_dict(self) -> dict[str, str]:
        return {"error": "UNSUPPORTED_CAPABILITY", "construct": self.code, "detail": self.detail}


class SparqlBackendError(RuntimeError):
    """The backend could not be reached or failed (partial/source failure surfaces to the caller)."""


class SparqlCancelled(RuntimeError):
    """Deadline exceeded: the backend aborted the query and released its resources."""


@dataclass
class SparqlResult:
    kind: str  # SELECT | ASK
    vars: list[str] = field(default_factory=list)
    bindings: list[dict[str, dict[str, str]]] = field(default_factory=list)
    boolean: bool | None = None
    truncated: bool = False
    elapsed_ms: float = 0.0
    backend: str = ""


def _walk(node: Any, seen: set[int] | None = None):
    seen = seen if seen is not None else set()
    if id(node) in seen:
        return
    seen.add(id(node))
    yield node
    if isinstance(node, dict):
        for v in node.values():
            yield from _walk(v, seen)
    elif isinstance(node, (list, tuple)):
        for v in node:
            yield from _walk(v, seen)
    elif isinstance(node, RdfPath):
        for attr in ("path", "args"):
            sub = getattr(node, attr, None)
            if sub is not None:
                yield from _walk(sub, seen)


def validate_query(text: str, *, allowed_service_endpoints: tuple[str, ...] = ()) -> str:
    """Parse to algebra and enforce the supported subset. Returns SELECT or ASK."""
    if re.search(r"^\s*(INSERT|DELETE|LOAD|CLEAR|CREATE|DROP|COPY|MOVE|ADD)\b", re.sub(r"(?m)^\s*(PREFIX|BASE)\b.*$", "",
                                                                                       text), re.I | re.M):
        raise SparqlRejected("UPDATE_NOT_PERMITTED", "SPARQL Update is not accepted on the query endpoint")
    try:
        q = prepareQuery(text)
    except Exception as exc:  # noqa: BLE001 - parser error message is the clear failure
        raise SparqlRejected("PARSE_ERROR", str(exc).splitlines()[0][:200]) from exc
    name = q.algebra.name
    if name not in ("SelectQuery", "AskQuery"):
        raise SparqlRejected("UNSUPPORTED_QUERY_FORM", f"{name} is not in the supported subset (SELECT, ASK)")
    for node in _walk(q.algebra):
        if isinstance(node, MulPath) and node.mod in ("*", "+"):
            raise SparqlRejected("UNBOUNDED_PROPERTY_PATH",
                                 "property paths with * or + are unbounded; use a fixed-length or ? path")
        if getattr(node, "name", None) == "ServiceGraphPattern":
            target = str(node.get("term"))
            if target not in allowed_service_endpoints:
                raise SparqlRejected("SERVICE_NOT_APPROVED", f"federation to {target} is not an approved source")
    return "SELECT" if name == "SelectQuery" else "ASK"


_PARAM = re.compile(r"\$([A-Za-z_][A-Za-z0-9_]*)")


def bind_parameters(template: str, params: dict[str, Any] | None) -> str:
    """Replace ``$name`` placeholders with typed RDF terms. Strings become escaped literals, ``URIRef``
    values must be absolute IRIs; unknown or missing parameters are an error."""
    params = params or {}

    def term(match: re.Match) -> str:
        key = match.group(1)
        if key not in params:
            raise SparqlRejected("MISSING_PARAMETER", f"no value for ${key}")
        value = params[key]
        if isinstance(value, URIRef):
            if not re.fullmatch(r"[A-Za-z][A-Za-z0-9+.-]*:[^\s<>\"{}|\\^`]*", str(value)):
                raise SparqlRejected("BAD_IRI", f"${key} is not an absolute IRI")
            return value.n3()
        return Literal(value).n3()

    return _PARAM.sub(term, template)


def _tail_start(text: str) -> int:
    """Index just past the ``}`` that closes the outermost WHERE group (strings, IRIs and comments are
    skipped), i.e. where the solution modifiers and an optional trailing VALUES block begin."""
    depth, i, n = 0, 0, len(text)
    while i < n:
        c = text[i]
        if c == "#":
            j = text.find("\n", i)
            i = n if j < 0 else j
            continue
        if c in "\"'":
            q = c * 3 if text.startswith(c * 3, i) else c
            j = i + len(q)
            while j < n and not text.startswith(q, j):
                j += 2 if text[j] == "\\" else 1
            i = j + len(q)
            continue
        if c == "<" and depth == 0:
            m = re.match(r"<[^\s<>\"{}|^`]*>", text[i:])
            if m:
                i += m.end()
                continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i + 1  # the prologue has no braces, so the first top-level group is the WHERE
        i += 1
    return n


def _limited(text: str, max_rows: int) -> str:
    """Ask the backend for one row past the page so truncation is detected, without unbounded scans.
    The LIMIT goes into the solution modifiers, before a trailing ``VALUES`` block if there is one."""
    start = _tail_start(text)
    tail = text[start:]
    values = re.search(r"\bVALUES\b", tail, re.I)
    modifiers = tail[:values.start()] if values else tail
    if re.search(r"\bLIMIT\s+\d+", re.sub(r"#[^\n]*", "", modifiers), re.I):
        return text
    if values:
        cut = start + values.start()
        return f"{text[:cut].rstrip()}\nLIMIT {max_rows + 1}\n{text[cut:]}"
    return f"{text.rstrip()}\nLIMIT {max_rows + 1}"


def has_unbounded_path(text: str) -> bool:
    """True when the parsed query or update uses a ``*`` or ``+`` property path. Decided on the algebra,
    not the text, so ``SELECT *``, ``COUNT(*)`` and arithmetic are never mistaken for paths; text that
    does not parse returns False and is refused by :func:`validate_query` as ``PARSE_ERROR``."""
    from rdflib.plugins.sparql import prepareUpdate

    # An undeclared prefix is still a path: declare the missing ones so ``?s :knows* ?o`` is reported as
    # an unbounded path (the clearer error) rather than only as a parse error.
    declared = {m.lower() for m in re.findall(r"(?im)^\s*PREFIX\s+([A-Za-z0-9_.-]*):", text)}
    used = set(re.findall(r"(?<![\w<?$])([A-Za-z][\w.-]*|):(?=[A-Za-z_*+?/(]|\s)", re.sub(r"<[^>\s]*>|\"[^\"]*\"", "", text)))
    shim = "".join(f"PREFIX {p}: <urn:undeclared:{p}#>\n" for p in sorted(used) if p.lower() not in declared)
    for candidate in (text, shim + text) if shim else (text,):
        for parse in (prepareQuery, prepareUpdate):
            try:
                tree = parse(candidate)
            except Exception:  # noqa: BLE001 - not this form
                continue
            tree = getattr(tree, "algebra", tree)
            return any(isinstance(node, MulPath) and node.mod in ("*", "+") for node in _walk(tree))
    return False


def _dataset(dataset: dict[str, list[str]] | None) -> dict[str, list[str]]:
    """SPARQL 1.1 Protocol RDF dataset parameters, forwarded to the engine (they override FROM/FROM NAMED).
    Only absolute IRIs are accepted; the engine resolves them inside the tenant's own dataset."""
    out: dict[str, list[str]] = {}
    for key in ("default-graph-uri", "named-graph-uri"):
        vals = list((dataset or {}).get(key) or [])
        bad = [v for v in vals if not re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:[^\s<>\"{}|^`\\]*$", v)]
        if bad:
            raise SparqlRejected("PARSE_ERROR", f"{key} must be an absolute IRI")
        if vals:
            out[key] = vals
    return out


class FusekiSparqlBackend:
    name = "fuseki"

    def __init__(self, endpoint: str, *, username: str = "", password: str = "",
                 deadline_ms: int = DEADLINE_MS, max_rows: int = MAX_ROWS) -> None:
        self.endpoint = endpoint.rstrip("/")
        self.auth = (username, password) if username else None
        self.deadline_ms, self.max_rows = min(deadline_ms, DEADLINE_MS), min(max_rows, MAX_ROWS)

    def load_turtle(self, turtle: str, *, graph: str | None = None) -> None:
        url = f"{self.endpoint}/data" + (f"?graph={urllib.parse.quote(graph, safe='')}" if graph else "?default")
        try:
            r = httpx.put(url, content=turtle.encode(), headers={"Content-Type": "text/turtle"}, auth=self.auth,
                          timeout=60)
            r.raise_for_status()
        except httpx.HTTPError as exc:
            raise SparqlBackendError(f"fuseki load failed: {type(exc).__name__}") from exc

    def query(self, text: str, params: dict[str, Any] | None = None, *, deadline_ms: int | None = None,
              max_rows: int | None = None, dataset: dict[str, list[str]] | None = None) -> SparqlResult:
        text = bind_parameters(text, params)
        kind = validate_query(text)
        deadline = min(deadline_ms or self.deadline_ms, self.deadline_ms)
        rows = min(max_rows or self.max_rows, self.max_rows)
        body = _limited(text, rows) if kind == "SELECT" else text
        t0 = time.perf_counter()
        try:
            # Fuseki's ``timeout`` parameter is in (fractional) seconds; sending milliseconds would let a runaway
            # query keep running server-side for hours after the client gave up (found by SP2Bench Q7).
            r = httpx.post(f"{self.endpoint}/sparql", data={"query": body, "timeout": f"{deadline / 1000:g}", **_dataset(dataset)},
                           headers={"Accept": "application/sparql-results+json"},
                           timeout=deadline / 1000 + 5)
        except httpx.TimeoutException as exc:
            raise SparqlCancelled(f"deadline {deadline} ms exceeded (client)") from exc
        except httpx.HTTPError as exc:
            raise SparqlBackendError(f"fuseki unreachable: {type(exc).__name__}") from exc
        elapsed = (time.perf_counter() - t0) * 1000
        if r.status_code == 503 or (r.status_code >= 400 and "timeout" in r.text.lower()):
            raise SparqlCancelled(f"deadline {deadline} ms exceeded; query aborted by the backend")
        if r.status_code == 400:  # the engine's own parser/static checks refused the text: a client error
            raise SparqlRejected("BACKEND_REJECTED_QUERY", r.text.strip().splitlines()[0][:200] if r.text.strip() else "")
        if r.status_code >= 400:
            raise SparqlBackendError(f"fuseki error {r.status_code}: {r.text[:200]}")
        try:
            data = r.json()
        except json.JSONDecodeError as exc:  # Fuseki streams results: a timeout mid-stream truncates the JSON
            raise SparqlCancelled(f"deadline {deadline} ms exceeded while streaming results") from exc
        if kind == "ASK":
            return SparqlResult("ASK", boolean=bool(data["boolean"]), elapsed_ms=elapsed, backend=self.name)
        b = data["results"]["bindings"]
        return SparqlResult("SELECT", vars=data["head"]["vars"], bindings=b[:rows], truncated=len(b) > rows,
                            elapsed_ms=elapsed, backend=self.name)


class GraphDBSparqlBackend(FusekiSparqlBackend):
    """Ontotext GraphDB (Free) over the RDF4J REST protocol: ``endpoint`` is the repository URL
    (``http://host:7200/repositories/<id>``). Same validation, budgets and paging as Fuseki."""

    name = "graphdb"

    def load_turtle(self, turtle: str, *, graph: str | None = None) -> None:
        url = f"{self.endpoint}/statements" + (f"?context={urllib.parse.quote('<' + graph + '>', safe='')}"
                                               if graph else "")
        try:
            r = httpx.post(url, content=turtle.encode(), headers={"Content-Type": "text/turtle"}, auth=self.auth,
                           timeout=60)
            r.raise_for_status()
        except httpx.HTTPError as exc:
            raise SparqlBackendError(f"graphdb load failed: {type(exc).__name__}") from exc

    def query(self, text: str, params: dict[str, Any] | None = None, *, deadline_ms: int | None = None,
              max_rows: int | None = None, dataset: dict[str, list[str]] | None = None) -> SparqlResult:
        text = bind_parameters(text, params)
        kind = validate_query(text)
        deadline = min(deadline_ms or self.deadline_ms, self.deadline_ms)
        rows = min(max_rows or self.max_rows, self.max_rows)
        body = _limited(text, rows) if kind == "SELECT" else text
        t0 = time.perf_counter()
        try:  # RDF4J ``timeout`` is in whole seconds; GraphDB aborts the query server-side when it expires
            r = httpx.post(self.endpoint, data={"query": body, "timeout": str(max(1, deadline // 1000)), **_dataset(dataset)},
                           headers={"Accept": "application/sparql-results+json"}, auth=self.auth,
                           timeout=deadline / 1000 + 5)
        except httpx.TimeoutException as exc:
            raise SparqlCancelled(f"deadline {deadline} ms exceeded (client)") from exc
        except httpx.HTTPError as exc:
            raise SparqlBackendError(f"graphdb unreachable: {type(exc).__name__}") from exc
        elapsed = (time.perf_counter() - t0) * 1000
        if r.status_code == 503 or (r.status_code >= 400 and "timeout" in r.text.lower()):
            raise SparqlCancelled(f"deadline {deadline} ms exceeded; query aborted by the backend")
        if r.status_code == 400:
            raise SparqlRejected("BACKEND_REJECTED_QUERY", r.text.strip().splitlines()[0][:200] if r.text.strip() else "")
        if r.status_code >= 400:
            if r.status_code >= 500 and elapsed >= deadline * 0.95:
                # GraphDB 10.7 sometimes fails an interrupted query with a 500 (NullPointerException) instead
                # of its 503; at the deadline that is the server-side cancellation, not a backend outage.
                raise SparqlCancelled(f"deadline {deadline} ms exceeded; GraphDB aborted the query "
                                      f"({r.status_code})")
            raise SparqlBackendError(f"graphdb error {r.status_code}: {r.text[:200]}")
        if "timed out" in r.headers.get("X-GraphDB-Warning", "").lower():
            # GraphDB answers an expired query with 200 and whatever it had found so far, flagged only in this
            # header; passing that off as the answer would be a silently wrong result (found by SP2Bench Q5a).
            raise SparqlCancelled(f"deadline {deadline} ms exceeded; GraphDB returned incomplete results")
        try:
            data = r.json()
        except json.JSONDecodeError as exc:
            raise SparqlCancelled(f"deadline {deadline} ms exceeded while streaming results") from exc
        if kind == "ASK":
            return SparqlResult("ASK", boolean=bool(data["boolean"]), elapsed_ms=elapsed, backend=self.name)
        b = data["results"]["bindings"]
        return SparqlResult("SELECT", vars=data["head"]["vars"], bindings=b[:rows], truncated=len(b) > rows,
                            elapsed_ms=elapsed, backend=self.name)


def _term_json(t: Any) -> dict[str, str]:
    if isinstance(t, URIRef):
        return {"type": "uri", "value": str(t)}
    if isinstance(t, Literal):
        d = {"type": "literal", "value": str(t)}
        if t.language:
            d["xml:lang"] = t.language
        elif t.datatype:
            d["datatype"] = str(t.datatype)
        return d
    return {"type": "bnode", "value": str(t)}


class RdflibSparqlBackend:
    name = "rdflib"

    def __init__(self, graph: Graph | None = None, *, deadline_ms: int = DEADLINE_MS, max_rows: int = MAX_ROWS):
        self.graph = graph if graph is not None else Graph()
        self.deadline_ms, self.max_rows = min(deadline_ms, DEADLINE_MS), min(max_rows, MAX_ROWS)

    def load_turtle(self, turtle: str, *, graph: str | None = None) -> None:
        self.graph.parse(data=turtle, format="turtle")

    def query(self, text: str, params: dict[str, Any] | None = None, *, deadline_ms: int | None = None,
              max_rows: int | None = None, dataset: dict[str, list[str]] | None = None) -> SparqlResult:
        if dataset:  # the embedded engine has a single graph: no protocol dataset selection
            raise SparqlRejected("DATASET_NOT_SUPPORTED", "default-graph-uri/named-graph-uri need an RDF server backend")
        text = bind_parameters(text, params)
        kind = validate_query(text)
        rows = min(max_rows or self.max_rows, self.max_rows)
        t0 = time.perf_counter()
        res = self.graph.query(_limited(text, rows) if kind == "SELECT" else text)
        elapsed = (time.perf_counter() - t0) * 1000
        if kind == "ASK":
            return SparqlResult("ASK", boolean=bool(res.askAnswer), elapsed_ms=elapsed, backend=self.name)
        vars_ = [str(v) for v in res.vars]
        out = [{v: _term_json(row[i]) for i, v in enumerate(vars_) if row[i] is not None} for row in res]
        return SparqlResult("SELECT", vars=vars_, bindings=out[:rows], truncated=len(out) > rows,
                            elapsed_ms=elapsed, backend=self.name)
