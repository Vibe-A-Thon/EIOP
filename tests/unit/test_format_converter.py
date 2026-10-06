"""Tests for FormatConverter: all 8 output formats."""

from eoip.graph.format_converter import FormatConverter
from eoip.graph.memory import MemoryGraphStore


def _populated_store():
    store = MemoryGraphStore()
    store.upsert_vertex("WorkItem", {
        "canonical_id": "issue:1", "issue_key": "EOIP-1",
        "summary": "Build ontology", "status": "Open",
    })
    store.upsert_vertex("Commit", {
        "canonical_id": "commit:abc", "commit_sha": "abc123",
        "message": "Initial commit",
    })
    store.upsert_edge("IMPLEMENTS", "commit:abc", "issue:1", {"evidence_key": "e1"})
    return store


def test_available_formats_returns_all_supported():
    formats = FormatConverter.available_formats()
    ids = [f["id"] for f in formats]
    assert ids == ["rdf", "rdf_xml", "rdfs", "owl", "gremlin", "cypher", "opencypher", "gql", "sparql", "shacl", "pgql"]
    for f in formats:
        assert f["label"]
        assert f["ext"].startswith(".")


def test_to_rdf_turtle():
    converter = FormatConverter(_populated_store())
    output = converter.to_rdf_turtle()
    assert "@prefix eoip:" in output
    assert "rdf:type eoip:WorkItem" in output
    assert "rdf:type eoip:Commit" in output
    assert "eoip:IMPLEMENTS" in output


def test_to_rdf_xml():
    converter = FormatConverter(_populated_store())
    output = converter.to_rdf_xml()
    assert "rdf:RDF" in output
    assert "eoip:WorkItem" in output or "WorkItem" in output
    assert "rdf:Description" in output


def test_to_rdfs():
    converter = FormatConverter(_populated_store())
    output = converter.to_rdfs()
    assert "rdfs:Class" in output
    assert "eoip:WorkItem" in output
    assert "eoip:Commit" in output
    assert "rdf:Property" in output
    assert "eoip:IMPLEMENTS" in output


def test_to_owl():
    converter = FormatConverter(_populated_store())
    output = converter.to_owl()
    assert "owl:Ontology" in output
    assert "owl:Class" in output
    assert "owl:ObjectProperty" in output
    assert "eoip:WorkItem" in output


def test_to_gremlin():
    converter = FormatConverter(_populated_store())
    output = converter.to_gremlin()
    assert "g.addV('WorkItem')" in output
    assert "g.addV('Commit')" in output
    assert "addE('IMPLEMENTS')" in output


def test_to_cypher():
    converter = FormatConverter(_populated_store())
    output = converter.to_cypher()
    assert "MERGE (n:WorkItem" in output
    assert "MERGE (n:Commit" in output
    assert "MERGE (a)-[:IMPLEMENTS]->(b)" in output


def test_to_gql():
    converter = FormatConverter(_populated_store())
    output = converter.to_gql()
    assert 'INSERT (:' in output
    assert '"WorkItem"' in output
    assert '"IMPLEMENTS"' in output


def test_to_sparql_insert():
    converter = FormatConverter(_populated_store())
    output = converter.to_sparql_insert()
    assert "INSERT DATA" in output
    assert "rdf:type eoip:WorkItem" in output
    assert "eoip:IMPLEMENTS" in output


def test_convert_dispatches_by_format_id():
    converter = FormatConverter(_populated_store())
    for fmt in FormatConverter.available_formats():
        output = converter.convert(fmt["id"])
        assert len(output) > 0


def test_convert_unknown_format_raises():
    converter = FormatConverter(_populated_store())
    try:
        converter.convert("unknown_format")
        assert False, "Should have raised ValueError"
    except ValueError as exc:
        assert "Unknown format" in str(exc)


def test_empty_graph_produces_headers_only():
    converter = FormatConverter(MemoryGraphStore())
    turtle = converter.to_rdf_turtle()
    assert "@prefix" in turtle
    assert "rdf:type" not in turtle

    sparql = converter.to_sparql_insert()
    assert "INSERT DATA" in sparql


def test_xml_special_chars_escaped():
    store = MemoryGraphStore()
    store.upsert_vertex("WorkItem", {
        "canonical_id": "issue:esc", "issue_key": "ESC-1",
        "summary": "Fix <script> & \"quotes\"",
    })
    converter = FormatConverter(store)
    output = converter.to_rdf_xml()
    assert "<script>" not in output or "&lt;script&gt;" in output
