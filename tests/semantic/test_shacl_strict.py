"""Differential and contract tests for strict SHACL and OWLReasoner (G01-G03, CRA-016, CRA-020)."""
from __future__ import annotations
from types import SimpleNamespace
import pytest

from eoip.ontology.shacl_validator import (
    SHACLValidator,
    SHACLShape,
    SHACLPropertyShape,
    SHACLSeverity,
    SHACLNodeKind,
    SHACLSetupError,
    UNSUPPORTED_CONSTRAINT,
    SHACL_CARDINALITY_VIOLATION,
    SHACL_DATATYPE_VIOLATION,
    SHACL_PATTERN_VIOLATION,
    SHACL_BOUND_VIOLATION,
    SHACL_LENGTH_VIOLATION,
    SHACL_LOGICAL_VIOLATION,
    SHACL_CLOSED_VIOLATION,
    SHACL_NODE_KIND_VIOLATION,
    PROFILE_SHACL_CORE_2017,
)
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
    store = SimpleNamespace(
        find_vertices=lambda: [{
            "label": "Service",
            "canonical_id": "urn:test:service-1",
            "properties": {
                "name": "OnlyOneName",
                "tag": ["alpha", "beta"],
            },
        }],
        find_edges=lambda: []
    )
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


def test_shacl_unknown_datatype_fails_setup():
    """CRA-020.3: Unknown datatype names fail validation setup."""
    v = SHACLValidator()
    with pytest.raises(SHACLSetupError) as exc_info:
        v.register_shape(SHACLShape(
            shape_id="BadDatatypeShape",
            target_class="Service",
            property_types={"custom_field": "unknown:special_datatype"},
        ))
    assert "Unknown datatype name or IRI" in str(exc_info.value)

    # Property shape setup failure
    with pytest.raises(SHACLSetupError):
        v.register_shape(SHACLShape(
            shape_id="BadPropShape",
            target_class="Service",
            property_shapes=[SHACLPropertyShape(path="custom_field", datatype="foo:nonexistent")],
        ))


def test_shacl_unsupported_constraint_rejected():
    """CRA-020.2: Unsupported constraints must produce an explicit unsupported result, never conforms=True."""
    v = SHACLValidator(profile=PROFILE_SHACL_CORE_2017)
    v.shapes = {}
    v.register_shape(SHACLShape(
        shape_id="AdvancedShape",
        target_class="Service",
        unsupported_components=["sh:SPARQLConstraintComponent"],
    ))
    store = SimpleNamespace(
        find_vertices=lambda: [{"label": "Service", "canonical_id": "srv-1", "properties": {}}],
        find_edges=lambda: []
    )
    report = v.validate(store)
    assert not report.conforms
    assert report.status == UNSUPPORTED_CONSTRAINT
    assert report.total_violations == 1
    assert report.violations[0].result_code == UNSUPPORTED_CONSTRAINT
    assert "sh:SPARQLConstraintComponent" in report.violations[0].source_constraint_component


def test_shacl_node_kind_and_patterns_and_lengths():
    """CRA-020.2: Enforce nodeKind, patterns, and min/max length bounds."""
    v = SHACLValidator()
    v.shapes = {}
    v.register_shape(SHACLShape(
        shape_id="StrictEntityShape",
        target_class="Artifact",
        patterns={"repo_id": r"^repo-[0-9]+$"},
        lengths={"code": (3, 8)},
        node_kinds={"source_uri": SHACLNodeKind.IRI},
    ))

    # Invalid: repo_id wrong pattern, code too short (len 2 < 3), source_uri not an IRI
    store = SimpleNamespace(
        find_vertices=lambda: [{
            "label": "Artifact",
            "canonical_id": "art-1",
            "properties": {
                "repo_id": "invalid_repo_name",
                "code": "ab",
                "source_uri": "just_a_string_without_scheme",
            },
        }],
        find_edges=lambda: []
    )
    report = v.validate(store)
    assert not report.conforms
    assert report.total_violations == 3
    result_codes = {viol.result_code for viol in report.violations}
    assert result_codes == {SHACL_PATTERN_VIOLATION, SHACL_LENGTH_VIOLATION, SHACL_NODE_KIND_VIOLATION}

    # Valid instance
    store_valid = SimpleNamespace(
        find_vertices=lambda: [{
            "label": "Artifact",
            "canonical_id": "art-1",
            "properties": {
                "repo_id": "repo-42",
                "code": "abcdef",
                "source_uri": "https://git.example.com/repo/1",
            },
        }],
        find_edges=lambda: []
    )
    report_valid = v.validate(store_valid)
    assert report_valid.conforms
    assert report_valid.total_violations == 0


