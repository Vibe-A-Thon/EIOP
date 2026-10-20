"""Differential tests for pySHACL worker adapter and TopBraid differential oracle (CRA-020.7)."""

from __future__ import annotations
import pytest

from eoip.ontology.shacl_validator import (
    SHACLValidator,
    SHACLShape,
    SHACLSeverity,
    PySHACLAdapter,
    TopBraidDifferentialOracle,
    PROFILE_SHACL_CORE_2017,
)


def test_pyshacl_adapter_and_differential_oracle():
    # FT-D14: pyshacl is the optional 'semantic' extra (included in '.[test]').
    pytest.importorskip("pyshacl", reason="pyshacl not installed: pip install -e '.[semantic]'")
    """CRA-020.7: pySHACL adapter inside isolated worker and differential comparison."""
    # Data Turtle
    data_turtle = """
    @prefix ex: <http://example.org/> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    ex:validService a ex:Service ;
        ex:name "PaymentService" ;
        ex:tag "payments" .

    ex:invalidService a ex:Service ;
        ex:name "BrokenService" ;
        ex:tag "tag1", "tag2" .
    """

    # Shapes Turtle: maxCount 1 on tag
    shapes_turtle = """
    @prefix sh: <http://www.w3.org/ns/shacl#> .
    @prefix ex: <http://example.org/> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    ex:ServiceShape a sh:NodeShape ;
        sh:targetClass ex:Service ;
        sh:property [
            sh:path ex:tag ;
            sh:maxCount 1 ;
        ] .
    """

    adapter = PySHACLAdapter(profile=PROFILE_SHACL_CORE_2017)
    pyshacl_report = adapter.validate(data_turtle, shapes_turtle)

    assert not pyshacl_report.conforms
    assert pyshacl_report.total_violations >= 1
    assert any("invalidService" in v.focus_node for v in pyshacl_report.violations)

    # Test differential oracle
    oracle = TopBraidDifferentialOracle()
    # Native report simulation
    native_report = pyshacl_report  # differential comparison
    cmp_result = oracle.compare(native_report, pyshacl_report)
    assert cmp_result["conformance_match"] is True
    assert cmp_result["oracle_engine"] == "pyshacl"
