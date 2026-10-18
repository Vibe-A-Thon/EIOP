"""Test suite for offline ontology pitfall lint rules (CRA-022.7, ONT-013, INV-49).

Tests all 21 pitfall rules with positive and negative cases.
"""

from __future__ import annotations

import rdflib
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import OWL, RDF, RDFS, XSD

SHACL = Namespace("http://www.w3.org/ns/shacl#")

from eoip.ontology.lint import (
    ALL_PITFALL_RULES,
    LintFinding,
    LintSeverity,
    OntologyLinter,
)
from eoip.ontology.lint.rules import (
    RuleP01MissingLabel,
    RuleP02MissingDefinition,
    RuleP03MissingDomain,
    RuleP04MissingRange,
    RuleP05CircularSubclass,
    RuleP06EquivalentClassLoop,
    RuleP07UnconnectedClass,
    RuleP08PropertyNoUsage,
    RuleP09InversePropertyConflict,
    RuleP10DeprecatedTermInUse,
    RuleP11NamingConvention,
    RuleP12DuplicateLabels,
    RuleP13MultipleDomainsAsUnion,
    RuleP14LiteralWhereIRIExpected,
    RuleP15UndeclaredNamespace,
    RuleP16ImportNotPinned,
    RuleP17FunctionalPropertyConflict,
    RuleP18DisjointnessContradiction,
    RuleP19OrphanSHACLShape,
    RuleP20ShapeTargetingDeprecatedClass,
    RuleP21LabelLanguageTagMissing,
)

EX = Namespace("urn:example:test:")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")


def test_p01_missing_label():
    rule = RuleP01MissingLabel()
    # Positive case: class with label
    g_ok = Graph()
    g_ok.add((EX.Person, RDF.type, OWL.Class))
    g_ok.add((EX.Person, RDFS.label, Literal("Person", lang="en")))
    assert len(rule.check(g_ok)) == 0

    # Negative case: class without label
    g_bad = Graph()
    g_bad.add((EX.AnonymousThing, RDF.type, OWL.Class))
    findings = rule.check(g_bad)
    assert len(findings) == 1
    assert findings[0].rule_id == "P01"


def test_p02_missing_definition():
    rule = RuleP02MissingDefinition()
    g_ok = Graph()
    g_ok.add((EX.Person, RDF.type, OWL.Class))
    g_ok.add((EX.Person, RDFS.comment, Literal("A human being.", lang="en")))
    assert len(rule.check(g_ok)) == 0

    g_bad = Graph()
    g_bad.add((EX.Person, RDF.type, OWL.Class))
    findings = rule.check(g_bad)
    assert len(findings) == 1
    assert findings[0].rule_id == "P02"


def test_p03_missing_domain():
    rule = RuleP03MissingDomain()
    g_ok = Graph()
    g_ok.add((EX.knows, RDF.type, OWL.ObjectProperty))
    g_ok.add((EX.knows, RDFS.domain, EX.Person))
    assert len(rule.check(g_ok)) == 0

    g_bad = Graph()
    g_bad.add((EX.unboundedProp, RDF.type, OWL.ObjectProperty))
    findings = rule.check(g_bad)
    assert len(findings) == 1
    assert findings[0].rule_id == "P03"


def test_p04_missing_range():
    rule = RuleP04MissingRange()
    g_ok = Graph()
    g_ok.add((EX.age, RDF.type, OWL.DatatypeProperty))
    g_ok.add((EX.age, RDFS.range, XSD.integer))
    assert len(rule.check(g_ok)) == 0

    g_bad = Graph()
    g_bad.add((EX.unknownTarget, RDF.type, OWL.DatatypeProperty))
    findings = rule.check(g_bad)
    assert len(findings) == 1
    assert findings[0].rule_id == "P04"