def test_shacl_numeric_bounds():
    """CRA-020.2: Enforce min/max inclusive/exclusive numeric bounds."""
    v = SHACLValidator()
    v.shapes = {}
    v.register_shape(SHACLShape(
        shape_id="ScoreShape",
        target_class="Metric",
        numeric_bounds={
            "score": {"min_inclusive": 0.0, "max_inclusive": 100.0},
            "rank": {"min_exclusive": 0, "max_exclusive": 10},
        },
    ))

    # Invalid: score > 100, rank == 0 (violates min_exclusive > 0)
    store = SimpleNamespace(
        find_vertices=lambda: [{
            "label": "Metric",
            "canonical_id": "m-1",
            "properties": {"score": 105.0, "rank": 0},
        }],
        find_edges=lambda: []
    )
    report = v.validate(store)
    assert not report.conforms
    assert report.total_violations == 2
    assert all(viol.result_code == SHACL_BOUND_VIOLATION for viol in report.violations)

    # Valid
    store_valid = SimpleNamespace(
        find_vertices=lambda: [{
            "label": "Metric",
            "canonical_id": "m-1",
            "properties": {"score": 95.5, "rank": 5},
        }],
        find_edges=lambda: []
    )
    assert v.validate(store_valid).conforms is True


def test_shacl_closed_shapes():
    """CRA-020.2: Enforce sh:closed and sh:ignoredProperties."""
    v = SHACLValidator()
    v.shapes = {}
    v.register_shape(SHACLShape(
        shape_id="ClosedShape",
        target_class="Person",
        required_properties=["name"],
        closed=True,
        ignored_properties=["middle_name"],
    ))

    # Invalid: person has extra property 'favorite_color'
    store = SimpleNamespace(
        find_vertices=lambda: [{
            "label": "Person",
            "canonical_id": "p-1",
            "properties": {"name": "Alice", "favorite_color": "blue"},
        }],
        find_edges=lambda: []
    )
    report = v.validate(store)
    assert not report.conforms
    assert report.total_violations == 1
    assert report.violations[0].result_code == SHACL_CLOSED_VIOLATION
    assert report.violations[0].path == "favorite_color"

    # Valid: only allowed and ignored properties
    store_valid = SimpleNamespace(
        find_vertices=lambda: [{
            "label": "Person",
            "canonical_id": "p-1",
            "properties": {"name": "Alice", "middle_name": "Marie"},
        }],
        find_edges=lambda: []
    )
    assert v.validate(store_valid).conforms is True


def test_shacl_logical_constraints():
    """CRA-020.2: Enforce logical constraints sh:not and sh:xone."""
    v = SHACLValidator()
    v.shapes = {}

    forbidden_shape = SHACLShape(shape_id="ForbiddenShape", target_class="Guest", min_counts={"admin_key": 1})
    v.register_shape(SHACLShape(
        shape_id="GuestShape",
        target_class="Guest",
        not_shape=forbidden_shape,
    ))

    # Guest has admin_key -> violates sh:not
    store_fail = SimpleNamespace(
        find_vertices=lambda: [{
            "label": "Guest",
            "canonical_id": "g-1",
            "properties": {"admin_key": "secret123"},
        }],
        find_edges=lambda: []
    )
    report_fail = v.validate(store_fail)
    assert not report_fail.conforms
    assert any(viol.result_code == SHACL_LOGICAL_VIOLATION for viol in report_fail.violations)

    # Guest does not have admin_key -> conforms
    store_pass = SimpleNamespace(
        find_vertices=lambda: [{
            "label": "Guest",
            "canonical_id": "g-1",
            "properties": {"name": "Bob"},
        }],
        find_edges=lambda: []
    )
    assert v.validate(store_pass).conforms is True
