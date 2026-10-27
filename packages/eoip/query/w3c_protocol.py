"""W3C SPARQL 1.1 Protocol test suite driver (CRA-024.7, D-CRA-024-02).

Reads ``sparql11/protocol/manifest.ttl`` from the pinned w3c/rdf-tests checkout (machine-readable
``mf:ProtocolTest`` records: HTTP method, path, headers, body, expected status class, expected boolean /
result format), loads each test's ``ut:graphData`` into a disposable engine dataset as named graphs, and
replays the requests against EOIP's ``/api/v1/sparql`` through a caller-supplied HTTP client (the real
app, auth middleware included).

Honest outcomes: ``pass`` / ``fail`` / ``rejected_by_design``. Only two refusals count as by design, and
each is verified on the actual response: update operations (the endpoint is read-only; EOIP answers 400)
and RDF-graph results (CONSTRUCT/DESCRIBE are outside the supported subset; EOIP answers 422).
"""
from __future__ import annotations

import json
import re
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

from rdflib import Graph, Namespace
from rdflib.collection import Collection
from rdflib.namespace import RDF

MF = Namespace("http://www.w3.org/2001/sw/DataAccess/tests/test-manifest#")
HT = Namespace("http://www.w3.org/2011/http#")
CNT = Namespace("http://www.w3.org/2011/content#")
UT = Namespace("http://www.w3.org/2009/sparql/tests/test-update#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
DAWGT = Namespace("http://www.w3.org/2001/sw/DataAccess/tests/test-dawg#")
TABULAR = ("application/sparql-results+json", "application/sparql-results+xml", "text/csv",
           "text/tab-separated-values")
BOOLEAN = TABULAR[:2]


@dataclass
class Request:
    method: str
    path: str
    headers: dict[str, str]
    body: bytes | None
    expected_status: set[int]  # status classes: 2, 3, 4, 5
    expected_boolean: bool | None
    expected_format: str | None


@dataclass
class ProtocolTest:
    id: str
    name: str
    graphs: list[tuple[Path, str]]
    requests: list[Request]
    approved: bool


@dataclass
class Outcome:
    id: str
    name: str
    outcome: str
    detail: str = ""
    statuses: list[int] = field(default_factory=list)


def load_protocol_tests(suite: Path) -> list[ProtocolTest]:
    base = Path(suite).resolve() / "protocol"
    g = Graph()
    g.parse(base / "manifest.ttl", format="turtle", publicID=(base / "manifest.ttl").as_uri())
    manifest = next(g.subjects(RDF.type, MF.Manifest))
    out = []
    for test in Collection(g, g.value(manifest, MF.entries)):
        action = g.value(test, MF.action)
        graphs = [(base / Path(str(g.value(gd, UT.graph))).name, str(g.value(gd, RDFS.label)))
                  for gd in g.objects(test, UT.graphData)]
        reqs = []
        for r in Collection(g, g.value(action, HT.requests)):
            body_node = g.value(r, HT.body)
            body = None
            if body_node is not None:
                enc = str(g.value(body_node, CNT.characterEncoding) or "UTF-8")
                body = str(g.value(body_node, CNT.chars)).encode(enc)
            headers = {}
            hl = g.value(r, HT.headers)
            if hl is not None:
                for h in Collection(g, hl):
                    headers[str(g.value(h, HT.fieldName)).lower()] = str(g.value(h, HT.fieldValue))
            resp = g.value(r, HT.resp)
            status = {int(re.search(r"StatusCode(\d)xx", str(s)).group(1)) for s in g.objects(resp, MF.expectedStatus)}
            eb = g.value(resp, MF.expectedBoolean)
            ef = g.value(resp, MF.expectedFormat)
            reqs.append(Request(str(g.value(r, HT.methodName)), str(g.value(r, HT.absolutePath)), headers, body,
                                status, None if eb is None else bool(eb.toPython()), None if ef is None else str(ef)))
        tid = str(test).rsplit("#", 1)[-1]
        out.append(ProtocolTest(tid, str(g.value(test, MF.name)), graphs, reqs,
                                (test, DAWGT.approval, DAWGT.Approved) in g))
    return out


def _is_update(t: ProtocolTest) -> bool:
    return t.id.startswith("update") or any(
        b"update=" in (r.body or b"") or "update=" in r.path or
        r.headers.get("content-type", "").startswith("application/sparql-update") for r in t.requests)


def _boolean(ctype: str, body: str) -> bool | None:
    if "json" in ctype:
        try:
            return json.loads(body).get("boolean")
        except ValueError:
            return None
    m = re.search(r"<boolean>\s*(true|false)\s*</boolean>", body)
    return None if m is None else m.group(1) == "true"


Client = Callable[[str, str, dict[str, str], bytes | None], tuple[int, dict[str, str], str]]


def run_protocol_tests(tests: list[ProtocolTest], client: Client, load_graph: Callable[[Path, str], None],
                       prefix: str = "/api/v1/sparql") -> list[Outcome]:
    loaded: set[str] = set()
    outcomes = []
    for t in tests:
        for path, iri in t.graphs:
            if iri not in loaded:
                load_graph(path, iri)
                loaded.add(iri)
        statuses, problems = [], []
        by_design = None
        for r in t.requests:
            path = re.sub(r"^/sparql/?", prefix, r.path)
            status, headers, body = client(r.method, path, r.headers, r.body)
            statuses.append(status)
            ctype = {k.lower(): v for k, v in headers.items()}.get("content-type", "").split(";")[0].strip()
            if status // 100 in r.expected_status:
                if r.expected_boolean is not None and _boolean(ctype, body) is not r.expected_boolean:
                    problems.append(f"expected boolean {r.expected_boolean}, got {body[:120]!r}")
                fmt_ok = {"tabular": TABULAR, "boolean": BOOLEAN}.get(r.expected_format or "", None)
                if fmt_ok is not None and ctype not in fmt_ok:
                    problems.append(f"expected {r.expected_format} results, got content-type {ctype!r}")
                continue
            if _is_update(t) and status == 400 and "read-only" in body:
                by_design = "update operation refused: the endpoint is read-only (D-CRA-024-02)"
            elif r.expected_format == "RDF" and status == 422 and "UNSUPPORTED_QUERY_FORM" in body:
                by_design = "CONSTRUCT/DESCRIBE outside the supported query subset (CRA-024.7)"
            else:
                problems.append(f"{r.method} {path[:90]} -> {status}, expected "
                                f"{'/'.join(f'{c}xx' for c in sorted(r.expected_status))}: {body[:160]!r}")
            break
        if problems:
            outcomes.append(Outcome(t.id, t.name, "fail", "; ".join(problems), statuses))
        elif by_design:
            outcomes.append(Outcome(t.id, t.name, "rejected_by_design", by_design, statuses))
        else:
            outcomes.append(Outcome(t.id, t.name, "pass", "", statuses))
    return outcomes


def summarize(outcomes: list[Outcome]) -> dict[str, int]:
    s: dict[str, int] = {"total": len(outcomes)}
    for o in outcomes:
        s[o.outcome] = s.get(o.outcome, 0) + 1
    return s

