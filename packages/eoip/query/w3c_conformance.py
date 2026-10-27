"""W3C SPARQL 1.1 test-suite runner for the EOIP /sparql pipeline (CRA-024.7).

Runs the official W3C manifests (https://github.com/w3c/rdf-tests, ``sparql/sparql11``) through the
same path production queries take: :class:`~eoip.query.sparql_protocol.SparqlProtocolHandler`
(HTTP-protocol parsing, governance checks, ``validate_query``, paging) on a qualified RDF backend
(Apache Jena Fuseki or Ontotext GraphDB Free). Every test gets an outcome; nothing is skipped
silently:

* ``pass`` / ``fail`` -- result set compared with the expected one (RDF term equality, blank-node
  isomorphism, order respected when the query has ORDER BY);
* ``rejected_by_design`` -- the query uses a form EOIP's read-only subset refuses on purpose
  (CONSTRUCT/DESCRIBE, unbounded ``*``/``+`` paths, SERVICE, update) and the endpoint answered
  422 with the documented error code -- checked, not assumed;
* ``error`` -- anything else (backend error, wrong status).

Syntax tests check EOIP's parser stage (``validate_query``): positive tests must parse, negative
ones must be refused with ``PARSE_ERROR``.

Usage::

    python -m eoip.query.w3c_conformance --suite /path/to/rdf-tests/sparql/sparql11 \\
        --backend fuseki --endpoint http://localhost:3030 --out report.json
"""
from __future__ import annotations

import argparse
import io
import itertools
import json
import os
import time
import urllib.parse
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable

import httpx
from rdflib import BNode, Dataset, Graph, Literal, Namespace, URIRef
from rdflib.graph import DATASET_DEFAULT_GRAPH_ID
from rdflib.collection import Collection
from rdflib.namespace import RDF, RDFS, XSD
from rdflib.plugins.sparql import prepareQuery
from rdflib.query import Result

MF = Namespace("http://www.w3.org/2001/sw/DataAccess/tests/test-manifest#")
QT = Namespace("http://www.w3.org/2001/sw/DataAccess/tests/test-query#")
DAWGT = Namespace("http://www.w3.org/2001/sw/DataAccess/tests/test-dawg#")
RS = Namespace("http://www.w3.org/2001/sw/DataAccess/tests/result-set#")
W3C_BASE = "https://w3c.github.io/rdf-tests/sparql/sparql11/"

#: Query-language manifests in scope for the read-only /sparql endpoint (update, federation,
#: entailment, service description and graph-store protocol suites are not query-endpoint features).
QUERY_DIRS = ("aggregates", "bind", "bindings", "cast", "construct", "exists", "functions", "grouping",
              "negation", "project-expression", "property-path", "subquery", "json-res", "csv-tsv-res",
              "syntax-query")
DESIGN_REJECTIONS = {"UNSUPPORTED_QUERY_FORM", "UNBOUNDED_PROPERTY_PATH", "SERVICE_NOT_APPROVED",
                     "UPDATE_NOT_PERMITTED"}


@dataclass
class TestCase:
    id: str
    name: str
    kind: str
    manifest: str
    query: Path | None = None
    data: list[Path] = field(default_factory=list)
    graph_data: list[tuple[Path, str]] = field(default_factory=list)
    result: Path | None = None


@dataclass
class Outcome:
    id: str
    name: str
    kind: str
    manifest: str
    outcome: str
    detail: str = ""
    elapsed_ms: float = 0.0
    engine_direct: str = ""  # outcome of the same request sent straight to the engine (only for non-passes)


def _url(path: Path, suite: Path) -> str:
    return W3C_BASE + path.resolve().relative_to(suite.resolve()).as_posix()