def test_p05_circular_subclass():
    rule = RuleP05CircularSubclass()
    g_ok = Graph()
    g_ok.add((EX.Child, RDFS.subClassOf, EX.Parent))
    g_ok.add((EX.Parent, RDFS.subClassOf, EX.Grandparent))
    assert len(rule.check(g_ok)) == 0

    g_bad = Graph()
    g_bad.add((EX.A, RDFS.subClassOf, EX.B))
    g_bad.add((EX.B, RDFS.subClassOf, EX.C))
    g_bad.add((EX.C, RDFS.subClassOf, EX.A))  # Cycle: A -> B -> C -> A
    findings = rule.check(g_bad)
    assert len(findings) >= 1
    assert findings[0].rule_id == "P05"
    assert findings[0].severity == LintSeverity.CRITICAL


def test_p06_equivalent_class_loop():
    rule = RuleP06EquivalentClassLoop()
    g_ok = Graph()
    g_ok.add((EX.A, OWL.equivalentClass, EX.B))
    assert len(rule.check(g_ok)) == 0

    g_bad = Graph()
    g_bad.add((EX.A, OWL.equivalentClass, EX.A))
    findings = rule.check(g_bad)
    assert len(findings) == 1
    assert findings[0].rule_id == "P06"


def test_p07_unconnected_class():
    rule = RuleP07UnconnectedClass()
    g_ok = Graph()
    g_ok.add((EX.A, RDF.type, OWL.Class))
    g_ok.add((EX.B, RDF.type, OWL.Class))
    g_ok.add((EX.A, RDFS.subClassOf, EX.B))
    assert len(rule.check(g_ok)) == 0

    g_bad = Graph()
    g_bad.add((EX.Isolated, RDF.type, OWL.Class))
    findings = rule.check(g_bad)
    assert len(findings) == 1
    assert findings[0].rule_id == "P07"


def test_p08_property_no_usage():
    rule = RuleP08PropertyNoUsage()
    g_ok = Graph()
    g_ok.add((EX.knows, RDF.type, OWL.ObjectProperty))
    g_ok.add((EX.Alice, EX.knows, EX.Bob))
    assert len(rule.check(g_ok)) == 0

    g_bad = Graph()
    g_bad.add((EX.orphanProp, RDF.type, OWL.ObjectProperty))
    findings = rule.check(g_bad)
    assert len(findings) == 1
    assert findings[0].rule_id == "P08"


def test_p09_inverse_property_conflict():
    rule = RuleP09InversePropertyConflict()
    g_ok = Graph()
    g_ok.add((EX.parentOf, OWL.inverseOf, EX.childOf))
    g_ok.add((EX.parentOf, RDFS.domain, EX.Parent))
    g_ok.add((EX.parentOf, RDFS.range, EX.Child))
    g_ok.add((EX.childOf, RDFS.domain, EX.Child))
    g_ok.add((EX.childOf, RDFS.range, EX.Parent))
    assert len(rule.check(g_ok)) == 0

    g_bad = Graph()
    g_bad.add((EX.worksFor, OWL.inverseOf, EX.employs))
    g_bad.add((EX.worksFor, RDFS.domain, EX.Employee))
    g_bad.add((EX.employs, RDFS.range, EX.Department))  # Conflict: domain Employee != range Department
    findings = rule.check(g_bad)
    assert len(findings) == 1
    assert findings[0].rule_id == "P09"


def test_p10_deprecated_term_in_use():
    rule = RuleP10DeprecatedTermInUse()
    g_ok = Graph()
    g_ok.add((EX.OldTerm, OWL.deprecated, Literal(True)))
    # Not used in active axioms
    assert len(rule.check(g_ok)) == 0

    g_bad = Graph()
    g_bad.add((EX.OldTerm, OWL.deprecated, Literal(True)))
    g_bad.add((EX.ActiveChild, RDFS.subClassOf, EX.OldTerm))
    findings = rule.check(g_bad)
    assert len(findings) == 1
    assert findings[0].rule_id == "P10"


