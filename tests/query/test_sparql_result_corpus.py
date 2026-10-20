"""CRA-024.A.1: independent result corpus run on real SPARQL engines - rdflib everywhere, Apache Jena
Fuseki (qualified reference backend) when EOIP_LIVE_FUSEKI_URL is set (CI job sparql-fuseki)."""
from __future__ import annotations

import json
import os
import time
from collections import Counter
from pathlib import Path

import pytest

from eoip.query.sparql_backend import (
    FusekiSparqlBackend,
    RdflibSparqlBackend,
    SparqlBackendError,
    SparqlCancelled,
    SparqlRejected,
)

pytestmark = pytest.mark.req("CRA-024")
HERE = Path(__file__).parent / "sparql_corpus"
CORPUS = json.loads((HERE / "corpus.json").read_text())
DATA = (HERE / "data.ttl").read_text()
FUSEKI = os.getenv("EOIP_LIVE_FUSEKI_URL", "")


def _backends():
    yield pytest.param("rdflib", id="rdflib")
    yield pytest.param("fuseki", id="fuseki",
                       marks=pytest.mark.skipif(not FUSEKI, reason="no live Fuseki (set EOIP_LIVE_FUSEKI_URL)"))


@pytest.fixture(scope="module", params=list(_backends()))
def backend(request):
    if request.param == "rdflib":
        b = RdflibSparqlBackend()
    else:
        b = FusekiSparqlBackend(FUSEKI, username=os.getenv("EOIP_LIVE_FUSEKI_USER", "admin"),
                                password=os.getenv("EOIP_LIVE_FUSEKI_PASSWORD", ""))
    b.load_turtle(DATA)
    return b


def _rows(result):
    return [{k: v["value"] for k, v in row.items()} for row in result.bindings]


@pytest.mark.parametrize("case", CORPUS["cases"], ids=[c["id"] for c in CORPUS["cases"]])
def test_expected_results(backend, case):
    res = backend.query(CORPUS["prefix"] + case["query"], case.get("params"))
    if "boolean" in case:
        assert res.kind == "ASK" and res.boolean is case["boolean"]
        return
    got = _rows(res)
    if case.get("ordered"):
        assert got == case["rows"]
    else:
        key = lambda r: json.dumps(r, sort_keys=True)  # noqa: E731
        assert Counter(map(key, got)) == Counter(map(key, case["rows"]))


@pytest.mark.parametrize("case", CORPUS["rejected"], ids=[c["id"] for c in CORPUS["rejected"]])
def test_unsupported_constructs_fail_clearly(backend, case):
    with pytest.raises(SparqlRejected) as exc:
        backend.query(CORPUS["prefix"] + case["query"])
    assert exc.value.code == case["code"]


def test_row_budget_truncates_and_reports(backend):
    res = backend.query(CORPUS["prefix"] + "SELECT ?p ?n WHERE { ?p ex:name ?n }", max_rows=2)
    assert len(res.bindings) == 2 and res.truncated


def test_source_failure_is_reported_not_hidden():
    with pytest.raises(SparqlBackendError):
        FusekiSparqlBackend("http://127.0.0.1:9/ds").query("ASK { ?s ?p ?o }")


@pytest.mark.skipif(not FUSEKI, reason="no live Fuseki (set EOIP_LIVE_FUSEKI_URL)")
def test_deadline_cancels_on_the_backend_and_releases_resources():
    b = FusekiSparqlBackend(FUSEKI, username=os.getenv("EOIP_LIVE_FUSEKI_USER", "admin"),
                            password=os.getenv("EOIP_LIVE_FUSEKI_PASSWORD", ""))
    filler = "\n".join(f"<urn:s{i}> <urn:p> <urn:o{i % 50}> ." for i in range(3000))
    b.load_turtle(filler, graph="urn:g:filler")
    heavy = ("SELECT (COUNT(*) AS ?n) WHERE { GRAPH <urn:g:filler> { ?a ?b ?c . ?d ?e ?f . ?g ?h ?i } }")
    t0 = time.perf_counter()
    with pytest.raises(SparqlCancelled):
        b.query(heavy, deadline_ms=500)
    assert time.perf_counter() - t0 < 10  # aborted near the deadline, not after the full 2.7e10-row scan
    t1 = time.perf_counter()
    assert b.query("ASK { ?s ?p ?o }").boolean is True  # backend is free again
    assert time.perf_counter() - t1 < 2