def load_tests(suite: Path, dirs: Iterable[str] = QUERY_DIRS) -> list[TestCase]:
    """Read the approved tests of the given manifests (``dawgt:Withdrawn``/``NotClassified`` are dropped)."""
    out: list[TestCase] = []
    for d in dirs:
        mpath = suite / d / "manifest.ttl"
        g = Graph()
        g.parse(mpath, format="turtle", publicID=_url(mpath, suite))
        base = mpath.parent
        manifest = next(g.subjects(RDF.type, MF.Manifest))
        entries = Collection(g, g.value(manifest, MF.entries)) if g.value(manifest, MF.entries) else []
        for t in entries:
            approval = g.value(t, DAWGT.approval)
            if approval is not None and approval != DAWGT.Approved:
                continue
            kind = str(g.value(t, RDF.type)).rsplit("#", 1)[-1]

            def local(u: Any) -> Path:
                return base / urllib.parse.unquote(str(u).rsplit("/", 1)[-1])

            tc = TestCase(id=str(t), name=str(g.value(t, MF.name) or t), kind=kind, manifest=d)
            action = g.value(t, MF.action)
            if kind.endswith("SyntaxTest11") or kind.endswith("SyntaxTest"):
                tc.query = local(action)
            else:
                tc.query = local(g.value(action, QT.query))
                tc.data = [local(x) for x in g.objects(action, QT.data)]
                for gd in g.objects(action, QT.graphData):
                    if isinstance(gd, BNode):
                        f, label = g.value(gd, QT.graph), str(g.value(gd, RDFS.label))
                        tc.graph_data.append((local(f), label))
                    else:
                        tc.graph_data.append((local(gd), _url(local(gd), suite)))
                res = g.value(t, MF.result)
                tc.result = local(res) if res is not None else None
            out.append(tc)
    return out


# ----------------------------------------------------------------------------------- backends


class _Store:
    """Test-fixture loader for one dedicated, disposable dataset (never the application dataset)."""

    def __init__(self, backend: str, server: str, dataset: str, auth: tuple[str, str] | None) -> None:
        self.backend, self.server, self.dataset, self.auth = backend, server.rstrip("/"), dataset, auth
        if backend == "fuseki":
            self.query_endpoint = f"{self.server}/{dataset}"
        else:
            self.query_endpoint = f"{self.server}/repositories/{dataset}"

    def create(self) -> None:
        if self.backend == "fuseki":
            r = httpx.get(f"{self.server}/$/datasets/{self.dataset}", auth=self.auth, timeout=30)
            if r.status_code == 404:
                httpx.post(f"{self.server}/$/datasets", data={"dbName": self.dataset, "dbType": "mem"},
                           auth=self.auth, timeout=30).raise_for_status()
            else:
                r.raise_for_status()
        else:
            ids = [x["id"] for x in httpx.get(f"{self.server}/rest/repositories", timeout=30).json()]
            if self.dataset not in ids:
                cfg = (Path(__file__).resolve().parents[3] / "deploy/graphdb/eoip-repo.ttl").read_text(encoding="utf-8")
                cfg = cfg.replace('rep:repositoryID "eoip"', f'rep:repositoryID "{self.dataset}"')
                httpx.post(f"{self.server}/rest/repositories", files={"config": ("repo.ttl", cfg, "text/turtle")},
                           timeout=60).raise_for_status()

    def clear(self) -> None:
        if self.backend == "fuseki":
            httpx.post(f"{self.query_endpoint}/update", data={"update": "DROP ALL"}, auth=self.auth,
                       timeout=60).raise_for_status()
        else:
            httpx.delete(f"{self.query_endpoint}/statements", auth=self.auth, timeout=60).raise_for_status()

    def load(self, path: Path, public_id: str, graph: str | None) -> None:
        import rdflib

        rdflib.NORMALIZE_LITERALS = False  # load literals with their exact lexical forms ("1.0e6" stays "1.0e6")
        if path.suffix in (".trig", ".nq"):
            ds = Dataset()
            ds.parse(path, format="trig" if path.suffix == ".trig" else "nquads", publicID=public_id)
            for ctx in ds.graphs():
                name = None if ctx.identifier == DATASET_DEFAULT_GRAPH_ID else str(ctx.identifier)
                if len(ctx):
                    self._put(ctx.serialize(format="nt"), name)
            return
        g = Graph()
        fmt = {".ttl": "turtle", ".rdf": "xml", ".nt": "nt", ".n3": "n3"}.get(path.suffix, "turtle")
        g.parse(path, format=fmt, publicID=public_id)
        self._put(g.serialize(format="nt"), graph)

    def _put(self, nt: str, graph: str | None) -> None:
        if self.backend == "fuseki":
            q = f"?graph={urllib.parse.quote(graph, safe='')}" if graph else "?default"
            r = httpx.post(f"{self.query_endpoint}/data{q}", content=nt.encode(),
                           headers={"Content-Type": "application/n-triples"}, auth=self.auth, timeout=60)
        else:
            q = f"?context={urllib.parse.quote('<' + graph + '>', safe='')}" if graph else ""
            r = httpx.post(f"{self.query_endpoint}/statements{q}", content=nt.encode(),
                           headers={"Content-Type": "text/plain"}, auth=self.auth, timeout=60)
        r.raise_for_status()

    def direct(self, query: str, accept: str) -> tuple[int, str]:
        """The same query straight to the engine's SPARQL endpoint, bypassing EOIP."""
        url = f"{self.query_endpoint}/sparql" if self.backend == "fuseki" else self.query_endpoint
        r = httpx.post(url, data={"query": query}, headers={"Accept": accept}, auth=self.auth, timeout=60)
        status = 400 if r.status_code == 400 else r.status_code
        return status, r.text

    def sparql_backend(self):
        from eoip.query.sparql_backend import FusekiSparqlBackend, GraphDBSparqlBackend

        cls = FusekiSparqlBackend if self.backend == "fuseki" else GraphDBSparqlBackend
        user, pw = self.auth or ("", "")
        return cls(self.query_endpoint, username=user, password=pw)


