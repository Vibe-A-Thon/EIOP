"""Defects the W3C SPARQL 1.1 suite found in the EOIP endpoint layer (CRA-024.7), pinned offline."""
from __future__ import annotations

import csv
import io
import json
import xml.etree.ElementTree as ET

import pytest
from rdflib.query import Result

from eoip.capabilities.model import UnsupportedCapabilityError
from eoip.qlang.manifest_registry import ManifestRegistry
from eoip.query.sparql_backend import RdflibSparqlBackend, _limited, has_unbounded_path, validate_query
from eoip.query.sparql_protocol import SparqlProtocolHandler

DATA = """@prefix : <http://example.org/> .
:s1 :p "a,b" . :s2 :p "x\\ty"@en . :s3 :p 1.0e6 . :s4 :p [] . :s5 :p 7 ."""


@pytest.fixture()
def handler() -> SparqlProtocolHandler:
    b = RdflibSparqlBackend()
    b.load_turtle(DATA)
    return SparqlProtocolHandler(rdf_backend=b)


def _post(handler, query: str, accept: str = "application/sparql-results+json"):
    return handler.handle_request("POST", headers={"Content-Type": "application/sparql-query", "Accept": accept},
                                  body=query)


@pytest.mark.parametrize("query, expected_tail", [
    ("SELECT * { ?s ?p ?o } VALUES ?s { <http://e/a> }", "\nLIMIT 6\nVALUES ?s { <http://e/a> }"),
    ("SELECT * { ?s ?p ?o } ORDER BY ?s VALUES (?s) { (<http://e/a>) }", "ORDER BY ?s\nLIMIT 6\nVALUES"),
    ("SELECT * { ?s ?p '}' } # } trailing\n", "\nLIMIT 6"),
])
def test_page_limit_goes_before_a_trailing_values_block(query: str, expected_tail: str) -> None:
    limited = _limited(query, 5)
    assert expected_tail in limited
    validate_query(limited)  # still a valid query (the old code appended LIMIT after VALUES: parse error)


def test_existing_limit_is_kept_even_with_trailing_values() -> None:
    q = "SELECT * { ?s ?p ?o } LIMIT 3 VALUES ?s { <http://e/a> }"
    assert _limited(q, 5) == q


@pytest.mark.parametrize("query, unbounded", [
    ("SELECT * { ?s <http://e/p>* ?o }", True),
    ("SELECT * { ?s (<http://e/p>/<http://e/q>)+ ?o }", True),
    ("SELECT * { ?s <http://e/p>? ?o }", False),
    ("SELECT (COUNT(*) AS ?c) { ?s ?p ?o }", False),
    ("SELECT ((?a)+?b AS ?x) { ?a ?p ?b }", False),
    ("SELECT (?a*?b AS ?x) { ?a ?p ?b }", False),
    ("not sparql at all *", False),
])
def test_unbounded_paths_are_decided_on_the_algebra(query: str, unbounded: bool) -> None:
    assert has_unbounded_path(query) is unbounded
    registry = ManifestRegistry()
    if unbounded:
        with pytest.raises(UnsupportedCapabilityError):
            registry.check_query_constructs("SPARQL", query)
    else:
        registry.check_query_constructs("SPARQL", query)  # arithmetic/COUNT(*) are not refused any more


def test_unbounded_path_is_a_clear_422_and_arithmetic_is_not(handler) -> None:
    status, _, body = _post(handler, "SELECT * { ?s <http://example.org/p>+ ?o }")
    assert status == 422 and "UNBOUNDED_PROPERTY_PATH" in body
    status, _, body = _post(handler, "SELECT ((?o)+1 AS ?x) { ?s <http://example.org/p> ?o FILTER(isNumeric(?o)) }")
    assert status == 200, body


def test_malformed_query_is_400_per_protocol(handler) -> None:
    status, _, body = _post(handler, "SELEC * { ?s ?p ?o }")
    assert status == 400 and "PARSE_ERROR" in body


def test_xml_results_carry_datatype_language_and_bnodes(handler) -> None:
    status, headers, body = _post(handler, "SELECT ?s ?o { ?s <http://example.org/p> ?o }",
                                  "application/sparql-results+xml")
    assert status == 200 and headers["Content-Type"] == "application/sparql-results+xml"
    parsed = Result.parse(io.BytesIO(body.encode()), format="xml")
    by_s = {str(r["s"]).rsplit("/", 1)[-1] if r["s"] is not None else "": r["o"] for r in parsed}
    assert by_s["s2"].language == "en"
    assert str(by_s["s5"].datatype) == "http://www.w3.org/2001/XMLSchema#integer"
    assert ET.fromstring(body).find(".//{http://www.w3.org/2005/sparql-results#}bnode") is not None


def test_csv_quotes_fields_and_prefixes_bnodes(handler) -> None:
    status, _, body = _post(handler, "SELECT ?s ?o { ?s <http://example.org/p> ?o } ORDER BY ?s", "text/csv")
    rows = list(csv.reader(io.StringIO(body)))
    assert rows[0] == ["s", "o"]
    values = [r[1] for r in rows[1:]]
    assert "a,b" in values  # one field, RFC 4180 quoted
    assert any(v.startswith("_:") for v in values)
    assert body.endswith("\r\n")


def test_tsv_uses_rdf_term_syntax(handler) -> None:
    status, _, body = _post(handler, "SELECT ?s ?o { ?s <http://example.org/p> ?o }", "text/tab-separated-values")
    lines = body.rstrip("\n").split("\n")
    assert lines[0] == "?s\t?o"
    cells = [line.split("\t") for line in lines[1:]]
    assert all(c[0].startswith("<") or c[0].startswith("_:") for c in cells)
    objs = {c[1] for c in cells}
    assert '"a,b"' in objs and '"x\\ty"@en' in objs and "7" in objs


def test_json_stays_the_default(handler) -> None:
    status, headers, body = _post(handler, "ASK { ?s ?p ?o }", "*/*")
    assert status == 200 and json.loads(body)["boolean"] is True