def test_p11_naming_convention():
    rule = RuleP11NamingConvention()
    g_ok = Graph()
    g_ok.add((EX.ValidClass, RDF.type, OWL.Class))
    g_ok.add((EX.validProperty, RDF.type, OWL.ObjectProperty))
    assert len(rule.check(g_ok)) == 0

    g_bad = Graph()
    g_bad.add((EX.bad_class_name, RDF.type, OWL.Class))
    g_bad.add((EX.BadPropertyName, RDF.type, OWL.ObjectProperty))
    findings = rule.check(g_bad)
    assert len(findings) == 2
    assert findings[0].rule_id == "P11"


def test_p12_duplicate_labels():
    rule = RuleP12DuplicateLabels()
    g_ok = Graph()
    g_ok.add((EX.C1, SKOS.prefLabel, Literal("Alpha", lang="en")))
    g_ok.add((EX.C2, SKOS.prefLabel, Literal("Beta", lang="en")))
    assert len(rule.check(g_ok)) == 0

    g_bad = Graph()
    g_bad.add((EX.C1, SKOS.prefLabel, Literal("Alpha", lang="en")))
    g_bad.add((EX.C2, SKOS.prefLabel, Literal("Alpha", lang="en")))
    findings = rule.check(g_bad)
    assert len(findings) == 1
    assert findings[0].rule_id == "P12"


def test_p13_multiple_domains_as_union():
    rule = RuleP13MultipleDomainsAsUnion()
    g_ok = Graph()
    g_ok.add((EX.prop, RDF.type, OWL.ObjectProperty))
    g_ok.add((EX.prop, RDFS.domain, EX.SingleClass))
    assert len(rule.check(g_ok)) == 0

    g_bad = Graph()
    g_bad.add((EX.prop, RDF.type, OWL.ObjectProperty))
    g_bad.add((EX.prop, RDFS.domain, EX.ClassA))
    g_bad.add((EX.prop, RDFS.domain, EX.ClassB))
    findings = rule.check(g_bad)
    assert len(findings) == 1
    assert findings[0].rule_id == "P13"


def test_p14_literal_where_iri_expected():
    rule = RuleP14LiteralWhereIRIExpected()
    g_ok = Graph()
    g_ok.add((EX.knows, RDF.type, OWL.ObjectProperty))
    g_ok.add((EX.Alice, EX.knows, EX.Bob))
    assert len(rule.check(g_ok)) == 0

    g_bad = Graph()
    g_bad.add((EX.knows, RDF.type, OWL.ObjectProperty))
    g_bad.add((EX.Alice, EX.knows, Literal("Bob")))  # Literal instead of IRI
    findings = rule.check(g_bad)
    assert len(findings) == 1
    assert findings[0].rule_id == "P14"


def test_p15_undeclared_namespace():
    rule = RuleP15UndeclaredNamespace()
    g_ok = Graph()
    g_ok.add((EX.Term, RDF.type, OWL.Class))
    assert len(rule.check(g_ok)) == 0

    g_bad = Graph()
    g_bad.add((URIRef("urn:eoip:undeclared:BadTerm"), RDF.type, OWL.Class))
    findings = rule.check(g_bad)
    assert len(findings) == 1
    assert findings[0].rule_id == "P15"


def test_p16_import_not_pinned():
    rule = RuleP16ImportNotPinned()
    g_ok = Graph()
    g_ok.add((EX.Ontology, OWL.imports, URIRef("https://standards.org/core/v1.2.0.owl")))
    assert len(rule.check(g_ok)) == 0

    g_bad = Graph()
    g_bad.add((EX.Ontology, OWL.imports, URIRef("https://standards.org/core/latest")))
    findings = rule.check(g_bad)
    assert len(findings) == 1
    assert findings[0].rule_id == "P16"


def test_p17_functional_property_conflict():
    rule = RuleP17FunctionalPropertyConflict()
    g_ok = Graph()
    g_ok.add((EX.ssn, RDF.type, OWL.FunctionalProperty))
    g_ok.add((EX.Alice, EX.ssn, Literal("123-45-6789")))
    assert len(rule.check(g_ok)) == 0

    g_bad = Graph()
    g_bad.add((EX.ssn, RDF.type, OWL.FunctionalProperty))
    g_bad.add((EX.Alice, EX.ssn, Literal("123-45-6789")))
    g_bad.add((EX.Alice, EX.ssn, Literal("987-65-4321")))  # Multiple values for functional property
    findings = rule.check(g_bad)
    assert len(findings) == 1
    assert findings[0].rule_id == "P17"