# ----------------------------------------------------------------------------------- comparison


def _term(b: dict[str, str] | None) -> Any:
    if b is None:
        return None
    t = b.get("type")
    if t == "uri":
        return URIRef(b["value"])
    if t == "bnode":
        return BNode(b["value"])
    if b.get("xml:lang"):
        return Literal(b["value"], lang=b["xml:lang"])
    if b.get("datatype"):
        return Literal(b["value"], datatype=URIRef(b["datatype"]))
    return Literal(b["value"])


_NUMERIC = {XSD.integer, XSD.decimal, XSD.double, XSD.float, XSD.int, XSD.long, XSD.short, XSD.byte,
            XSD.nonNegativeInteger, XSD.positiveInteger, XSD.negativeInteger, XSD.nonPositiveInteger,
            XSD.unsignedInt, XSD.unsignedLong, XSD.unsignedShort, XSD.unsignedByte}


def _norm(t: Any) -> Any:
    """RDF term equality on lexical form (no value canonicalisation); plain == xsd:string (RDF 1.1)."""
    if isinstance(t, Literal):
        dt = t.datatype if t.datatype != XSD.string else None
        if dt in _NUMERIC:  # numeric results compare by value ("2.0"^^xsd:decimal == "2"^^xsd:decimal)
            try:
                return ("N", repr(float(t.toPython())), str(dt))
            except (TypeError, ValueError):
                pass
        return ("L", str(t), (t.language or "").lower(), str(dt) if dt else "")
    if isinstance(t, BNode):
        return ("B", str(t))
    return ("U", str(t)) if t is not None else None


def _rows_from_result(res: Result) -> tuple[list[str], list[dict[str, Any]]]:
    vars_ = [str(v) for v in (res.vars or [])]
    rows = []
    for row in res.bindings:
        rows.append({str(k): v for k, v in row.items() if v is not None})
    return vars_, rows


