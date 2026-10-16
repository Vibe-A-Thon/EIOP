"""Unit tests for GAP-TAX-001 / GAP-STUDIO-005 SKOS taxonomy management."""

import pytest
from eoip.ontology.skos import (
    MappingKind,
    SkosTaxonomy,
    concept_qname,
)


@pytest.fixture
def taxonomy():
    tax = SkosTaxonomy()
    tax.create_scheme("Technology Stack", "Core technology taxonomy", scheme_id="tech")
    return tax


def _tech_stack(tax: SkosTaxonomy):
    programming = tax.add_concept("tech", "Programming", concept_id="prog")
    python = tax.add_concept(
        "tech",
        "Python",
        concept_id="python",
        definition="Python programming language",
        notation="PY",
        alt_labels=["py"],
        hidden_labels=["snake"],
    )
    java = tax.add_concept("tech", "Java", concept_id="java")
    fastapi = tax.add_concept("tech", "FastAPI", concept_id="fastapi")
    tax.add_broader("python", "prog")
    tax.add_broader("java", "prog")
    tax.add_broader("fastapi", "python")
    return programming, python, java, fastapi


def test_scheme_and_concept_creation(taxonomy):
    scheme = taxonomy.schemes["tech"]
    assert scheme.urn == "urn:eoip:ontology:scheme:tech"
    _, python, _, _ = _tech_stack(taxonomy)
    assert python.pref_label == "Python"
    assert python.alt_labels == ["py"]
    assert python.hidden_labels == ["snake"]
    assert python.definition.startswith("Python")
    assert python.notation == "PY"
    assert python.urn == "urn:eoip:ontology:concept:python"
    assert concept_qname("python") == python.urn


def test_concept_requires_known_scheme(taxonomy):
    with pytest.raises(KeyError):
        taxonomy.add_concept("missing", "Ghost")


def test_duplicate_concept_id_rejected(taxonomy):
    taxonomy.add_concept("tech", "One", concept_id="dup")
    with pytest.raises(ValueError):
        taxonomy.add_concept("tech", "Two", concept_id="dup")


def test_empty_pref_label_rejected(taxonomy):
    with pytest.raises(ValueError):
        taxonomy.add_concept("tech", "   ")


def test_broader_narrower_are_reciprocal(taxonomy):
    _tech_stack(taxonomy)
    assert taxonomy.concepts["python"].broader == ["prog"]
    assert taxonomy.concepts["prog"].narrower == ["python", "java"]
    with pytest.raises(ValueError):
        taxonomy.add_broader("python", "python")


def test_cross_scheme_relationship_rejected(taxonomy):
    taxonomy.create_scheme("Other", scheme_id="other")
    taxonomy.add_concept("tech", "A", concept_id="a")
    taxonomy.add_concept("other", "B", concept_id="b")
    with pytest.raises(ValueError):
        taxonomy.add_broader("a", "b")
    with pytest.raises(ValueError):
        taxonomy.add_related("a", "b")


def test_transitive_broader_closure(taxonomy):
    _tech_stack(taxonomy)
    assert taxonomy.broader_closure("fastapi") == ["prog", "python"]
    assert taxonomy.broader_closure("python") == ["prog"]
    assert taxonomy.broader_closure("prog") == []


def test_transitive_narrower_closure(taxonomy):
    _tech_stack(taxonomy)
    assert taxonomy.narrower_closure("prog") == ["fastapi", "java", "python"]
    assert taxonomy.narrower_closure("python") == ["fastapi"]


def test_related_is_symmetric(taxonomy):
    _tech_stack(taxonomy)
    taxonomy.add_related("python", "java")
    assert taxonomy.concepts["python"].related == ["java"]
    assert taxonomy.concepts["java"].related == ["python"]
    with pytest.raises(ValueError):
        taxonomy.add_related("python", "python")


def test_collection_membership(taxonomy):
    _tech_stack(taxonomy)
    coll = taxonomy.create_collection("tech", "Languages", collection_id="langs")
    taxonomy.add_to_collection("langs", "python")
    taxonomy.add_to_collection("langs", "java")
    assert coll.member_ids == ["python", "java"]
    assert taxonomy.concepts["python"].in_collections == ["langs"]
    taxonomy.add_concept("tech", "Unrelated", concept_id="solo")
    taxonomy.add_to_collection("langs", "solo")
    assert taxonomy.concepts["solo"].in_collections == ["langs"]


def test_cross_scheme_collection_membership_rejected(taxonomy):
    taxonomy.create_scheme("Other", scheme_id="other")
    taxonomy.add_concept("other", "B", concept_id="b")
    taxonomy.create_collection("tech", "Tech Coll", collection_id="c1")
    with pytest.raises(ValueError):
        taxonomy.add_to_collection("c1", "b")


def test_mappings_for_crosswalks(taxonomy):
    _tech_stack(taxonomy)
    taxonomy.create_scheme("Glossary", "Business glossary", scheme_id="gloss")
    taxonomy.add_concept("gloss", "Python (glossary)", concept_id="g-python")
    m1 = taxonomy.add_mapping("python", "g-python", MappingKind.EXACT)
    m2 = taxonomy.add_mapping("python", "g-python", MappingKind.CLOSE)
    assert m1.urn == "urn:eoip:ontology:mapping:python:exactMatch:g-python"
    found = taxonomy.mappings_for("python")
    assert {m.kind for m in found} == {MappingKind.EXACT, MappingKind.CLOSE}
    assert taxonomy.mappings_for("python", MappingKind.EXACT) == [m1]
    # reverse lookup via target id
    assert taxonomy.mappings_for("g-python", MappingKind.CLOSE) == [m2]
    with pytest.raises(ValueError):
        taxonomy.add_mapping("python", "python", MappingKind.EXACT)


