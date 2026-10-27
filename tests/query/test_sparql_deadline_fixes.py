"""Deadline defects SP2Bench found in the live SPARQL backends (CRA-024.9 / A.2), pinned offline.

* Fuseki's ``timeout`` parameter is in seconds: EOIP sent milliseconds, so an over-budget query kept
  running server-side long after the client gave up.
* GraphDB answers an expired query with HTTP 200 plus partial rows, flagged only by ``X-GraphDB-Warning``;
  EOIP returned those rows as the answer.
* GraphDB 10.7 sometimes fails an interrupted query with a 500 at the deadline instead of a 503.
"""
from __future__ import annotations

import json

import httpx
import pytest

from eoip.query import sparql_backend as sb
from eoip.query.sparql_backend import FusekiSparqlBackend, GraphDBSparqlBackend, SparqlBackendError, SparqlCancelled
from eoip.query.sparql_protocol import SparqlProtocolHandler

Q = "SELECT ?s WHERE { ?s ?p ?o }"
ROWS = {"head": {"vars": ["s"]}, "results": {"bindings": [{"s": {"type": "uri", "value": "http://x/1"}}]}}


def _fake(monkeypatch, response: httpx.Response, seen: list, elapsed_s: float = 0.0):
    clock = iter([0.0, elapsed_s])

    def post(url, **kw):
        seen.append(kw)
        return response

    monkeypatch.setattr(sb.httpx, "post", post)
    monkeypatch.setattr(sb.time, "perf_counter", lambda: next(clock))


@pytest.mark.parametrize("deadline_ms,expected", [(30_000, "30"), (2_500, "2.5"), (5_000, "5")])
def test_fuseki_timeout_parameter_is_sent_in_seconds(monkeypatch, deadline_ms, expected) -> None:
    seen: list = []
    _fake(monkeypatch, httpx.Response(200, json=ROWS), seen)
    FusekiSparqlBackend("http://f/ds", deadline_ms=deadline_ms).query(Q)
    assert seen[0]["data"]["timeout"] == expected


def test_graphdb_timeout_parameter_is_whole_seconds(monkeypatch) -> None:
    seen: list = []
    _fake(monkeypatch, httpx.Response(200, json=ROWS), seen)
    GraphDBSparqlBackend("http://g/repositories/r", deadline_ms=30_000).query(Q)
    assert seen[0]["data"]["timeout"] == "30"


def test_graphdb_partial_results_at_timeout_are_a_cancellation_not_an_answer(monkeypatch) -> None:
    resp = httpx.Response(200, json=ROWS,
                          headers={"X-GraphDB-Warning": "The query has timed out, results may be incomplete."})
    _fake(monkeypatch, resp, [], elapsed_s=30.0)
    with pytest.raises(SparqlCancelled, match="incomplete"):
        GraphDBSparqlBackend("http://g/repositories/r").query(Q)


def test_endpoint_answers_504_for_graphdb_partial_results(monkeypatch) -> None:
    resp = httpx.Response(200, json=ROWS, headers={"X-GraphDB-Warning": "The query has timed out"})
    _fake(monkeypatch, resp, [], elapsed_s=30.0)
    h = SparqlProtocolHandler(rdf_backend=GraphDBSparqlBackend("http://g/repositories/r"))
    status, _, body = h.handle_request("POST", headers={"Content-Type": "application/sparql-query"}, body=Q)
    assert status == 504 and "incomplete" in body


def test_graphdb_500_at_the_deadline_is_a_cancellation(monkeypatch) -> None:
    _fake(monkeypatch, httpx.Response(500, text="Query evaluation error: java.lang.NullPointerException"), [],
          elapsed_s=30.0)
    with pytest.raises(SparqlCancelled):
        GraphDBSparqlBackend("http://g/repositories/r").query(Q)


def test_graphdb_500_well_before_the_deadline_stays_a_backend_error(monkeypatch) -> None:
    _fake(monkeypatch, httpx.Response(500, text="boom"), [], elapsed_s=0.2)
    with pytest.raises(SparqlBackendError):
        GraphDBSparqlBackend("http://g/repositories/r").query(Q)


def test_complete_graphdb_results_are_returned(monkeypatch) -> None:
    _fake(monkeypatch, httpx.Response(200, content=json.dumps(ROWS).encode()), [])
    res = GraphDBSparqlBackend("http://g/repositories/r").query(Q)
    assert res.vars == ["s"] and len(res.bindings) == 1 and not res.truncated