def _rs_graph(path: Path, public_id: str) -> tuple[str, Any]:
    g = Graph()
    g.parse(path, format="turtle" if path.suffix == ".ttl" else "xml", publicID=public_id)
    rs = next(g.subjects(RDF.type, RS.ResultSet), None)
    if rs is None:
        return "GRAPH", g
    boolean = g.value(rs, RS.boolean)
    if boolean is not None:
        return "ASK", bool(boolean.toPython())
    rows, ordered = [], False
    for sol in g.objects(rs, RS.solution):
        idx = g.value(sol, RS.index)
        ordered = ordered or idx is not None
        row = {str(g.value(b, RS.variable)): g.value(b, RS.value) for b in g.objects(sol, RS.binding)}
        rows.append((int(idx) if idx is not None else 0, row))
    rows.sort(key=lambda x: x[0])
    return "SELECT", ([r for _, r in rows], ordered)


def expected(path: Path, public_id: str = "") -> tuple[str, Any]:
    if path.suffix in (".ttl", ".rdf"):
        return _rs_graph(path, public_id or path.as_uri())
    fmt = {".srx": "xml", ".srj": "json", ".tsv": "tsv", ".csv": "csv"}[path.suffix]
    with path.open("rb") as fh:
        res = Result.parse(fh, format=fmt)
    if res.type == "ASK":
        return "ASK", bool(res.askAnswer)
    return "SELECT", (_rows_from_result(res)[1], False)


def _match(exp: list[dict[str, Any]], got: list[dict[str, Any]], ordered: bool) -> bool:
    """Multiset (or sequence) equality of solutions up to a consistent blank-node bijection."""
    if len(exp) != len(got):
        return False
    e = [{k: _norm(v) for k, v in r.items()} for r in exp]
    g = [{k: _norm(v) for k, v in r.items()} for r in got]

    def key(r: dict[str, Any]) -> tuple:
        return tuple(sorted((k, v if v[0] != "B" else ("B", "")) for k, v in r.items()))

    if not any(v[0] == "B" for r in e + g for v in r.values()):
        return e == g if ordered else sorted(map(key, e)) == sorted(map(key, g))
    if sorted(map(key, e)) != sorted(map(key, g)):
        return False

    def search(i: int, used: set[int], m: dict[str, str], rm: dict[str, str]) -> bool:
        if i == len(e):
            return True
        cands = [i] if ordered else range(len(g))
        for j in cands:
            if j in used or key(e[i]) != key(g[j]):
                continue
            m2, rm2, ok = dict(m), dict(rm), True
            for k, v in e[i].items():
                w = g[j][k]
                if v[0] == "B":
                    if m2.setdefault(v[1], w[1]) != w[1] or rm2.setdefault(w[1], v[1]) != v[1]:
                        ok = False
                        break
            if ok and search(i + 1, used | {j}, m2, rm2):
                return True
        return False

    return search(0, set(), {}, {})


def _is_ordered(query_text: str) -> bool:
    try:
        alg = prepareQuery(query_text).algebra
    except Exception:  # noqa: BLE001 - unparsable here means the endpoint decides
        return False
    node = alg.get("p")
    while node is not None and getattr(node, "name", "") in ("Project", "Slice", "Distinct", "Reduced",
                                                              "ToMultiSet", "Extend"):
        node = node.get("p")
    return getattr(node, "name", "") == "OrderBy"


_ACCEPT = {".csv": "text/csv", ".tsv": "text/tab-separated-values", ".srx": "application/sparql-results+xml"}


def _to_json(t: Any) -> dict[str, str]:
    if isinstance(t, URIRef):
        return {"type": "uri", "value": str(t)}
    if isinstance(t, BNode):
        return {"type": "bnode", "value": str(t)}
    d = {"type": "literal", "value": str(t)}
    if t.language:
        d["xml:lang"] = t.language
    elif t.datatype:
        d["datatype"] = str(t.datatype)
    return d


def _with_base(text: str, base: str) -> str:
    """Resolve relative IRIs against the test's published location, unless the query sets its own BASE."""
    import re

    if re.search(r"^\s*BASE\s*<", re.sub(r"#[^\n]*", "", text), re.I | re.M):
        return text
    return f"BASE <{base}>\n{text}"


def _show(rows: list[dict[str, Any]]) -> str:
    return "; ".join(", ".join(f"{k}={v.n3() if hasattr(v, 'n3') else v}" for k, v in sorted(r.items()))
                     for r in rows)[:300]


