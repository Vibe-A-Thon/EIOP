"""Differential and contract tests for strict SHACL and OWLReasoner (G01-G03, CRA-016, CRA-020)."""
from __future__ import annotations
from types import SimpleNamespace
import pytest

from eoip.ontology.shacl_validator import SHACLValidator, SHACLShape, SHACLSeverity
from eoip.ontology.rdf import OWLReasoner

def test_shacl_min_counts_and_max_counts_enforced():
    """G01: SHACLShape.min_counts/max_counts must produce violations on out-of-bound counts."""
    v = SHACLValidator()
    v.shapes = {}
    v.register_shape(SHACLShape(
        shape_id="CardinalityShape",
        target_class="Service",
        min_counts={"name": 2, "required_tag": 1},
        max_counts={"tag": 1},
        severity=SHACLSeverity.VIOLATION,
    ))
    
    # Node has name with 1 item (needs >= 2), tag with 2 items (allows <= 1), required_tag missing (needs >= 1)
    store = SimpleNamespace(find_vertices=lambda: [{
        "label": "Service",
        "canonical_id": "urn:test:service-1",
        "properties": {
            "name": "OnlyOneName",
            "tag": ["alpha", "beta"],
        },
    }])
    report = v.validate(store)
    assert not report.conforms
    assert report.total_violations == 3
    paths = {viol.path for viol in report.violations}
    assert paths == {"name", "tag", "required_tag"}

def test_shacl_check_datatype_strict():
    """G02: _check_datatype must reject unsupported datatypes and validate known types strictly."""
    v = SHACLValidator()
    assert v._check_datatype("hello", "string") is True
    assert v._check_datatype(123, "int") is True
    assert v._check_datatype(True, "int") is False  # bool is not int
    assert v._check_datatype(3.14, "float") is True
    assert v._check_datatype(True, "bool") is True
    assert v._check_datatype([1, 2], "list") is True
    assert v._check_datatype({"a": 1}, "dict") is True
    assert v._check_datatype("hello", "xsd:string") is True
    assert v._check_datatype(42, "xsd:integer") is True
    
    # Unknown datatype must return False
    assert v._check_datatype("text", "unsupported_type") is False
    assert v._check_datatype("text", "custom:nonexistent") is False
    assert v._check_datatype(123, "magic_type") is False

def test_owl_reasoner_preserves_case_sensitivity():
    """G03: Case-distinct IRIs must never be equated by lowercasing."""
    reasoner = OWLReasoner()
    # Distinct IRIs without explicit axiom must NOT be subclasses of each other
    assert reasoner.is_subclass_of("urn:example:A", "urn:example:a") is False
    assert reasoner.is_subclass_of("urn:example:a", "urn:example:A") is False
    assert reasoner.is_subclass_of("urn:example:A", "urn:example:A") is True

    # When explicit case-preserved axiom is added
    reasoner.add_subclass("urn:example:ChildA", "urn:example:ParentA")
    assert reasoner.is_subclass_of("urn:example:ChildA", "urn:example:ParentA") is True
    assert reasoner.is_subclass_of("urn:example:childa", "urn:example:ParentA") is False
    assert reasoner.is_subclass_of("urn:example:ChildA", "urn:example:parenta") is False