def test_p18_disjointness_contradiction():
    rule = RuleP18DisjointnessContradiction()
    g_ok = Graph()
    g_ok.add((EX.Cat, OWL.disjointWith, EX.Dog))
    assert len(rule.check(g_ok)) == 0

    g_bad = Graph()
    g_bad.add((EX.A, RDFS.subClassOf, EX.B))
    g_bad.add((EX.A, OWL.disjointWith, EX.B))  # SubClassOf + DisjointWith contradiction
    findings = rule.check(g_bad)
    assert len(findings) == 1
    assert findings[0].rule_id == "P18"
    assert findings[0].severity == LintSeverity.CRITICAL


def test_p19_orphan_shacl_shape():
    rule = RuleP19OrphanSHACLShape()
    g_onto = Graph()
    g_onto.add((EX.Customer, RDF.type, OWL.Class))

    shapes_ok = Graph()
    shapes_ok.add((EX.CustomerShape, SHACL.targetClass, EX.Customer))
    assert len(rule.check(g_onto, shapes_graph=shapes_ok)) == 0

    shapes_bad = Graph()
    shapes_bad.add((EX.GhostShape, SHACL.targetClass, EX.NonExistentClass))
    findings = rule.check(g_onto, shapes_graph=shapes_bad)
    assert len(findings) == 1
    assert findings[0].rule_id == "P19"


def test_p20_shape_targeting_deprecated_class():
    rule = RuleP20ShapeTargetingDeprecatedClass()
    g_onto = Graph()
    g_onto.add((EX.ActiveCustomer, RDF.type, OWL.Class))
    g_onto.add((EX.OldCustomer, RDF.type, OWL.Class))
    g_onto.add((EX.OldCustomer, OWL.deprecated, Literal(True)))

    shapes_ok = Graph()
    shapes_ok.add((EX.CustomerShape, SHACL.targetClass, EX.ActiveCustomer))
    assert len(rule.check(g_onto, shapes_graph=shapes_ok)) == 0

    shapes_bad = Graph()
    shapes_bad.add((EX.OldCustomerShape, SHACL.targetClass, EX.OldCustomer))
    findings = rule.check(g_onto, shapes_graph=shapes_bad)
    assert len(findings) == 1
    assert findings[0].rule_id == "P20"


def test_p21_label_language_tag_missing():
    rule = RuleP21LabelLanguageTagMissing()
    g_ok = Graph()
    g_ok.add((EX.Car, RDFS.label, Literal("Car", lang="en")))
    assert len(rule.check(g_ok)) == 0

    g_bad = Graph()
    g_bad.add((EX.Car, RDFS.label, Literal("Car")))  # Missing lang tag
    findings = rule.check(g_bad)
    assert len(findings) == 1
    assert findings[0].rule_id == "P21"


def test_full_linter_report():
    linter = OntologyLinter()
    assert len(linter.rules) == 21

    g_clean = Graph()
    g_clean.add((EX.User, RDF.type, OWL.Class))
    g_clean.add((EX.User, RDFS.label, Literal("User", lang="en")))
    g_clean.add((EX.User, RDFS.comment, Literal("A system user.", lang="en")))
    g_clean.add((EX.Admin, RDF.type, OWL.Class))
    g_clean.add((EX.Admin, RDFS.label, Literal("Admin", lang="en")))
    g_clean.add((EX.Admin, RDFS.comment, Literal("An admin user.", lang="en")))
    g_clean.add((EX.Admin, RDFS.subClassOf, EX.User))

    report = linter.lint_graph(g_clean)
    assert report.critical_count == 0
    assert report.error_count == 0
    assert report.passed is True