def _design_code(body: str) -> str:
    """The documented refusal code in a 422 body when it is a deliberate supported-subset refusal."""
    for code in sorted(DESIGN_REJECTIONS):
        if code in body:
            return code
    return ""


def _same_table(expected_text: str, got_text: str, fmt: str, ordered: bool) -> tuple[bool, str]:
    """CSV/TSV result-format tests: same header and same rows (row order only when ORDER BY)."""
    import csv
    import io

    def rows(t: str) -> list[list[str]]:
        t = t.replace("\r\n", "\n").strip("\n")
        if fmt == ".csv":
            return [r for r in csv.reader(io.StringIO(t))]
        return [line.split("\t") for line in t.split("\n")]

    def canon(table: list[list[str]]) -> list[list[str]]:  # blank-node labels are local to a document
        labels: dict[str, str] = {}
        return [[labels.setdefault(c, f"_:n{len(labels)}") if c.startswith("_:") else c for c in r] for r in table]

    def num(table: list[list[str]]) -> list[list[str]]:  # bare numerals compare by value, as in _norm
        def cell(c: str) -> str:
            try:
                return repr(float(c)) if c and c[0] in "+-.0123456789" else c
            except ValueError:
                return c
        return [table[0]] + [[cell(c) for c in r] for r in table[1:]] if table else table

    e, g = num(canon(rows(expected_text))), num(canon(rows(got_text)))
    if not e or not g or e[0] != g[0]:
        return False, f"header differs: expected {e[:1]}, got {g[:1]}"
    eb, gb = e[1:], g[1:]
    if (eb == gb) if ordered else (sorted(eb) == sorted(gb)):
        return True, ""
    diff = [(a, b) for a, b in zip(eb, gb) if a != b][:2]
    return False, f"{len(eb)} vs {len(gb)} rows; first differences {diff}"


# ----------------------------------------------------------------------------------- runner


def _judge_syntax(kind: str, status: int, body: str) -> tuple[str, str]:
    positive = "Positive" in kind
    if positive and status == 422 and _design_code(body):
        return "rejected_by_design", _design_code(body)
    if positive:
        return ("pass", "") if status == 200 else ("fail", f"valid query answered {status}: {body[:160]}")
    return ("pass", "") if status == 400 else ("fail", f"invalid query answered {status}")


def _judge(tc: TestCase, text: str, status: int, body: str, suite: Path) -> tuple[str, str]:
    fmt = tc.result.suffix if tc.result is not None else ""
    if status == 422:
        code = _design_code(body)
        return ("rejected_by_design", code) if code else ("fail", f"refused: {body[:160]}")
    if status != 200:
        return "error", f"HTTP {status}: {body[:200]}"
    if fmt in (".csv", ".tsv"):
        ok, why = _same_table(tc.result.read_text(encoding="utf-8"), body, fmt, _is_ordered(text))
        return ("pass", "") if ok else ("fail", why)
    if fmt == ".srx":  # exercise the XML results serializer, read back with an independent parser
        parsed = Result.parse(io.BytesIO(body.encode("utf-8")), format="xml")
        data = ({"boolean": bool(parsed.askAnswer)} if parsed.type == "ASK" else
                {"results": {"bindings": [{k: _to_json(v) for k, v in r.items()}
                                          for r in _rows_from_result(parsed)[1]]}})
    else:
        data = json.loads(body)
    kind, exp = expected(tc.result, _url(tc.result, suite))
    if kind == "ASK":
        got = data.get("boolean")
        return ("pass", "") if got == exp else ("fail", f"ASK expected {exp}, got {got}")
    if kind != "SELECT":
        return "fail", "graph result expected but endpoint returned a result set"
    rows, ordered = exp
    ordered = ordered or _is_ordered(text)
    got = [{k: _term(v) for k, v in b.items()} for b in data["results"]["bindings"]]
    if _match(rows, got, ordered):
        return "pass", ""
    return "fail", (f"expected {len(rows)} rows, got {len(got)}" + (" (ordered)" if ordered else "")
                    + f"; first expected {_show(rows[:2])}; first got {_show(got[:2])}")