def test_label_conflict_detection(taxonomy):
    taxonomy.add_concept("tech", "Python", concept_id="python-1")
    taxonomy.add_concept("tech", "python", concept_id="python-2")
    taxonomy.add_concept("tech", "Java", concept_id="java")
    conflicts = taxonomy.detect_label_conflicts()
    assert len(conflicts) == 1
    conflict = conflicts[0]
    assert conflict.scheme_id == "tech"
    assert conflict.concept_ids == ["python-1", "python-2"]
    assert taxonomy.detect_label_conflicts(scheme_id="other-not-real") == []


def test_integrity_orphan_concepts(taxonomy):
    _tech_stack(taxonomy)
    taxonomy.add_concept("tech", "Lonely", concept_id="lonely")
    orphans = [i for i in taxonomy.validate_integrity() if i.kind == "orphan_concept"]
    assert [i.concept_ids for i in orphans] == [["lonely"]]


def test_integrity_broader_cycle(taxonomy):
    taxonomy.add_concept("tech", "A", concept_id="a")
    taxonomy.add_concept("tech", "B", concept_id="b")
    taxonomy.add_concept("tech", "C", concept_id="c")
    # hand-forge a cycle (add_broader blocks self-loops only)
    taxonomy.concepts["a"].broader = ["b"]
    taxonomy.concepts["b"].broader = ["c"]
    taxonomy.concepts["c"].broader = ["a"]
    cycles = [i for i in taxonomy.validate_integrity() if i.kind == "broader_cycle"]
    assert len(cycles) == 1
    assert sorted(cycles[0].concept_ids) == ["a", "b", "c"]


def test_integrity_cycle_dedup(taxonomy):
    taxonomy.add_concept("tech", "A", concept_id="a")
    taxonomy.add_concept("tech", "B", concept_id="b")
    taxonomy.concepts["a"].broader = ["b"]
    taxonomy.concepts["b"].broader = ["a"]
    cycles = [i for i in taxonomy.validate_integrity() if i.kind == "broader_cycle"]
    assert len(cycles) == 1
    assert sorted(cycles[0].concept_ids) == ["a", "b"]


def test_validate_integrity_scoped_to_scheme(taxonomy):
    _tech_stack(taxonomy)
    taxonomy.create_scheme("Other", scheme_id="other")
    taxonomy.add_concept("other", "Ghost", concept_id="ghost")
    issues = taxonomy.validate_integrity(scheme_id="tech")
    assert all(i.concept_ids != ["ghost"] for i in issues)
    assert any(i.concept_ids == ["ghost"] for i in taxonomy.validate_integrity(scheme_id="other"))


def test_export_rdf_jsonld(taxonomy):
    _tech_stack(taxonomy)
    taxonomy.add_related("python", "java")
    taxonomy.create_collection("tech", "Languages", collection_id="langs")
    taxonomy.add_to_collection("langs", "python")
    taxonomy.create_scheme("Glossary", scheme_id="gloss")
    taxonomy.add_concept("gloss", "Python (glossary)", concept_id="g-python")
    taxonomy.add_mapping("python", "g-python", MappingKind.EXACT)

    doc = taxonomy.export_rdf()
    assert doc["@context"]["skos"] == "http://www.w3.org/2004/02/skos/core#"
    assert doc["export"]["format"].startswith("SKOS JSON-LD")
    by_id = {item["@id"]: item for item in doc["@graph"]}

    scheme = by_id["urn:eoip:ontology:scheme:tech"]
    assert scheme["@type"] == "skos:ConceptScheme"
    assert scheme["title"] == "Technology Stack"

    python = by_id["urn:eoip:ontology:concept:python"]
    assert python["@type"] == "skos:Concept"
    assert python["prefLabel"] == "Python"
    assert python["altLabel"] == ["py"]
    assert python["notation"] == "PY"
    assert python["broader"] == [{"@id": "urn:eoip:ontology:concept:prog"}]
    assert {"@id": "urn:eoip:ontology:concept:java"} in python["related"]

    prog = by_id["urn:eoip:ontology:concept:prog"]
    assert {m["@id"] for m in prog["narrower"]} == {
        "urn:eoip:ontology:concept:python",
        "urn:eoip:ontology:concept:java",
    }

    coll = by_id["urn:eoip:ontology:collection:langs"]
    assert coll["@type"] == "skos:Collection"
    assert coll["member"] == [{"@id": "urn:eoip:ontology:concept:python"}]

    mapping = by_id["urn:eoip:ontology:mapping:python:exactMatch:g-python"]
    assert mapping["@type"] == "skos:mappingRelation"
    assert mapping["exactMatch"] == [{"@id": "urn:eoip:ontology:concept:g-python"}]

    assert doc["export"]["concepts"] == 5
    assert doc["export"]["mappings"] == 1
