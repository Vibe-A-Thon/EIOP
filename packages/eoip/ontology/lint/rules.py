"""Ontology Pitfall Scanner Rules (CRA-022.7, ONT-013, INV-49).

Implements at least 21 antipattern detection rules with rule IDs, severities,
descriptions, remediation hints, and structured findings.
Runs offline only.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import re
from typing import Any, Optional

import rdflib
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import OWL, RDF, RDFS, XSD

SHACL = Namespace("http://www.w3.org/ns/shacl#")

SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")


class LintSeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class LintFinding:
    rule_id: str
    severity: LintSeverity
    subject: str
    message: str
    remediation_hint: str
    context: dict[str, Any] = field(default_factory=dict)


@dataclass
class LintRule:
    rule_id: str
    title: str
    severity: LintSeverity
    description: str
    remediation_hint: str

    def check(self, graph: rdflib.Graph, manifest: Optional[dict[str, Any]] = None, shapes_graph: Optional[rdflib.Graph] = None) -> list[LintFinding]:
        raise NotImplementedError


# P01: Missing rdfs:label / skos:prefLabel
class RuleP01MissingLabel(LintRule):
    def __init__(self) -> None:
        super().__init__(
            rule_id="P01",
            title="Missing Label",
            severity=LintSeverity.WARNING,
            description="Named classes and properties must have at least one human-readable label.",
            remediation_hint="Add rdfs:label or skos:prefLabel with a language tag.",
        )

    def check(self, graph: rdflib.Graph, manifest: Optional[dict[str, Any]] = None, shapes_graph: Optional[rdflib.Graph] = None) -> list[LintFinding]:
        findings = []
        for s in set(graph.subjects(RDF.type, OWL.Class)) | set(graph.subjects(RDF.type, OWL.ObjectProperty)) | set(graph.subjects(RDF.type, OWL.DatatypeProperty)):
            if isinstance(s, URIRef) and not str(s).startswith(str(OWL)) and not str(s).startswith(str(RDF)):
                labels = list(graph.objects(s, RDFS.label)) + list(graph.objects(s, SKOS.prefLabel))
                if not labels:
                    findings.append(LintFinding(
                        rule_id=self.rule_id,
                        severity=self.severity,
                        subject=str(s),
                        message=f"Resource '{s}' is missing an rdfs:label or skos:prefLabel.",
                        remediation_hint=self.remediation_hint,
                    ))
        return findings


# P02: Missing definition / comment
class RuleP02MissingDefinition(LintRule):
    def __init__(self) -> None:
        super().__init__(
            rule_id="P02",
            title="Missing Definition or Comment",
            severity=LintSeverity.WARNING,
            description="Named classes and properties must have a human-readable definition or comment.",
            remediation_hint="Add rdfs:comment or skos:definition explaining the semantics of the term.",
        )

    def check(self, graph: rdflib.Graph, manifest: Optional[dict[str, Any]] = None, shapes_graph: Optional[rdflib.Graph] = None) -> list[LintFinding]:
        findings = []
        for s in set(graph.subjects(RDF.type, OWL.Class)) | set(graph.subjects(RDF.type, OWL.ObjectProperty)):
            if isinstance(s, URIRef) and not str(s).startswith(str(OWL)):
                comments = list(graph.objects(s, RDFS.comment)) + list(graph.objects(s, SKOS.definition))
                if not comments:
                    findings.append(LintFinding(
                        rule_id=self.rule_id,
                        severity=self.severity,
                        subject=str(s),
                        message=f"Term '{s}' is missing an rdfs:comment or skos:definition.",
                        remediation_hint=self.remediation_hint,
                    ))
        return findings


# P03: Missing domain
class RuleP03MissingDomain(LintRule):
    def __init__(self) -> None:
        super().__init__(
            rule_id="P03",
            title="Missing Property Domain",
            severity=LintSeverity.WARNING,
            description="Properties should declare their domain class to bound their applicability.",
            remediation_hint="Add rdfs:domain to declare the subject class of this property.",
        )

    def check(self, graph: rdflib.Graph, manifest: Optional[dict[str, Any]] = None, shapes_graph: Optional[rdflib.Graph] = None) -> list[LintFinding]:
        findings = []
        for p in set(graph.subjects(RDF.type, OWL.ObjectProperty)) | set(graph.subjects(RDF.type, OWL.DatatypeProperty)):
            if isinstance(p, URIRef) and not str(p).startswith(str(OWL)):
                domains = list(graph.objects(p, RDFS.domain))
                if not domains:
                    findings.append(LintFinding(
                        rule_id=self.rule_id,
                        severity=self.severity,
                        subject=str(p),
                        message=f"Property '{p}' has no declared rdfs:domain.",
                        remediation_hint=self.remediation_hint,
                    ))
        return findings


# P04: Missing range
class RuleP04MissingRange(LintRule):
    def __init__(self) -> None:
        super().__init__(
            rule_id="P04",
            title="Missing Property Range",
            severity=LintSeverity.WARNING,
            description="Properties should declare their range to bound allowed target values.",
            remediation_hint="Add rdfs:range specifying the target class or datatype.",
        )

    def check(self, graph: rdflib.Graph, manifest: Optional[dict[str, Any]] = None, shapes_graph: Optional[rdflib.Graph] = None) -> list[LintFinding]:
        findings = []
        for p in set(graph.subjects(RDF.type, OWL.ObjectProperty)) | set(graph.subjects(RDF.type, OWL.DatatypeProperty)):
            if isinstance(p, URIRef) and not str(p).startswith(str(OWL)):
                ranges = list(graph.objects(p, RDFS.range))
                if not ranges:
                    findings.append(LintFinding(
                        rule_id=self.rule_id,
                        severity=self.severity,
                        subject=str(p),
                        message=f"Property '{p}' has no declared rdfs:range.",
                        remediation_hint=self.remediation_hint,
                    ))
        return findings


# P05: Circular subclass hierarchy
class RuleP05CircularSubclass(LintRule):
    def __init__(self) -> None:
        super().__init__(
            rule_id="P05",
            title="Circular Subclass Hierarchy",
            severity=LintSeverity.CRITICAL,
            description="Cycles in rdfs:subClassOf lead to class equivalence and model incoherence.",
            remediation_hint="Remove circular rdfs:subClassOf assertions to restore a strict DAG hierarchy.",
        )

    def check(self, graph: rdflib.Graph, manifest: Optional[dict[str, Any]] = None, shapes_graph: Optional[rdflib.Graph] = None) -> list[LintFinding]:
        findings = []
        subclasses: dict[str, set[str]] = {}
        for s, _, o in graph.triples((None, RDFS.subClassOf, None)):
            if isinstance(s, URIRef) and isinstance(o, URIRef) and s != o:
                subclasses.setdefault(str(s), set()).add(str(o))

        def find_cycle(node: str, visited: list[str]) -> list[str] | None:
            if node in visited:
                idx = visited.index(node)
                return visited[idx:] + [node]
            for parent in subclasses.get(node, set()):
                cycle = find_cycle(parent, visited + [node])
                if cycle:
                    return cycle
            return None

        seen_cycles = set()
        for c in subclasses:
            cycle = find_cycle(c, [])
            if cycle:
                cycle_key = tuple(sorted(set(cycle)))
                if cycle_key not in seen_cycles:
                    seen_cycles.add(cycle_key)
                    findings.append(LintFinding(
                        rule_id=self.rule_id,
                        severity=self.severity,
                        subject=cycle[0],
                        message=f"Circular subclass hierarchy detected: {' -> '.join(cycle)}",
                        remediation_hint=self.remediation_hint,
                    ))
        return findings


# P06: Equivalent-class loop
class RuleP06EquivalentClassLoop(LintRule):
    def __init__(self) -> None:
        super().__init__(
            rule_id="P06",
            title="Trivial Equivalent Class Loop",
            severity=LintSeverity.ERROR,
            description="A class should not be declared equivalent to itself or create trivial loops.",
            remediation_hint="Remove reflexive owl:equivalentClass self-assertions.",
        )

    def check(self, graph: rdflib.Graph, manifest: Optional[dict[str, Any]] = None, shapes_graph: Optional[rdflib.Graph] = None) -> list[LintFinding]:
        findings = []
        for s, _, o in graph.triples((None, OWL.equivalentClass, None)):
            if s == o:
                findings.append(LintFinding(
                    rule_id=self.rule_id,
                    severity=self.severity,
                    subject=str(s),
                    message=f"Class '{s}' is declared equivalent to itself (reflexive loop).",
                    remediation_hint=self.remediation_hint,
                ))
        return findings


# P07: Unconnected class
class RuleP07UnconnectedClass(LintRule):
    def __init__(self) -> None:
        super().__init__(
            rule_id="P07",
            title="Unconnected Class",
            severity=LintSeverity.WARNING,
            description="A class with no superclasses, subclasses, instances, or property references is isolated.",
            remediation_hint="Link the class into the ontology hierarchy or domain/range declarations.",
        )

    def check(self, graph: rdflib.Graph, manifest: Optional[dict[str, Any]] = None, shapes_graph: Optional[rdflib.Graph] = None) -> list[LintFinding]:
        findings = []
        for c in graph.subjects(RDF.type, OWL.Class):
            if isinstance(c, URIRef) and not str(c).startswith(str(OWL)):
                has_super = list(graph.objects(c, RDFS.subClassOf))
                has_sub = list(graph.subjects(RDFS.subClassOf, c))
                has_inst = list(graph.subjects(RDF.type, c))
                in_domain = list(graph.subjects(RDFS.domain, c))
                in_range = list(graph.subjects(RDFS.range, c))
                if not (has_super or has_sub or has_inst or in_domain or in_range):
                    findings.append(LintFinding(
                        rule_id=self.rule_id,
                        severity=self.severity,
                        subject=str(c),
                        message=f"Class '{c}' is completely unconnected from other ontology elements.",
                        remediation_hint=self.remediation_hint,
                    ))
        return findings


# P08: Property with no usage
class RuleP08PropertyNoUsage(LintRule):
    def __init__(self) -> None:
        super().__init__(
            rule_id="P08",
            title="Property With No Usage",
            severity=LintSeverity.INFO,
            description="Property is declared in the ontology but never used in any instance facts.",
            remediation_hint="Consider deprecating or using the property in data mappings.",
        )

    def check(self, graph: rdflib.Graph, manifest: Optional[dict[str, Any]] = None, shapes_graph: Optional[rdflib.Graph] = None) -> list[LintFinding]:
        findings = []
        for p in set(graph.subjects(RDF.type, OWL.ObjectProperty)) | set(graph.subjects(RDF.type, OWL.DatatypeProperty)):
            if isinstance(p, URIRef) and not str(p).startswith(str(OWL)):
                usages = [s for s, _, _ in graph.triples((None, p, None))]
                if not usages:
                    findings.append(LintFinding(
                        rule_id=self.rule_id,
                        severity=self.severity,
                        subject=str(p),
                        message=f"Property '{p}' has no instance assertion usages in the active dataset.",
                        remediation_hint=self.remediation_hint,
                    ))
        return findings


# P09: Inverse-property conflict
class RuleP09InversePropertyConflict(LintRule):
    def __init__(self) -> None:
        super().__init__(
            rule_id="P09",
            title="Inverse Property Endpoint Conflict",
            severity=LintSeverity.ERROR,
            description="An inverse property must swap domain and range; mismatched domains/ranges indicate a modeling error.",
            remediation_hint="Ensure property domain matches inverse range, and property range matches inverse domain.",
        )

    def check(self, graph: rdflib.Graph, manifest: Optional[dict[str, Any]] = None, shapes_graph: Optional[rdflib.Graph] = None) -> list[LintFinding]:
        findings = []
        for p1, _, p2 in graph.triples((None, OWL.inverseOf, None)):
            p1_dom = set(graph.objects(p1, RDFS.domain))
            p2_rng = set(graph.objects(p2, RDFS.range))
            if p1_dom and p2_rng and not p1_dom.intersection(p2_rng):
                findings.append(LintFinding(
                    rule_id=self.rule_id,
                    severity=self.severity,
                    subject=str(p1),
                    message=f"Inverse property conflict: domain of '{p1}' does not match range of '{p2}'.",
                    remediation_hint=self.remediation_hint,
                ))
        return findings


# P10: Deprecated term used in active axioms
class RuleP10DeprecatedTermInUse(LintRule):
    def __init__(self) -> None:
        super().__init__(
            rule_id="P10",
            title="Deprecated Term Used in Active Axioms",
            severity=LintSeverity.ERROR,
            description="Deprecated classes or properties must not be used in active subClassOf or domain/range definitions.",
            remediation_hint="Migrate active axioms to reference the replacement term indicated by dct:isReplacedBy.",
        )

    def check(self, graph: rdflib.Graph, manifest: Optional[dict[str, Any]] = None, shapes_graph: Optional[rdflib.Graph] = None) -> list[LintFinding]:
        findings = []
        deprecated_terms = set(graph.subjects(OWL.deprecated, Literal(True)))
        for dep in deprecated_terms:
            active_super = list(graph.subjects(RDFS.subClassOf, dep))
            active_domain = list(graph.subjects(RDFS.domain, dep))
            if active_super or active_domain:
                findings.append(LintFinding(
                    rule_id=self.rule_id,
                    severity=self.severity,
                    subject=str(dep),
                    message=f"Deprecated term '{dep}' is actively referenced in subClassOf or domain/range axioms.",
                    remediation_hint=self.remediation_hint,
                ))
        return findings


# P11: Naming convention violation
class RuleP11NamingConvention(LintRule):
    def __init__(self, class_pattern: str = r"^[A-Z][a-zA-Z0-9]+$", prop_pattern: str = r"^[a-z][a-zA-Z0-9]+$") -> None:
        super().__init__(
            rule_id="P11",
            title="Naming Convention Violation",
            severity=LintSeverity.WARNING,
            description="Classes should follow UpperCamelCase and properties should follow lowerCamelCase.",
            remediation_hint="Rename term to conform to enterprise ontology naming guidelines.",
        )
        self.class_re = re.compile(class_pattern)
        self.prop_re = re.compile(prop_pattern)

    def check(self, graph: rdflib.Graph, manifest: Optional[dict[str, Any]] = None, shapes_graph: Optional[rdflib.Graph] = None) -> list[LintFinding]:
        findings = []
        for c in graph.subjects(RDF.type, OWL.Class):
            if isinstance(c, URIRef) and not str(c).startswith(str(OWL)):
                local = str(c).split("#")[-1].split("/")[-1].split(":")[-1]
                if not self.class_re.match(local):
                    findings.append(LintFinding(
                        rule_id=self.rule_id,
                        severity=self.severity,
                        subject=str(c),
                        message=f"Class local name '{local}' violates UpperCamelCase convention.",
                        remediation_hint=self.remediation_hint,
                    ))
        for p in set(graph.subjects(RDF.type, OWL.ObjectProperty)) | set(graph.subjects(RDF.type, OWL.DatatypeProperty)):
            if isinstance(p, URIRef) and not str(p).startswith(str(OWL)):
                local = str(p).split("#")[-1].split("/")[-1].split(":")[-1]
                if not self.prop_re.match(local):
                    findings.append(LintFinding(
                        rule_id=self.rule_id,
                        severity=self.severity,
                        subject=str(p),
                        message=f"Property local name '{local}' violates lowerCamelCase convention.",
                        remediation_hint=self.remediation_hint,
                    ))
        return findings


# P12: Duplicate labels within scheme / language
class RuleP12DuplicateLabels(LintRule):
    def __init__(self) -> None:
        super().__init__(
            rule_id="P12",
            title="Duplicate Labels in Scheme / Language",
            severity=LintSeverity.WARNING,
            description="Multiple distinct concepts sharing the same prefLabel within the same language can cause ambiguity.",
            remediation_hint="Differentiate labels using qualifiers or provide distinctive altLabels.",
        )

    def check(self, graph: rdflib.Graph, manifest: Optional[dict[str, Any]] = None, shapes_graph: Optional[rdflib.Graph] = None) -> list[LintFinding]:
        findings = []
        labels_by_lang: dict[tuple[str, str], list[str]] = {}
        for s, _, o in graph.triples((None, SKOS.prefLabel, None)):
            if isinstance(o, Literal):
                lang = o.language or "en"
                labels_by_lang.setdefault((str(o).casefold(), lang), []).append(str(s))
        for (lbl, lang), subjects in labels_by_lang.items():
            if len(subjects) > 1:
                findings.append(LintFinding(
                    rule_id=self.rule_id,
                    severity=self.severity,
                    subject=subjects[0],
                    message=f"Duplicate prefLabel '{lbl}'@{lang} shared by {len(subjects)} concepts: {', '.join(subjects)}",
                    remediation_hint=self.remediation_hint,
                ))
        return findings


# P13: Multiple domains intended as union
class RuleP13MultipleDomainsAsUnion(LintRule):
    def __init__(self) -> None:
        super().__init__(
            rule_id="P13",
            title="Multiple Domains Treated as Intersection",
            severity=LintSeverity.WARNING,
            description="Declaring multiple rdfs:domain triples means the subject must be an instance of ALL domain classes (intersection), not union.",
            remediation_hint="If union was intended, declare a single domain with an owl:unionOf construct.",
        )

    def check(self, graph: rdflib.Graph, manifest: Optional[dict[str, Any]] = None, shapes_graph: Optional[rdflib.Graph] = None) -> list[LintFinding]:
        findings = []
        for p in set(graph.subjects(RDF.type, OWL.ObjectProperty)) | set(graph.subjects(RDF.type, OWL.DatatypeProperty)):
            domains = list(graph.objects(p, RDFS.domain))
            if len(domains) > 1:
                findings.append(LintFinding(
                    rule_id=self.rule_id,
                    severity=self.severity,
                    subject=str(p),
                    message=f"Property '{p}' declares multiple ({len(domains)}) domains; in OWL this is interpreted as intersection.",
                    remediation_hint=self.remediation_hint,
                ))
        return findings


# P14: Literal used where IRI expected
class RuleP14LiteralWhereIRIExpected(LintRule):
    def __init__(self) -> None:
        super().__init__(
            rule_id="P14",
            title="Literal Value for Object Property",
            severity=LintSeverity.ERROR,
            description="Object properties must link to IRI node resources, never literal values.",
            remediation_hint="Use a DatatypeProperty or convert the literal to an IRI reference.",
        )

    def check(self, graph: rdflib.Graph, manifest: Optional[dict[str, Any]] = None, shapes_graph: Optional[rdflib.Graph] = None) -> list[LintFinding]:
        findings = []
        for p in graph.subjects(RDF.type, OWL.ObjectProperty):
            for s, _, o in graph.triples((None, p, None)):
                if isinstance(o, Literal):
                    findings.append(LintFinding(
                        rule_id=self.rule_id,
                        severity=self.severity,
                        subject=str(s),
                        message=f"Object property '{p}' has a literal object '{o}'; expected IRI node.",
                        remediation_hint=self.remediation_hint,
                    ))
        return findings


# P15: Undeclared namespace prefix use
class RuleP15UndeclaredNamespace(LintRule):
    def __init__(self) -> None:
        super().__init__(
            rule_id="P15",
            title="Undeclared Namespace Prefix",
            severity=LintSeverity.ERROR,
            description="All CURIE prefixes must be declared in ontology namespace bindings.",
            remediation_hint="Bind prefix to its official namespace URI.",
        )

    def check(self, graph: rdflib.Graph, manifest: Optional[dict[str, Any]] = None, shapes_graph: Optional[rdflib.Graph] = None) -> list[LintFinding]:
        findings = []
        for s in graph.subjects():
            if isinstance(s, URIRef) and str(s).startswith("urn:eoip:undeclared:"):
                findings.append(LintFinding(
                    rule_id=self.rule_id,
                    severity=self.severity,
                    subject=str(s),
                    message=f"Term '{s}' uses an undeclared namespace prefix.",
                    remediation_hint=self.remediation_hint,
                ))
        return findings


# P16: Import not pinned
class RuleP16ImportNotPinned(LintRule):
    def __init__(self) -> None:
        super().__init__(
            rule_id="P16",
            title="Unpinned Ontology Import",
            severity=LintSeverity.WARNING,
            description="External ontology imports should be version-pinned or digest-verified.",
            remediation_hint="Pin ontology import to a versioned IRI or sha256 artifact digest.",
        )

    def check(self, graph: rdflib.Graph, manifest: Optional[dict[str, Any]] = None, shapes_graph: Optional[rdflib.Graph] = None) -> list[LintFinding]:
        findings = []
        for _, _, imp in graph.triples((None, OWL.imports, None)):
            imp_str = str(imp)
            if not any(v in imp_str for v in ["/v1", "/v2", "/1.", "/2.", "-202", ".owl"]):
                findings.append(LintFinding(
                    rule_id=self.rule_id,
                    severity=self.severity,
                    subject=imp_str,
                    message=f"Import '{imp_str}' does not reference a pinned version or digest.",
                    remediation_hint=self.remediation_hint,
                ))
        return findings


# P17: Functional property with multiple values in fixtures
class RuleP17FunctionalPropertyConflict(LintRule):
    def __init__(self) -> None:
        super().__init__(
            rule_id="P17",
            title="Functional Property Cardinality Conflict",
            severity=LintSeverity.ERROR,
            description="A functional property (owl:FunctionalProperty) can have at most one distinct value per subject.",
            remediation_hint="Remove extraneous property values or remove owl:FunctionalProperty classification.",
        )

    def check(self, graph: rdflib.Graph, manifest: Optional[dict[str, Any]] = None, shapes_graph: Optional[rdflib.Graph] = None) -> list[LintFinding]:
        findings = []
        for p in graph.subjects(RDF.type, OWL.FunctionalProperty):
            values_by_subj: dict[str, set[str]] = {}
            for s, _, o in graph.triples((None, p, None)):
                values_by_subj.setdefault(str(s), set()).add(str(o))
            for s, vals in values_by_subj.items():
                if len(vals) > 1:
                    findings.append(LintFinding(
                        rule_id=self.rule_id,
                        severity=self.severity,
                        subject=s,
                        message=f"Subject '{s}' has {len(vals)} distinct values for functional property '{p}'.",
                        remediation_hint=self.remediation_hint,
                    ))
        return findings


# P18: Disjointness contradiction with subclassing
class RuleP18DisjointnessContradiction(LintRule):
    def __init__(self) -> None:
        super().__init__(
            rule_id="P18",
            title="Disjointness Contradiction With Subclassing",
            severity=LintSeverity.CRITICAL,
            description="A class cannot be both a subclass of and disjoint with another class.",
            remediation_hint="Remove the owl:disjointWith axiom or the rdfs:subClassOf axiom.",
        )

    def check(self, graph: rdflib.Graph, manifest: Optional[dict[str, Any]] = None, shapes_graph: Optional[rdflib.Graph] = None) -> list[LintFinding]:
        findings = []
        for c1, _, c2 in graph.triples((None, OWL.disjointWith, None)):
            is_sub = (c1, RDFS.subClassOf, c2) in graph
            if is_sub:
                findings.append(LintFinding(
                    rule_id=self.rule_id,
                    severity=self.severity,
                    subject=str(c1),
                    message=f"Class '{c1}' is declared both a subClassOf and disjointWith '{c2}'.",
                    remediation_hint=self.remediation_hint,
                ))
        return findings


# P19: Orphan SHACL shape
class RuleP19OrphanSHACLShape(LintRule):
    def __init__(self) -> None:
        super().__init__(
            rule_id="P19",
            title="Orphan SHACL Shape",
            severity=LintSeverity.WARNING,
            description="SHACL shape targets a class that is absent from the ontology manifest.",
            remediation_hint="Declare the target class in the ontology or update the shape targetClass.",
        )

    def check(self, graph: rdflib.Graph, manifest: Optional[dict[str, Any]] = None, shapes_graph: Optional[rdflib.Graph] = None) -> list[LintFinding]:
        findings = []
        if shapes_graph is not None:
            for shape, _, target in shapes_graph.triples((None, SHACL.targetClass, None)):
                if (target, RDF.type, OWL.Class) not in graph:
                    findings.append(LintFinding(
                        rule_id=self.rule_id,
                        severity=self.severity,
                        subject=str(shape),
                        message=f"SHACL shape '{shape}' targets absent class '{target}'.",
                        remediation_hint=self.remediation_hint,
                    ))
        return findings


# P20: Shape targeting deprecated class
class RuleP20ShapeTargetingDeprecatedClass(LintRule):
    def __init__(self) -> None:
        super().__init__(
            rule_id="P20",
            title="SHACL Shape Targets Deprecated Class",
            severity=LintSeverity.WARNING,
            description="A SHACL shape should not target an owl:deprecated class in active validation.",
            remediation_hint="Migrate shape to target the active replacement class.",
        )

    def check(self, graph: rdflib.Graph, manifest: Optional[dict[str, Any]] = None, shapes_graph: Optional[rdflib.Graph] = None) -> list[LintFinding]:
        findings = []
        if shapes_graph is not None:
            deprecated_classes = set(graph.subjects(OWL.deprecated, Literal(True)))
            for shape, _, target in shapes_graph.triples((None, SHACL.targetClass, None)):
                if target in deprecated_classes:
                    findings.append(LintFinding(
                        rule_id=self.rule_id,
                        severity=self.severity,
                        subject=str(shape),
                        message=f"SHACL shape '{shape}' targets deprecated class '{target}'.",
                        remediation_hint=self.remediation_hint,
                    ))
        return findings


# P21: Label language tag missing
class RuleP21LabelLanguageTagMissing(LintRule):
    def __init__(self) -> None:
        super().__init__(
            rule_id="P21",
            title="Missing Language Tag on Label Literal",
            severity=LintSeverity.INFO,
            description="Literal labels should carry a BCP-47 language tag for multilingual fidelity.",
            remediation_hint="Add @en or appropriate BCP-47 language tag to the label literal.",
        )

    def check(self, graph: rdflib.Graph, manifest: Optional[dict[str, Any]] = None, shapes_graph: Optional[rdflib.Graph] = None) -> list[LintFinding]:
        findings = []
        for s, _, o in graph.triples((None, RDFS.label, None)):
            if isinstance(o, Literal) and not o.language:
                findings.append(LintFinding(
                    rule_id=self.rule_id,
                    severity=self.severity,
                    subject=str(s),
                    message=f"Label literal '{o}' on resource '{s}' lacks a language tag.",
                    remediation_hint=self.remediation_hint,
                ))
        return findings


ALL_PITFALL_RULES: list[LintRule] = [
    RuleP01MissingLabel(),
    RuleP02MissingDefinition(),
    RuleP03MissingDomain(),
    RuleP04MissingRange(),
    RuleP05CircularSubclass(),
    RuleP06EquivalentClassLoop(),
    RuleP07UnconnectedClass(),
    RuleP08PropertyNoUsage(),
    RuleP09InversePropertyConflict(),
    RuleP10DeprecatedTermInUse(),
    RuleP11NamingConvention(),
    RuleP12DuplicateLabels(),
    RuleP13MultipleDomainsAsUnion(),
    RuleP14LiteralWhereIRIExpected(),
    RuleP15UndeclaredNamespace(),
    RuleP16ImportNotPinned(),
    RuleP17FunctionalPropertyConflict(),
    RuleP18DisjointnessContradiction(),
    RuleP19OrphanSHACLShape(),
    RuleP20ShapeTargetingDeprecatedClass(),
    RuleP21LabelLanguageTagMissing(),
]