def run(tests: list[TestCase], store: _Store, suite: Path) -> list[Outcome]:
    """Run every test through EOIP's endpoint. When one does not pass, the identical request is replayed
    directly against the engine (``engine_direct``) so an engine deviation is told apart from an EOIP bug."""
    from eoip.query.sparql_protocol import SparqlProtocolHandler

    handler = SparqlProtocolHandler(rdf_backend=store.sparql_backend())
    out: list[Outcome] = []
    for tc in tests:
        o = Outcome(tc.id, tc.name, tc.kind, tc.manifest, "error")
        t0 = time.perf_counter()
        try:
            text = tc.query.read_text(encoding="utf-8")
            query = _with_base(text, _url(tc.query, suite))
            if "SyntaxTest" in tc.kind:
                # Through the endpoint: a malformed query must be answered 400 (SPARQL 1.1 Protocol), a
                # well-formed one must not be (200, or 422 when the supported subset refuses it on purpose).
                status, _, body = handler.handle_request(
                    "POST", headers={"Content-Type": "application/sparql-query"}, body=query)
                o.outcome, o.detail = _judge_syntax(tc.kind, status, body)
                if o.outcome in ("fail", "error"):
                    o.engine_direct = _judge_syntax(tc.kind, *store.direct(query, "application/sparql-results+json"))[0]
            else:
                store.clear()
                for d in tc.data:
                    store.load(d, _url(d, suite), None)
                for f, gname in tc.graph_data:
                    store.load(f, _url(f, suite), gname)
                accept = _ACCEPT.get(tc.result.suffix if tc.result else "", "application/sparql-results+json")
                status, _, body = handler.handle_request(
                    "POST", headers={"Content-Type": "application/x-www-form-urlencoded", "Accept": accept},
                    body=urllib.parse.urlencode({"query": query}))
                o.outcome, o.detail = _judge(tc, text, status, body, suite)
                if o.outcome in ("fail", "error"):
                    try:
                        o.engine_direct = _judge(tc, text, *store.direct(query, accept), suite)[0]
                    except Exception as exc:  # noqa: BLE001
                        o.engine_direct = f"error: {type(exc).__name__}"
        except Exception as exc:  # noqa: BLE001 - every test gets an outcome, never silently dropped
            o.outcome, o.detail = "error", f"{type(exc).__name__}: {str(exc)[:200]}"
        o.elapsed_ms = round((time.perf_counter() - t0) * 1000, 1)
        out.append(o)
    return out


def summarize(outcomes: list[Outcome]) -> dict[str, Any]:
    summary: dict[str, Any] = {"total": len(outcomes)}
    for key, grp in itertools.groupby(sorted(o.outcome for o in outcomes)):
        summary[key] = len(list(grp))
    by_manifest: dict[str, dict[str, int]] = {}
    for o in outcomes:
        by_manifest.setdefault(o.manifest, {}).setdefault(o.outcome, 0)
        by_manifest[o.manifest][o.outcome] += 1
    summary["by_manifest"] = by_manifest
    return summary


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--suite", required=True, type=Path, help="rdf-tests/sparql/sparql11 directory")
    ap.add_argument("--backend", choices=("fuseki", "graphdb"), required=True)
    ap.add_argument("--server", required=True, help="Fuseki server root or GraphDB root URL")
    ap.add_argument("--dataset", default="w3c")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--dirs", nargs="*", default=list(QUERY_DIRS))
    args = ap.parse_args(argv)
    user = os.environ.get("EOIP_W3C_BACKEND_USER", "")
    auth = (user, os.environ.get("EOIP_W3C_BACKEND_PASSWORD", "")) if user else None
    store = _Store(args.backend, args.server, args.dataset, auth)
    store.create()
    outcomes = run(load_tests(args.suite, args.dirs), store, args.suite)
    report = {"backend": args.backend, "suite": str(args.suite), "summary": summarize(outcomes),
              "outcomes": [asdict(o) for o in outcomes]}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
